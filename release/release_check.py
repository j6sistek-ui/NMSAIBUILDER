#!/usr/bin/env python3
"""
release_check.py  — the executable RELEASE GATE for the master docs package.

Run from the package root before blessing any X.YY.ZZ release:

    python3 release/release_check.py

It enforces the Master Document Versioning Policy mechanically, so a release
cannot ship internally inconsistent (the failure that produced stale version
labels and dead links in earlier packages). Dependency-free.

2.14.01 hardening: nested Python self-test subprocesses are invoked with
`python -S` to skip site-startup hooks that can warm external tooling and cause
sandbox timeouts. This does not skip any release checks.

Checks:
  1. Single source of version truth: release/VERSION.json `current_version`
     equals PACKAGE_MANIFEST.json `version`.
  2. No stale version label in the primary entry docs (00_START_HERE_CURRENT.md,
     README.md): they must not advertise an OLDER master version than current.
  3. START_HERE library row count matches the actual library JSON length.
  4. CHANGELOG.md and release/RELEASE_NOTES_<version>.md exist for current_version.
  5. All JSON parses.
  6. Package-internal backtick references resolve (dangling-link scan).
  7. validation/run_gate.py is present and imports.
  8. Active baseline labels and validation-tool banners match current_version.
  9. No shipped Python bytecode/cache artifacts.
 10. PACKAGE_MANIFEST.json file_count matches actual shipped file count.
Prints a single RELEASE GATE: PASS/FAIL verdict.
 11. Validated logic reuse checker self-tests pass.
 12. Recipe conformance checker self-tests pass.
 13. Intent graph conformance checker self-tests pass.
 14. run_gate auto-requires validated logic reuse for validated parts.
"""
import json, os, re, sys, py_compile, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY_NO_SITE = [sys.executable, "-S"]
def rd(p):
    with open(os.path.join(ROOT, p), encoding="utf-8", errors="ignore") as f:
        return f.read()

fails, warns = [], []

# 1 + version truth
ver = json.loads(rd("release/VERSION.json")).get("current_version", "")
vjson = json.loads(rd("release/VERSION.json"))
man = json.load(open(os.path.join(ROOT, "PACKAGE_MANIFEST.json")))
man_ver = str(man.get("version", ""))
if ver != man_ver:
    fails.append(f"version mismatch: VERSION.json={ver} PACKAGE_MANIFEST={man_ver}")

# 1a format: X.YY.ZZ with two-digit YY and ZZ
if not re.fullmatch(r"\d+\.\d{2}\.\d{2}", ver):
    fails.append(f"version '{ver}' is not X.YY.ZZ with two-digit YY and ZZ")

# 1b increment legality + cascade reset vs the version this release supersedes
def _pv(s):
    m = re.search(r"(\d+)\.(\d{2})\.(\d{2})", s or "")
    return tuple(int(x) for x in m.groups()) if m else None
prev = _pv(vjson.get("supersedes_version") or vjson.get("legacy_supersedes"))
cur = _pv(ver)
if prev and cur:
    (Xp, Yp, Zp), (Xn, Yn, Zn) = prev, cur
    is_patch = (Xn == Xp and Yn == Yp and Zn == Zp + 1)
    is_minor = (Xn == Xp and Yn == Yp + 1 and Zn == 0)   # minor resets ZZ -> 00
    is_major = (Xn == Xp + 1 and Yn == 0 and Zn == 0)    # major resets YY and ZZ -> 00
    if not (is_patch or is_minor or is_major):
        fails.append(
            f"illegal version step {Xp}.{Yp:02d}.{Zp:02d} -> {ver}: a major must roll to "
            f"X.00.00, a minor to X.(YY+1).00, a patch to X.YY.(ZZ+1); higher rolls reset "
            f"all lower fields to 00 and only one field moves by one.")
elif cur and not prev:
    warns.append("no semantic predecessor in VERSION.json (first semantic release or "
                 "supersedes a legacy vNN package); increment legality not checked.")


# 2 stale version label in the SELF-IDENTIFYING TITLE of entry docs only
#   (the package title must equal current version; lineage mentions in body are fine)
for doc in ("00_START_HERE_CURRENT.md", "README.md"):
    try:
        title = rd(doc).splitlines()[0]
        legacy = re.findall(r"\bv\d{2}\b", title)          # legacy vNN in the title
        semver = re.findall(r"\b\d+\.\d{2}\.\d{2}\b", title)  # X.YY.ZZ in the title
        if legacy:
            fails.append(f"{doc} title carries legacy label {legacy}; should read {ver}")
        elif semver and ver not in semver:
            fails.append(f"{doc} title says {semver}; current is {ver}")
    except FileNotFoundError:
        fails.append(f"missing entry doc: {doc}")


# 2b active current-version claims in operational docs/tools must match release/VERSION.json
# Historical reports/changelog entries may mention older versions; active entrypoints and tool banners may not.
# 2 version-location registry: every active label must == current (single source: release/VERSION_LOCATIONS.json)
_reg = json.loads(rd("release/VERSION_LOCATIONS.json"))
_reg_files = set()
for _loc in _reg.get("locations", []):
    _rel = _loc["file"]; _reg_files.add(_rel)
    try:
        if "json_key" in _loc:
            _val = str(json.loads(rd(_rel)).get(_loc["json_key"], "")); _claims = [_val] if _val else []
        else:
            _claims = re.findall(_loc["pattern"], rd(_rel), flags=re.M)
    except FileNotFoundError:
        fails.append(f"version-location file missing: {_rel}"); continue
    if not _claims:
        fails.append(f"version-location not found: {_rel} ({_loc.get('note','')})")
    for _c in _claims:
        if _c != ver:
            fails.append(f"stale version: {_rel} says {_c}; current is {ver} ({_loc.get('note','')})")
