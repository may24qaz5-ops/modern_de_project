-- models/marts/dim_customers.sql

{{ config(materialized='table')}}

with customers as(
    select * from {{ref('stg_customers')}}
)
select 

-- Surrogate Key / Business Key
        customer_id,
        customer_unique_id,
-- Attribute
        customer_city,
        customer_state
from customers