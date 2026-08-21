#!/usr/bin/env node
/**
 * The `js-supply-chain` verdict: `npm audit --json` read against a committed
 * allowlist of accepted advisories.
 *
 * Policy and rulings: docs/NPM_AUDIT_SEVERITY_POLICY_DECISION.md sections 4 and
 * 6.1, signed 2026-08-15. The five that shape this file:
 *
 *   D-1  Severity floor is `high`, read PER ADVISORY (section 4.4) -- never from
 *        `vulnerabilities[pkg].severity`, which is the package-level maximum and
 *        would let a `high` sibling drag a `moderate` over the floor.
 *   D-2  The whole graph, including devDependencies. No dev-only carve-out.
 *   D-3  MAX_TTL is 90 days on `expiresOn - approvedOn`.
 *   D-4  An audit that could not run, or whose report will not parse, FAILS.
 *   D-5  A stale allowlist entry -- one whose advisory has left the audit --
 *        FAILS, and the entry must be deleted.
 *
 * Every abnormal condition below fails. None is warned-and-skipped, and that
 * direction is the whole design: a broken allowlist makes this gate HARDER to
 * pass, never easier. The failure mode being avoided is the one this repository
 * keeps rediscovering -- `--omit=dev` scoring "found 0 vulnerabilities", and a
 * compiled-SCSS drift gate that parsed cleanly while detecting nothing. A
 * validator that skipped malformed entries would let a typo in an `id` silently
 * widen the gate.
 *
 * Usage:
 *   node scripts/npm_audit_gate.mjs \
 *     --audit artifacts/npm-audit/npm-audit.json \
 *     --allowlist docs/npm_audit_allowlist.json \
 *     [--audit-exit-status N] [--audit-stderr PATH] \
 *     [--summary PATH] [--today YYYY-MM-DD]
 *
 * Exit 0 = gate passes. Exit 1 = gate fails, with every reason printed. Exit 2 =
 * this script was invoked wrongly (unknown flag, missing required flag), which
 * is also a failure but is the operator's bug rather than the graph's.
 */

import fs from 'node:fs';

const SCHEMA_VERSION = 1;
const SEVERITY_FLOOR = 'high';
const MAX_TTL_DAYS = 90;

// Ascending. `>= indexOf(SEVERITY_FLOOR)` is the floor test, so an unknown
// severity string has index -1 and never clears it by accident -- it is caught
// explicitly instead, below, and fails.
const SEVERITY_ORDER = ['info', 'low', 'moderate', 'high', 'critical'];

const GHSA = /^GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}$/;
const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;

const REQUIRED_FIELDS = [
  'id',
  'package',
  'severity',
  'rationale',
  'owner',
  'approvedOn',
  'expiresOn',
];
const MIN_RATIONALE = 40;

const MS_PER_DAY = 24 * 60 * 60 * 1000;

// ------------------------------------------------------------------ arguments

function parseArgs(argv) {
  const known = new Set([
    '--audit',
    '--allowlist',
    '--audit-exit-status',
    '--audit-stderr',
    '--summary',
    '--today',
  ]);
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const flag = argv[i];
    if (!known.has(flag)) {
      throw new UsageError(`unknown argument ${JSON.stringify(flag)}`);
    }
    const value = argv[i + 1];
    if (value === undefined || value.startsWith('--')) {
      throw new UsageError(`${flag} requires a value`);
    }
    args[flag.slice(2)] = value;
    i += 1;
  }
  for (const required of ['audit', 'allowlist']) {
    if (!args[required]) {
      throw new UsageError(`--${required} is required`);
    }
  }
  return args;
}

class UsageError extends Error {}

// ------------------------------------------------------------------- failures

/** Collected reasons. Every check appends; nothing throws past the first one,
 *  so one run reports every problem rather than making the operator peel them
 *  off one CI round at a time. */
const failures = [];
const fail = (message) => failures.push(message);

// ---------------------------------------------------------------- date helpers

function parseDate(value) {
  if (typeof value !== 'string' || !ISO_DATE.test(value)) return null;
  const stamp = Date.parse(`${value}T00:00:00Z`);
  if (Number.isNaN(stamp)) return null;
  // Date.parse accepts 2026-02-31 on some engines by rolling over; round-trip to
  // reject a date that is well-formed but does not exist.
  const roundTrip = new Date(stamp).toISOString().slice(0, 10);
  return roundTrip === value ? stamp : null;
}

