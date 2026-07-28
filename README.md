# WorkFlow Pro — QA Automation Case Study

End-to-end test automation for **WorkFlow Pro**, a multi-tenant B2B project-management SaaS. This repository demonstrates a maintainable, CI-first automation framework using **Playwright + pytest**, with API + UI integration testing and BrowserStack (mobile/cross-browser) concepts.

## 📁 Repository Structure

```
Workflowpro/
├── README.md                       # this file
├── requirements.txt                # Python dependencies
├── pytest.ini                      # pytest config & markers
├── conftest.py                     # shared fixtures (browser, api, tenant)
├── docs/                           # test plan & approach documentation
│   ├── TEST_PLAN.md
│   ├── TESTING_APPROACH.md
│   ├── ASSUMPTIONS.md
│   └── PART1_FLAKY_ANALYSIS.md
├── config/                         # environment & browser configuration
│   ├── environments.yaml
│   └── browsers.yaml
├── src/                            # framework code
│   ├── pages/                      # Page Object Model
│   ├── api/                        # API client layer
│   └── utils/                      # driver factory, config loader
├── data/                           # test data
│   ├── users.json
│   └── test_data.json
├── tests/                          # automated test scripts
│   ├── ui/                         # Part 1 (flaky fix)
│   ├── api/
│   └── integration/                # Part 3 (API+UI+mobile)
├── reports/                        # test execution reports
└── .github/workflows/ci.yaml       # CI/CD pipeline
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10+
- pip

### Installation
```bash
# 1. Clone the repository
git clone https://github.com/maneyash85/Workflowpro.git
cd Workflowpro

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install
```

### Environment Variables
Create a `.env` file (never commit real secrets):
```bash
APP_BASE_URL=https://app.workflowpro.com
API_URL=https://app.workflowpro.com/api/v1
TEST_PASSWORD=your_test_password
TOKEN_1001=company1_bearer_token
TOKEN_1002=company2_bearer_token
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
CI=false
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run a specific suite
pytest tests/ui/
pytest tests/api/
pytest tests/integration/

# Run by marker
pytest -m smoke
pytest -m regression

# Run in parallel
pytest -n auto

# Generate an HTML report
pytest --html=reports/report.html --self-contained-html

# Generate Allure results
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 📚 Documentation
| Document | Purpose |
|----------|---------|
| [Test Plan](docs/TEST_PLAN.md) | Scope, strategy, risks, entry/exit criteria |
| [Testing Approach](docs/TESTING_APPROACH.md) | Framework thinking & tool choices |
| [Assumptions](docs/ASSUMPTIONS.md) | Assumptions & reasoning for all parts |
| [Flaky Test Analysis](docs/PART1_FLAKY_ANALYSIS.md) | Part 1: root-cause analysis & fixes |

## 🏗️ Framework Highlights
- **Page Object Model** for maintainable UI tests
- **API + UI integration** following the test pyramid
- **Multi-tenant isolation** verified at both UI and API layers
- **Auto-waiting** (Playwright `expect`) — no `sleep()` calls
- **Config-driven** environments, browsers, and devices
- **CI-first**: headless, parallel-safe, artifacts on failure