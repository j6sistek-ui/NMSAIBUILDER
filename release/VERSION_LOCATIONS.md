# Version Locations (GENERATED from release/VERSION_LOCATIONS.json — do not hand-edit)

Required version this release: **5.04.03**. The release gate fails if any location below does not read this version. Add a row to the JSON when a new active label appears.

| File | Location | Read via |
|---|---|---|
| `00_START_HERE_CURRENT.md` | title | regex |
| `00_START_HERE_CURRENT.md` | baseline line | regex |
| `README.md` | title | regex |
| `FILE_INVENTORY.md` | title | regex |
| `validation/run_gate.py` | docstring banner | regex |
| `validation/run_gate.py` | gate output banner | regex |
| `transfer_prompts/NMS_BUILDER_BOOTSTRAP_CURRENT.txt` | bootstrap title | regex |
| `release/VERSION.json` | version source of truth | json key `current_version` |
| `release/VERSION.json` | version mirror | json key `version` |
| `PACKAGE_MANIFEST.json` | manifest version | json key `version` |
| `00_KICKOFF_INTAKE_GATE.md` | kickoff title | regex |
| `OPEN_TOPICS_LOG.md` | open topics active version | regex |
| `PROJECT_STATE_CURRENT.md` | project state active version | regex |
| `OPEN_ISSUES_CURRENT.md` | open issues active version | regex |
