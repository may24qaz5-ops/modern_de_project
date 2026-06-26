from prefect import task, flow
import subprocess
import os

# 💡 請在這裡設定你的實體路徑
DBT_PROJECT_PATH = r"D:\dbt-project\dbt_project"
UPLOAD_SCRIPT_PATH = r"D:\modern_de_project\upload.py" # 假設 upload.py 在這裡，請依據實際狀況修改

@task(retries=2, retry_delay_seconds=60)
def run_python_ingestion():
    print("🚚 砂石車啟動：開始讀取 Olist CSV 並寫入 PostgreSQL...")
    
    # 使用絕對路徑來讀取與執行 upload.py，確保不管在哪跑都抓得到
    with open(UPLOAD_SCRIPT_PATH, "r", encoding="utf-8") as f:
        exec(f.read(), globals())
        
    print("🟢 數據攝取完成！")

@task
def run_dbt_transform():
    print("⚡ dbt 啟動：開始執行資料轉換與繁中翻譯...")
    
    # 💡 關鍵：使用 subprocess 並指定 cwd (Current Working Directory)
    # 這樣就等於叫作業系統「先切換到 dbt 目錄，再執行 dbt run」
    result = subprocess.run(["dbt", "run"], cwd=DBT_PROJECT_PATH)
    
    if result.returncode != 0:
        raise Exception("❌ dbt run 執行失敗！")

@task
def run_dbt_test():
    print("🧪 dbt 測試：開始驗證資料完整性...")
    
    # 同理，去 dbt 的目錄下執行 dbt test
    result = subprocess.run(["dbt", "test", "--select", "marts"], cwd=DBT_PROJECT_PATH)
    
    if result.returncode != 0:
        raise Exception("❌ dbt test 發現髒資料！")

@flow(name="Olist Data Pipeline")
def olist_data_pipeline_flow():
    run_python_ingestion()
    run_dbt_transform()
    run_dbt_test()

if __name__ == "__main__":
    olist_data_pipeline_flow()