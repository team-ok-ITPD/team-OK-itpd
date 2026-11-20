// The workspace image supplies Python and Node without per-exercise installs.
function testCommand(language, report, targets) {
  if (language === "javascript") {
    return {
      executable: "/usr/lib/code-server/lib/node",
      args: ["--test", "--test-reporter=junit", "--test-reporter-destination=" + report],
    };
  }
  return {
    executable: "python",
    args: ["-m", "pytest", "-q", "-p", "no:cacheprovider", "-o", "junit_family=xunit1", "--junitxml=" + report, ...targets],
  };
}
module.exports = { testCommand };
