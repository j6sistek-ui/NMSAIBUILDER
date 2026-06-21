# Single Current-State Source Rule

Governance and active-build documents state **current** requirements only. They are not change histories.

## Scope

Applies to every `.md` document in the package EXCEPT the historical or version-defining ones, which may carry version labels:

* `CHANGELOG.md`
* `release/RELEASE_NOTES_*.md` (and anything under `release/`)
* `reports/**` — point-in-time records (studies, contradiction reports)
* `archive/**` — retired material
* `MASTER_DOC_VERSIONING_POLICY.md` — defines the versioning scheme

## The rule

* A governance/active-build doc contains the **current statement** of each requirement, written in present tense.
* It MUST NOT carry per-version section headers (`## X.YY.ZZ <topic>`) or otherwise treat its own body as a dated change history.
* When a requirement changes, the doc is edited **in place** to the new current statement. The superseded statement is **removed** from the doc — never preserved as a stale version-labeled section. If a later rule supersedes an earlier one, the earlier header is simply wrong now and is deleted.
* History lives in `CHANGELOG.md`. If a superseded detail is worth keeping, it is moved to `archive/` and the relevant `CHANGELOG.md` entry points to it.
* The only version labels allowed in a governance/active-build doc are the registered current-state anchors: the title version stamp and a single `Current baseline:` line, and only where that file is a registered version location.

## Why

A reader — human or AI — loading the package must treat every requirement as equally current. Version-labeled sections make an older requirement look like co-equal current law, which invites mis-weighting and the accidental reuse of a rule that a later revision already replaced. One current statement per requirement removes that ambiguity.

## Enforcement

`validation/version_callout_check.py` runs inside the release gate. It FAILS the release when a non-exempt doc gains a `## X.YY.ZZ` section header that is not recorded in `validation/version_callout_debt.json`, and when an existing offender's call-out count increases. Existing debt is tracked in that ledger and is burned down to empty as documents are harmonized; after cleaning a doc, run the check with `--refresh` to lower the baseline.