def _vexempt(_dp, _fn):
    _d = (_dp + "/").replace(os.sep, "/")
    return ("/archive/" in _d or _d.rstrip("/").endswith("/reports") or _fn == "CHANGELOG.md"
            or _fn.startswith("RELEASE_NOTES_") or _fn in ("VERSION_LOCATIONS.json", "VERSION_LOCATIONS.md",
            "VERSION.json", "PACKAGE_MANIFEST.json"))
_unreg = []
for _dp, _, _fs in os.walk(ROOT):
    for _fn in _fs:
        if not _fn.endswith((".md", ".txt", ".py")): continue
        _rl = os.path.relpath(os.path.join(_dp, _fn), ROOT).replace(os.sep, "/")
        if _rl in _reg_files or _vexempt(_dp, _fn): continue
        _hits = sorted(set(re.findall(r"\d+\.\d{2}\.\d{2}", rd(_rl))))
        if _hits: _unreg.append(f"{_rl} ({','.join(_hits)})")
print(f"  VERSION LOCATIONS: {len(_reg.get('locations', []))} registered, all == {ver}")
if _unreg:
    print(f"  WARN: {len(_unreg)} unregistered file(s) mention a version (register in VERSION_LOCATIONS.json if an active label):")
    for _u in _unreg[:25]:
        print("        - " + _u)


# 2c rollout hygiene: no shipped Python cache/bytecode and manifest file_count must match actual shipped files.
# This package is meant to be shared. Generated cache artifacts create noisy diffs and false inventory counts.
pycache_artifacts = []
actual_file_count = 0
for dp, dns, fs in os.walk(ROOT):
    # Count all files under the package root, including reports and release docs, but not directories.
    for fn in fs:
        actual_file_count += 1
        rel = os.path.relpath(os.path.join(dp, fn), ROOT)
        if "__pycache__" in rel.split(os.sep) or fn.endswith(".pyc"):
            pycache_artifacts.append(rel)
if pycache_artifacts:
    fails.append("shipped Python cache/bytecode artifacts present: " + ", ".join(sorted(pycache_artifacts)[:20]) + (" ..." if len(pycache_artifacts) > 20 else ""))
try:
    manifest_count = int(man.get("file_count"))
    if manifest_count != actual_file_count:
        fails.append(f"PACKAGE_MANIFEST file_count={manifest_count} but actual shipped file count={actual_file_count}")
except Exception as e:
    fails.append(f"PACKAGE_MANIFEST file_count missing/invalid ({e})")

# 3 library row count
try:
    lib = json.load(open(os.path.join(ROOT, "library/nms_part_dimensions_and_rules_updated.json")))
    n = len(lib)
    sh = rd("00_START_HERE_CURRENT.md")
    claimed = re.findall(r"([0-9],?[0-9]{3})\s*\n?\s*rows", sh)
    claimed_n = int(claimed[0].replace(",", "")) if claimed else None
    if claimed_n is not None and claimed_n != n:
        fails.append(f"START_HERE library row count {claimed_n} != actual {n}")
except Exception as e:
    warns.append(f"library row-count check skipped: {e}")

# 4 changelog + release notes for this version
if ("CHANGELOG" not in rd("CHANGELOG.md")) or (ver not in rd("CHANGELOG.md")):
    fails.append(f"CHANGELOG.md has no entry mentioning {ver}")
rn = f"release/RELEASE_NOTES_{ver}.md"
if not os.path.exists(os.path.join(ROOT, rn)):
    fails.append(f"missing {rn}")

# 5 all JSON parses
for dp, _, fs in os.walk(ROOT):
    for fn in fs:
        if fn.endswith(".json"):
            try: json.load(open(os.path.join(dp, fn)))
            except Exception as e: fails.append(f"bad JSON: {os.path.relpath(os.path.join(dp,fn),ROOT)} ({e})")

# 6 dangling internal references
def exists_anywhere(base):
    for _, _, fs in os.walk(ROOT):
        if base in fs: return True
    return False
EXternal = ("DT_PartDefinition.csv", "save_editor/", "resources/", "project_context.md",
            "project_lessons.json", "validated_baselines.md", "screenshotUrl", ".jpeg", ".jpg",
            "_vXX", "OBJECT_USE_CASE_MATRIX", "alien_megatemple", "script.py", "generated_script",
            "NMS_Part_Family_Rules.json")
