#!/usr/bin/env python3
"""
version_callout_check.py — enforce the Single Current-State Source rule.

Governance and active-build docs must state CURRENT requirements only. They must not
carry per-version section headers ("## X.YY.ZZ <topic>") that turn a live rule doc into a
dated change history. History belongs in CHANGELOG.md (and, if critical, archive/).

This check scans every .md doc except the legitimately historical / version-defining ones:
  - CHANGELOG.md
  - release/RELEASE_NOTES_*.md  (and anything under release/)
  - reports/**          (point-in-time records)
  - archive/**          (retired material)
  - MASTER_DOC_VERSIONING_POLICY.md  (defines the scheme; version examples expected)
  - validation/gate_fixtures/**      (fixtures may carry a sample rev)

A "version-section call-out" is a heading line whose text starts with an X.YY.ZZ token,
e.g. `## 2.04.05 Connected-piece curvature routing`. Title version stamps
(`# 00 — START HERE  (5.04.05 ...)`) and `Current baseline:` lines are NOT call-outs and
are not matched.

Existing debt is tracked in validation/version_callout_debt.json as {path: count}. The
gate FAILS when:
  - a non-exempt, non-debt doc has >=1 call-out (a NEW offender), or
  - a debt doc's call-out count INCREASES above its recorded baseline (it got worse).
It PASSES on known debt at or below baseline. Burn the ledger down to {} as docs are
harmonized; run with --refresh to rewrite the ledger to the current counts after cleaning.

Exit 0 = PASS, exit 1 = FAIL.
"""
import os, re, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEBT = os.path.join(HERE, "version_callout_debt.json")

HEADER = re.compile(r'^#{1,6}\s*\d+\.\d{2}\.\d{2}\b', re.M)


def exempt(rel):
    rel = rel.replace(os.sep, "/")
    base = rel.split("/")[-1]
    if rel.startswith("release/"):
        return True
    if rel.startswith("reports/") or rel.startswith("archive/"):
        return True
    if "/gate_fixtures/" in ("/" + rel):
        return True
    if base in ("CHANGELOG.md", "MASTER_DOC_VERSIONING_POLICY.md"):
        return True
    return False


def scan(root):
    """Return {rel_path: callout_count} for every non-exempt .md with >=1 call-out."""
    out = {}
    for dp, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/")
            if exempt(rel):
                continue
            n = len(HEADER.findall(open(os.path.join(dp, f), encoding="utf-8").read()))
            if n:
                out[rel] = n
    return out


def load_debt():
    try:
        return json.load(open(DEBT, encoding="utf-8")).get("files", {})
    except Exception:
        return {}


def main():
    refresh = "--refresh" in sys.argv
    current = scan(ROOT)
    if refresh:
        json.dump({"files": dict(sorted(current.items()))},
                  open(DEBT, "w", encoding="utf-8"), indent=2)
        print(f"version_callout_debt.json refreshed: {len(current)} file(s), "
              f"{sum(current.values())} call-out(s).")
        return 0

    debt = load_debt()
    new_offenders, worsened = [], []
    for rel, n in sorted(current.items()):
        if rel not in debt:
            new_offenders.append((rel, n))
        elif n > debt[rel]:
            worsened.append((rel, n, debt[rel]))

    remaining = sum(current.get(r, 0) for r in debt if r in current)
    cleaned = [r for r in debt if r not in current]

    print("SINGLE CURRENT-STATE SOURCE CHECK")
    print(f"  tracked debt: {len(debt)} file(s); still dirty: "
          f"{len([r for r in debt if r in current])}; cleaned since baseline: {len(cleaned)}")
    if cleaned:
        print("  cleaned (drop from ledger via --refresh): " + ", ".join(sorted(cleaned)[:10])
              + (" ..." if len(cleaned) > 10 else ""))

    if not new_offenders and not worsened:
        print("VERSION-CALLOUT GATE: PASS")
        return 0
    for rel, n in new_offenders:
        print(f"  FAIL new version-callout doc (not in ledger): {rel} ({n} call-out(s))")
    for rel, n, base in worsened:
        print(f"  FAIL version-callouts increased: {rel} {base} -> {n}")
    print("VERSION-CALLOUT GATE: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
