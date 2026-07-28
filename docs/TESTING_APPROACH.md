# Testing Approach & Framework Design

## Philosophy
**Reliability over quantity.** A small, trustworthy suite beats a large, flaky one. Every design decision below serves reliability, maintainability, and cost-awareness.

## Tool Choices & Reasoning
| Tool | Why |
|------|-----|
| **Playwright** | Built-in auto-waiting eliminates the #1 cause of flakiness; strong cross-browser support. |
| **pytest** | Powerful fixtures, markers, parametrization; industry standard. |
| **requests** | Simple, reliable API layer for setup and backend assertions. |
| **BrowserStack** | Real devices/browsers at scale without maintaining a device lab. |
| **pytest-xdist** | Parallel execution for faster CI. |
| **Allure / pytest-html** | Actionable failure reports with artifacts. |

## Architecture
- **Page Object Model** (`src/pages/`) — centralizes selectors; UI changes touch one file.
- **API client layer** (`src/api/`) — encapsulates auth, headers (`X-Tenant-ID`), retries.
- **Driver factory** (`src/utils/`) — abstracts local vs BrowserStack, web vs mobile.
- **Config-driven** (`config/`) — environments, browsers, devices selected via env vars.

## Test Pyramid Application
1. **Create state via API** (fast, stable).
2. **Verify via UI** (only what UI can show).
3. **Reserve mobile/real-device runs** for nightly/pre-release to control cost.

## Handling Flakiness (see PART1_FLAKY_ANALYSIS.md)
- Auto-waiting `expect()` — never `sleep()`.
- Stable selectors; fixed viewport.
- Test isolation with fresh, uniquely-named data.
- Guaranteed cleanup even on failure.

## Multi-Tenant Testing
Tenant isolation is treated as a **security requirement**, asserted at two layers:
- **UI:** other tenant sees zero cards for the project.
- **API:** other tenant's token returns 403/404.

## CI/CD Strategy
- Smoke on every PR (fast feedback); full regression nightly; device sweep pre-release.
- Parallel-safe via data isolation.
- Trace/video/screenshots published on failure.

## Reporting & Monitoring
- Per-run HTML/Allure reports with artifacts on failure.
- Track flaky rate and suite duration over time to catch degradation.