function today(args) {
  // `--today` exists so the expiry and MAX_TTL rules are testable without
  // waiting 90 days or rewriting fixtures each morning. CI never passes it.
  if (args.today !== undefined) {
    const stamp = parseDate(args.today);
    if (stamp === null) {
      throw new UsageError(`--today must be an ISO-8601 date, got ${JSON.stringify(args.today)}`);
    }
    return stamp;
  }
  return Date.parse(`${new Date().toISOString().slice(0, 10)}T00:00:00Z`);
}

// ----------------------------------------------------------------- audit read

/** The advisories in the report, keyed by GHSA id.
 *
 *  D-4 lives here: anything that stops this from producing a trustworthy set is
 *  a failure, not an empty set. An empty set and an unreadable report must never
 *  reach the same verdict. */
function readAudit(args) {
  const status = args['audit-exit-status'];
  if (status !== undefined && !/^\d+$/.test(status)) {
    throw new UsageError(`--audit-exit-status must be a non-negative integer, got ${JSON.stringify(status)}`);
  }

  let raw;
  try {
    raw = fs.readFileSync(args.audit, 'utf8');
  } catch (error) {
    fail(`D-4: the npm audit report could not be read at ${args.audit} (${error.message}). ` +
      'This is "the audit could not run", not "no advisories found".');
    return null;
  }

  let report;
  try {
    report = JSON.parse(raw);
  } catch (error) {
    const stderr = readAuditStderr(args);
    fail(`D-4: the npm audit report at ${args.audit} is not valid JSON (${error.message}). ` +
      'An unparseable report is an audit that could not run.' + stderr);
    return null;
  }

  if (report === null || typeof report !== 'object' || Array.isArray(report)) {
    fail(`D-4: the npm audit report at ${args.audit} is not a JSON object.`);
    return null;
  }

  // npm writes `{"error": {...}}` instead of a report when the registry or the
  // advisory endpoint is unreachable. That parses fine and has no
  // `vulnerabilities` key, which is exactly the shape a lenient reader scores as
  // clean.
  if (report.error) {
    const detail = typeof report.error === 'object'
      ? JSON.stringify(report.error)
      : String(report.error);
    fail(`D-4: npm audit reported an error instead of a report: ${detail}` + readAuditStderr(args));
    return null;
  }

  if (report.auditReportVersion !== 2) {
    fail(`D-4: unexpected auditReportVersion ${JSON.stringify(report.auditReportVersion)} ` +
      '(expected 2). A report shape this script has not been read against must not be ' +
      'interpreted by guesswork.');
    return null;
  }

  if (report.vulnerabilities === null || typeof report.vulnerabilities !== 'object' ||
      Array.isArray(report.vulnerabilities)) {
    fail(`D-4: the npm audit report at ${args.audit} has no \`vulnerabilities\` mapping.`);
    return null;
  }

  const metadata = report.metadata;
  const counts = metadata && metadata.vulnerabilities;
  const deps = metadata && metadata.dependencies;
  if (!counts || !deps) {
    fail(`D-4: the npm audit report at ${args.audit} has no \`metadata.vulnerabilities\` / ` +
      '`metadata.dependencies` block.');
    return null;
  }

  // Section 4.5: exit code 1 with a valid report is npm saying "some advisory
  // exists", including allowlisted ones. Using it directly would make the
  // allowlist inert. Anything above 1 is npm failing rather than reporting.
  if (status !== undefined && Number(status) > 1) {
    fail(`D-4: \`npm audit\` exited ${status}, which is npm failing rather than reporting. ` +
      'Exit 1 means "advisories exist" and is handled from the report; anything higher is not.' +
      readAuditStderr(args));
    return null;
  }

  const advisories = new Map();
  for (const [pkg, node] of Object.entries(report.vulnerabilities)) {
    const via = node && node.via;
    if (!Array.isArray(via)) {
      fail(`D-4: \`vulnerabilities[${pkg}]\` has no \`via\` array; the report shape is not the ` +
        'one this gate reads.');
      continue;
    }
    for (const entry of via) {
      // A string entry names another vulnerable package rather than an advisory:
      // `postcss` is "vulnerable because nanoid is". The advisory itself is
      // recorded on the package it was filed against, so skipping strings loses
      // nothing -- it just avoids counting one advisory once per dependent.
      if (typeof entry === 'string') continue;
      if (entry === null || typeof entry !== 'object') {
        fail(`D-4: \`vulnerabilities[${pkg}].via\` holds an entry that is neither a string nor ` +
          'an object.');
        continue;
      }

      const id = advisoryId(entry);
      if (id === null) {
        fail(`D-4: an advisory on \`${pkg}\` carries no GHSA id (url ` +
          `${JSON.stringify(entry.url)}). An advisory this gate cannot key is an advisory it ` +
          'cannot allowlist, so it cannot be waved through either.');
        continue;
      }

      if (!SEVERITY_ORDER.includes(entry.severity)) {
        fail(`D-4: advisory ${id} on \`${pkg}\` has severity ${JSON.stringify(entry.severity)}, ` +
          `which is not one of ${SEVERITY_ORDER.join(', ')}.`);
        continue;
      }

      const existing = advisories.get(id);
      if (existing) {
        existing.packages.add(pkg);
        // The same advisory can be reported against several packages; keep the
        // highest severity seen so a lower duplicate cannot lower the verdict.
        if (rank(entry.severity) > rank(existing.severity)) existing.severity = entry.severity;
      } else {
        advisories.set(id, {
          id,
          severity: entry.severity,
          title: typeof entry.title === 'string' ? entry.title : '',
          range: typeof entry.range === 'string' ? entry.range : '',
          packages: new Set([pkg]),
          fixAvailable: node.fixAvailable,
        });
      }
    }
  }

  return { report, counts, deps, advisories };
}

