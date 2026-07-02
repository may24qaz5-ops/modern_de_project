-- models/marts/dim_products.sql

{{ config(materialized='table')}}

with products as (
    select 
        product_id,
        product_category_name,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm,
        (product_length_cm * product_height_cm * product_width_cm) as product_volume_cm3
    from {{ ref('stg_products') }}
),

translation as (
    -- 這裡直接引入我們剛剛用 Python 灌進去的對照表
    select 
        product_category_name,
        product_category_name_zh
    {# -- from {{ source('public', 'raw_category_translation') }} #}
    -- 💡 注意：如果你還沒在 src.yml 設定 source，可以直接用 text 寫法：
    from public.raw_category_translation
)

select 
    p.product_id,
    -- 🌟 核心邏輯：如果有對到中文就用中文，沒對到（NULL）就保留原始葡萄牙文
    coalesce(t.product_category_name_zh, p.product_category_name) as product_category_name,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm,
    p.product_volume_cm3
from products p
left join translation t on p.product_category_name = t.product_category_name