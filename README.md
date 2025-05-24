# HavenTest: API Testing Framework for Style Haven

HavenTest is a modular, scalable, and maintainable API testing framework designed for the "Style Haven" fashion e-commerce platform. Built on top of pytest, it provides:

- Structured, functional test grouping (user, product, cart, checkout, seller, support)
- Data-driven testing with JSON-managed test data
- Detailed assertion reporting for fast debugging
- Easy configuration and environment management
- HTML reporting for clear test results
- CI/CD integration with GitHub Actions

HavenTest empowers QA teams to validate RESTful APIs efficiently, ensuring robust, secure, and high-quality releases for Style Haven and similar modern web platforms.

---

# PyTestify API Test Framework

## Features
- **pytest** for test execution
- **pytest-html** for HTML reporting
- **requests** for HTTP calls
- Modular test structure by feature
- Test data managed via JSON
- ID_TOKEN injected via environment variable
- Automated CI with GitHub Actions

## Usage

1. **Create a virtual environment (recommended)**

   Using [uv](https://github.com/astral-sh/uv):
   ```powershell
   uv venv .venv
   .venv\Scripts\Activate.ps1   # Windows PowerShell
   # Or, for Ubuntu on Windows (WSL):
   source .venv/bin/activate
   ```

2. **Install dependencies**

   Using uv (recommended for speed and reliability):
   ```powershell
   uv pip install -r requirements.txt
   ```
   
   Or, using pip:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Set environment variable**
   ```powershell
   $env:ID_TOKEN="your_token_here"   # Windows PowerShell
   export ID_TOKEN=your_token_here    # Ubuntu on Windows (WSL)
   ```

4. **Run tests**
   ```powershell
   pytest
   ```

5. **View HTML report**
   Open `report.html` after test run.

## Project Structure

```
PyTestify/
│
├── README.md
├── requirements.txt
├── pytest.ini
├── .github/
│   └── workflows/
│       └── api-tests.yml
├── conftest.py
├── testdata/
│   ├── badge.json
│   ├── user.json
│   └── product.json
├── tests/
│   ├── badge/
│   │   └── test_badge_api.py
│   ├── user/
│   │   └── test_user_api.py
│   └── product/
│       └── test_product_api.py
└── utils/
    ├── api_client.py
    └── data_loader.py
```

## CI/CD

Tests run automatically on push/PR via GitHub Actions. The ID_TOKEN is securely injected using GitHub Secrets.

## Extending

- Add new test modules under `tests/<feature>/`
- Add test data in `testdata/`
- Extend `APIClient` for more HTTP methods as needed
