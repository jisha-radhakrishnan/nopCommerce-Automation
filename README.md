# 🛒 nopCommerce Admin Automation Framework

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-green?logo=selenium)
![Pytest](https://img.shields.io/badge/Tested%20with-Pytest-yellow?logo=pytest)
![Framework](https://img.shields.io/badge/Pattern-Page%20Object%20Model-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

> End-to-end automation testing suite for the **nopCommerce e-commerce admin portal**,
> built with Python, Selenium WebDriver, and Pytest following the Page Object Model design pattern.

🔗 **Live Demo Site:** [admin-demo.nopcommerce.com](https://admin-demo.nopcommerce.com/login?returnUrl=%2Fadmin%2F)

---

## 📋 Table of Contents
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Test Scenarios](#test-scenarios)
- [How to Run](#how-to-run)
- [Reports & Screenshots](#reports--screenshots)
- [Key Skills Demonstrated](#key-skills-demonstrated)

---

## 📌 Overview

This project is a professional automation framework for the **nopCommerce admin portal** — a real-world e-commerce platform. It demonstrates:

- Clean **Page Object Model (POM)** architecture
- **Data-driven testing** using external test data files
- **Automatic screenshots** on test failure
- **HTML test reports** for every test run
- Modular, reusable, and maintainable code structure

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.x** | Core programming language |
| **Selenium WebDriver** | Browser automation |
| **Pytest** | Test framework & execution |
| **Page Object Model** | Design pattern for maintainability |
| **Pytest-HTML** | Test execution reports |
| **Chrome WebDriver** | Browser (configurable) |
| **Git & GitHub** | Version control |

---

## 📁 Project Structure

```
nopCommerce-Automation/
│
├── 📂 pageObjects/          # Page classes (POM)
│   ├── LoginPage.py
│   ├── CustomersPage.py
│   └── ...
│
├── 📂 testCases/            # Pytest test files
│   ├── test_login.py
│   ├── test_customers.py
│   └── ...
│
├── 📂 utilities/            # Reusable helpers
│   ├── readConfig.py
│   └── customLogger.py
│
├── 📂 TestData/             # External test data
├── 📂 Configurations/       # Config & settings
├── 📂 Logs/                 # Execution logs
├── 📂 Screenshots/          # Failure screenshots
├── 📂 Reports/              # HTML test reports
├── 📄 conftest.py           # Pytest fixtures
├── 📄 pytest.ini            # Pytest configuration
└── 📄 requirements.txt      # Dependencies
```

---

## ✅ Test Scenarios Covered

| Module | Test Cases |
|--------|-----------|
| **Login** | Valid login, Invalid credentials, Empty fields |
| **Customer Management** | Search customer, Add customer, Edit customer |
| **Product Management** | Add product, Search product, Edit product |
| **Order Management** | View orders, Filter by status |

---

## ▶️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/jisha-radhakrishnan/nopCommerce-Automation.git
cd nopCommerce-Automation
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run all tests
```bash
pytest testCases/ -v --html=Reports/report.html
```

### 4. Run a specific test
```bash
pytest testCases/test_login.py -v
```

---

## 📊 Reports & Screenshots

- After every test run, an **HTML report** is generated in the `Reports/` folder
- On test **failure**, a screenshot is automatically saved to `Screenshots/`

---

## 💡 Key Skills Demonstrated

- ✅ **Functional Testing** — Login, customer, product, and order workflows
- ✅ **Page Object Model** — Clean separation of page logic and test logic
- ✅ **Data-Driven Testing** — External test data for reusable test cases
- ✅ **Test Reporting** — HTML reports with pass/fail details
- ✅ **Logging** — Detailed execution logs for debugging
- ✅ **Pytest Fixtures** — Reusable browser setup and teardown

---

## 👩‍💻 Author

**Jisha Radhakrishnan**
QA Automation Engineer | Python | Selenium | Pytest

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/jisharadhakrishnan/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/jisha-radhakrishnan)
