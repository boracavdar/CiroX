# CiroX: Local ERP & Decision Support System

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
</p>

## 🚀 Project Overview
**CiroX** is a custom, end-to-end local Enterprise Resource Planning (ERP) and Point of Sale (POS) architecture engineered to digitalize the commercial operations of a local business (Coşkun Fish Restaurant). 

Designed with an Industrial Engineering perspective, the system moves beyond traditional cash registers by integrating a **Decision Support System (DSS)** that utilizes statistical analysis to optimize demand forecasting and minimize operational bottlenecks.

> ⚠️ **Note:** Due to data privacy and security protocols regarding the business's actual financial records, this repository contains the **Front-End/Analytical Interface architecture** configured to run with mock/simulated data. The core financial backend operates exclusively on local on-premise servers.

## ⚙️ Core Architecture & Features
- **Data Security First:** Core financial records (daily sales, cash flow reconciliation) are stored locally in an `SQLite` database. Only the necessary analytical aggregates are deployed to the cloud via Git version control.
- **AI-Assisted Architecture:** Generative AI tools were utilized as a development co-pilot to accelerate data modeling, backend logic design, and robust database structuring.
- **Interactive Dashboard:** Built with `Streamlit` to visualize historical cash flows, track credit card pool distributions, and estimate expected daily revenue based on moving weekday averages.
- **Error Mitigation:** Automated daily cash flow reconciliation significantly reduces manual calculation errors during peak service hours.

## 🛠️ Technical Stack
- **Backend/Logic:** Python
- **Database:** SQLite (Upgraded from legacy JSON architecture)
- **Web Framework (Dashboard):** Streamlit
- **API Routing (Local):** Flask

## 📊 Analytics Module (The DSS)
The analytics module of CiroX is designed to assist management in data-driven decision-making. By analyzing past operational days, the DSS module can:
1. Identify high-traffic hours to optimize staff scheduling.
2. Forecast inventory depletion rates based on predictive models.
3. Provide a clear visual breakdown of profitability margins per product category.

---
*Developed by **Yusuf Bora Çavdar** as part of a real-world digital transformation initiative.*
