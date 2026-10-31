// Run with: node --test app/adel_b/vscode-extension/test/links.test.js
const assert = require("node:assert/strict");
const test = require("node:test");
const { siteLink } = require("../links");

test("a localhost link escapes code-server's proxy rewrite", () => {
  assert.equal(
    siteLink("http://localhost:8001/#/practice/remove-negatives"),
    "http://LOCALHOST:8001/#/practice/remove-negatives",
  );
});

test("other sites are left alone", () => {
  assert.equal(siteLink("https://debug-gym.example.org/#/practice/x"), "https://debug-gym.example.org/#/practice/x");
  assert.equal(siteLink("http://localhost.example.org:8001/"), "http://localhost.example.org:8001/");
});
