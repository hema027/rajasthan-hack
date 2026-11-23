# Agent Working Guidelines & Governance

This document establishes development conventions, security constraints, ownership boundaries, and operational rules for automated and human agents contributing to CloneTrace.

---

## 1. File & Module Ownership

| Directory / Files | Owning Agent | Editing Rules & Boundaries |
|---|---|---|
| `detect/` | **Detection Agent** | Ingestion, feature extraction, model scoring, heuristics, APK static analysis, and evaluation. |
| `corpus/` | **Data Agent** | Synthetic corpus generator, templates, site manifests, and real feed loaders. |
| `graph/`, `report/`, `app/` | **Graph / Product Agent** | Graph construction, clustering algorithms, visualization, takedown report generation, and Streamlit UI. |
| `contract/`, `config.yaml` | **Shared / Lead** | **Restricted**: May only be modified with an explicit, dated entry in `CHANGELOG.md`. |

---

## 2. Evaluation & Metric Integrity

- **Strict Source of Truth**: All reported metrics (accuracy, precision, recall, F1, ARI) **must** come directly from `detect/eval.py` execution.
- **Never Hardcode Numbers**: Hardcoded benchmark or evaluation figures in documentation or commit messages are strictly prohibited.
- **Data Segregation**: Real observations and synthetic datasets must **always** be segregated and reported separately using the `is_synthetic` column flag.

---

## 3. Operational & Security Guardrails

- **No Live Crawling Outside Containers**: Never fetch live phishing or untrusted URLs outside isolated Docker sandboxes.
- **No Form Interaction**: Never submit data, credentials, OTPs, or test strings into live phishing forms.
- **No Dynamic APK Execution**: Never install or execute APK binaries. Only static analysis and artifact inspection are permitted.
- **Stub Preservation**: Every stub implementation must retain an explicit `# TODO(step N)` marker until fully replaced with production code.

---

## 4. Verification Workflow

- **Pre-Commit Gate**: Always run `make test` (or `pytest -q`) and verify that all test suites pass with zero failures before creating any commit.
