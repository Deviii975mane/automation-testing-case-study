# Sample Test Execution Report

**Run:** 2026-07-28 02:00 UTC · **Environment:** staging · **Trigger:** nightly regression

## Summary
| Metric | Value |
|--------|-------|
| Total tests | 12 |
| Passed | 11 |
| Failed | 0 |
| Skipped | 1 (BrowserStack not configured) |
| Duration | 3m 42s |
| Flaky rate (30-day) | 0.8% |

## Results by Suite
| Suite | Passed | Failed | Skipped |
|-------|--------|--------|---------|
| UI (Part 1) | 2 | 0 | 0 |
| API | 3 | 0 | 0 |
| Integration (Part 3) | 4 | 0 | 1 |
| Cross-browser | 3 | 0 | 0 |

## Notes
- Mobile test skipped: `BROWSERSTACK_USERNAME` not set in this run.
- All tenant-isolation (security) assertions passed at both UI and API layers.

> This is an illustrative sample. Real reports are generated via pytest-html / Allure.