# RAKSHA-HACK // Unified Cyber Fraud & Scam Attribution Console
**Rajasthan Police Cyber Security Hackathon 2026 (R4C — Problem Statement PS01)**  
*Cyber Fraud / Phishing / Malicious Apps: Scam Message & Phishing Link Detection with Fake Loan / Investment App and Fraudulent Website Analysis*

---

## Overview
**RAKSHA-HACK** is a law-enforcement-grade cyber-intelligence and digital forensics platform built for the **Rajasthan Cyber Crime Control Centre (R4C)**. Fraud syndicates routinely reuse the same UPI VPAs, phone numbers, domains, and C2 endpoints across SMS/WhatsApp lures, fake loan/investment Android APKs, and fraudulent Ponzi or betting websites—yet victims report these channels in isolation.

**RAKSHA-HACK** unifies multi-channel ingestion, explainable risk scoring (**High / Medium / Low Risk**), cross-channel syndicate attribution, and automated police takedown dossier generation into a single investigation console.

---

## Core Capabilities (PS01 Alignment)

### 1. Multi-Channel Intake & Static Scanner
* **SMS, WhatsApp, Email & URL Analyzer:** Detects urgency lures, fake KYC/electricity/parcel warnings, brand impersonation (PhonePe, Paytm, GPay, BHIM, SBI, HDFC), risky TLDs, and look-alike domains.
* **Fraudulent Website / Ponzi & Betting Scanner:** Flags guaranteed-ROI claims, MLM referral schemes, betting lures, and extracts UPI IDs (`@upi`, `@okicici`), phone numbers, domains, and cryptocurrency collection wallets (ERC-20, TRC-20, BTC).
* **Android APK Static Inspector:** Safely unpacks `.apk` packages without executing malware, computes SHA-256 hashes, flags data-harvesting permissions (`READ_SMS`, `RECEIVE_SMS`, `SEND_SMS`, `READ_CONTACTS`, `CAMERA`, `SYSTEM_ALERT_WINDOW`), and extracts embedded C2/payment URLs from `AndroidManifest.xml` and `.dex` bytecode.

### 2. Explainable Risk Assessment & Case History
* Assigns clear **HIGH RISK**, **MEDIUM RISK**, and **LOW RISK** classifications with transparent heuristic signal weights explaining *why* an artifact was flagged.
* Searchable investigation queue with filtering by risk tier, impersonated brand, and evidence channel (`sms`, `web`, `apk`), plus side-by-side suspect vs. official brand visual comparison.

### 3. Cross-Channel Campaign & Syndicate Attribution
* Automatically correlates separate cases sharing common UPI VPAs, mobile numbers, domains, or crypto wallets into linked syndicate clusters.
* Interactive network attribution graph visualizing shared infrastructure across messages, apps, and websites.

### 4. R4C Police Investigation & Takedown Dossiers
* One-click generation of structured **PDF** and **Markdown** evidence dossiers containing campaign timelines, linked cases, shared financial/telecom anchors, and actionable Section 91 CrPC / BNSS freeze/takedown recommendations.

### 5. Trending Threat Heat-List
* Real-time leaderboard of the most frequently reported scam domains, phone numbers, UPI payment handles, and impersonated institutions.

---

## Project Architecture

```text
rajasthan-hack/
├── app/
│   ├── streamlit_app.py       # Main RAKSHA-HACK 5-view Cyber-SOC web console
│   └── theme.py               # Law-enforcement dark UI palette & indicator styling
├── detect/
│   └── ingest.py              # Artifact normalization & SQLite ingestion pipeline
├── graph/
│   └── build.py               # Interactive PyVis bipartite syndicate attribution graph
├── report/
│   └── takedown.py            # Automated PDF & Markdown law-enforcement dossier builder
├── db.py                      # SQLite schema & connection manager (observations, verdicts, indicators, campaigns)
├── config.yaml                # Monitored financial/UPI brands & detection configuration
└── requirements.txt           # Python dependencies
