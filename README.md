# 🛡️ SmishGuard PH 🇵🇭

![Deploy ready](https://img.shields.io/badge/Deploy-Ready-success.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)
![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)

**SmishGuard PH** is an open-source, crowdsourced cybersecurity platform designed to combat the rising wave of SMS phishing ("smishing") in the Philippines. 

With scammers constantly bypassing telco filters using spoofed sender IDs and fake cell towers, this project provides a centralized clearinghouse for Filipinos to report malicious text messages targeting mobile wallets (GCash, Maya) and local banks. It instantly parses reports to generate a localized Threat Intelligence API feed that local IT teams, LGUs, and telcos can use to block malicious links in real-time.

---

## ✨ Features

* **Crowdsourced Reporting:** A mobile-first, lightweight web UI for users to easily report scam texts and sender IDs.
* **Localized Context:** Built for the Philippines, featuring automatic Light/Dark mode and bilingual support (English & Filipino/Tagalog).
* **Automated Extraction:** Backend automatically parses messages to extract malicious URLs using regex.
* **Open Threat Feed API:** Provides a real-time endpoint of verified malicious links and numbers.
* **Frictionless Deployment:** Fully Dockerized architecture. Deploy to any Linux server with a single command.

---

## 🏗️ Tech Stack

* **Frontend:** Vue.js 3, Tailwind CSS, Vite, Vue-i18n
* **Backend:** Python, FastAPI, SQLAlchemy
* **Database:** PostgreSQL
* **Infrastructure:** Docker & Docker Compose, Nginx

---

## 💻 Local Development Setup

Want to run SmishGuard PH on your local machine to test it or contribute code? All you need is **Docker Desktop**.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/osintph/SmishGuardPH.git](https://github.com/osintph/SmishGuardPH.git)
   cd SmishGuardPH