// Runs the learner's Python in the browser with Pyodide, inside a worker so a
// stuck loop can be stopped without freezing the page.

importScripts("https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js");

const HARNESS = `
import contextlib
import copy
import io
import json


def _error_text(error):
    if isinstance(error, SyntaxError):
        return f"SyntaxError: {error.msg} (line {error.lineno})"
    return f"{type(error).__name__}: {error}"


def run_exercise(code, function_name, tests_json):
    tests = json.loads(tests_json)
    stdout = io.StringIO()
    namespace = {"__name__": "exercise"}
    try:
        with contextlib.redirect_stdout(stdout):
            exec(compile(code, "exercise.py", "exec"), namespace)
    except Exception as error:
        return json.dumps({"error": _error_text(error), "stdout": stdout.getvalue()})

    function = namespace.get(function_name)
    if not callable(function):
        return json.dumps({
            "error": f"NameError: {function_name}() is not defined",
            "stdout": stdout.getvalue(),
        })

    results = []
    for test in tests:
        try:
            with contextlib.redirect_stdout(stdout):
                actual = function(copy.deepcopy(test["input"]))
            results.append({"actualRepr": repr(actual), "passed": actual == test["expected"]})
        except Exception as error:
            results.append({"error": _error_text(error), "passed": False})
    return json.dumps({"results": results, "stdout": stdout.getvalue()})
`;

const ready = (async () => {
  const pyodide = await loadPyodide();
  pyodide.runPython(HARNESS);
  self.postMessage({ type: "ready" });
  return pyodide;
})();
ready.catch((error) => self.postMessage({ type: "load-failed", failure: String(error.message || error) }));

self.onmessage = async (event) => {
  const { id, code, functionName, tests } = event.data;
  try {
    const pyodide = await ready;
    const run = pyodide.globals.get("run_exercise");
    const output = run(code, functionName, JSON.stringify(tests));
    run.destroy();
    self.postMessage({ id, ...JSON.parse(output) });
  } catch (error) {
    self.postMessage({ id, failure: String(error.message || error) });
  }
};