function readAuditStderr(args) {
  if (!args['audit-stderr']) return '';
  let text;
  try {
    text = fs.readFileSync(args['audit-stderr'], 'utf8').trim();
  } catch {
    return '';
  }
  return text ? `\n  npm audit stderr:\n${text.split('\n').map((l) => `    ${l}`).join('\n')}` : '';
}

function advisoryId(entry) {
  if (typeof entry.url === 'string') {
    const tail = entry.url.split('/').pop();
    if (GHSA.test(tail)) return tail;
  }
  // `source` is npm's numeric advisory id and cannot be allowlisted under the
  // section 4.1 format, so it is deliberately not used as a fallback key.
  return null;
}

const rank = (severity) => SEVERITY_ORDER.indexOf(severity);

// ------------------------------------------------------------- allowlist read

function readAllowlist(args, now) {
  let raw;
  try {
    raw = fs.readFileSync(args.allowlist, 'utf8');
  } catch (error) {
    fail(`The allowlist is missing at ${args.allowlist} (${error.message}). ` +
      'An empty allowlist is written as `"allow": []`, never as a missing file -- ' +
      '"no exceptions" and "the file was deleted" must not look alike.');
    return null;
  }

  let doc;
  try {
    doc = JSON.parse(raw);
  } catch (error) {
    fail(`The allowlist at ${args.allowlist} is not valid JSON: ${error.message}`);
    return null;
  }

  if (doc === null || typeof doc !== 'object' || Array.isArray(doc)) {
    fail(`The allowlist at ${args.allowlist} must be a JSON object.`);
    return null;
  }

  if (doc.schemaVersion !== SCHEMA_VERSION) {
    fail(`The allowlist declares schemaVersion ${JSON.stringify(doc.schemaVersion)}; this gate ` +
      `reads ${SCHEMA_VERSION}. A future entry shape must not be silently reinterpreted by an ` +
      'older reader.');
    return null;
  }

  if (!Array.isArray(doc.allow)) {
    fail('The allowlist has no `allow` array.');
    return null;
  }

  const entries = new Map();
  doc.allow.forEach((entry, index) => {
    const where = `allow[${index}]`;
    if (entry === null || typeof entry !== 'object' || Array.isArray(entry)) {
      fail(`${where} is not an object.`);
      return;
    }

    let sound = true;
    for (const field of REQUIRED_FIELDS) {
      const value = entry[field];
      if (typeof value !== 'string' || value.trim() === '') {
        fail(`${where}.${field} is missing, empty, or not a string.`);
        sound = false;
      }
    }
    for (const field of Object.keys(entry)) {
      if (!REQUIRED_FIELDS.includes(field)) {
        fail(`${where}.${field} is not a field of schemaVersion ${SCHEMA_VERSION}. ` +
          'There is no optional field and no default; an unrecognized key is a typo or a ' +
          'format this reader does not implement.');
        sound = false;
      }
    }
    if (!sound) return;

    if (!GHSA.test(entry.id)) {
      fail(`${where}.id ${JSON.stringify(entry.id)} is not a GHSA id. A CVE id or a bare ` +
        'package name is a malformed entry, not a lenient one.');
      return;
    }

    if (entries.has(entry.id)) {
      fail(`${where}.id ${entry.id} duplicates allow[${entries.get(entry.id).index}]. ` +
        'Two entries for one advisory means two rationales, one of which is unread.');
      return;
    }

    if (!SEVERITY_ORDER.includes(entry.severity)) {
      fail(`${where}.severity ${JSON.stringify(entry.severity)} is not one of ` +
        `${SEVERITY_ORDER.join(', ')}.`);
      return;
    }

    if (entry.rationale.trim().length < MIN_RATIONALE) {
      fail(`${where}.rationale is ${entry.rationale.trim().length} characters; at least ` +
        `${MIN_RATIONALE} are required. "We accept postcss problems" is not a decision anyone ` +
        'can review.');
      return;
    }

    const approvedOn = parseDate(entry.approvedOn);
    const expiresOn = parseDate(entry.expiresOn);
    if (approvedOn === null) {
      fail(`${where}.approvedOn ${JSON.stringify(entry.approvedOn)} is not an ISO-8601 date.`);
      return;
    }
    if (expiresOn === null) {
      fail(`${where}.expiresOn ${JSON.stringify(entry.expiresOn)} is not an ISO-8601 date.`);
      return;
    }
    if (expiresOn <= approvedOn) {
      fail(`${where} (${entry.id}) expires ${entry.expiresOn}, on or before its approval ` +
        `${entry.approvedOn}.`);
      return;
    }

    const ttl = Math.round((expiresOn - approvedOn) / MS_PER_DAY);
    if (ttl > MAX_TTL_DAYS) {
      fail(`${where} (${entry.id}) has a ${ttl}-day TTL; D-3 caps it at ${MAX_TTL_DAYS}. ` +
        'Without a ceiling, "expiry" is satisfied by the year 2099.');
      return;
    }

    if (expiresOn <= now) {
      fail(`${where} (${entry.id}) expired on ${entry.expiresOn}. An expired exception is ` +
        'STRICTER than no exception, which is what makes expiry a real deadline: renew it with ' +
        'a fresh review or delete it and fix the advisory.');
      return;
    }

    // The parsed timestamps go under their own names. Spreading them over
    // `approvedOn` / `expiresOn` would replace the ISO strings the messages and
    // the job summary print, and every date in the output would render as a
    // 13-digit epoch instead.
    entries.set(entry.id, { ...entry, index, approvedAt: approvedOn, expiresAt: expiresOn, ttl });
  });

  return entries;
}

