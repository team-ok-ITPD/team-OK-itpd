# Observability

Use the Django catalog's request signals to diagnose slow or failed exercise
searches. This page defines the signals emitted by the application and the
queries to use when configuring OpenObserve. Staging and production verification
is pending.

## Signals

| Signal | Application source | Collection |
| --- | --- | --- |
| Metric | A Prometheus duration histogram for `POST /api/exercises` | Scrape `GET /metrics` with the environment's bearer token and remote-write to its OpenObserve organization. |
| Log | One JSON line on standard output per catalog search request | Collect JSON lines with `event=catalog_request` in the `debug_gym_requests` log stream. |
| Trace | No distributed tracing is configured. | Correlate the client response with the request log using `X-Request-ID`. |

The log records `request_id`, `route`, `outcome`, `status` and `duration_ms`.
The application generates the request ID and returns it in `X-Request-ID`.
The structured signal excludes query text, user identifiers, headers and
request bodies. Keep request IDs in logs so metric series have bounded labels.

The following log line uses synthetic values.

```json
{"event":"catalog_request","request_id":"e00d9939bbd64b6386407f4417151632","route":"/api/exercises","outcome":"client_error","status":404,"duration_ms":12.3}
```

Set `DEBUG_GYM_METRICS_TOKEN` in the Django process environment and configure the
scraper with the same token. Use separate tokens and OpenObserve organizations
for staging and production. Keep the endpoint on the monitoring network. The
endpoint returns 404 when the token is absent or invalid. The registry is local
to each Django process, so scrape each serving instance separately. The current
configuration assumes one serving process per scrape target.

## The SLIs

### SLI-01

Catalog request duration (P95)

- **Status:** Active
- **Definition:** The 95th percentile of elapsed Django handling time for
  `POST /api/exercises`, grouped by `route` and `outcome`. The outcome is
  `success` for responses below 400, `client_error` for 4xx or `server_error`
  for 5xx. The log's `request_id` identifies an individual request. This covers
  the server-side catalog portion of [QR-04](quality-requirements/qr/QR-04.md).
  Its browser and workspace timings still require separate measurements.
- **Unit:** Seconds
- **Window:** Rolling five minutes
- **Source:** `debug_gym_http_request_duration_seconds_bucket` in the
  environment's OpenObserve organization.
- **Query:**

  ```promql
  histogram_quantile(
    0.95,
    sum by (le, route, outcome) (
      rate(debug_gym_http_request_duration_seconds_bucket{route="/api/exercises"}[5m])
    )
  )
  ```

Run this log query in the same organization. Replace the example ID with the
value of the failed request's response header.

```sql
SELECT request_id, route, outcome, status, duration_ms
FROM "debug_gym_requests"
WHERE request_id = 'e00d9939bbd64b6386407f4417151632'
```

Use SLI-01 for the Assignment 6 demonstration. On staging, allow one baseline
scrape, then send an authenticated search that returns 200 and one that returns
404 because the catalog has no match. After the next scrape, look up the 404 by
its request ID and verify a numeric `client_error` P95 within the five-minute
window. Use the same query in production and keep the smoke traffic on staging.
