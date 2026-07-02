-- models/stg_orders_items.sql

with source_orders_items as (
    -- 🎯 dbt 靈魂語法：動態引入剛剛在 sources.yml 定義的表
    select * from {{ source('ecom_raw', 'raw_orders_items') }}
),

renamed_orders_items as (
    select
        -- 1. 把原本可能亂糟糟或不直覺的欄位名稱改漂亮（乾淨的小寫底線）
        order_id,
        order_item_id,
        product_id,
        
        -- 2. 把字串型態的時間，強制轉換成正確的 timestamp
        cast(price as numeric) as price,
        cast(freight_value as numeric) as freight_value
        
    from source_orders_items
)

select * from renamed_orders_items