<#
Drive-root child monitor. Read-only; report-only; never blocks.

A POSIX drive path such as /d/x handed unconverted to a native Windows program
resolves against the root of the CURRENT drive, so a write lands in a new
direct child of a drive root (D:\d\..., C:\c\...). This script snapshots the
direct children of each monitored root and later reports any child that was
not in the snapshot. It is independent of every other check: it reads no
other report, no owner baseline and no ledger, so their state can neither mask
nor produce its result. Design: docs/msys_destination_validation/PLANNING.md.

THIS FILE MUST STAY PURE ASCII AND KEEP ITS UTF-8 BOM (see the guard header;
tests/test_guard_destructive_command.py pins every hook in this directory).

Arguments (parsed from $args; there is deliberately no param() block, so a
malformed call reaches the fail-closed path instead of a binding error):
  -Mode Snapshot|Compare|ListRoots|HookSessionStart|HookStop   (required)
  -Root <path>            repeat once per root. Omitted: every fixed volume as
                          X:\ (Windows only; this includes subst drives). On
                          other platforms a root list is required.
  -SnapshotDir <dir>      where the snapshot lives. Default: the user TEMP
                          directory. It must already exist; it is never created.
  -SessionId <id>         Snapshot and Compare only; [A-Za-z0-9_-]{1,128}.
  -ProtectedPath <path>   repeat; added to the built-in protected trees.

Snapshot file: <SnapshotDir>\claude-drive-root-<session id>.json, the same name
in every mode, so a standalone Compare can read a hook session's snapshot. It
is the only file this script writes. It is opened with FileShare.None, so the
file is its own lock, and it is rewritten in place under that handle: there is
no temp file and no lock file. The snapshot path is refused (UNKNOWN, nothing
written) when its parent is a monitored root or when it lies under a protected
tree.

Modes and exit codes:
  Snapshot   record the roots' children. Prints the JSON report.
  Compare    report children not in the snapshot. Prints the JSON report
             {status, new[], unknown[{root, reason}], faultShapedPresent[],
             protected[]}. Ignores what the hooks have already announced.
  ListRoots  print {"roots": [...]}, the roots that would be monitored.
  Exit: 0 CLEAN, 10 NEW_CHILDREN, 11 UNKNOWN (also bad arguments and any
  internal failure). UNKNOWN wins over NEW_CHILDREN; new[] is still listed.
  Reason codes: snapshot-missing, snapshot-invalid, schema-mismatch,
  root-missing, root-unreadable, root-new, protected-path, root-parent-path,
  session-id-invalid, bad-arguments, internal.

  HookSessionStart  (SessionStart hook) snapshot for the payload's session_id.
             startup, clear and resume replace the snapshot; compact keeps a
             valid one. Writes nothing to stdout in any path.
  HookStop   (Stop hook) compare against the session's snapshot. Prints
             nothing, or exactly one {"systemMessage": "..."} object. Each new
             child, single-letter (fault-shaped) child, newly discovered root,
             missing root and the mid-session baseline is announced once per
             snapshot; an invalid snapshot is announced on every Stop and never
             overwritten. With no snapshot, or a zero-length one, it records
             one now (mid-session baseline). A snapshot held by another instance is skipped
             silently.
  Recognised hook modes always exit 0: a monitor hit is a notice, never a
  block. (An unrecognised -Mode is a standalone bad-arguments call: 11.)

Accumulation: one small snapshot file per session stays in TEMP. Nothing here
deletes it; clearing TEMP is safe at any time.

Registration (user level only, in C:\Users\<you>\.claude\settings.json, under
"hooks"; not in a project settings file, where it would run twice in that
project and not at all elsewhere):
  "SessionStart": [{"hooks": [{"type": "command", "timeout": 30, "command":
    "powershell -NoProfile -ExecutionPolicy Bypass -File \"C:/Users/<you>/.claude/hooks/drive-root-monitor.ps1\" -Mode HookSessionStart"}]}],
  "Stop": [{"hooks": [{"type": "command", "timeout": 30, "command":
    "powershell -NoProfile -ExecutionPolicy Bypass -File \"C:/Users/<you>/.claude/hooks/drive-root-monitor.ps1\" -Mode HookStop"}]}]

Limits: only direct root children are seen, and only between snapshot and
compare; writes beneath an existing child are invisible (a single-letter child
is flagged as the one dangerous shape). Children made by other sessions, the
owner or the OS are reported too; the notices never claim a cause.
#>
$ErrorActionPreference = 'Stop'

$script:exitCode = 11
$script:hookMode = $null
$script:printed = $false
$script:onWindows = ([Environment]::OSVersion.Platform -eq [PlatformID]::Win32NT)
if ($script:onWindows) {
    $script:nameComparer = [StringComparer]::OrdinalIgnoreCase
    $script:nameComparison = [StringComparison]::OrdinalIgnoreCase
}
else {
    $script:nameComparer = [StringComparer]::Ordinal
    $script:nameComparison = [StringComparison]::Ordinal
}
$builtinProtected = @('D:\dev-cleanup-20260824-digest', 'D:\_digest-discard-bin')
$snapshotPrefix = 'claude-drive-root-'
$sessionIdPattern = '\A[A-Za-z0-9_-]{1,128}\z'
$modes = @('Snapshot', 'Compare', 'ListRoots', 'HookSessionStart', 'HookStop')
$sources = @('startup', 'clear', 'resume', 'compact', 'stop-baseline')
$announcedPattern = '\A(?:child|fault|newroot|midsession|rootgone)\|'
$snapshotKeys = @('schemaVersion', 'sessionId', 'createdUtc', 'source', 'roots', 'announced')

