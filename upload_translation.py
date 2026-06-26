import pandas as pd
from sqlalchemy import create_engine

# 1. 設定你的 PostgreSQL 連線字串（請替換成你的帳密與 DB Name）
DATABASE_URL = "postgresql://postgres:post1234@localhost:5433/postgres"
engine = create_engine(DATABASE_URL)

# 2. 準備核心葡萄牙文與中文對照資料
data = {
    "product_category_name": [
        "cama_mesa_banho", "beleza_saude", "esporte_lazer", "moveis_decoracao",
        "informatica_acessorios", "utilidades_domesticas", "relogios_presentes",
        "telefonia", "ferramentas_jardim", "automotivo", "brinquedos", "cool_stuff"
    ],
    "product_category_name_zh": [
        "床單沐浴紡織", "美容健康", "運動休閒", "家具裝飾",
        "電腦週邊", "生活家用品", "鐘錶禮品",
        "手機通訊", "園藝工具", "汽車用品", "玩具", "潮物文創"
    ]
}

df = pd.DataFrame(data)

# 3. 寫入 PostgreSQL 作為新的 Raw 表
df.to_sql(
    name="raw_category_translation",
    con=engine,
    schema="public",
    if_exists="replace",
    index=False
)

print("✅ 語言對照原始表 raw_category_translation 寫入成功！")