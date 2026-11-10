# Print the JUnit results of the ant jdk15to18 test run: one line per suite, every
# skipped/failed test with its message, then the grand total.
# Usage: python3 .travis/seal-test-summary.py <reports-xml-dir>
import glob
import os
import sys
import xml.etree.ElementTree as ET

report_dir = sys.argv[1]
totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
files = sorted(glob.glob(os.path.join(report_dir, "TEST-*.xml")))
for path in files:
    suite = ET.parse(path).getroot()
    counts = {k: int(suite.get(k, "0") or 0) for k in totals}
    skipped_cases = []
    for case in suite.iter("testcase"):
        name = "%s.%s" % (case.get("classname"), case.get("name"))
        for tag in ("skipped", "failure", "error"):
            el = case.find(tag)
            if el is not None:
                if tag == "skipped":
                    skipped_cases.append(case)
                msg = el.get("message") or ""
                if not msg and (el.text or "").strip():
                    msg = el.text.strip().splitlines()[0]
                print("  %s: %s -- %s" % (tag.upper(), name, msg))
    if counts["skipped"] == 0 and skipped_cases:
        counts["skipped"] = len(skipped_cases)
    for k in totals:
        totals[k] += counts[k]
    passed = counts["tests"] - counts["failures"] - counts["errors"] - counts["skipped"]
    print("SUITE %s: tests=%d passed=%d failures=%d errors=%d skipped=%d time=%ss" % (
        suite.get("name"), counts["tests"], passed, counts["failures"], counts["errors"],
        counts["skipped"], suite.get("time")))
passed = totals["tests"] - totals["failures"] - totals["errors"] - totals["skipped"]
print("SEAL TEST TOTAL (%d suites): tests=%d passed=%d failures=%d errors=%d skipped=%d" % (
    len(files), totals["tests"], passed, totals["failures"], totals["errors"], totals["skipped"]))
