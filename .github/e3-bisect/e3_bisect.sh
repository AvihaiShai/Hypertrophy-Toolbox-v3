#!/usr/bin/env bash
# TEMP E3 diagnostic for H-LINUX-UNSYNC-01: compare-only, bounded first-parent
# bisect of 31659a59..b36ea9e1 for the single capture `backup desktop light`.
# Pre-registered in docs/deep_gate_linux_visual_failure_20260831/GATE2.md.
#
# Usage: e3_bisect.sh bisect
#        e3_bisect.sh confirm <last-good-sha> <first-bad-sha>
#
# Every diagnostic outcome, including "inconclusive", exits 0 and is reported in
# verdict.env; the job conclusion is not the result. A non-zero exit means a
# harness fault: a pre-registered input did not match, or a baseline was written.
set -euo pipefail

MODE="${1:?mode}"
REPO="$GITHUB_WORKSPACE/repo"
OUT="$GITHUB_WORKSPACE/e3-artifacts"
WORK="$RUNNER_TEMP/e3-probes"

CONTROL=31659a59ccc82391287d98f2e9d899a048d20b2c
TREATMENT=b36ea9e1a3d7e0e37918e9db4198cb4bf7e0ecf8
CANDIDATE_COUNT=50
CANDIDATE_DIGEST=d11d59a010a447bb0866d6f9d0b15145a3cf9c89b44f2ce192b51849011bc6d2
LINUX_BASELINE_TREE=206f30d8b7e90777bcf157217d04839045528000
BASELINE_REL=e2e/__screenshots__/linux/visual.spec.ts-snapshots/backup-desktop-light.png
BASELINE_SHA=4e116bdb35cc6697d92d3f77249f9b9e032f8ceef3b0e6e0d5c2159ba4ff87ca
SELECTOR='backup desktop light$'
INVOCATIONS=3
MAX_BISECT_PROBES=6

mkdir -p "$OUT/probes" "$WORK"
RESULTS="$OUT/results.tsv"
printf 'order\tphase\tcommit\tclass\tinvocations\tactual_sha256\tdiff_sha256\tpixel_line\n' > "$RESULTS"

die() { printf 'HARNESS FAULT: %s\n' "$*" | tee -a "$OUT/harness-fault.txt" >&2; exit 1; }