// ----------------------------------------------------------------- the verdict

function judge(audit, allowed, now) {
  const blocking = [];
  const waived = [];
  const belowFloor = [];

  for (const advisory of audit.advisories.values()) {
    const entry = allowed.get(advisory.id);
    const packages = [...advisory.packages].sort().join(', ');

    if (entry) {
      // Section 4.5: a rise above the recorded severity voids the approval; a
      // fall is strictly less exposure than what was approved, so it passes.
      if (rank(advisory.severity) > rank(entry.severity)) {
        blocking.push(`${advisory.id} (${packages}) is now ${advisory.severity}, above the ` +
          `${entry.severity} recorded in its allowlist entry by ${entry.owner} on ` +
          `${entry.approvedOn}. The approval was given for the severity written in the entry.`);
      } else {
        const daysLeft = Math.round((entry.expiresAt - now) / MS_PER_DAY);
        waived.push({ ...entry, observed: advisory.severity, packages, daysLeft });
      }
      continue;
    }

    if (rank(advisory.severity) < rank(SEVERITY_FLOOR)) {
      belowFloor.push({ ...advisory, packages });
      continue;
    }

    const fix = advisory.fixAvailable === true
      ? 'a fix is in range (`npm audit fix`)'
      : advisory.fixAvailable && typeof advisory.fixAvailable === 'object'
        ? `the only fix is a breaking change to ${advisory.fixAvailable.name}@${advisory.fixAvailable.version}`
        : 'no fix is available';
    blocking.push(`${advisory.id} ${advisory.severity} on ${packages}` +
      (advisory.range ? ` ${advisory.range}` : '') +
      (advisory.title ? ` -- ${advisory.title}` : '') +
      `. ${fix}. https://github.com/advisories/${advisory.id}`);
  }

  // D-5. Checked against the whole audit rather than the blocking set: an entry
  // whose advisory is present but below the floor is still watching something
  // real, while an entry whose advisory has left the graph is a live exception
  // nobody is watching.
  for (const entry of allowed.values()) {
    if (!audit.advisories.has(entry.id)) {
      blocking.push(`D-5: allow[${entry.index}] (${entry.id}, ${entry.package}) is STALE -- the ` +
        'advisory is no longer in the audit. Delete the entry. A stale entry is a live exception ' +
        'nobody is watching, and if the advisory returns it is pre-approved by a decision nobody ' +
        're-made.');
    }
  }

  return { blocking, waived, belowFloor };
}

// ------------------------------------------------------------------ reporting

