# Architecture

## System Shape

- entrypoints:
- core services:
- storage:
- external integrations:

## Module Map

| Module | Responsibility | Depends On | Notes |
| --- | --- | --- | --- |
| `example/module` | What it owns | Main upstreams | Important caveats |

## Key Flows

### Flow: Example Request

1. entrypoint receives input
2. validation layer checks shape
3. domain service performs work
4. storage or external call persists state
5. response is returned

## Data Boundaries

- Source of truth:
- Cached state:
- Derived state:
- Temporary artifacts:

## Failure-Prone Areas

- area:
  - why it is risky
  - how to detect failure
  - recovery notes

## Change Guide

When touching this system, answer:

1. which module truly owns the change?
2. which callers might break?
3. which tests prove the change?
4. which docs need updating?

