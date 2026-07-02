-- models/stg_orders.sql

with source_orders as (
    -- 🎯 dbt 靈魂語法：動態引入剛剛在 sources.yml 定義的表
    select * from {{ source('ecom_raw', 'raw_orders') }}
),

renamed_orders as (
    select
        -- 1. 把原本可能亂糟糟或不直覺的欄位名稱改漂亮（乾淨的小寫底線）
        order_id,
        customer_id,
        order_status,
        
        -- 2. 把字串型態的時間，強制轉換成正確的 timestamp
        cast(order_purchase_timestamp as timestamp) as purchase_at,
        cast(order_approved_at as timestamp) as approved_at
        
    from source_orders
)

select * from renamed_orders