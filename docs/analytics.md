# Product analytics

This page defines how Debug GYM's use is measured: the one number its value is
read from, the metrics that explain it, and the events the product records.
Instrumentation and dashboards follow this plan; until they run, every query
below is a specification and not a result.

## The Value And The Metrics

The focus metric is **solved exercises per active learner per week**. It
expresses [VP-01](research/value-proposition.md#vp-01), practising debugging in
realistic code.

### The Metric Tree

The label is the metric's level: `Focus` is the focus metric, `L1` an input
metric one level under it, and `L2` an input under an L1 input.
`(counter-metric)` marks the counter-metric, which guards the focus metric
rather than feeding it. Each metric's name links to its section.

- **Focus:** [Solved exercises per active learner per week](#solved-exercises-per-active-learner-per-week)
  - **L1 (counter-metric):** [Attempts per solved exercise](#attempts-per-solved-exercise)
  - **L1:** [Started exercises per active learner per week](#started-exercises-per-active-learner-per-week)
    - **L2:** [Search match rate](#search-match-rate)
    - **L2:** [Workspace open rate](#workspace-open-rate)

### Why This Focus Metric

The focus metric may depend on several input metrics, and it may have no value
until people outside the team use the product. Test and smoke traffic is
excluded and is not presented as its value.

The seven criteria of the
[North Star Framework](https://openpracticelibrary.com/practice/north-star-framework/):

- **Expresses value:** a learner who solves an exercise has practised the whole
  loop of reproducing, investigating and fixing a bug.
- **Represents the vision and strategy:** the product exists to give learners
  repeated debugging practice, and this counts completed practice.
- **Is a leading indicator:** learners who keep solving exercises are the ones
  who keep using the product.
- **Is actionable:** the team can move it with better exercises, a faster
  start and clearer test output.
- **Is understandable:** it is the number of exercises a typical active learner
  solved this week.
- **Is measurable:** it is computed from the events in [The Events](#the-events)
  and from no hand-kept table.
- **Is not a vanity metric:** it counts solutions verified by the server, not
  visits or sign-ups.

Rejected as a vanity metric: total registered accounts, because it only grows
and says nothing about whether anyone practises.

### Solved exercises per active learner per week

- **Definition:** The number of distinct learner and exercise pairs with a
  `solution_verified` event whose tests all passed, divided by the number of
  distinct learners with an `exercise_opened` event, over the last seven days.
- **Source:** [`solution_verified`](#the-events) and
  [`exercise_opened`](#the-events).
- **Query:** Over the last seven days, excluding `source = 'smoke'`:

  ```sql
  SELECT
    count(DISTINCT learner_id || ':' || exercise_slug)
      FILTER (WHERE name = 'solution_verified' AND all_passed)::numeric
    / nullif(count(DISTINCT learner_id)
      FILTER (WHERE name = 'exercise_opened'), 0) AS solved_per_active_learner
  FROM events
  WHERE source <> 'smoke' AND timestamp >= now() - interval '7 days';
  ```

### Attempts per solved exercise

- **Definition:** The number of `solution_verified` events divided by the
  number of distinct learner and exercise pairs that passed all tests, over the
  last seven days. A rising value while the focus metric rises suggests
  learners are guessing instead of investigating.
- **Source:** [`solution_verified`](#the-events).
- **Query:** Over the last seven days, excluding `source = 'smoke'`:

  ```sql
  SELECT
    count(*) FILTER (WHERE name = 'solution_verified')::numeric
    / nullif(count(DISTINCT learner_id || ':' || exercise_slug)
      FILTER (WHERE name = 'solution_verified' AND all_passed), 0) AS attempts_per_solve
  FROM events
  WHERE source <> 'smoke' AND timestamp >= now() - interval '7 days';
  ```

### Started exercises per active learner per week

- **Definition:** The number of distinct learner and exercise pairs with a
  `workspace_opened` event, divided by the number of distinct learners with an
  `exercise_opened` event, over the last seven days.
- **Source:** [`workspace_opened`](#the-events) and
  [`exercise_opened`](#the-events).
- **Query:** Over the last seven days, excluding `source = 'smoke'`:

  ```sql
  SELECT
    count(DISTINCT learner_id || ':' || exercise_slug)
      FILTER (WHERE name = 'workspace_opened')::numeric
    / nullif(count(DISTINCT learner_id)
      FILTER (WHERE name = 'exercise_opened'), 0) AS started_per_active_learner
  FROM events
  WHERE source <> 'smoke' AND timestamp >= now() - interval '7 days';
  ```

### Search match rate

- **Definition:** The number of `exercise_searched` events with at least one
  result divided by all `exercise_searched` events, over the last seven days.
- **Source:** [`exercise_searched`](#the-events).
- **Query:** Over the last seven days, excluding `source = 'smoke'`:

  ```sql
  SELECT
    count(*) FILTER (WHERE result_count > 0)::numeric
    / nullif(count(*), 0) AS search_match_rate
  FROM events
  WHERE name = 'exercise_searched'
    AND source <> 'smoke' AND timestamp >= now() - interval '7 days';
  ```

### Workspace open rate

- **Definition:** The number of distinct learner and exercise pairs with a
  `workspace_opened` event divided by the number with an `exercise_opened`
  event, over the last seven days.
- **Source:** [`workspace_opened`](#the-events) and
  [`exercise_opened`](#the-events).
- **Query:** Over the last seven days, excluding `source = 'smoke'`:

  ```sql
  SELECT
    count(DISTINCT learner_id || ':' || exercise_slug)
      FILTER (WHERE name = 'workspace_opened')::numeric
    / nullif(count(DISTINCT learner_id || ':' || exercise_slug)
      FILTER (WHERE name = 'exercise_opened'), 0) AS workspace_open_rate
  FROM events
  WHERE source <> 'smoke' AND timestamp >= now() - interval '7 days';
  ```

This rate is computed by the query rather than by hand.

## The Events

An event is one action the product records. Names follow the convention
`object_action` in snake case. Every event carries `learner_id` (an opaque
random identifier that is not derived from the username or email) and `source`
(`web`, `usability-test` or `smoke`; `smoke` marks the team's pipeline checks
and every metric excludes it). No event carries a name, email address or free
text. The queries above use the pipeline's `events` table with `name`,
`timestamp`, `learner_id` and `source` columns plus the fields below, and are
adapted to the chosen backend's query language when it is deployed.

| Event | Fires when | Fields | Collected at |
| --- | --- | --- | --- |
| `exercise_searched` | A learner searches the prepared exercises. | `learner_id` (UUID, required), `source` (`web`, `usability-test` or `smoke`, required), `result_count` (integer, required) | `exercise catalog`, staging and production |
| `exercise_opened` | A learner opens an exercise page. | `learner_id` (UUID, required), `source` (`web`, `usability-test` or `smoke`, required), `exercise_slug` (string, required) | `exercise catalog`, staging and production |
| `workspace_opened` | A learner opens an exercise's VS Code workspace. | `learner_id` (UUID, required), `source` (`web`, `usability-test` or `smoke`, required), `exercise_slug` (string, required) | `exercise catalog`, staging and production |
| `solution_verified` | The server finishes verifying a submitted solution ([FR-011](functional-requirements/fr/FR-011.md)). | `learner_id` (UUID, required), `source` (`web`, `usability-test` or `smoke`, required), `exercise_slug` (string, required), `passed_count` (integer, required), `total_count` (integer, required), `all_passed` (boolean, required) | `exercise catalog`, staging and production |

## Pipeline

The `exercise catalog` sends each event over HTTPS from a bounded background
queue to the self-hosted analytics backend ([ADR-006](architecture/adr/ADR-006.md)).
Collection is off unless `DEBUG_GYM_ANALYTICS_URL` is set, and a failed send
never affects the learner's request
([FR-014](functional-requirements/fr/FR-014.md)). The target deployment is one
OpenPanel instance on the university VM with separate `staging` and `production`
projects and credentials. Retention is planned for 90 days, which covers every
seven-day metric window. The backend has not been deployed yet.

The steps and configuration belong to the
[telemetry pipeline runbook](deployment.md#telemetry-pipelines); `.env.example`
records the configuration shape and no credential.

To check the pipeline without counting as learner activity, run
`python scripts/send_smoke_event.py --url <backend address>`. It sends one event
of each kind with `source = smoke`, and every query on this page excludes that
source.

## Dashboard

The planned dashboards are `Debug GYM usage (staging)` and
`Debug GYM usage (production)`. Each contains a chart named
`Started exercises per active learner per week` that runs that metric's query.
The staging dashboard also contains a recent-events panel that shows the
`source=smoke` pipeline check while the metric chart excludes it. The production
dashboard carries the same query and receives no test traffic.

Neither dashboard exists yet. Their private addresses and the required
sanitized screenshots therefore are not recorded as evidence.

## Collected data

Each event holds its name, a UTC timestamp, a random opaque `learner_id`, a
`source` (`web`, `usability-test` or `smoke`) and the fields in the event table.
It holds no name, email, username, exercise code or free-text search query. The
`learner_id` is stored on the learner's profile and cannot be derived from
account data.
The planned OpenPanel instance on the university VM stores the events in the
environment's project. Collection is disabled by leaving
`DEBUG_GYM_ANALYTICS_URL` unset. No analytics backend currently stores the
events outside temporary development checks.
