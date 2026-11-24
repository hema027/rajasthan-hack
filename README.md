# 🛡️ THADAM — The Intelligent Cyber-Fraud Investigation Companion

**Problem Statement:** PS01 · Cyber Fraud / Phishing / Malicious Apps  
**Title:** Scam Message & Phishing Link Detection with Fake Loan / Investment App and Fraudulent Website Analysis  
**Event:** Rajasthan Police Cyber Security Hackathon 2026 (R4C)  
**Team:** DYNAMITE  

---

## 📋 Problem Statement (5 Key Challenges)

1. **Multi-Channel Scam Proliferation:** Citizens are continuously targeted via fraudulent KYC, parcel delivery, electricity-bill, and job-offer messages carrying malicious phishing links across SMS, WhatsApp, and email.
2. **Predatory Fake Loan & Investment Apps:** Malicious Android APKs masquerading as instant-loan or high-return trading platforms misuse sensitive permissions (contacts, SMS, call logs, screen overlays) to extort and defraud victims.
3. **Deceptive Ponzi, MLM & Betting Websites:** Fraudulent web portals lure users with unrealistic guaranteed ROI schemes, fake regulatory badges, and rigged betting interfaces.
4. **Siloed & Fragmented Investigations:** Although scam campaigns routinely reuse identical domains, app signing metadata, phone numbers, and UPI/bank/crypto accounts across channels, individual complaints are analyzed in isolation.
5. **Lack of Explainable, Court-Ready Evidence:** Investigators lack a unified triage tool that produces transparent **Low / Medium / High** risk verdicts alongside structured, actionable dossiers for rapid takedown and bank/UPI freeze requests.

---

## 💡 Our Solution — THADAM (5 Core Pillars)

1. **Unified Multimodal Artifact Intake:** Ingests suspicious SMS/WhatsApp/email text, phishing URLs, fraudulent websites, Android APKs, and screenshots/QR codes inside a single investigator console.
2. **Dialect-Aware Multilingual Scam NLP:** Detects social-engineering urgency lures, fake KYC/bill traps, and brand impersonation across English, Hindi, and 6 regional Rajasthani dialects (*Marwari, Mewari, Dhundhari, Hadoti, Mewati, Bagri*).
3. **Safe Static-Only APK & Website Forensics:** Decompiles `AndroidManifest.xml` permissions and `.dex` bytecode strings while inspecting website DOM/payment trails in isolation—eliminating live malware execution risks.
4. **Automated Identifier Extraction & Syndicate Correlation:** Automatically extracts UPI VPAs, `+91` phone numbers, look-alike domains, crypto wallets, and SHA-256 hashes, linking separate complaints that share infrastructure into unified syndicate campaigns.
5. **Explainable Risk Scoring & One-Click Police Dossiers:** Computes transparent **Low / Medium / High** risk tiers backed by human-readable trigger reasons and exports investigation-ready PDF and Markdown evidence reports.

---

## 🌟 Novelty & Unique Selling Propositions (5 USPs)

1. **Rajasthani Dialect & Code-Mixed Scam Intelligence:** Unlike generic English-only phishing filters, THADAM natively understands regional Rajasthani dialects and Hinglish coercion patterns used in localized rural and urban cyber frauds.
2. **Cross-Channel Syndicate Graph Attribution:** Connects seemingly unrelated SMS lures, fake websites, and sideloaded APKs through shared payment trails (UPI/bank/crypto) and infrastructure pivots to expose the master syndicate behind multiple cases.
3. **Zero-Execution Static Binary & Web Forensics:** Extracts embedded Command-and-Control (C2) endpoints, dangerous permission combinations, and payment handles statically in seconds without requiring heavy dynamic sandboxes.
4. **Glass-Box Explainable Forensics for Law Enforcement:** Every risk score is paired with exact indicator provenance, feature weights, and rule justifications so investigators can defend findings in legal and banking freeze proceedings.
5. **Instant Actionable Takedown & Freeze Readiness:** Bridges the gap between detection and enforcement by auto-formatting extracted indicators into ready-to-dispatch PDF/Markdown dossiers and live threat heat-lists.

---

## 🏗️ System Architecture

<img width="1408" height="768" alt="Gemini_Generated_Image_oqpwywoqpwywoqpw" src="https://github.com/user-attachments/assets/580eb930-e362-491d-af77-ba4b97386f09" />
