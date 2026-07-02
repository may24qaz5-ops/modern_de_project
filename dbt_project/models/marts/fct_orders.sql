-- models/marts/fct_orders.sql

{{ config(materialized='table')}}

with orders as (
    select 
        order_id, 
        customer_id, 
        order_status, 
        purchase_at
    from {{ref('stg_orders')}}
),
order_items as(
    select 
        order_id, 
        product_id, 
        price, 
        freight_value
    from {{ref('stg_orders_items')}}
)
-- 徹底拿掉 customers 的 CTE，因為事實表不需要關聯維度屬性！

select 
    o.order_id,
    o.customer_id,        -- 作為連接 dim_customers 的外鍵 (FK)
    o.order_status,
    o.purchase_at,
    i.product_id,         -- 作為連接 dim_products 的外鍵 (FK)
    i.price,
    i.freight_value,
    (i.price + i.freight_value) as total_order_amount
from orders o
inner join order_items i on o.order_id = i.order_id