function summarize(args, audit, verdict) {
  const path = args.summary || process.env.GITHUB_STEP_SUMMARY;
  if (!path) return;

  const counts = audit ? audit.counts : null;
  const deps = audit ? audit.deps : null;
  const lines = ['### npm audit — full graph, enforcing', ''];

  if (counts) {
    lines.push('| Severity | Count |', '|---|---:|');
    for (const severity of ['critical', 'high', 'moderate', 'low', 'info']) {
      lines.push(`| ${severity} | ${counts[severity]} |`);
    }
    lines.push(`| **total** | **${counts.total}** |`, '');
    lines.push(`Scanned **${deps.total}** dependencies (prod ${deps.prod}, dev ${deps.dev}, ` +
      `optional ${deps.optional}).`, '');
    lines.push('`--omit=dev` is deliberately NOT used: it would scan ' +
      `${deps.prod} of ${deps.total} packages and report a false clean bill of health.`, '');
  }

  lines.push(`Failing floor: **${SEVERITY_FLOOR}** and above, read per advisory (D-1). ` +
    'Exceptions: `docs/npm_audit_allowlist.json`.', '');

  if (verdict) {
    if (verdict.waived.length) {
      lines.push('#### Allowlisted, unexpired', '',
        '| Advisory | Packages | Observed | Approved as | Owner | Expires | Days left |',
        '|---|---|---|---|---|---|---:|');
      for (const entry of verdict.waived) {
        lines.push(`| \`${entry.id}\` | ${entry.packages} | ${entry.observed} | ${entry.severity} ` +
          `| ${entry.owner} | ${entry.expiresOn} | ${entry.daysLeft} |`);
      }
      lines.push('');
    }
    if (verdict.belowFloor.length) {
      lines.push('#### Below the failing floor — reported, not blocking', '');
      for (const advisory of verdict.belowFloor) {
        lines.push(`- \`${advisory.id}\` ${advisory.severity} on ${advisory.packages}`);
      }
      lines.push('');
    }
  }

  if (failures.length) {
    lines.push('#### Gate FAILED', '');
    for (const message of failures) lines.push(`- ${message}`);
    lines.push('');
  } else {
    lines.push('Gate **passed**.', '');
  }

  fs.appendFileSync(path, `${lines.join('\n')}\n`);
}

// ----------------------------------------------------------------------- main

function main(argv) {
  let args;
  let now;
  try {
    args = parseArgs(argv);
    now = today(args);
  } catch (error) {
    if (error instanceof UsageError) {
      console.error(`npm_audit_gate: ${error.message}`);
      return 2;
    }
    throw error;
  }

  const audit = readAudit(args);
  const allowed = readAllowlist(args, now);

  // Only judge when both inputs were trustworthy. Judging a partial audit
  // against a partial allowlist would manufacture stale-entry reports out of an
  // unreadable file -- noise on top of a failure that is already recorded.
  const verdict = audit && allowed ? judge(audit, allowed, now) : null;
  if (verdict) failures.push(...verdict.blocking);

  if (verdict) {
    for (const entry of verdict.waived) {
      console.log(`::notice title=npm audit::${entry.id} allowlisted by ${entry.owner} until ` +
        `${entry.expiresOn} (${entry.daysLeft} days left) -- ${entry.rationale}`);
    }
    for (const advisory of verdict.belowFloor) {
      console.log(`::notice title=npm audit::${advisory.id} ${advisory.severity} on ` +
        `${advisory.packages} is below the ${SEVERITY_FLOOR} floor; reported, not blocking.`);
    }
  }

  if (audit) {
    const v = audit.counts;
    const line = ['critical', 'high', 'moderate', 'low', 'info']
      .map((s) => `${s}=${v[s]}`).join(' ');
    console.log(`::notice title=npm audit::${line} total=${v.total} over ${audit.deps.total} ` +
      `dependencies (prod ${audit.deps.prod}, dev ${audit.deps.dev})`);
  }

  summarize(args, audit, verdict);

  if (failures.length) {
    // Twice on purpose. `::error` is what puts a reason on the Actions job page,
    // but Actions renders at most ten annotations per step -- and a malformed
    // allowlist can easily produce more than ten. The stderr copy is the
    // complete record.
    for (const message of failures) {
      console.log(`::error title=npm audit::${message}`);
      console.error(`npm_audit_gate: ${message}`);
    }
    console.error(`npm_audit_gate: FAILED with ${failures.length} problem(s).`);
    return 1;
  }

  console.log('npm_audit_gate: PASSED.');
  return 0;
}

process.exit(main(process.argv.slice(2)));