{
  printf 'harness_commit=%s\n' "$(git -C "$REPO" rev-parse HEAD)"
  printf 'mode=%s\n' "$MODE"
  printf 'ImageOS=%s\nImageVersion=%s\nRUNNER_NAME=%s\n' "${ImageOS:-unset}" "${ImageVersion:-unset}" "${RUNNER_NAME:-unset}"
  uname -a
  cat /etc/os-release
  printf 'node=%s\nnpm=%s\n' "$(node --version)" "$(npm --version)"
  python --version
  printf 'started_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$OUT/environment.txt"

# --- the candidate set must be exactly the pre-registered one ---------------------
mapfile -t CANDIDATES < <(git -C "$REPO" rev-list --first-parent --reverse "$CONTROL..$TREATMENT")
[ "${#CANDIDATES[@]}" -eq "$CANDIDATE_COUNT" ] || die "candidate count ${#CANDIDATES[@]} != $CANDIDATE_COUNT"
[ "${CANDIDATES[-1]}" = "$TREATMENT" ] || die "last candidate is not the treatment endpoint"
[ "$(git -C "$REPO" rev-parse "${CANDIDATES[0]}^1")" = "$CONTROL" ] || die "first candidate's first parent is not the control"
digest="$(printf '%s\n' "${CANDIDATES[@]}" | sha256sum | cut -d' ' -f1)"
[ "$digest" = "$CANDIDATE_DIGEST" ] || die "candidate digest $digest != $CANDIDATE_DIGEST"
POSITIONS=("$CONTROL" "${CANDIDATES[@]}")   # POSITIONS[0]=control, POSITIONS[50]=treatment
printf '%s\n' "${POSITIONS[@]}" > "$OUT/positions.txt"

REF_PYTHON_VERSION_FILE=""
REF_PLAYWRIGHT=""
REF_BROWSER_PATH=""
REF_BROWSER_VERSION=""
BROWSER_INSTALLED=0
ORDER=0
NEXT_PORT=5100

record() {  # phase commit class invocations actual diff pixel_line
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$ORDER" "$@" >> "$RESULTS"
}

classify_invocation() {  # run_dir -> PASS | RENDER_FAIL | STARTUP_FAIL | OTHER_FAIL
  local run="$1" log="$1/playwright.log" code actuals
  code="$(cat "$run/exit-code.txt")"
  actuals="$(find "$run" -type f -name '*-actual.png' | wc -l)"
  if [ "$code" = 0 ] && [ "$actuals" -eq 0 ] \
     && grep -Eq '(^|[^0-9])1 passed' "$log" \
     && ! grep -Eq '[0-9]+ (failed|flaky|skipped|did not run)' "$log"; then
    echo PASS
  elif [ "$code" = 1 ] && [ "$actuals" -eq 1 ] \
     && grep -Fq 'toHaveScreenshot' "$log" \
     && grep -Eq 'pixels \(ratio [0-9.]+ of all image pixels\) are different|Expected an image [0-9]+px by [0-9]+px' "$log" \
     && ! grep -Eq 'consecutive|Timeout [0-9]+ms exceeded' "$log"; then
    echo RENDER_FAIL
  elif grep -Eq 'Process from config\.webServer|from config\.webServer|ECONNREFUSED|ERR_CONNECTION_REFUSED' "$log"; then
    echo STARTUP_FAIL
  else
    echo OTHER_FAIL
  fi
}

# probe <phase> <commit>; sets PROBE_CLASS, PROBE_ACTUAL, PROBE_DIFF.
# A baseline write is a hard stop for the whole run, never a probe result.
probe() {
  local phase="$1" commit="$2" short dir pdir run code i
  ORDER=$((ORDER + 1))
  short="${commit:0:8}"
  dir="$WORK/$ORDER-$short"
  pdir="$OUT/probes/$ORDER-$phase-$short"
  mkdir -p "$pdir"
  PROBE_CLASS="" PROBE_ACTUAL="-" PROBE_DIFF="-"
  local pixel_line="-"

  git -C "$REPO" worktree add --detach "$dir" "$commit" > "$pdir/checkout.log" 2>&1
  [ "$(git -C "$dir" rev-parse HEAD)" = "$commit" ] || die "checkout of $commit resolved elsewhere"

  # Inputs held equal across the whole interval (pre-registered).
  if [ "$(git -C "$dir" rev-parse "HEAD:e2e/__screenshots__/linux")" != "$LINUX_BASELINE_TREE" ] \
     || [ "$(sha256sum "$dir/$BASELINE_REL" | cut -d' ' -f1)" != "$BASELINE_SHA" ]; then
    PROBE_CLASS=INPUT_MISMATCH
  elif [ -n "$REF_PYTHON_VERSION_FILE" ] && ! cmp -s "$REF_PYTHON_VERSION_FILE" "$dir/.python-version"; then
    PROBE_CLASS=INPUT_MISMATCH
  fi

  if [ -z "$PROBE_CLASS" ]; then
    if ! (
      set -e
      cd "$dir"
      python -m venv .venv
      .venv/bin/python -m pip install --upgrade pip
      .venv/bin/python -m pip install -r requirements.txt
      npm ci
      npm run build:css
    ) > "$pdir/install.log" 2>&1; then
      PROBE_CLASS=INSTALL_FAIL
    fi
  fi

  if [ -z "$PROBE_CLASS" ] && [ "$BROWSER_INSTALLED" = 0 ]; then
    (cd "$dir" && npx playwright install --with-deps chromium) > "$OUT/browser-install.log" 2>&1 \
      || die "browser installation failed"
    BROWSER_INSTALLED=1
  fi

  if [ -z "$PROBE_CLASS" ]; then
    (
      cd "$dir"
      printf 'commit=%s\n' "$commit"
      npx sass --version
      npx playwright --version
      node -e "const { chromium } = require('playwright'); const p = chromium.executablePath(); console.log('browser_executable=' + p); console.log('browser_version=' + require('node:child_process').execFileSync(p, ['--version'], { encoding: 'utf8' }).trim());"
    ) > "$pdir/versions.txt" 2>&1 || true
    local pw bpath bver
    pw="$(grep -m1 '^Version ' "$pdir/versions.txt" || true)"
    bpath="$(grep -m1 '^browser_executable=' "$pdir/versions.txt" || true)"
    bver="$(grep -m1 '^browser_version=' "$pdir/versions.txt" || true)"
    if [ -z "$REF_PLAYWRIGHT" ]; then
      [ -n "$pw" ] && [ -n "$bpath" ] && [ -n "$bver" ] || die "could not read toolchain versions at $commit"
      REF_PLAYWRIGHT="$pw" REF_BROWSER_PATH="$bpath" REF_BROWSER_VERSION="$bver"
      REF_PYTHON_VERSION_FILE="$OUT/reference-python-version"
      cp "$dir/.python-version" "$REF_PYTHON_VERSION_FILE"
    elif [ "$pw" != "$REF_PLAYWRIGHT" ] || [ "$bpath" != "$REF_BROWSER_PATH" ] || [ "$bver" != "$REF_BROWSER_VERSION" ]; then
      PROBE_CLASS=ENV_MISMATCH
    fi
  fi

  if [ -z "$PROBE_CLASS" ]; then
    (cd "$dir" && npx playwright test e2e/visual.spec.ts --project=chromium --grep "$SELECTOR" --list) \
      > "$pdir/test-list.txt" 2>&1 || true
    grep -Fxq 'Total: 1 test in 1 file' "$pdir/test-list.txt" || PROBE_CLASS=SELECTOR_FAIL
  fi

  local classes=()
  if [ -z "$PROBE_CLASS" ]; then
    find "$dir/e2e/__screenshots__" -type f -print0 | sort -z | xargs -0 sha256sum > "$pdir/baselines-before.sha256"
    for i in $(seq 1 "$INVOCATIONS"); do
      run="$pdir/run-$i"
      mkdir -p "$run"
      NEXT_PORT=$((NEXT_PORT + 1))
      set +e
      (
        cd "$dir"
        CI=true PW_VISUAL_SEED=1 PW_WORKERS=1 \
        PW_PORT="$NEXT_PORT" PW_DB_PATH="$run/database.db" TEST_ARTIFACTS_DIR="$run" \
        npx playwright test e2e/visual.spec.ts --project=chromium --grep "$SELECTOR" \
          --retries=0 --workers=1 --reporter=line
      ) > "$run/playwright.log" 2>&1
      code=$?
      set -e
      printf '%s\n' "$code" > "$run/exit-code.txt"
      classes+=("$(classify_invocation "$run")")
      printf '%s\n' "${classes[-1]}" > "$run/class.txt"
    done

    find "$dir/e2e/__screenshots__" -type f -print0 | sort -z | xargs -0 sha256sum > "$pdir/baselines-after.sha256"
    cmp -s "$pdir/baselines-before.sha256" "$pdir/baselines-after.sha256" || die "baseline tree changed at $commit"
    [ -z "$(git -C "$dir" status --porcelain -- e2e/__screenshots__)" ] || die "git reports a baseline change at $commit"

    find "$pdir" -type f \( -name '*-actual.png' -o -name '*-diff.png' \) -print0 \
      | sort -z | xargs -0 -r sha256sum > "$pdir/actual-and-diff.sha256"
    local actual_set diff_set joined
    actual_set="$(grep -- '-actual.png$' "$pdir/actual-and-diff.sha256" | cut -d' ' -f1 | sort -u || true)"
    diff_set="$(grep -- '-diff.png$' "$pdir/actual-and-diff.sha256" | cut -d' ' -f1 | sort -u || true)"
    joined="$(printf '%s\n' "${classes[@]}" | sort -u | paste -sd, -)"
    pixel_line="$(grep -ohE '[0-9]+ pixels \(ratio [0-9.]+ of all image pixels\) are different|Expected an image [0-9]+px by [0-9]+px, received [0-9]+px by [0-9]+px' "$pdir"/run-*/playwright.log | sort -u | paste -sd'|' - || true)"
    [ -n "$pixel_line" ] || pixel_line="-"

    case "$joined" in
      PASS) PROBE_CLASS=GOOD ;;
      RENDER_FAIL)
        if [ "$(printf '%s\n' "$actual_set" | grep -c .)" -eq 1 ] \
           && [ "$(printf '%s\n' "$diff_set" | grep -c .)" -eq 1 ] \
           && [ "$actual_set" != "$BASELINE_SHA" ]; then
          PROBE_CLASS=BAD PROBE_ACTUAL="$actual_set" PROBE_DIFF="$diff_set"
        else
          PROBE_CLASS=NONDETERMINISTIC
        fi ;;
      PASS,RENDER_FAIL) PROBE_CLASS=NONDETERMINISTIC ;;
      *STARTUP_FAIL*) PROBE_CLASS=STARTUP_FAIL ;;
      *) PROBE_CLASS=OTHER_FAIL ;;
    esac
  fi

  record "$phase" "$commit" "$PROBE_CLASS" "$(IFS=,; echo "${classes[*]:-none}")" "$PROBE_ACTUAL" "$PROBE_DIFF" "$pixel_line"
  printf 'probe %s %s %s -> %s\n' "$ORDER" "$phase" "$commit" "$PROBE_CLASS"
}

