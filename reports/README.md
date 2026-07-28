# Test Execution Reports

This folder holds generated test execution reports. Reports are **generated at runtime** (and by CI) rather than committed, so this folder ships with documentation and a sample only.

## Generating Reports Locally

### HTML report (pytest-html)
```bash
pytest --html=reports/report.html --self-contained-html
```
Open `reports/report.html` in a browser.

### Allure report (richer, with trends)
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## In CI
The GitHub Actions pipeline (`.github/workflows/ci.yaml`) runs tests and uploads the report as a build **artifact**:
- `smoke-report` — on every PR/push
- `regression-report` — nightly full run

Download artifacts from the **Actions** tab of the run.

## What's Captured on Failure
- Screenshots (`reports/*.png` via `BasePage.screenshot`)
- HTML/Allure result with error trace
- (Recommended) Playwright trace/video for UI failures

## Sample
See [`sample-report.md`](sample-report.md) for an example of a report summary layout.