$textInvalidSnapshot = "Drive-root monitoring: this session's snapshot is invalid or unreadable; UNKNOWN. No claim is made about drive roots."
$textInvalidSessionId = 'Drive-root monitoring: the session id is not usable, so nothing was recorded; UNKNOWN. No claim is made about drive roots.'
$textInternal = 'Drive-root monitoring failed internally; UNKNOWN. No claim is made about drive roots.'

# --- JSON -----------------------------------------------------------------------
# A small strict reader and writer, so both hosts read and write the same bytes.
# ConvertFrom-Json in PowerShell 7 turns ISO 8601 strings into DateTime values,
# which would change createdUtc on the way through.

class MonitorJsonReader {
    hidden [string]$Text
    hidden [int]$Pos
    static [regex]$Number = [regex]::new('\G-?(?:0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?')

    MonitorJsonReader([string]$text) {
        $this.Text = $text
        $this.Pos = 0
    }

    static [object] Parse([string]$text) {
        $reader = [MonitorJsonReader]::new($text)
        $reader.SkipSpace()
        $value = $reader.ReadValue()
        $reader.SkipSpace()
        if ($reader.Pos -ne $reader.Text.Length) { throw 'JSON: unexpected trailing text' }
        return $value
    }

    [void] SkipSpace() {
        while ($this.Pos -lt $this.Text.Length -and " `t`r`n".IndexOf($this.Text[$this.Pos]) -ge 0) { $this.Pos++ }
    }

    [char] Next() {
        if ($this.Pos -ge $this.Text.Length) { throw 'JSON: unexpected end' }
        $c = $this.Text[$this.Pos]
        $this.Pos++
        return $c
    }

    [object] ReadValue() {
        if ($this.Pos -ge $this.Text.Length) { throw 'JSON: unexpected end' }
        $c = $this.Text[$this.Pos]
        if ($c -eq [char]'{') { return $this.ReadObject() }
        if ($c -eq [char]'[') { return $this.ReadArray() }
        if ($c -eq [char]'"') { return $this.ReadString() }
        if ([string]::CompareOrdinal($this.Text, $this.Pos, 'true', 0, 4) -eq 0) { $this.Pos += 4; return $true }
        if ([string]::CompareOrdinal($this.Text, $this.Pos, 'false', 0, 5) -eq 0) { $this.Pos += 5; return $false }
        if ([string]::CompareOrdinal($this.Text, $this.Pos, 'null', 0, 4) -eq 0) { $this.Pos += 4; return $null }
        $match = [MonitorJsonReader]::Number.Match($this.Text, $this.Pos)
        if (-not $match.Success) { throw 'JSON: unexpected character' }
        $this.Pos += $match.Length
        $invariant = [Globalization.CultureInfo]::InvariantCulture
        if (-not $match.Groups[1].Success -and -not $match.Groups[2].Success) {
            $integer = [long]0
            if ([long]::TryParse($match.Value, [Globalization.NumberStyles]::AllowLeadingSign, $invariant, [ref]$integer)) {
                return $integer
            }
        }
        return [double]::Parse($match.Value, $invariant)
    }

    [object] ReadObject() {
        $result = [System.Collections.Specialized.OrderedDictionary]::new([StringComparer]::Ordinal)
        $this.Pos++
        $this.SkipSpace()
        if ($this.Pos -lt $this.Text.Length -and $this.Text[$this.Pos] -eq [char]'}') { $this.Pos++; return $result }
        while ($true) {
            $this.SkipSpace()
            if ($this.Pos -ge $this.Text.Length -or $this.Text[$this.Pos] -ne [char]'"') { throw 'JSON: expected a key' }
            $key = $this.ReadString()
            if ($result.Contains($key)) { throw 'JSON: duplicate key' }
            $this.SkipSpace()
            if ($this.Next() -ne [char]':') { throw 'JSON: expected :' }
            $this.SkipSpace()
            $result.Add($key, $this.ReadValue())
            $this.SkipSpace()
            $c = $this.Next()
            if ($c -eq [char]'}') { return $result }
            if ($c -ne [char]',') { throw 'JSON: expected , or }' }
        }
        return $result
    }

    [object] ReadArray() {
        $list = [System.Collections.ArrayList]::new()
        $this.Pos++
        $this.SkipSpace()
        if ($this.Pos -lt $this.Text.Length -and $this.Text[$this.Pos] -eq [char]']') { $this.Pos++; return $list.ToArray() }
        while ($true) {
            $this.SkipSpace()
            [void]$list.Add($this.ReadValue())
            $this.SkipSpace()
            $c = $this.Next()
            if ($c -eq [char]']') { return $list.ToArray() }
            if ($c -ne [char]',') { throw 'JSON: expected , or ]' }
        }
        return $list.ToArray()
    }