write_verdict() {  # verdict lo hi probes_used
  local verdict="$1" lo="$2" hi="$3" used="$4"
  {
    printf 'verdict=%s\n' "$verdict"
    printf 'last_good=%s\n' "${POSITIONS[$lo]}"
    printf 'first_bad=%s\n' "${POSITIONS[$hi]}"
    printf 'last_good_position=%s\nfirst_bad_position=%s\n' "$lo" "$hi"
    printf 'probes_used=%s\ninvocations_used=%s\n' "$used" "$((used * INVOCATIONS))"
    printf 'finished_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  } | tee "$OUT/verdict.env" >> "$GITHUB_OUTPUT"
  {
    printf '## E3 %s: %s\n\n' "$MODE" "$verdict"
    printf 'Interval positions %s..%s: `%s`..`%s`\n\n```\n' "$lo" "$hi" "${POSITIONS[$lo]}" "${POSITIONS[$hi]}"
    cat "$RESULTS"
    printf '```\n'
  } >> "$GITHUB_STEP_SUMMARY"
}

position_of() {
  local i
  for i in "${!POSITIONS[@]}"; do
    [ "${POSITIONS[$i]}" = "$1" ] && { echo "$i"; return 0; }
  done
  return 1
}

case "$MODE" in
  bisect)
    probe endpoint "$CONTROL";   control_class="$PROBE_CLASS"
    probe endpoint "$TREATMENT"; treatment_class="$PROBE_CLASS"
    if [ "$control_class" != GOOD ] || [ "$treatment_class" != BAD ]; then
      write_verdict ENDPOINTS_NOT_DISTINGUISHED 0 "$CANDIDATE_COUNT" "$ORDER"
      exit 0
    fi
    lo=0 hi="$CANDIDATE_COUNT" used=0 verdict=""
    while [ $((hi - lo)) -gt 1 ]; do
      if [ "$used" -ge "$MAX_BISECT_PROBES" ]; then verdict=BUDGET_EXHAUSTED; break; fi
      mid=$(((lo + hi) / 2))
      used=$((used + 1))
      probe bisect "${POSITIONS[$mid]}"
      case "$PROBE_CLASS" in
        GOOD) lo="$mid" ;;
        BAD) hi="$mid" ;;
        *) verdict="INCONCLUSIVE_${PROBE_CLASS}"; break ;;
      esac
    done
    write_verdict "${verdict:-BOUNDARY_FOUND}" "$lo" "$hi" "$ORDER"
    ;;
  confirm)
    last_good="${2:?last good}" first_bad="${3:?first bad}"
    [[ "$last_good" =~ ^[0-9a-f]{40}$ && "$first_bad" =~ ^[0-9a-f]{40}$ ]] || die "boundary SHAs malformed"
    lo="$(position_of "$last_good")" || die "last good is not in the pre-registered interval"
    hi="$(position_of "$first_bad")" || die "first bad is not in the pre-registered interval"
    [ $((hi - lo)) -eq 1 ] || die "boundary commits are not adjacent first-parent positions"
    probe confirm "$last_good"; good_class="$PROBE_CLASS"
    probe confirm "$first_bad"; bad_class="$PROBE_CLASS"
    if [ "$good_class" = GOOD ] && [ "$bad_class" = BAD ]; then
      write_verdict CONFIRMED "$lo" "$hi" "$ORDER"
    else
      write_verdict NOT_CONFIRMED "$lo" "$hi" "$ORDER"
    fi
    ;;
  *) die "unknown mode $MODE" ;;
esac
