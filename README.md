# EcoSphere AI - Enterprise Sustainability & ESG Intelligence Platform

EcoSphere AI is an advanced, enterprise-grade Sustainability & ESG Intelligence Platform built as a modular suite of Odoo 18 ERP custom addons. It integrates real-time carbon tracking, corporate social responsibility management, compliance audit trails, gamified employee initiatives, and a context-aware Generative AI decision-support advisor.

The platform provides standard ESG metric aggregations, strict Role-Based Access Control (RBAC) permission matrices, dynamic approval and verification cycles, and an interactive simulation dashboard.

---

## Core Features

- **🌱 Carbon Ledger (Environmental)**: Granular tracking of Scope 1, Scope 2, and Scope 3 greenhouse gas emissions, calculated in real-time from transactional logs using versioned conversion factors.
- **👥 CSR & Volunteering (Social)**: Employee volunteer logs, diversity index scorecards, and management of corporate social responsibility activities with validation workflows.
- **📄 Policies & Compliance (Governance)**: Compliance registers, risk matrices, policy acknowledgments tracker, and external audits scheduler.
- **🎯 Gamification & Badges**: Sustainability challenge campaigns, points ledger, redeemable rewards catalog, and leaderboards to drive employee engagement.
- **💡 AI Strategic Advisor**: Generative AI decision intelligence bot reading calculated database statistics to recommend context-aware mitigations.
- **📊 Interactive Simulator Dashboard**: Live preview dashboard with a dynamic SVG gauge needle, Odoo REST API simulations, and role-based interface visibility controls.

---

## Repository Structure

All custom Odoo modules are stored under the `addons/` directory:

* **`addons/ecosphere_base`**: Core configuration settings, company and department extensions, and role-based permissions (RBAC).
* **`addons/ecosphere_environmental`**: Versioned emission factors, carbon ledger, and calculation engine.
* **`addons/ecosphere_governance`**: Compliance policies, audits, compliance issues, and risk registers.
* **`addons/ecosphere_social`**: CSR activities, employee volunteer participation, diversity reports, and training registers.
* **`addons/ecosphere_gamification`**: Point ledgers, rewards catalog, and leaderboard campaigns.
* **`addons/ecosphere_insights`**: Engine that pre-calculates carbon hotspots and departmental trend analysis.
* **`addons/ecosphere_reports`**: Layout outputs (PDF/Excel) for reporting.
* **`addons/ecosphere_dashboard`**: Unified visualization with a central KPI engine.
* **`addons/ecosphere_notifications`**: Standardized notifications and email template schedulers.
* **`addons/ecosphere_ai`**: LLM integrations, advisory supervisor, explainability, feedback, and scenario simulator.

---

## Dependency Graph

```
           [ecosphere_base]
             │         │
      ┌──────┘         └──────┐
      ▼                       ▼
[ecosphere_environmental] [ecosphere_governance]
      │                       │
      ▼                       ▼
[ecosphere_social]       [ecosphere_gamification]
      │                       │
      └──────┬────────────────┘
             ▼
      [ecosphere_insights]
             │
             ▼
      [ecosphere_reports]
             │
             ▼
      [ecosphere_dashboard]
             │
             ▼
      [ecosphere_notifications]
             │
             ▼
      [ecosphere_ai]
```

---

## Development Prerequisites

* **Odoo Version**: Odoo 18.0 (Community or Enterprise)
* **Python**: Python 3.10+ (tested with Python 3.13.1)
* **Database**: PostgreSQL 13+

---

## Installation & Setup

1. Copy the addons directory to your Odoo custom addons directory:
   ```bash
   cp -r addons/* /path/to/odoo/custom/addons/
   ```
2. Add your custom addons path to your Odoo configuration file (`odoo.conf`):
   ```ini
   addons_path = /path/to/odoo/addons, /path/to/odoo/custom/addons
   ```
3. Restart the Odoo server:
   ```bash
   python odoo-bin -c odoo.conf
   ```
4. Log into Odoo, enable **Developer Mode**, navigate to the **Apps** menu, click **Update Apps List**, and search for `EcoSphere Base` to install.

---

## Running the Project

### 1. Interactive Web Preview (Local Simulation)
The repository includes a lightweight Python HTTP server that runs the frontend dashboard interface and mock Odoo REST API endpoints.

To start the interactive simulation:
```bash
python web_preview/server.py
```
Once running, open your web browser and go to:
👉 **http://localhost:8000**

---

### 2. Running Odoo ERP Unit Tests
To execute backend unit tests for the EcoSphere modules inside an active Odoo environment:
```bash
python odoo-bin -c odoo.conf -d <your_database> -i ecosphere_base,ecosphere_environmental,ecosphere_governance,ecosphere_social,ecosphere_gamification,ecosphere_reports,ecosphere_notifications,ecosphere_ai --test-enable
```