    [string] ReadString() {
        $this.Pos++
        $builder = [System.Text.StringBuilder]::new()
        $stops = [char[]]@([char]'"', [char]'\')
        while ($true) {
            $stop = $this.Text.IndexOfAny($stops, $this.Pos)
            if ($stop -lt 0) { throw 'JSON: unterminated string' }
            for ($k = $this.Pos; $k -lt $stop; $k++) {
                if ([int]$this.Text[$k] -lt 32) { throw 'JSON: control character in string' }
            }
            [void]$builder.Append($this.Text, $this.Pos, $stop - $this.Pos)
            $this.Pos = $stop + 1
            if ($this.Text[$stop] -eq [char]'"') { return $builder.ToString() }
            $escape = $this.Next()
            if ($escape -ceq [char]'"') { [void]$builder.Append([char]'"') }
            elseif ($escape -ceq [char]'\') { [void]$builder.Append([char]'\') }
            elseif ($escape -ceq [char]'/') { [void]$builder.Append([char]'/') }
            elseif ($escape -ceq [char]'b') { [void]$builder.Append([char]8) }
            elseif ($escape -ceq [char]'f') { [void]$builder.Append([char]12) }
            elseif ($escape -ceq [char]'n') { [void]$builder.Append([char]10) }
            elseif ($escape -ceq [char]'r') { [void]$builder.Append([char]13) }
            elseif ($escape -ceq [char]'t') { [void]$builder.Append([char]9) }
            elseif ($escape -ceq [char]'u') {
                if ($this.Pos + 4 -gt $this.Text.Length) { throw 'JSON: short unicode escape' }
                $hex = $this.Text.Substring($this.Pos, 4)
                if ($hex -notmatch '\A[0-9A-Fa-f]{4}\z') { throw 'JSON: bad unicode escape' }
                [void]$builder.Append([char][Convert]::ToInt32($hex, 16))
                $this.Pos += 4
            }
            else { throw 'JSON: bad escape' }
        }
        return $builder.ToString()
    }
}

function Add-JsonString([System.Text.StringBuilder]$builder, [string]$text) {
    # Pure ASCII output: every character outside printable ASCII is escaped.
    [void]$builder.Append('"')
    foreach ($ch in $text.ToCharArray()) {
        $code = [int]$ch
        if ($ch -eq [char]'"') { [void]$builder.Append('\"') }
        elseif ($ch -eq [char]'\') { [void]$builder.Append('\\') }
        elseif ($code -eq 10) { [void]$builder.Append('\n') }
        elseif ($code -eq 13) { [void]$builder.Append('\r') }
        elseif ($code -eq 9) { [void]$builder.Append('\t') }
        elseif ($code -lt 32 -or $code -gt 126) { [void]$builder.Append('\u').Append($code.ToString('x4')) }
        else { [void]$builder.Append($ch) }
    }
    [void]$builder.Append('"')
}

function Add-JsonValue([System.Text.StringBuilder]$builder, $value) {
    if ($null -eq $value) { [void]$builder.Append('null'); return }
    if ($value -is [string]) { Add-JsonString $builder $value; return }
    if ($value -is [bool]) {
        if ($value) { [void]$builder.Append('true') } else { [void]$builder.Append('false') }
        return
    }
    if ($value -is [int] -or $value -is [long]) {
        [void]$builder.Append($value.ToString([Globalization.CultureInfo]::InvariantCulture))
        return
    }
    if ($value -is [System.Collections.IDictionary]) {
        [void]$builder.Append('{')
        $first = $true
        foreach ($entry in $value.GetEnumerator()) {
            if (-not $first) { [void]$builder.Append(',') }
            $first = $false
            Add-JsonString $builder ([string]$entry.Key)
            [void]$builder.Append(':')
            Add-JsonValue $builder $entry.Value
        }
        [void]$builder.Append('}')
        return
    }
    if ($value -is [System.Collections.IEnumerable]) {
        [void]$builder.Append('[')
        $first = $true
        foreach ($item in $value) {
            if (-not $first) { [void]$builder.Append(',') }
            $first = $false
            Add-JsonValue $builder $item
        }
        [void]$builder.Append(']')
        return
    }
    throw "JSON: cannot write a value of type $($value.GetType().FullName)"
}

function ConvertTo-MonitorJson($value) {
    $builder = New-Object System.Text.StringBuilder
    Add-JsonValue $builder $value
    return $builder.ToString()
}

function New-JsonObject {
    return [System.Collections.Specialized.OrderedDictionary]::new([StringComparer]::Ordinal)
}

# --- output -----------------------------------------------------------------------

function Write-MonitorLine([string]$text) {
    [Console]::Out.Write($text + "`n")
    [Console]::Out.Flush()
    $script:printed = $true
}

function Write-Report([string]$status, $new, $unknown, $faults, $protected) {
    $report = New-JsonObject
    $report.Add('status', $status)
    $report.Add('new', @($new))
    $report.Add('unknown', @($unknown))
    $report.Add('faultShapedPresent', @($faults))
    $report.Add('protected', @($protected))
    Write-MonitorLine (ConvertTo-MonitorJson $report)
}

function New-UnknownEntry($root, [string]$reason) {
    $entry = New-JsonObject
    $entry.Add('root', $root)
    $entry.Add('reason', $reason)
    return $entry
}

function Write-Notice([string[]]$notices) {
    # One object whose only key is systemMessage.
    $message = New-JsonObject
    $message.Add('systemMessage', ($notices -join "`n"))
    Write-MonitorLine (ConvertTo-MonitorJson $message)
}

# --- arguments ----------------------------------------------------------------------

function Read-MonitorArguments([string[]]$arguments) {
    $parsed = @{
        Mode = $null; Roots = New-Object System.Collections.ArrayList; SnapshotDir = $null
        SessionId = $null; Protected = New-Object System.Collections.ArrayList; Bad = $false
    }
    $names = @{ '-mode' = 'Mode'; '-root' = 'Roots'; '-snapshotdir' = 'SnapshotDir'; '-sessionid' = 'SessionId'; '-protectedpath' = 'Protected' }
    $index = 0
    while ($index -lt $arguments.Count) {
        $token = [string]$arguments[$index]
        $name = $null
        if ($token -match '\A-[A-Za-z]+\z') { $name = $names[$token.ToLowerInvariant()] }
        if ($null -eq $name -or $index + 1 -ge $arguments.Count -or [string]::IsNullOrEmpty([string]$arguments[$index + 1])) {
            $parsed.Bad = $true
            $index++
            continue
        }
        $value = [string]$arguments[$index + 1]
        if ($name -eq 'Roots' -or $name -eq 'Protected') {
            [void]$parsed[$name].Add($value)
        }
        elseif ($null -ne $parsed[$name]) {
            $parsed.Bad = $true
        }
        else {
            $parsed[$name] = $value
        }
        $index += 2
    }
    if ($null -ne $parsed.Mode) {
        $canonical = $null
        foreach ($mode in $modes) { if ($mode -eq $parsed.Mode) { $canonical = $mode } }
        if ($null -eq $canonical) { $parsed.Bad = $true }
        $parsed.Mode = $canonical
    }
    else {
        $parsed.Bad = $true
    }
    return $parsed
}

# --- paths and roots ------------------------------------------------------------------

function Get-MonitorRoots($parsed) {
    if ($parsed.Roots.Count -gt 0) { return @($parsed.Roots.ToArray()) }
    if (-not $script:onWindows) { return $null }
    $fixed = New-Object System.Collections.ArrayList
    foreach ($drive in [IO.DriveInfo]::GetDrives()) {
        if ($drive.DriveType -eq [IO.DriveType]::Fixed) { [void]$fixed.Add($drive.Name) }
    }
    return @($fixed.ToArray())
}

function Get-ComparablePath([string]$path) {
    $full = [IO.Path]::GetFullPath($path)
    $trimmed = $full.TrimEnd([char[]]@([char]'\', [char]'/'))
    if ($trimmed.Length -eq 0) { return $full }
    return $trimmed
}

function Get-SnapshotPathRefusal([string]$snapshotPath, [string[]]$roots, $protected) {
    # The one written file is never a direct child of a monitored root nor
    # inside a protected tree. Returns a reason code, or $null.
    $target = Get-ComparablePath $snapshotPath
    $parent = Get-ComparablePath ([IO.Path]::GetDirectoryName($target))
    foreach ($tree in @($builtinProtected) + @($protected)) {
        $guarded = $null
        try { $guarded = Get-ComparablePath $tree } catch { return 'protected-path' }
        if ([string]::Equals($target, $guarded, $script:nameComparison) -or
            $target.StartsWith($guarded + '\', $script:nameComparison) -or
            $target.StartsWith($guarded + '/', $script:nameComparison)) {
            return 'protected-path'
        }
    }
    foreach ($root in $roots) {
        if ([string]::Equals($parent, (Get-ComparablePath $root), $script:nameComparison)) { return 'root-parent-path' }
    }
    return $null
}

function Get-RootState([string]$root) {
    # Names only, one level, hidden and system entries included, nothing
    # followed. Any enumeration error makes the root unreadable.
    if (-not [IO.Directory]::Exists($root)) { return @{ State = 'missing'; Names = @() } }
    $names = New-Object System.Collections.ArrayList
    try {
        foreach ($entry in [IO.Directory]::EnumerateFileSystemEntries($root)) {
            [void]$names.Add([IO.Path]::GetFileName($entry))
        }
    }
    catch {
        return @{ State = 'unreadable'; Names = @() }
    }
    return @{ State = 'ok'; Names = @($names.ToArray()) }
}

function Get-FaultShaped([string]$root, [string[]]$names) {
    # An existing single-letter child is the X:\<letter> fault shape.
    $found = New-Object System.Collections.ArrayList
    foreach ($name in $names) {
        if ($name -cmatch '\A[A-Za-z]\z') { [void]$found.Add([IO.Path]::Combine($root, $name)) }
    }
    return @($found.ToArray())
}

# --- the snapshot file ---------------------------------------------------------------------

function Get-UtcStamp {
    return [DateTime]::UtcNow.ToString("yyyy-MM-dd'T'HH:mm:ss.fff'Z'", [Globalization.CultureInfo]::InvariantCulture)
}

function Test-SharingViolation($exception) {
    $e = $exception
    while ($e -is [System.Management.Automation.MethodInvocationException] -and $null -ne $e.InnerException) { $e = $e.InnerException }
    if (-not ($e -is [IO.IOException])) { return $false }
    if ($e -is [IO.FileNotFoundException] -or $e -is [IO.DirectoryNotFoundException] -or $e -is [IO.PathTooLongException]) { return $false }
    $code = $e.HResult
    if ($script:onWindows) {
        # ERROR_SHARING_VIOLATION (32) and ERROR_LOCK_VIOLATION (33).
        return ($code -lt 0 -and @(32, 33) -contains ($code -band 0xFFFF))
    }
    # .NET on Unix implements FileShare.None with flock; a held lock is
    # EWOULDBLOCK (errno 11 on Linux, 35 on macOS), raised with the same
    # sharing-violation message Windows uses.
    if (@(11, 35) -contains $code) { return $true }
    return ($e.Message -like '*being used by another process*')
}

function Open-Snapshot([string]$path, [IO.FileMode]$mode, [IO.FileAccess]$access, [IO.FileShare]$share) {
    # $null means another instance holds the file. Every other failure throws.
    try {
        return [IO.File]::Open($path, $mode, $access, $share)
    }
    catch {
        if (Test-SharingViolation $_.Exception) { return $null }
        throw
    }
}

function Read-SnapshotText([IO.FileStream]$stream) {
    $stream.Position = 0
    $length = [int]$stream.Length
    $buffer = New-Object byte[] $length
    $read = 0
    while ($read -lt $length) {
        $count = $stream.Read($buffer, $read, $length - $read)
        if ($count -le 0) { break }
        $read += $count
    }
    $text = [Text.Encoding]::UTF8.GetString($buffer, 0, $read)
    if ($text.Length -gt 0 -and $text[0] -eq [char]0xFEFF) { $text = $text.Substring(1) }
    return $text
}

function Write-SnapshotStream([IO.FileStream]$stream, $document) {
    $bytes = [Text.Encoding]::UTF8.GetBytes((ConvertTo-MonitorJson $document))
    $stream.SetLength(0)
    $stream.Position = 0
    $stream.Write($bytes, 0, $bytes.Length)
    $stream.Flush($true)
}

function Read-SnapshotDocument([string]$text, [string]$sessionId) {
    # Returns @{ Reason = $null or snapshot-invalid / schema-mismatch; Document }.
    $document = $null
    try { $document = [MonitorJsonReader]::Parse($text) }
    catch { return @{ Reason = 'snapshot-invalid'; Document = $null } }
    $mismatch = @{ Reason = 'schema-mismatch'; Document = $null }
    if (-not ($document -is [System.Collections.IDictionary])) { return $mismatch }
    if ($document.Count -ne $snapshotKeys.Count) { return $mismatch }
    foreach ($key in $snapshotKeys) { if (-not $document.Contains($key)) { return $mismatch } }
    $version = $document['schemaVersion']
    if (-not ($version -is [long]) -or $version -ne 1) { return $mismatch }
    if (-not ($document['sessionId'] -is [string]) -or $document['sessionId'] -cne $sessionId) { return $mismatch }
    $created = $document['createdUtc']
    if (-not ($created -is [string]) -or $created -cnotmatch '\A\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z\z') { return $mismatch }
    if (-not ($document['source'] -is [string]) -or $sources -cnotcontains $document['source']) { return $mismatch }
    $roots = $document['roots']
    if (-not ($roots -is [System.Collections.IDictionary])) { return $mismatch }
    foreach ($entry in $roots.GetEnumerator()) {
        if (-not ($entry.Value -is [object[]])) { return $mismatch }
        foreach ($name in $entry.Value) { if (-not ($name -is [string])) { return $mismatch } }
    }
    $announced = $document['announced']
    if (-not ($announced -is [System.Collections.IDictionary])) { return $mismatch }
    foreach ($entry in $announced.GetEnumerator()) {
        if ([string]$entry.Key -cnotmatch $announcedPattern -or -not ($entry.Value -is [string])) { return $mismatch }
    }
    return @{ Reason = $null; Document = $document }
}

function New-SnapshotDocument([string]$sessionId, [string]$source, [string[]]$roots) {
    # Returns @{ Document; Unknown = [{root, reason}] } for roots that could not
    # be recorded (missing or unreadable now).
    $recorded = New-JsonObject
    $unknown = New-Object System.Collections.ArrayList
    foreach ($root in $roots) {
        if ($recorded.Contains($root)) { continue }
        $state = Get-RootState $root
        if ($state.State -eq 'ok') { $recorded.Add($root, @($state.Names)) }
        elseif ($state.State -eq 'missing') { [void]$unknown.Add((New-UnknownEntry $root 'root-missing')) }
        else { [void]$unknown.Add((New-UnknownEntry $root 'root-unreadable')) }
    }
    $document = New-JsonObject
    $document.Add('schemaVersion', 1)
    $document.Add('sessionId', $sessionId)
    $document.Add('createdUtc', (Get-UtcStamp))
    $document.Add('source', $source)
    $document.Add('roots', $recorded)
    $document.Add('announced', (New-JsonObject))
    return @{ Document = $document; Unknown = @($unknown.ToArray()) }
}

function Compare-MonitorSnapshot($document, [string[]]$roots) {
    # The delta between the snapshot and the roots now. Every root named now or
    # in the snapshot is classified once.
    $snapshotRoots = $document['roots']
    $result = @{
        New = New-Object System.Collections.ArrayList        # @{ Root; Paths }
        Unknown = New-Object System.Collections.ArrayList    # {root, reason}
        RootNew = New-Object System.Collections.ArrayList    # roots absent from the snapshot
        RootGone = New-Object System.Collections.ArrayList   # snapshot roots missing or unreadable
        Faults = New-Object System.Collections.ArrayList
    }
    $all = New-Object System.Collections.ArrayList
    $seen = New-Object 'System.Collections.Generic.HashSet[string]' ($script:nameComparer)
    foreach ($root in $roots) {
        if ($seen.Add([string]$root)) { [void]$all.Add([string]$root) }
    }
    foreach ($entry in $snapshotRoots.GetEnumerator()) {
        if ($seen.Add([string]$entry.Key)) { [void]$all.Add([string]$entry.Key) }
    }
    foreach ($root in $all) {
        $recorded = $null
        foreach ($entry in $snapshotRoots.GetEnumerator()) {
            if ([string]::Equals([string]$entry.Key, $root, $script:nameComparison)) { $recorded = @($entry.Value); break }
        }
        $state = Get-RootState $root
        if ($state.State -eq 'ok') {
            foreach ($fault in (Get-FaultShaped $root $state.Names)) { [void]$result.Faults.Add($fault) }
        }
        if ($null -eq $recorded) {
            [void]$result.RootNew.Add($root)
            if ($state.State -eq 'missing') { [void]$result.Unknown.Add((New-UnknownEntry $root 'root-missing')) }
            else { [void]$result.Unknown.Add((New-UnknownEntry $root 'root-new')) }
            continue
        }
        if ($state.State -ne 'ok') {
            [void]$result.RootGone.Add($root)
            if ($state.State -eq 'missing') { [void]$result.Unknown.Add((New-UnknownEntry $root 'root-missing')) }
            else { [void]$result.Unknown.Add((New-UnknownEntry $root 'root-unreadable')) }
            continue
        }
        $known = New-Object 'System.Collections.Generic.HashSet[string]' ($script:nameComparer)
        foreach ($name in $recorded) { [void]$known.Add([string]$name) }
        $paths = New-Object System.Collections.ArrayList
        foreach ($name in $state.Names) {
            if (-not $known.Contains($name)) { [void]$paths.Add([IO.Path]::Combine($root, $name)) }
        }
        if ($paths.Count -gt 0) { [void]$result.New.Add(@{ Root = $root; Paths = @($paths.ToArray()) }) }
    }
    return $result
}

# --- modes ---------------------------------------------------------------------------------

function Get-SnapshotDirectory($parsed) {
    if ([string]::IsNullOrEmpty($parsed.SnapshotDir)) { return [IO.Path]::GetTempPath() }
    return $parsed.SnapshotDir
}

function Get-SnapshotPath([string]$directory, [string]$sessionId) {
    return [IO.Path]::Combine($directory, $snapshotPrefix + $sessionId + '.json')
}

function Invoke-Standalone($parsed) {
    $protectedList = @(@($builtinProtected) + @($parsed.Protected.ToArray()))
    $roots = $null
    if (-not $parsed.Bad) { $roots = Get-MonitorRoots $parsed }
    if ($parsed.Bad -or $null -eq $roots -or @($roots).Count -eq 0) {
        Write-Report 'UNKNOWN' @() @((New-UnknownEntry $null 'bad-arguments')) @() $protectedList
        $script:exitCode = 11
        return
    }
    $roots = @($roots)
    if ($parsed.Mode -eq 'ListRoots') {
        $listing = New-JsonObject
        $listing.Add('roots', $roots)
        Write-MonitorLine (ConvertTo-MonitorJson $listing)
        $script:exitCode = 0
        return
    }
    if ($null -eq $parsed.SessionId) {
        Write-Report 'UNKNOWN' @() @((New-UnknownEntry $null 'bad-arguments')) @() $protectedList
        $script:exitCode = 11
        return
    }
    if ($parsed.SessionId -cnotmatch $sessionIdPattern) {
        Write-Report 'UNKNOWN' @() @((New-UnknownEntry $null 'session-id-invalid')) @() $protectedList
        $script:exitCode = 11
        return
    }
    $path = Get-SnapshotPath (Get-SnapshotDirectory $parsed) $parsed.SessionId
    $refusal = Get-SnapshotPathRefusal $path $roots $parsed.Protected.ToArray()
    if ($null -ne $refusal) {
        Write-Report 'UNKNOWN' @() @((New-UnknownEntry $null $refusal)) @() $protectedList
        $script:exitCode = 11
        return
    }

    if ($parsed.Mode -eq 'Snapshot') {
        $stream = Open-Snapshot $path ([IO.FileMode]::OpenOrCreate) ([IO.FileAccess]::ReadWrite) ([IO.FileShare]::None)
        if ($null -eq $stream) { throw 'the snapshot is held by another instance' }
        $faults = New-Object System.Collections.ArrayList
        try {
            $created = New-SnapshotDocument $parsed.SessionId 'startup' $roots
            Write-SnapshotStream $stream $created.Document
        }
        finally { $stream.Dispose() }
        foreach ($entry in $created.Document['roots'].GetEnumerator()) {
            foreach ($fault in (Get-FaultShaped ([string]$entry.Key) @($entry.Value))) { [void]$faults.Add($fault) }
        }
        $unknown = @($created.Unknown)
        if ($unknown.Count -gt 0) { $status = 'UNKNOWN'; $script:exitCode = 11 } else { $status = 'CLEAN'; $script:exitCode = 0 }
        Write-Report $status @() $unknown @($faults.ToArray()) $protectedList
        return
    }

    $unknown = New-Object System.Collections.ArrayList
    $new = New-Object System.Collections.ArrayList
    $faults = New-Object System.Collections.ArrayList
    $document = $null
    if (-not [IO.File]::Exists($path)) {
        [void]$unknown.Add((New-UnknownEntry $null 'snapshot-missing'))
    }
    else {
        $stream = Open-Snapshot $path ([IO.FileMode]::Open) ([IO.FileAccess]::Read) ([IO.FileShare]::Read)
        if ($null -eq $stream) { throw 'the snapshot is held by another instance' }
        try { $text = Read-SnapshotText $stream } finally { $stream.Dispose() }
        $read = Read-SnapshotDocument $text $parsed.SessionId
        if ($null -ne $read.Reason) { [void]$unknown.Add((New-UnknownEntry $null $read.Reason)) }
        else { $document = $read.Document }
    }
    if ($null -ne $document) {
        $delta = Compare-MonitorSnapshot $document $roots
        foreach ($item in $delta.New) { foreach ($p in $item.Paths) { [void]$new.Add($p) } }
        foreach ($item in $delta.Unknown) { [void]$unknown.Add($item) }
        foreach ($item in $delta.Faults) { [void]$faults.Add($item) }
    }
    else {
        foreach ($root in $roots) {
            $state = Get-RootState $root
            if ($state.State -eq 'ok') { foreach ($fault in (Get-FaultShaped $root $state.Names)) { [void]$faults.Add($fault) } }
        }
    }
    if ($unknown.Count -gt 0) { $status = 'UNKNOWN'; $script:exitCode = 11 }
    elseif ($new.Count -gt 0) { $status = 'NEW_CHILDREN'; $script:exitCode = 10 }
    else { $status = 'CLEAN'; $script:exitCode = 0 }
    Write-Report $status @($new.ToArray()) @($unknown.ToArray()) @($faults.ToArray()) $protectedList
}

function Read-HookSessionId {
    # Returns @{ SessionId; Source } or $null when the payload has no usable id.
    $raw = [Console]::In.ReadToEnd()
    $payload = $null
    try { $payload = [MonitorJsonReader]::Parse($raw) } catch { return $null }
    if (-not ($payload -is [System.Collections.IDictionary])) { return $null }
    $sessionId = $payload['session_id']
    if (-not ($sessionId -is [string]) -or $sessionId -cnotmatch $sessionIdPattern) { return $null }
    $source = $payload['source']
    if (-not ($source -is [string]) -or @('startup', 'clear', 'resume', 'compact') -cnotcontains $source) { $source = 'startup' }
    return @{ SessionId = $sessionId; Source = $source }
}

function Get-HookContext($parsed) {
    # Everything a hook needs before it touches the file. Throws on bad
    # arguments or an unusable snapshot path; $null means an unusable session id.
    if ($parsed.Bad) { throw 'bad arguments' }
    $roots = Get-MonitorRoots $parsed
    if ($null -eq $roots -or @($roots).Count -eq 0) { throw 'no roots to monitor' }
    $identity = Read-HookSessionId
    if ($null -eq $identity) { return $null }
    $directory = Get-SnapshotDirectory $parsed
    $path = Get-SnapshotPath $directory $identity.SessionId
    $refusal = Get-SnapshotPathRefusal $path @($roots) $parsed.Protected.ToArray()
    if ($null -ne $refusal) { throw "snapshot path refused: $refusal" }
    if (-not [IO.Directory]::Exists($directory)) { throw 'the snapshot directory does not exist' }
    return @{ Roots = @($roots); SessionId = $identity.SessionId; Source = $identity.Source; Path = $path }
}

function Invoke-HookSessionStart($parsed) {
    # Nothing on stdout in any path.
    $context = Get-HookContext $parsed
    if ($null -eq $context) { return }
    $stream = Open-Snapshot $context.Path ([IO.FileMode]::OpenOrCreate) ([IO.FileAccess]::ReadWrite) ([IO.FileShare]::None)
    if ($null -eq $stream) { return }
    try {
        if ($context.Source -eq 'compact') {
            $read = Read-SnapshotDocument (Read-SnapshotText $stream) $context.SessionId
            if ($null -eq $read.Reason) { return }
        }
        $created = New-SnapshotDocument $context.SessionId $context.Source $context.Roots
        Write-SnapshotStream $stream $created.Document
    }
    finally { $stream.Dispose() }
}

function Get-StopNotices($document, [string[]]$roots, [string]$sessionId) {
    # Every kind once per snapshot; `announced` is the only gate.
    # Returns @{ Notices; Keys } for what has not been announced yet.
    $announced = New-Object 'System.Collections.Generic.HashSet[string]' ($script:nameComparer)
    foreach ($key in $document['announced'].Keys) { [void]$announced.Add([string]$key) }
    $since = [string]$document['createdUtc']
    $notices = New-Object System.Collections.ArrayList
    $keys = New-Object System.Collections.ArrayList
    $delta = Compare-MonitorSnapshot $document $roots

    $midsession = 'midsession|' + $sessionId
    if ($document['source'] -ceq 'stop-baseline' -and -not $announced.Contains($midsession)) {
        [void]$notices.Add("Drive-root monitoring began mid-session at $since; children created earlier in this session are not covered.")
        [void]$keys.Add($midsession)
    }
    foreach ($root in $delta.RootNew) {
        $key = 'newroot|' + $root
        if ($announced.Contains($key)) { continue }
        [void]$notices.Add("$root was not present when monitoring began at $since; UNKNOWN.")
        [void]$keys.Add($key)
    }
    foreach ($root in $delta.RootGone) {
        $key = 'rootgone|' + $root
        if ($announced.Contains($key)) { continue }
        [void]$notices.Add("$root was present when monitoring began at $since but is missing or unreadable now; UNKNOWN.")
        [void]$keys.Add($key)
    }
    foreach ($item in $delta.New) {
        $fresh = New-Object System.Collections.ArrayList
        foreach ($path in $item.Paths) {
            $key = 'child|' + $path
            if ($announced.Contains($key)) { continue }
            [void]$fresh.Add($path)
            [void]$keys.Add($key)
        }
        if ($fresh.Count -gt 0) {
            [void]$notices.Add("New direct child(ren) of $($item.Root) since monitoring began at ${since}: $($fresh -join ', '). Cause unknown; not necessarily created by this session.")
        }
    }
    foreach ($fault in $delta.Faults) {
        $key = 'fault|' + $fault
        if ($announced.Contains($key)) { continue }
        [void]$notices.Add("Single-letter child exists: $fault. It matches the MSYS fault shape; its origin is not known.")
        [void]$keys.Add($key)
    }
    return @{ Notices = @($notices.ToArray()); Keys = @($keys.ToArray()) }
}

function Invoke-HookStop($parsed) {
    $context = Get-HookContext $parsed
    if ($null -eq $context) {
        Write-Notice @($textInvalidSessionId)
        return
    }
    $stream = $null
    $baseline = $false
    if ([IO.File]::Exists($context.Path)) {
        $stream = Open-Snapshot $context.Path ([IO.FileMode]::Open) ([IO.FileAccess]::ReadWrite) ([IO.FileShare]::None)
        if ($null -eq $stream) { return }
        # A zero-length file (a crash between creation and the first write)
        # holds no state, so it is baselined like a missing one, under the
        # handle already held. Any non-empty invalid content stays evidence.
        if ($stream.Length -eq 0) { $baseline = $true }
    }
    else {
        # Mid-session baseline: created under the same exclusive handle.
        try {
            $stream = [IO.File]::Open($context.Path, [IO.FileMode]::CreateNew, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
        }
        catch {
            # Another instance created it first, or holds it: its job, not ours.
            if ([IO.File]::Exists($context.Path) -or (Test-SharingViolation $_.Exception)) { return }
            throw
        }
        $baseline = $true
    }
    try {
        if ($baseline) {
            $document = (New-SnapshotDocument $context.SessionId 'stop-baseline' $context.Roots).Document
            Write-SnapshotStream $stream $document
        }
        else {
            $read = Read-SnapshotDocument (Read-SnapshotText $stream) $context.SessionId
            if ($null -ne $read.Reason) {
                # No usable state to dedupe against, so this repeats every Stop,
                # and the file is evidence: it is never overwritten here.
                Write-Notice @($textInvalidSnapshot)
                return
            }
            $document = $read.Document
        }
        $pending = Get-StopNotices $document $context.Roots $context.SessionId
        if ($pending.Notices.Count -eq 0) { return }
        # Print first, then record, still holding the handle.
        Write-Notice $pending.Notices
        $stamp = Get-UtcStamp
        foreach ($key in $pending.Keys) {
            if (-not $document['announced'].Contains($key)) { $document['announced'].Add($key, $stamp) }
        }
        Write-SnapshotStream $stream $document
    }
    finally { $stream.Dispose() }
}

function Invoke-MonitorMain([string[]]$arguments) {
    $parsed = Read-MonitorArguments $arguments
    if ($parsed.Mode -eq 'HookSessionStart' -or $parsed.Mode -eq 'HookStop') {
        $script:hookMode = $parsed.Mode
        $script:exitCode = 0
        if ($parsed.Mode -eq 'HookSessionStart') { Invoke-HookSessionStart $parsed } else { Invoke-HookStop $parsed }
        return
    }
    Invoke-Standalone $parsed
}

# --- entry point ------------------------------------------------------------------------------
# Pipeline output is discarded; everything this script prints goes through
# Write-MonitorLine, so no stray value can reach stdout.
try {
    $null = Invoke-MonitorMain @($args)
}
catch {
    if ($script:hookMode -eq 'HookStop') {
        if (-not $script:printed) { Write-Notice @($textInternal) }
        $script:exitCode = 0
    }
    elseif ($script:hookMode -eq 'HookSessionStart') {
        $script:exitCode = 0
    }
    else {
        if (-not $script:printed) {
            Write-Report 'UNKNOWN' @() @((New-UnknownEntry $null 'internal')) @() @($builtinProtected)
        }
        $script:exitCode = 11
    }
}
exit $script:exitCode
