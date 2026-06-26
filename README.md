# 🛒 Olist 現代數據中台實作專案 (Modern Data Platform)

本專案以 Olist 電商數據集為基礎，端到端 (End-to-End) 打造具備企業級自動化調度與現代化資料轉換架構的數據中台。

## 🏗️ 系統架構
1. **資料吞吐 (Ingestion)**：使用 Python 進行高效能 Batch 寫入至 PostgreSQL 落地。
2. **資料轉換 (Transformation)**：導入 **dbt (Data Build Tool)** 進行模組化、版本控制的資料清洗、維度建模與繁中化轉換。
3. **自動化調度 (Orchestration)**：整合 **Prefect** 建立資料管道監控、重試機制與端到端排程。
4. **自動化防禦 (DataOps CI)**：設定 **GitHub Actions**，在程式碼合併前自動執行 `dbt compile` 語法與關聯性安檢。
5. **資料視覺化 (BI)**：串接 **Power BI** 打造營運決策看板。

## ⚡ 專案核心技術亮點
- **Monorepo 專案管理**：將 Python 調度腳本與 dbt 專案整合管理，符合現代 DataOps 開發規範。
- **自動化語法防護**：內建 CI/CD Pipeline，大幅減少人為粗心導致的生產環境錯誤。
