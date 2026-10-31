// Run with: node --test app/adel_b/vscode-extension/test/*.test.js
const assert = require("node:assert/strict");
const test = require("node:test");
const { parseJUnit } = require("../junit");

// Trimmed from a real pytest 8.4 report (-o junit_family=xunit1) on the buggy remove_negatives.
const REPORT = `<?xml version="1.0" encoding="utf-8"?><testsuites name="pytest tests"><testsuite name="pytest" errors="0" failures="2" skipped="0" tests="3" time="0.033"><testcase classname="tests.test_remove_negatives" name="test_empty_list" file="tests/test_remove_negatives.py" line="3" time="0.000" /><testcase classname="tests.test_remove_negatives" name="test_mixed_numbers" file="tests/test_remove_negatives.py" line="7" time="0.001"><failure message="assert [4, -2, 5] == [4, 5]&#10;  &#10;  At index 1 diff: -2 != 5">def test_mixed_numbers() -&gt; None:
&gt;       assert remove_negatives([4, -3, -2, 5]) == [4, 5]
E       assert [4, -2, 5] == [4, 5]

tests/test_remove_negatives.py:9: AssertionError</failure></testcase><testcase classname="tests.test_remove_negatives" name="test_consecutive_negatives" file="tests/test_remove_negatives.py" line="11" time="0.001"><failure message="assert [-2] == []">E       assert [-2] == []</failure></testcase></testsuite></testsuites>`;

test("reads passed and failed tests from a real pytest report", () => {
  const results = parseJUnit(REPORT);
  assert.deepEqual(
    results.map(({ name, status, line }) => [name, status, line]),
    [
      ["test_empty_list", "passed", 3],
      ["test_mixed_numbers", "failed", 7],
      ["test_consecutive_negatives", "failed", 11],
    ],
  );
  assert.equal(results[1].file, "tests/test_remove_negatives.py");
  assert.equal(results[1].message.split("\n")[0], "assert [4, -2, 5] == [4, 5]");
  assert.match(results[1].details, /^def test_mixed_numbers\(\) -> None:\n>\s+assert/);
});

test("reads errors, skips and escaped characters", () => {
  const results = parseJUnit(
    '<testsuite><testcase name="test_import" file="tests/test_x.py" line="0"><error message="ImportError: cannot import &quot;x&quot; &amp; y">trace</error></testcase>' +
      '<testcase name="test_later" file="tests/test_x.py" line="4"><skipped message="not yet"/></testcase></testsuite>',
  );
  assert.deepEqual(results[0], {
    name: "test_import",
    file: "tests/test_x.py",
    line: 0,
    status: "failed",
    message: 'ImportError: cannot import "x" & y',
    details: "trace",
  });
  assert.equal(results[1].status, "skipped");
});

test("an empty report has no results", () => {
  assert.deepEqual(parseJUnit('<testsuites><testsuite tests="0"></testsuite></testsuites>'), []);
});
