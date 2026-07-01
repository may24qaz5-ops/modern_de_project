# 🛒 Olist 現代數據中台實作專案 (Modern Data Platform)

本專案以 Olist 電商數據集為基礎，端到端 (End-to-End) 打造具備企業級自動化調度與現代化資料轉換架構的數據中台。

## 🏗️ 系統架構
1. **資料吞吐 (Ingestion)**：使用 Python 進行高效能 Batch 寫入至 PostgreSQL 落地。
2. **資料轉換 (Transformation)**：導入 **dbt (Data Build Tool)** 進行模組化、版本控制的資料清洗、維度建模與繁中化轉換。
3. **自動化調度 (Orchestration)**：整合 **Prefect** 建立資料管道監控、重試機制與端到端排程。
4. **自動化防禦 (DataOps CI)**：設定 **GitHub Actions**，在程式碼合併前自動執行 `dbt compile` 語法與關聯性安檢。
5. **資料視覺化 (BI)**：串接 **Power BI** 打造營運決策看板。

## ⚡ 專案核心技術亮點
- **Monorepo 專案管理**：將 Python Ingestion 腳本、Prefect 排程與 dbt 轉型專案整合於單一儲存庫，符合現代 DataOps 的基礎建設開發規範。
- **企業級自動化語法防護**：內建 CI/CD Pipeline，於 GitHub Background 自動執行 `dbt compile` 驗證與 Schema 檢查，大幅減少人為粗心導致的生產環境中斷。
- *   **維度建模實務 (Dimensional Modeling)**：擺脫傳統大寬表思維，於 dbt 內部實作經典的星狀模型 (Star Schema)，嚴格定義 Dimensions 與 Fact Tables，優化下游 BI 的查詢效能。

## 📁 專案目錄結構 (Project Structure)

```text
├── .github/workflows/                 # DataOps CI (GitHub Actions 定義)
├── olist_customers_dataset.csv        # Olist 原始數據集 (示例)
├── olist_order_items_dataset.csv      
├── olist_orders_dataset.csv           
├── olist_products_dataset.csv         
├── upload.py                          # 核心 Ingestion 腳本 (將 CSV 寫入 PostgreSQL)
├── orchestrate_pipeline.py            # Prefect 自動化工作流與排程調度腳本
├── upload_translation.py              # 繁中化與資料轉換處理
├── make_ppt.py                        # 專案簡報自動化產出腳本
├── README.md                          # 專案說明文件
└── modern_de_project_presentation...  # 專案簡報與架構說明
