-- models/stg_customers.sql

with source_customers as (
    -- 🎯 dbt 靈魂語法：動態引入剛剛在 sources.yml 定義的表
    select * from {{ source('ecom_raw', 'raw_customers') }}
),

renamed_customers as (
    select

        customer_id,
        customer_unique_id,
        customer_city,
        customer_state
        
    from source_customers
)

select * from renamed_customers