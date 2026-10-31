/* One serial subscription per open practice page. No submission writes. */
(function (root) {
  function createSubmissionSync({ read, apply, isActive, onError, interval = 2000, setTimer = setTimeout, clearTimer = clearTimeout }) {
    let stopped = false;
    let timer = null;
    let pending = null;
    let controller = null;

    function schedule() {
      if (stopped) return;
      if (timer !== null) clearTimer(timer);
      timer = setTimer(() => { timer = null; void refresh(); }, interval);
    }

    function refresh() {
      if (stopped) return Promise.resolve();
      if (pending) return pending;
      if (timer !== null) { clearTimer(timer); timer = null; }
      if (!isActive()) { schedule(); return Promise.resolve(); }
      controller = new AbortController();
      pending = Promise.resolve()
        .then(() => read(controller.signal))
        .then((snapshot) => {
          if (!stopped && isActive()) return apply(snapshot);
        })
        .catch((error) => {
          if (!stopped && isActive()) onError(error);
        })
        .finally(() => { pending = null; controller = null; schedule(); });
      return pending;
    }

    function stop() {
      stopped = true;
      if (timer !== null) clearTimer(timer);
      timer = null;
      controller?.abort();
    }

    return { refresh, stop };
  }

  const api = { createSubmissionSync };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.DebugGymSubmissionSync = api;
})(globalThis);
