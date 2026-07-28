# Assumptions & Reasoning

The requirements were intentionally incomplete. Below are the assumptions made to proceed, each with reasoning. Open questions for discussion are listed at the end.

## Global
| # | Assumption | Reasoning |
|---|-----------|-----------|
| 1 | A dedicated **staging environment** exists mirroring production. | Data-creating tests must never run against production. |
| 2 | Tests run in **CI/CD** headless containers. | The login test fails "in CI/CD"; framework is CI-first. |
| 3 | **Secrets injected via env/vault**, never committed. | Multi-tenant B2B security; hardcoding is a risk. |
| 4 | Stable **selectors** (`data-testid`/IDs) are available. | Reliable automation needs stable locators. |

## Part 1 — Flaky Test
| # | Assumption | Reasoning |
|---|-----------|-----------|
| 5 | Dashboard elements **load asynchronously**. | Given context; drives auto-waiting fixes. |
| 6 | **Some users trigger 2FA**; login handles it optionally. | Given context. |
| 7 | Test users can **bypass 2FA / fetch OTP** programmatically. | Full automation impossible with human-delivered OTP. |
| 8 | Post-login URL may include **query strings/slashes**. | Why strict equality was replaced with regex match. |
| 9 | An **empty project list is a real failure**. | Original loop passes vacuously (false positive). |

## Part 2 — Framework
| # | Assumption | Reasoning |
|---|-----------|-----------|
| 10 | Multi-tenancy uses **subdomains**. | Matches requirement; drives config design. |
| 11 | **Disposable data** via API per run. | Enables isolated, repeatable, parallel-safe tests. |
| 12 | **Limited BrowserStack parallel sessions** (cost-capped). | Balance speed vs. cost. |
| 13 | **Allure/HTML reporting** with artifacts on failure. | Essential for debugging CI failures. |
| 14 | **Role-based users** exist per tenant. | Given requirement. |

## Part 3 — Integration
| # | Assumption | Reasoning |
|---|-----------|-----------|
| 15 | An **auth API returns a bearer token** per tenant/user. | Faster/reliable setup vs. UI login. |
| 16 | A **`DELETE /projects/{id}`** endpoint exists. | Guaranteed teardown. |
| 17 | **Mobile = mobile web** via BrowserStack. | Flow is web-based; native app not confirmed. |
| 18 | Cross-tenant request returns **403/404**. | The tenant isolation security contract. |
| 19 | API may have **transient network issues**. | Real CI/network reality; retries added. |

## Open Questions for the Live Discussion
- Is there a **seed/reset API** for test data, or shared accounts? Cleanup policy?
- Do we test against **staging or production**? Stability?
- How is **2FA** handled for automated accounts?
- How many **BrowserStack parallel sessions** are licensed?
- **Native apps or mobile web**? Priority devices/OS?
- Preferred **reporting tool** and artifact storage?
- **CI triggers**, max pipeline runtime, and **flaky-test quarantine** policy?