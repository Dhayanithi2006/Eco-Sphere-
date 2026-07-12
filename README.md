# EcoSphere AI - Enterprise Sustainability Intelligence Platform

EcoSphere AI is an Enterprise Sustainability Intelligence Platform built as a modular suite of Odoo 18 ERP custom addons. It provides standard ESG tracking, enterprise validation workflows (RBAC, audit logs, and approval cycles), and a powerful generative AI decision-support layer.

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