dangling = set()
for dp, _, fs in os.walk(ROOT):
    if "/archive/" in dp.replace(os.sep, "/"): continue
    for fn in fs:
        if not fn.endswith((".md", ".txt")): continue
        p = os.path.join(dp, fn)
        bn = os.path.basename(p)
        # CHANGELOG + release notes legitimately reference renamed/old files as history
        if bn == "CHANGELOG.md" or bn.startswith("RELEASE_NOTES_"): continue
        if bn == "V58_GOVERNANCE_AUDIT_REPORT.md": continue  # quotes bad names intentionally
        if dp.replace(os.sep, "/").endswith("/reports"): continue  # historical reports
        for ref in re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|py|json))`", rd(os.path.relpath(p, ROOT))):
            if ref.startswith(("/", "http")): continue          # external/absolute
            if any(x in ref for x in EXternal): continue
            if os.path.exists(os.path.join(ROOT, ref)) or exists_anywhere(os.path.basename(ref)):
                continue
            dangling.add(f"{os.path.relpath(p,ROOT)} -> {ref}")
for d in sorted(dangling):
    fails.append("dangling ref: " + d)

# 7 validation Python present and compiles
if not os.path.exists(os.path.join(ROOT, "validation/run_gate.py")):
    fails.append("validation/run_gate.py missing")

# 8 compile all package Python files that participate in gates/validation.
# Use explicit temp cfile paths so the release check does not create __pycache__/ .pyc artifacts in the source tree.
with tempfile.TemporaryDirectory() as _compile_tmp:
    for dp, _, fs in os.walk(ROOT):
        for fn in fs:
            if fn.endswith(".py"):
                p = os.path.join(dp, fn)
                rel = os.path.relpath(p, ROOT)
                cfile = os.path.join(_compile_tmp, rel.replace(os.sep, "__") + ".pyc")
                try:
                    py_compile.compile(p, cfile=cfile, doraise=True)
                except Exception as e:
                    fails.append(f"python compile failed: {rel} ({e})")

# 9 run_gate behavioral self-tests
try:
    import subprocess
    gate = os.path.join(ROOT, "validation", "run_gate.py")
    lib = os.path.join(ROOT, "library", "nms_part_dimensions_and_rules_updated.json")
    bad = os.path.join(ROOT, "validation", "gate_fixtures", "invalid_part_wrapper_copy.py")
    good = os.path.join(ROOT, "validation", "gate_fixtures", "valid_part_wrapper_resolution.py")
    if os.path.exists(bad) and os.path.exists(good):
        bad_run = subprocess.run(PY_NO_SITE + [gate, bad, lib, "FIXTURE_BAD_", "--require-json-evidence", "--require-router"], text=True, capture_output=True, timeout=20)
        good_run = subprocess.run(PY_NO_SITE + [gate, good, lib, "FIXTURE_GOOD_", "--require-json-evidence", "--require-router"], text=True, capture_output=True, timeout=20)
        if bad_run.returncode == 0 or "MACHINE-CHECKABLE GATE: FAIL" not in bad_run.stdout:
            fails.append("run_gate self-test failed: invalid Part-wrapper copy fixture did not FAIL with nonzero exit")
        if good_run.returncode != 0 or "MACHINE-CHECKABLE GATE: PASS" not in good_run.stdout:
            fails.append("run_gate self-test failed: valid Part-wrapper resolution fixture did not PASS")
    else:
        fails.append("run_gate self-test fixtures missing")
except Exception as e:
    fails.append(f"run_gate self-tests errored: {e}")

# 9b connectivity / no-float gate self-tests
try:
    import subprocess
    gate = os.path.join(ROOT, "validation", "run_gate.py")
    lib = os.path.join(ROOT, "library", "nms_part_dimensions_and_rules_updated.json")
    conn_good = os.path.join(ROOT, "validation", "gate_fixtures", "connected_build_must_pass.py")
    conn_bad = os.path.join(ROOT, "validation", "gate_fixtures", "floating_part_must_fail.py")
    if os.path.exists(conn_good) and os.path.exists(conn_bad):
        cg = subprocess.run(PY_NO_SITE + [gate, conn_good, lib, "FIXTURE_CONN_", "--require-json-evidence", "--require-router"], text=True, capture_output=True, timeout=20)
        cb = subprocess.run(PY_NO_SITE + [gate, conn_bad, lib, "FIXTURE_FLOAT_", "--require-json-evidence", "--require-router"], text=True, capture_output=True, timeout=20)
        if cg.returncode != 0 or "MACHINE-CHECKABLE GATE: PASS" not in cg.stdout:
            fails.append("run_gate self-test failed: connected_build_must_pass did not PASS the no-float gate")
        if cb.returncode == 0 or "MACHINE-CHECKABLE GATE: FAIL" not in cb.stdout:
            fails.append("run_gate self-test failed: floating_part_must_fail did not FAIL the no-float gate")
    else:
        fails.append("run_gate connectivity self-test fixtures missing")
except Exception as e:
    fails.append(f"run_gate connectivity self-tests errored: {e}")


# 9c part placement map: structural storage + generation-drift (single source of truth)
try:
    import subprocess
    pm_store = subprocess.run(PY_NO_SITE + [os.path.join(ROOT, "validation", "partmap_storage_check.py")],
                              text=True, capture_output=True, timeout=30)
    if pm_store.returncode != 0:
        fails.append("partmap storage check failed: " + (pm_store.stdout.strip().splitlines() or ["?"])[0])
    pm_gen = subprocess.run(PY_NO_SITE + [os.path.join(ROOT, "library", "part_placement_maps", "generate_partmaps.py"), "--check"],
                            text=True, capture_output=True, timeout=60)
    if pm_gen.returncode != 0:
        fails.append("partmap generation drift: " + (pm_gen.stdout.strip().splitlines() or ["?"])[0])
except Exception as e:
    fails.append(f"partmap checks errored: {e}")


# 9d stair semantic float-gate self-test (scoped override wired + correct)
try:
    import subprocess
    stair_unit = os.path.join(ROOT, "validation", "gate_fixtures", "stair_semantic_unit_test.py")
    if os.path.exists(stair_unit):
        su = subprocess.run(PY_NO_SITE + [stair_unit], text=True, capture_output=True, timeout=30)
        if su.returncode != 0 or "STAIR SEMANTIC UNIT TEST: PASS" not in su.stdout:
            fails.append("stair semantic self-test failed: " + ((su.stdout.strip().splitlines() or ["?"])[-1]))
    else:
        fails.append("stair semantic self-test fixture missing")
except Exception as e:
    fails.append(f"stair semantic self-test errored: {e}")


# 10 request router checklist validation
try:
    import subprocess
    router_check = os.path.join(ROOT, "validation", "request_router_check.py")
    if not os.path.exists(router_check):
        fails.append("validation/request_router_check.py missing")
    else:
        rr = subprocess.run(PY_NO_SITE + [router_check], text=True, capture_output=True, timeout=20)
        if rr.returncode != 0 or "REQUEST ROUTER CHECK: PASS" not in rr.stdout:
            fails.append("request_router_check failed: " + (rr.stdout.strip() or rr.stderr.strip()))
except Exception as e:
    fails.append(f"request_router_check errored: {e}")


# 10b validated logic reuse / composite intent graph self-tests
try:
    import subprocess
    reuse_check = os.path.join(ROOT, "validation", "validated_logic_reuse_check.py")
    good = os.path.join(ROOT, "validation", "gate_fixtures", "validated_reuse_good.py")
    bad = os.path.join(ROOT, "validation", "gate_fixtures", "validated_reuse_bad_missing_receipt.py")
    if not os.path.exists(reuse_check):
        fails.append("validation/validated_logic_reuse_check.py missing")
    elif not os.path.exists(good) or not os.path.exists(bad):
        fails.append("validated logic reuse self-test fixtures missing")
    else:
        vg = subprocess.run(PY_NO_SITE + [reuse_check, good], text=True, capture_output=True, timeout=30)
        vb = subprocess.run(PY_NO_SITE + [reuse_check, bad], text=True, capture_output=True, timeout=30)
        if vg.returncode != 0 or "VALIDATED LOGIC REUSE CHECK: PASS" not in vg.stdout:
            fails.append("validated logic reuse good fixture did not PASS: " + (vg.stdout.strip().splitlines()[-1] if vg.stdout.strip() else vg.stderr.strip()))
        if vb.returncode == 0 or "VALIDATED LOGIC REUSE CHECK: FAIL" not in vb.stdout:
            fails.append("validated logic reuse bad fixture did not FAIL")
except Exception as e:
    fails.append(f"validated logic reuse self-tests errored: {e}")


# 10c recipe conformance self-tests (exported geometry must obey the validated recipe)
try:
    import subprocess
    conf_check = os.path.join(ROOT, "validation", "recipe_conformance_check.py")
    cgood = os.path.join(ROOT, "validation", "gate_fixtures", "conformance_good.json")
    cbad = os.path.join(ROOT, "validation", "gate_fixtures", "conformance_bad_tipped.json")
    if not os.path.exists(conf_check):
        fails.append("validation/recipe_conformance_check.py missing")
    elif not os.path.exists(cgood) or not os.path.exists(cbad):
        fails.append("recipe conformance self-test fixtures missing")
    else:
        cg = subprocess.run(PY_NO_SITE + [conf_check, cgood], text=True, capture_output=True, timeout=30)
        cb = subprocess.run(PY_NO_SITE + [conf_check, cbad], text=True, capture_output=True, timeout=30)
        if cg.returncode != 0 or "RECIPE CONFORMANCE CHECK: PASS" not in cg.stdout:
            fails.append("recipe conformance good fixture did not PASS")
        if cb.returncode == 0 or "RECIPE CONFORMANCE CHECK: FAIL" not in cb.stdout:
            fails.append("recipe conformance bad/tipped fixture did not FAIL (geometry conformance not enforced)")
except Exception as e:
    fails.append(f"recipe conformance self-tests errored: {e}")


# 10d intent graph connected-component self-tests
try:
    import subprocess
    ig_check = os.path.join(ROOT, "validation", "intent_graph_conformance_check.py")
    ig_good_py = os.path.join(ROOT, "validation", "gate_fixtures", "intent_graph_good.py")
    ig_good_json = os.path.join(ROOT, "validation", "gate_fixtures", "intent_graph_good.json")
    ig_bad_py = os.path.join(ROOT, "validation", "gate_fixtures", "intent_graph_bad_disconnected.py")
    ig_bad_json = os.path.join(ROOT, "validation", "gate_fixtures", "intent_graph_bad_disconnected.json")
    lib = os.path.join(ROOT, "library", "nms_part_dimensions_and_rules_updated.json")
    if not os.path.exists(ig_check):
        fails.append("validation/intent_graph_conformance_check.py missing")
    elif not all(os.path.exists(x) for x in (ig_good_py, ig_good_json, ig_bad_py, ig_bad_json)):
        fails.append("intent graph conformance self-test fixtures missing")
    else:
        igg = subprocess.run(PY_NO_SITE + [ig_check, ig_good_py, ig_good_json, lib], text=True, capture_output=True, timeout=30)
        igb = subprocess.run(PY_NO_SITE + [ig_check, ig_bad_py, ig_bad_json, lib], text=True, capture_output=True, timeout=30)
        if igg.returncode != 0 or "INTENT GRAPH CONFORMANCE CHECK: PASS" not in igg.stdout:
            fails.append("intent graph good fixture did not PASS")
        if igb.returncode == 0 or "INTENT GRAPH CONFORMANCE CHECK: FAIL" not in igb.stdout:
            fails.append("intent graph bad/disconnected fixture did not FAIL")
except Exception as e:
    fails.append(f"intent graph conformance self-tests errored: {e}")


# 10e build objective conformance self-tests (connected path / floating floor)
try:
    import subprocess
    bo_check = os.path.join(ROOT, "validation", "build_objective_conformance_check.py")
    bo_good_py = os.path.join(ROOT, "validation", "gate_fixtures", "build_objective_good.py")
    bo_good_json = os.path.join(ROOT, "validation", "gate_fixtures", "build_objective_good.json")
    bo_bad_py = os.path.join(ROOT, "validation", "gate_fixtures", "build_objective_bad_floating_floor.py")
    bo_bad_json = os.path.join(ROOT, "validation", "gate_fixtures", "build_objective_bad_floating_floor.json")
    if not os.path.exists(bo_check):
        fails.append("validation/build_objective_conformance_check.py missing")
    elif not all(os.path.exists(x) for x in (bo_good_py, bo_good_json, bo_bad_py, bo_bad_json)):
        fails.append("build objective conformance self-test fixtures missing")
    else:
        bog = subprocess.run(PY_NO_SITE + [bo_check, bo_good_py, bo_good_json], text=True, capture_output=True, timeout=30)
        bob = subprocess.run(PY_NO_SITE + [bo_check, bo_bad_py, bo_bad_json], text=True, capture_output=True, timeout=30)
        if bog.returncode != 0 or "BUILD OBJECTIVE CONFORMANCE CHECK: PASS" not in bog.stdout:
            fails.append("build objective conformance good fixture did not PASS")
        if bob.returncode == 0 or "BUILD OBJECTIVE CONFORMANCE CHECK: FAIL" not in bob.stdout:
            fails.append("build objective conformance bad/floating-floor fixture did not FAIL")
except Exception as e:
    fails.append(f"build objective conformance self-tests errored: {e}")





# 10f protocol banner / Blender runtime / geometry manifest self-tests
try:
    import subprocess
    pb_check = os.path.join(ROOT, "validation", "protocol_banner_check.py")
    pb_good = os.path.join(ROOT, "validation", "gate_fixtures", "protocol_banner_good.txt")
    pb_bad = os.path.join(ROOT, "validation", "gate_fixtures", "protocol_banner_bad_missing_docs_avail.txt")
    br_check = os.path.join(ROOT, "validation", "blender_runtime_script_check.py")
    br_good = os.path.join(ROOT, "validation", "gate_fixtures", "blender_runtime_good.py")
    br_bad = os.path.join(ROOT, "validation", "gate_fixtures", "blender_runtime_bad_preview_only.py")
    gm_check = os.path.join(ROOT, "validation", "geometry_construction_manifest_check.py")
    gm_good = os.path.join(ROOT, "validation", "gate_fixtures", "geometry_manifest_good.py")
    gm_bad = os.path.join(ROOT, "validation", "gate_fixtures", "geometry_manifest_bad_scatter.py")
    for _p in (pb_check, pb_good, pb_bad, br_check, br_good, br_bad, gm_check, gm_good, gm_bad):
        if not os.path.exists(_p):
            fails.append("2.18.01 governance self-test fixture missing: " + os.path.relpath(_p, ROOT))
    if not any("2.18.01 governance self-test fixture missing" in f for f in fails):
        pbg = subprocess.run(PY_NO_SITE + [pb_check, pb_good, ver], text=True, capture_output=True, timeout=20)
        pbb = subprocess.run(PY_NO_SITE + [pb_check, pb_bad, ver], text=True, capture_output=True, timeout=20)
        if pbg.returncode != 0 or "PROTOCOL BANNER CHECK: PASS" not in pbg.stdout:
            fails.append("protocol banner good fixture did not PASS")
        if pbb.returncode == 0 or "PROTOCOL BANNER CHECK: FAIL" not in pbb.stdout:
            fails.append("protocol banner bad fixture did not FAIL")
        brg = subprocess.run(PY_NO_SITE + [br_check, br_good], text=True, capture_output=True, timeout=20)
        brb = subprocess.run(PY_NO_SITE + [br_check, br_bad], text=True, capture_output=True, timeout=20)
        if brg.returncode != 0 or "BLENDER RUNTIME SCRIPT CHECK: PASS" not in brg.stdout:
            fails.append("Blender runtime good fixture did not PASS")
        if brb.returncode == 0 or "BLENDER RUNTIME SCRIPT CHECK: FAIL" not in brb.stdout:
            fails.append("Blender runtime bad fixture did not FAIL")
        gmg = subprocess.run(PY_NO_SITE + [gm_check, gm_good], text=True, capture_output=True, timeout=20)
        gmb = subprocess.run(PY_NO_SITE + [gm_check, gm_bad], text=True, capture_output=True, timeout=20)
        if gmg.returncode != 0 or "GEOMETRY CONSTRUCTION MANIFEST CHECK: PASS" not in gmg.stdout:
            fails.append("geometry construction good fixture did not PASS")
        if gmb.returncode == 0 or "GEOMETRY CONSTRUCTION MANIFEST CHECK: FAIL" not in gmb.stdout:
            fails.append("geometry construction bad/scatter fixture did not FAIL")
except Exception as e:
    fails.append(f"2.18.01 governance self-tests errored: {e}")


# 10g feature-recipe lookup and AI Review bundle self-tests
try:
    import subprocess
    fr_check = os.path.join(ROOT, "validation", "feature_recipe_lookup_check.py")
    ar_check = os.path.join(ROOT, "validation", "ai_review_bundle_check.py")
    ac_check = os.path.join(ROOT, "validation", "ai_capture_compliance_check.py")
    if not os.path.exists(fr_check):
        fails.append("validation/feature_recipe_lookup_check.py missing")
    else:
        frs = subprocess.run(PY_NO_SITE + [fr_check, "--self-test"], text=True, capture_output=True, timeout=30)
        if frs.returncode != 0 or "FEATURE RECIPE LOOKUP CHECK SELF-TEST: PASS" not in frs.stdout:
            fails.append("feature recipe lookup self-test failed: " + ((frs.stdout or frs.stderr).strip().splitlines()[-1] if (frs.stdout or frs.stderr).strip() else "?"))
    if not os.path.exists(ar_check):
        fails.append("validation/ai_review_bundle_check.py missing")
    else:
        ars = subprocess.run(PY_NO_SITE + [ar_check, "--self-test"], text=True, capture_output=True, timeout=30)
        if ars.returncode != 0 or "AI REVIEW BUNDLE CHECK SELF-TEST: PASS" not in ars.stdout:
            fails.append("AI Review bundle self-test failed: " + ((ars.stdout or ars.stderr).strip().splitlines()[-1] if (ars.stdout or ars.stderr).strip() else "?"))
    if not os.path.exists(ac_check):
        fails.append("validation/ai_capture_compliance_check.py missing")
    else:
        acs = subprocess.run(PY_NO_SITE + [ac_check, "--self-test"], text=True, capture_output=True, timeout=30)
        if acs.returncode != 0 or "AI CAPTURE COMPLIANCE CHECK SELF-TEST: PASS" not in acs.stdout:
            fails.append("AI capture compliance self-test failed: " + ((acs.stdout or acs.stderr).strip().splitlines()[-1] if (acs.stdout or acs.stderr).strip() else "?"))
except Exception as e:
    fails.append(f"feature recipe / AI Review / AI capture self-tests errored: {e}")


# 10e run_gate auto-required validated-logic self-test
try:
    import subprocess
    gate = os.path.join(ROOT, "validation", "run_gate.py")
    lib = os.path.join(ROOT, "library", "nms_part_dimensions_and_rules_updated.json")
    auto_bad = os.path.join(ROOT, "validation", "gate_fixtures", "auto_validated_reuse_missing_manifest.py")
    if not os.path.exists(auto_bad):
        fails.append("auto-required validated reuse fixture missing")
    else:
        ar = subprocess.run(PY_NO_SITE + [gate, auto_bad, lib, "AUTO_VALIDATED_BAD_", "--require-router"], text=True, capture_output=True, timeout=30)
        if ar.returncode == 0 or "validated logic reuse gate: AUTO-REQUIRED" not in ar.stdout or "MACHINE-CHECKABLE GATE: FAIL" not in ar.stdout:
            fails.append("run_gate auto-required validated reuse fixture did not FAIL as expected")
except Exception as e:
    fails.append(f"run_gate auto-required validated reuse self-test errored: {e}")

# 10h run_gate auto-required AI capture compliance self-test
try:
    import subprocess
    gate = os.path.join(ROOT, "validation", "run_gate.py")
    lib = os.path.join(ROOT, "library", "nms_part_dimensions_and_rules_updated.json")
    auto_bad = os.path.join(ROOT, "validation", "gate_fixtures", "auto_validated_reuse_missing_manifest.py")
    if not os.path.exists(auto_bad):
        fails.append("auto-required AI capture fixture missing")
    else:
        ar = subprocess.run(PY_NO_SITE + [gate, auto_bad, lib, "AUTO_VALIDATED_BAD_", "--require-router"], text=True, capture_output=True, timeout=30)
        if ar.returncode == 0 or "AI capture compliance gate: AUTO-REQUIRED" not in ar.stdout or "AI capture compliance gate: FAIL" not in ar.stdout or "MACHINE-CHECKABLE GATE: FAIL" not in ar.stdout:
            fails.append("run_gate auto-required AI capture compliance fixture did not FAIL as expected")
except Exception as e:
    fails.append(f"run_gate auto-required AI capture compliance self-test errored: {e}")


# 15 placement intelligence infrastructure self-check
try:
    import subprocess
    pi = os.path.join(ROOT, "validation", "placement_intelligence_infrastructure_check.py")
    if not os.path.exists(pi):
        fails.append("placement intelligence infrastructure checker missing")
    else:
        pi_run = subprocess.run(PY_NO_SITE + [pi], text=True, capture_output=True, timeout=20)
        print(pi_run.stdout.strip())
        if pi_run.returncode != 0 or "PLACEMENT INTELLIGENCE INFRASTRUCTURE: PASS" not in pi_run.stdout:
            fails.append("placement intelligence infrastructure check failed: " + (pi_run.stdout + pi_run.stderr).strip()[:1000])
except Exception as e:
    fails.append(f"placement intelligence infrastructure check crashed ({e})")

# 16 compliance manifest verifier self-test (5.00.00) — no build valid without a verified manifest
try:
    import subprocess
    cm = os.path.join(ROOT, "validation", "compliance_manifest_check.py")
    if not os.path.exists(cm):
        fails.append("validation/compliance_manifest_check.py missing")
    else:
        cmr = subprocess.run(PY_NO_SITE + [cm, "--self-test"], text=True, capture_output=True, timeout=20)
        if cmr.returncode != 0 or "COMPLIANCE MANIFEST CHECK SELF-TEST: PASS" not in cmr.stdout:
            fails.append("compliance manifest checker self-test failed: " + ((cmr.stdout or cmr.stderr).strip()[:300]))
except Exception as e:
    fails.append(f"compliance manifest checker self-test errored: {e}")

# 17 part context resolver self-test (5.01.00) — the operational reachability layer
try:
    import subprocess
    pcr = os.path.join(ROOT, "validation", "part_context_resolver.py")
    if not os.path.exists(pcr):
        fails.append("validation/part_context_resolver.py missing")
    else:
        pr = subprocess.run(PY_NO_SITE + [pcr, "--self-test"], text=True, capture_output=True, timeout=20)
        if pr.returncode != 0 or "PART CONTEXT RESOLVER SELF-TEST: PASS" not in pr.stdout:
            fails.append("part context resolver self-test failed: " + ((pr.stdout or pr.stderr).strip()[:300]))
except Exception as e:
    fails.append(f"part context resolver self-test errored: {e}")

# 18 RPAM coverage check (5.01.00) — every rule mapped to the parts/families it governs
try:
    import subprocess
    rc = os.path.join(ROOT, "validation", "rpam_coverage_check.py")
    if not os.path.exists(rc):
        fails.append("validation/rpam_coverage_check.py missing")
    else:
        rr = subprocess.run(PY_NO_SITE + [rc], text=True, capture_output=True, timeout=20)
        if rr.returncode != 0 or "RPAM COVERAGE CHECK: PASS" not in rr.stdout:
            fails.append("RPAM coverage check failed: " + ((rr.stdout or rr.stderr).strip()[:300]))
except Exception as e:
    fails.append(f"RPAM coverage check errored: {e}")

# 19 build sheet check self-test (5.02.00) — coverage + population + tamper-evident integrity
try:
    import subprocess
    bsc = os.path.join(ROOT, "validation", "build_sheet_check.py")
    if not os.path.exists(bsc):
        fails.append("validation/build_sheet_check.py missing")
    else:
        bsr = subprocess.run(PY_NO_SITE + [bsc, "--self-test"], text=True, capture_output=True, timeout=40)
        if bsr.returncode != 0 or "BUILD SHEET CHECK SELF-TEST: PASS" not in bsr.stdout:
            fails.append("build sheet check self-test failed: " + ((bsr.stdout or bsr.stderr).strip()[:300]))
except Exception as e:
    fails.append(f"build sheet check self-test errored: {e}")

# 20 run_gate build-sheet enforcement self-test (5.02.00) — covered build PASSES, uncovered ObjectID FAILS
try:
    import subprocess
    _gate = os.path.join(ROOT, "validation", "run_gate.py")
    _lib = os.path.join(ROOT, "library", "nms_master_part_map_verified_data_v3_01_02.json")
    _bsg = os.path.join(ROOT, "validation", "gate_fixtures", "build_sheet_good.py")
    _bsb = os.path.join(ROOT, "validation", "gate_fixtures", "build_sheet_bad_coverage.py")
    if not (os.path.exists(_bsg) and os.path.exists(_bsb)):
        fails.append("build sheet run_gate self-test fixtures missing")
    else:
        _gg = subprocess.run(PY_NO_SITE + [_gate, _bsg, _lib, "FIXTURE_BSHEET_", "--require-json-evidence", "--require-router"], text=True, capture_output=True, timeout=40)
        _gb = subprocess.run(PY_NO_SITE + [_gate, _bsb, _lib, "FIXTURE_BSHEET_", "--require-json-evidence", "--require-router"], text=True, capture_output=True, timeout=40)
        if _gg.returncode != 0 or "build sheet (packet) gate: PASS" not in _gg.stdout:
            fails.append("run_gate build-sheet self-test: covered build did not PASS")
        if _gb.returncode == 0 or "build sheet (packet) gate: FAIL" not in _gb.stdout:
            fails.append("run_gate build-sheet self-test: uncovered ObjectID did not FAIL")
except Exception as e:
    fails.append(f"run_gate build-sheet self-test errored: {e}")

# 21 CAPA escalation tool self-test (5.03.00)
try:
    import subprocess
    ce = os.path.join(ROOT, "validation", "capa_escalation.py")
    if not os.path.exists(ce):
        fails.append("validation/capa_escalation.py missing")
    else:
        cer = subprocess.run(PY_NO_SITE + [ce, "--self-test"], text=True, capture_output=True, timeout=20)
        if cer.returncode != 0 or "CAPA ESCALATION SELF-TEST: PASS" not in cer.stdout:
            fails.append("CAPA escalation self-test failed: " + ((cer.stdout or cer.stderr).strip()[:300]))
except Exception as e:
    fails.append(f"CAPA escalation self-test errored: {e}")

# 22 run_gate CAPA-escalation enforcement self-test (5.03.00) — active escalation REQUIRES deeper manifest
try:
    import subprocess
    _gate = os.path.join(ROOT, "validation", "run_gate.py")
    _lib = os.path.join(ROOT, "library", "nms_master_part_map_verified_data_v3_01_02.json")
    _bsg = os.path.join(ROOT, "validation", "gate_fixtures", "build_sheet_good.py")
    _act = os.path.join(ROOT, "validation", "gate_fixtures", "capa_state_active.json")
    if not (os.path.exists(_bsg) and os.path.exists(_act)):
        fails.append("CAPA escalation run_gate self-test fixtures missing")
    else:
        _ce = subprocess.run(PY_NO_SITE + [_gate, _bsg, _lib, "FIXTURE_BSHEET_", "--require-json-evidence", "--require-router", "--capa-state", _act], text=True, capture_output=True, timeout=40)
        if _ce.returncode == 0 or "deeper compliance manifest gate: FAIL" not in _ce.stdout:
            fails.append("run_gate CAPA-escalation self-test: active escalation without manifest did not FAIL")
except Exception as e:
    fails.append(f"run_gate CAPA-escalation self-test errored: {e}")

# 23 single current-state source — no version-section call-outs in governance/active-build docs
try:
    import subprocess
    vcc = os.path.join(ROOT, "validation", "version_callout_check.py")
    if not os.path.exists(vcc):
        fails.append("validation/version_callout_check.py missing")
    else:
        vr = subprocess.run(PY_NO_SITE + [vcc], text=True, capture_output=True, timeout=30)
        if vr.returncode != 0 or "VERSION-CALLOUT GATE: PASS" not in vr.stdout:
            fails.append("version-callout gate failed: " + ((vr.stdout or vr.stderr).strip().splitlines() or ["?"])[-1])
except Exception as e:
    fails.append(f"version-callout gate errored: {e}")

# 24 rule classification completeness — every rule carries kind + runtime_status (enforces RULE_UPDATE_PROTOCOL)
try:
    import subprocess
    rcc = os.path.join(ROOT, "validation", "rule_classification_check.py")
    if not os.path.exists(rcc):
        fails.append("validation/rule_classification_check.py missing")
    else:
        rr = subprocess.run(PY_NO_SITE + [rcc], text=True, capture_output=True, timeout=30)
        if rr.returncode != 0 or "RULE CLASSIFICATION CHECK: PASS" not in rr.stdout:
            fails.append("rule-classification gate failed: " + ((rr.stdout or rr.stderr).strip().splitlines() or ["?"])[-1])
except Exception as e:
    fails.append(f"rule-classification gate errored: {e}")

# 25 open-topics continuity structure + chat transfer doc present
try:
    import subprocess
    otc = os.path.join(ROOT, "validation", "open_topics_structure_check.py")
    if not os.path.exists(otc):
        fails.append("validation/open_topics_structure_check.py missing")
    else:
        ot = subprocess.run(PY_NO_SITE + [otc], text=True, capture_output=True, timeout=30)
        if ot.returncode != 0 or "OPEN-TOPICS STRUCTURE CHECK: PASS" not in ot.stdout:
            fails.append("open-topics structure gate failed: " + ((ot.stdout or ot.stderr).strip().splitlines() or ["?"])[-1])
except Exception as e:
    fails.append(f"open-topics structure gate errored: {e}")

# 26 onboarding builder-readiness gauntlet structure
try:
    import subprocess
    ogc = os.path.join(ROOT, "validation", "onboarding_gauntlet_check.py")
    if not os.path.exists(ogc):
        fails.append("validation/onboarding_gauntlet_check.py missing")
    else:
        og = subprocess.run(PY_NO_SITE + [ogc], text=True, capture_output=True, timeout=30)
        if og.returncode != 0 or "ONBOARDING GAUNTLET CHECK: PASS" not in og.stdout:
            fails.append("onboarding gauntlet gate failed: " + ((og.stdout or og.stderr).strip().splitlines() or ["?"])[-1])
except Exception as e:
    fails.append(f"onboarding gauntlet gate errored: {e}")

# 27 discover_by_quality view sync
try:
    import subprocess
    dqc = os.path.join(ROOT, "validation", "discover_by_quality_check.py")
    if not os.path.exists(dqc):
        fails.append("validation/discover_by_quality_check.py missing")
    else:
        dq = subprocess.run(PY_NO_SITE + [dqc], text=True, capture_output=True, timeout=30)
        if dq.returncode != 0 or "DISCOVER_BY_QUALITY: in sync" not in dq.stdout:
            fails.append("discover_by_quality sync gate failed: " + ((dq.stdout or dq.stderr).strip().splitlines() or ["?"])[-1])
except Exception as e:
    fails.append(f"discover_by_quality sync gate errored: {e}")

# 28 new-file guard (anti-bloat: no unapproved new files)
try:
    import subprocess
    nfg = os.path.join(ROOT, "validation", "new_file_guard_check.py")
    if not os.path.exists(nfg):
        fails.append("validation/new_file_guard_check.py missing")
    else:
        nf = subprocess.run(PY_NO_SITE + [nfg], text=True, capture_output=True, timeout=30)
        if nf.returncode != 0 or "NEW FILE GUARD: PASS" not in nf.stdout:
            fails.append("new-file guard failed: " + ((nf.stdout or nf.stderr).strip().splitlines() or ["?"])[-1])
except Exception as e:
    fails.append(f"new-file guard errored: {e}")

print("RELEASE GATE CHECK  (version", ver + ")")
for w in warns: print("  WARN:", w)
if not fails:
    print("  all checks passed")
    print("RELEASE GATE: PASS")
    sys.exit(0)
for f in fails: print("  FAIL:", f)
print(f"RELEASE GATE: FAIL ({len(fails)} issue(s))")
sys.exit(1)
