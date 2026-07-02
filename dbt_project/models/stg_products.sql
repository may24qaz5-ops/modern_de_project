-- models/stg_products.sql

with source_products as (
    -- 🎯 dbt 靈魂語法：動態引入剛剛在 sources.yml 定義的表
    select * from {{ source('ecom_raw', 'raw_products') }}
),

renamed_products as (
    select

        product_id,
        product_category_name,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm

        
    from source_products
)

select * from renamed_products