# Part 1 — Flaky Test Analysis

## Summary
The intern's Playwright login tests are flaky because they **assert before the app is ready** (race conditions) and contain a **false-positive** in the multi-tenant test.

## 1. Flakiness Issues
| # | Issue | Impact |
|---|-------|--------|
| 1 | No explicit waits — assertions fire immediately after `click()` | Race condition |
| 2 | Strict URL equality (`==`) | Fails on query strings/slashes/redirect delay |
| 3 | `is_visible()` used as assertion (no waiting) | Race-prone |
| 4 | Dynamic dashboard loading not handled | Intermittent failures |
| 5 | `.all()` captures cards too early → empty list → **vacuous pass** | **False positive** |
| 6 | 2FA screen not handled | Flow never reaches dashboard |
| 7 | No cleanup on failure (`browser.close()` skipped) | Resource leak |
| 8 | Hardcoded credentials/URLs | Security & maintainability |
| 9 | No viewport control | Responsive layout hides elements in CI |
| 10 | No timeout/retry config | Slow tenants time out |

## 2. Root Causes — Why CI ≠ Local
- **Slower CI CPU** (shared, headless) widens timing gaps.
- **Network latency** to data-center-hosted app amplifies async delays.
- **Resource contention** from parallel jobs starves each test.
- **Headless + default viewport** may hide/relocate elements.
- Net effect: the race the app usually wins locally is frequently **lost in CI**.

## 3. Fixes (see `tests/ui/test_login_fixed.py`)
- Replace immediate checks with auto-waiting `expect()`.
- Regex URL matching instead of strict equality.
- Optional 2FA handling in a reusable `login()` helper.
- Guaranteed cleanup via fixture teardown.
- Fixed viewport + externalized config + configurable timeouts.
- **Fix the false positive**: wait for the first card and assert the list is non-empty before checking tenant isolation.

## Key Insight
A flaky test that **passes while verifying nothing** (issue #5) is more dangerous than one that fails — it provides false confidence. Catching this is the most important fix here.