from prefect import task, flow
import subprocess
import os

# 🟢 動態偵測目前專案的根目錄，不管是 D 槽還是雲端 Ubuntu 都能自動對齊！
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 💡 這樣寫，本機、雲端都能完美找到正確位置
DBT_PROJECT_PATH = os.path.join(BASE_DIR, "dbt_project")
UPLOAD_SCRIPT_PATH = os.path.join(BASE_DIR, "upload.py")

@task(retries=2, retry_delay_seconds=60)
def run_python_ingestion():
    print("🚚 砂石車啟動：開始讀取 Olist CSV 並寫入 PostgreSQL...")
    
    # 使用動態絕對路徑來讀取與執行 upload.py
    with open(UPLOAD_SCRIPT_PATH, "r", encoding="utf-8") as f:
        exec(f.read(), globals())
        
    print("🟢 數據攝取完成！")

@task
def run_dbt_transform():
    print("⚡ dbt 啟動：開始執行資料轉換與繁中翻譯...")
    
    # 💡 保安會乖乖走進 ./dbt_project 底下執行，而且會帶上我們設定好的 profiles 參數
    result = subprocess.run(["dbt", "run", "--profiles-dir", "."], cwd=DBT_PROJECT_PATH)
    
    if result.returncode != 0:
        raise Exception("❌ dbt run 執行失敗！")

@task
def run_dbt_test():
    print("🧪 dbt 測試：開始驗證資料完整性...")
    
    result = subprocess.run(["dbt", "test", "--select", "marts", "--profiles-dir", "."], cwd=DBT_PROJECT_PATH)
    
    if result.returncode != 0:
        raise Exception("❌ dbt test 發現髒資料！")

@flow(name="Olist Data Pipeline")
def olist_data_pipeline_flow():
    run_python_ingestion()
    run_dbt_transform()
    run_dbt_test()

if __name__ == "__main__":
    olist_data_pipeline_flow()