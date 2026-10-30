// Links from VS Code back to the Debug GYM website.

// code-server rewrites links to exactly "localhost:<port>" or "127.0.0.1:<port>" into its own
// /proxy/<port> route, which cannot reach the website. Its check is case-sensitive, while
// browsers ignore the case of host names, so "LOCALHOST" opens the same site, login included.
function siteLink(site) {
  return site.replace(/^(https?:\/\/)localhost(:\d+)/, "$1LOCALHOST$2");
}

module.exports = { siteLink };
