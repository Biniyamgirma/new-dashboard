import pandas as pd
from db_connection import create_db_engine

# >= CURDATE() - INTERVAL 1 MONTH
# date(orders.placed_at) order_Date,


engine = create_db_engine()

def fetch_data_not_working_hour():
    """
    Fetch data for orders Not worrking hour.
    """
    query = """
   select 
        CAST(orders.id AS CHAR) AS order_id,
        date(orders.placed_at) order_Date,
        orders.placed_at order_Time,
        restaurants.name restaurant_name,
        orders.order_amount,
        restaurants.address restaurants_address,
        concat(delivery_men.f_name,"-",delivery_men.l_name) delivery_men,
        orders.responsible_person responsible_person_Id,
        concat(admins.f_name,"-",admins.l_name) responsible_person,
        json_extract(delivery_address, '$.address') Delivery_address,
        orders.order_status,
        concat(a1.f_name," ",a1.l_name) cancelled_by,
        orders.cancelation_reason cancellation,
        cancellation_reasons.message cancellation_reason,
        orders.cancelation_note cancellation_note


    From orders
        left join delivery_men 
        on delivery_men.id = orders.delivery_man_id
        join restaurants 
        on restaurants.id = orders.restaurant_id
        join cancellation_reasons 
        on cancellation_reasons.id = orders.cancelation_reason
        join admins
        on admins.id = orders.responsible_person
        join admins as a1
        on a1.id = orders.canceled_by


    where orders.placed_at >= CURDATE() - INTERVAL 1 MONTH
        and orders.cancelation_reason like "R15" -- Not Working Hour
        and orders.restaurant_id not in (1329 , 999);
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_driver_not_available_a():
    """
    Fetch data for Driver not available after .
    """
    query = """
    select 
        CAST(orders.id AS CHAR) AS order_id,
        date(orders.placed_at) order_Date,
        orders.placed_at order_time,
        restaurants.name restaurant_name,
        restaurants.id,
        orders.order_amount,
        orders.delivery_charge,
        restaurants.address restaurants_address,
        concat(delivery_men.f_name,"-",delivery_men.l_name) delivery_men,
        delivery_men.area,
        concat(admins.f_name,"-",admins.l_name) responsible_person,
        (json_extract(delivery_address, '$.address')) Delivery_address,
        orders.order_status,
        concat(a1.f_name," ",a1.l_name) cancelled_by,
        orders.cancelation_reason,
        cancellation_reasons.message cancelationReason,
        orders.cancelation_note cancellation_note
        ,orders.original_delivery_charge,
        orders.log_details ->> '$.delivery_charges.distance' distance,
        cs.name


    From orders
        left join delivery_men on delivery_men.id = orders.delivery_man_id
        join restaurants on restaurants.id = orders.restaurant_id
        join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        join order_details on order_details.order_id = orders.id
        join food on food.id = order_details.food_id
        join categories cs on cs.id = food.category_id
        join admins on admins.id = orders.responsible_person
        join admins as a1
        on a1.id = orders.canceled_by


    where 
        orders.placed_at >= CURDATE() - INTERVAL 1 MONTH

        and orders.cancelation_reason like "R42" 
        and orders.order_status = 'canceled';

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_driver_not_available_b():
    """
    Fetch data for Driver not available before .
    """
    query = """
    select 
        CAST(orders.id AS CHAR) AS order_id,
        date(orders.placed_at) order_Date,
        orders.placed_at order_time,
        restaurants.name restaurant_name,
        restaurants.id,
        orders.order_amount,
        orders.delivery_charge,
        restaurants.address restaurants_address,
        concat(delivery_men.f_name,"-",delivery_men.l_name) delivery_men,
        delivery_men.area,
        concat(admins.f_name,"-",admins.l_name) responsible_person,
        (json_extract(delivery_address, '$.address')) Delivery_address,
        orders.order_status,
        concat(a1.f_name," ",a1.l_name) cancelled_by,
        orders.cancelation_reason,
        cancellation_reasons.message cancelationReason,
        orders.cancelation_note cancellation_note
        ,orders.original_delivery_charge,
        orders.log_details ->> '$.delivery_charges.distance' distance,
        cs.name


    From orders
        left join delivery_men on delivery_men.id = orders.delivery_man_id
        join restaurants on restaurants.id = orders.restaurant_id
        join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        join order_details on order_details.order_id = orders.id
        join food on food.id = order_details.food_id
        join categories cs on cs.id = food.category_id
        join admins on admins.id = orders.responsible_person
        join admins as a1
        on a1.id = orders.canceled_by


    where 
        orders.placed_at >= CURDATE() - INTERVAL 1 MONTH

        and orders.cancelation_reason like "R25" 
        and orders.order_status = 'canceled';

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_cancellation_count():
    """
    Fetch data for All Cancellation Count
    """
    query = """
   select 
        date(orders.created_at) order_Date,
        orders.cancelation_reason cancelation_reason_code,
        cancellation_reasons.message cancelation_reason,
        count(if(orders.order_status = 'canceled',orders.id,null)) Canceled_orders

    From orders
        join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason


    where 
        orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        and orders.restaurant_id not in (1329 , 999)
        group by order_Date, cancelation_reason
        order by 4 desc;

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_incomplete_orders():
    """
    Fetch data for Incomplete Orders
    """
    query = """
    select 
        CAST(orders.id AS CHAR) AS order_id,
        date(orders.placed_at) order_Date,
        orders.placed_at order_time,
        restaurants.name restaurant_name,
        restaurant_fee_details.restaurant_fee Restaurant_fee,
        orders.order_amount orderAmount,
        orders.delivery_charge deliveryCharge,
        json_unquote(
                JSON_Extract(
                    orders.log_details,
                    "$.service_charges.restaurant_service_charge_amount"
                )
                )as  serviceCharge,
        restaurants.address restaurants_address,
        concat(delivery_men.f_name,"-",delivery_men.l_name) delivery_men,
        delivery_men.phone,
        users.f_name,
        users.phone Customer_phone,
        concat(admins.f_name,"-",admins.l_name) responsible_person,
        (json_extract(delivery_address, '$.address')) Delivery_address,
        orders.order_status,
        concat(a1.f_name," ",a1.l_name) cancelled_by,
        orders.cancelation_reason,
        cancellation_reasons.message cancellation_message,
        orders.cancelation_note Cancel_Note

    From 
        orders
        left join restaurant_fee_details on restaurant_fee_details.order_id = orders.id
        left join delivery_men 
        on delivery_men.id = orders.delivery_man_id
        join restaurants 
        on restaurants.id = orders.restaurant_id
        join cancellation_reasons 
        on cancellation_reasons.id = orders.cancelation_reason
        join admins
        on admins.id = orders.responsible_person
        join admins as a1
        on a1.id = orders.canceled_by
        join users
        on users.id = orders.user_id
        
    where
        orders.placed_at >= CURDATE() - INTERVAL 1 MONTH
        and orders.restaurant_id not in (1329 , 999)
        and orders.order_status = 'canceled'
        and cancellation_reasons.id in ('I01', 'I02', 'I03', 'I04', 'I05', 'I06', 'I07', 'I08', 'I09','I10','I11','I12','I13','I14','I15','I16','I17','I18','I19','I20','I21','I22','I23','I24', 'R41', 'R42', 'R28')


    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_more_than_60_min():
    """
    Fetch data for More than 60 Min orders
    """
    query = """
    select
        date(orders.created_at) order_Date,
        CAST(orders.id AS CHAR) AS "order ID",
        orders.delivery_charge,
        concat(delivery_men.f_name, "-" , delivery_men.l_name) Driver_Name,
        concat(admins.f_name," ",admins.l_name) Dispatcher_Name,
        restaurants.name Rest_Name,
        restaurants.address,
        json_unquote(
            JSON_Extract(orders.delivery_address, "$.address")
        ) as Delivery_address,
        count(if( timestampdiff(second, orders.created_at, orders.delivered)/60 >= 59 , orders.id , null )) Morethan_60,
        round(timestampdiff(second,orders.created_at , orders.delivered)/60 , 2) created_delivered_Min,
        round(timestampdiff(second,orders.accepted , orders.delivered)/60,2) accepted_delivered_min,
        case
        when (timestampdiff(second,orders.accepted,orders.delivered) / 60 > 45 and orders.picked_up is not null) then 'late driver'
            when (timestampdiff(second,orders.handover,orders.accepted) / 60 > 35 and orders.picked_up is not null) then 'late assignment'
            when (timestampdiff(second,orders.created_at,orders.handover) / 60 > 5 and orders.picked_up is not null) then 'late crm'
            when orders.picked_up is null then 'drivers ontime fixed'
        when ((timestampdiff(second,orders.handover,orders.accepted) / 60 < 0 or timestampdiff(second,orders.accepted,orders.delivered) / 60 < 0
                    or timestampdiff(second,orders.created_at,orders.handover) / 60 < 0) and orders.picked_up is not null) then 'Negative'    
            else 'other'
            end as late_reason

    from orders
        join restaurants on orders.restaurant_id = restaurants.id
        left join delivery_men on orders.delivery_man_id = delivery_men.id
        left join admins on orders.dispatcher_id = admins.id

    where orders.order_status = "delivered" 
        and  orders.delivery_charge < 150
        and orders.restaurant_id not in ( '999' , '1329' , '317', '1202' , '39' ,'315' , '316' , '319',1535,1585,1586,1587,1588,1589,1590,46,387,1221,348,1202,1729,1617)
        and date(orders.created_at)  >= CURDATE() - INTERVAL 1 MONTH
        and timestampdiff(second,orders.created_at , orders.delivered)/ 60 >= 59


        group by order_Date,orders.id  
        order by 7 desc;

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_more_than_150():
    """
    Fetch data for More than 150 orders
    """
    query = """
    select
        date(orders.created_at) order_Date,
        CAST(orders.id AS CHAR) AS orderId,
        concat(admins.f_name," ",admins.l_name) Dispatcher_Name,
        concat(delivery_men.f_name," ",delivery_men.l_name) DeliveryMan,
        restaurants.name RestaurantName,
        restaurants.address RestaurantAddress,
        json_unquote(
            JSON_Extract(orders.delivery_address, "$.address")
        ) as Delivery_address,
        orders.delivery_charge DeliveryCharge,
        orders.placed_at OrderCreationHour,
        orders.delivered OrderDeliveryHour
                
    from orders
        left join admins on admins.id = orders.dispatcher_id
        left join delivery_men on delivery_men.id = orders.delivery_man_id
        join restaurants on restaurants.id = orders.restaurant_id
    where orders.order_status = 'delivered' 
        and orders.created_at  >= CURDATE() - INTERVAL 1 MONTH 
        and orders.delivery_charge >= 150 and time(orders.created_at) < "20:00:00" -- Morethan_150 
        and orders.restaurant_id not in (1329 , 999);
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_on_time():
    """
    Fetch data for on time 
    """
    query = """
    select
        date(orders.created_at) order_Date,
        delivery_men.id DeliveryManId,
        delivery_men.area District,
        concat(delivery_men.f_name," ",delivery_men.l_name) DeliveryMan,
        count(orders.id) DeliveredCount,
        count(if(orders.restaurant_id not in ( '999' , '1329' , '317', '1202' , '39' ,'315' , '316' , '319','1477','1221','1509','1536','1527',1585,1586,1587,1588,1589,1590,46,387,1221,348,1202,1729,1617),orders.id,null)) orders_without_ontimeRestaurants,
        count(if(orders.accepted is not null and orders.delivered is not null 
            and orders.order_status = 'delivered' and timestampdiff(second, orders.accepted, orders.delivered) / 60 <= 45
            and orders.restaurant_id not in ( '999' , '1329' , '317', '1202' , '39' ,'315' , '316' , '319','1477','1221','1509','1536','1527',1585,1586,1587,1588,1589,1590,46,387,1221,348,1202,1729,1617), 
                orders.id,null)) OnTime45,
        round(count(if(orders.accepted is not null and orders.delivered is not null 
                and orders.order_status = 'delivered' and timestampdiff(second, orders.accepted, orders.delivered) / 60 <= 45
            and orders.restaurant_id not in ( '999' , '1329' , '317', '1202' , '39' ,'315' , '316' , '319','1477','1221','1509','1536','1527',1585,1586,1587,1588,1589,1590,46,387,1221,348,1202,1729,1617),
                orders.id,null)) / count(if(orders.restaurant_id not in (1329,999,1585,1586,1587,1588,1589,1590),orders.id,null)) * 100, 2) "<=45(%)", 
                    
        count(if(orders.placed_at is not null and orders.delivered is not null 
                and orders.order_status = 'delivered' and timestampdiff(second, orders.placed_at, orders.delivered) / 60 >= 59
            and orders.restaurant_id not in ( '999' , '1329' , '317', '1202' , '39' ,'315' , '316' , '319','1477','1221','1509','1536','1527',1585,1586,1587,1588,1589,1590,46,387,1221,348,1202,1729,1617),
                orders.id,null)) as ">=59",
        round(count(if(orders.placed_at is not null and orders.delivered is not null 
                    and orders.order_status = 'delivered' and timestampdiff(second, orders.placed_at, orders.delivered) / 60 >= 59
            and orders.restaurant_id not in ( '999' , '1329' , '317', '1202' , '39' ,'315' , '316' , '319','1477','1221','1509','1536','1527',1585,1586,1587,1588,1589,1590,46,387,1221,348,1202,1729,1617),
                    orders.id,null)) / count(if(orders.restaurant_id not in (1329,999,1585,1586,1587,1588,1589,1590),orders.id,null)) * 100, 2)   ">=59(%)"
        
    from orders
        join delivery_men 
        on orders.delivery_man_id = delivery_men.id

        where orders.order_status = 'delivered' 
        and  orders.delivery_charge < 150
        # and orders.restaurant_id not in ( '999' , '1329' , '317', '1202' , '39' ,'315' , '316' , '319','1477','1221','1509','1536','1527')
        and orders.restaurant_id not in (1329,999,1585,1586,1587,1588,1589,1590)
        and orders.created_at >= CURDATE() - INTERVAL 1 MONTH

        group by date(orders.created_at),orders.delivery_man_id -- Ontime
        order by 4 desc;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_crm_cancelation():
    """
    Fetch data for crm cancelation
    """
    query = """
         
    select 
        date(orders.placed_at) order_Date,
        concat(monthname(orders.placed_at),"-",day(orders.placed_at)) Date,
        concat(admins.f_name," ",admins.l_name) responsible_person,
        concat(a1.f_name," ",a1.l_name) cancelled_by,
        cancellation_reasons.message CancellationMessage,
        count(orders.cancelation_reason) cancelledNumbers
        -- orders.created_at OrderCreationHour,
        -- orders.cancelation_note cancellation_note
        
        
    from orders
        join cancellation_reasons 
        on cancellation_reasons.id = orders.cancelation_reason
        join admins 
        on admins.id = orders.responsible_person
        join admins as a1
        on a1.id = orders.canceled_by
         
    where orders.order_status = 'canceled' 
        -- and  cancellation_reasons.message like '%CRM%'  -- CRM Cancellation
        and orders.restaurant_id not in (1329 , 999,1535,1585,1586,1587,1588,1589,1590)
        and date(orders.placed_at) >= CURDATE() - INTERVAL 1 MONTH 
        
        group by date(orders.placed_at), orders.cancelation_reason,3;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_unsafe():
    """
    Fetch data for Unsafe   
    """
    query = """
                
    select
        date(orders.placed_at) order_Date,
        concat(monthname(orders.placed_at),"-",day(orders.placed_at)) Date,
        CAST(orders.id AS CHAR) AS orderId,
        orders.created_at AS OrderCreationHour,
        restaurants.name RestaurantName,
        restaurants.address RestaurantAddress,
        # users.id,
        json_unquote(
            JSON_Extract(orders.delivery_address, "$.address")
        ) as Delivery_address,
        concat(delivery_men.f_name," ",delivery_men.l_name) DeliveryMan,
        concat(a1.f_name," ",a1.l_name) cancelled_by,
        orders.cancelation_reason CancellationReasonCode,
        cancellation_reasons.message CancellationMessage,
        orders.cancelation_note,
        orders.order_amount CustomerSpend,
        orders.handover,
        orders.original_delivery_charge

                
                
    from orders
        join restaurants 
        on restaurants.id =  orders.restaurant_id
        left join delivery_men 
        on delivery_men.id = orders.delivery_man_id
        join cancellation_reasons 
        on cancellation_reasons.id = orders.cancelation_reason
        join admins as a1
        on a1.id = orders.canceled_by
        # join users on users.id = orders.user_id

        
    where orders.order_status like '%canceled'  
        and orders.created_at  >= CURDATE() - INTERVAL 1 MONTH
        # and orders.created_at >= "2025-01-01" and orders.created_at < "2025-01-12"
        and orders.cancelation_reason in('R2','U4','U5','U6') -- Unsafe Location
        # and orders.cancelation_reaso÷n in('R55') -- Unsafe Location
        and orders.restaurant_id not in (1329 , 999)
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_other_reason():
    """
    Fetch data for other Reason 
    """
    query = """
        select 
            CAST(orders.id AS CHAR) AS orderId,
            orders.created_at,
            date(orders.placed_at) order_Date,
            restaurants.name,
            restaurants.address Restaurant_addreess,
            json_unquote(
                JSON_Extract(orders.delivery_address, "$.address")
            ) as Delivery_address,
            concat(admins.f_name, "-" , admins.l_name) Responsible_person,
            orders.delivery_charge Delivery_charge,
            concat(a1.f_name," ",a1.l_name) cancelled_by,
            orders.cancelation_reason,
            cancellation_reasons.message ,
            orders.cancelation_note

        from orders
            join users on orders.user_id = users.id
            join cancellation_reasons on orders.cancelation_reason = cancellation_reasons.id
            join restaurants on orders.restaurant_id = restaurants.id
            join admins on orders.responsible_person = admins.id
            join admins as a1
            on a1.id = orders.canceled_by

        where orders.order_status like "%canceled"
            
            and orders.cancelation_reason in ('R26','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10') -- other
            and orders.created_at >= CURDATE() - INTERVAL 1 MONTH
            -- >= "2023-11-01" and orders.created_at < "2023-11-17"
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_distance_too_long():
    """
    Fetch data for other Reason 
    """
    query = """
        # 11_Distance too long
    select
        date(orders.created_at) order_Date,
        concat(monthname(orders.created_at),"-",day(orders.created_at)) Date,
        CAST(orders.id AS CHAR) AS orderId,
        orders.placed_at OrderCreationHour,
        restaurants.name RestaurantName,
        restaurants.address RestaurantAddress,
        json_unquote(
            JSON_Extract(orders.delivery_address, "$.address")
        ) as Delivery_address,
        orders.delivery_charge Delivery_charge,
        concat(delivery_men.f_name," ",delivery_men.l_name) DeliveryMan,
        concat(a1.f_name," ",a1.l_name) cancelled_by,
        orders.cancelation_reason CancellationReasonCode,
        cancellation_reasons.message CancellationMessage,
        orders.order_amount CustomerSpend,
        orders.cancelation_note cancellation_note,
        orders.log_details ->> '$.delivery_charges.distance' distance,
        cs.name

    from orders
        join restaurants 
        on restaurants.id =  orders.restaurant_id
        left join delivery_men 
        on delivery_men.id = orders.delivery_man_id
        join cancellation_reasons 
        on cancellation_reasons.id = orders.cancelation_reason
        join admins as a1
        on a1.id = orders.canceled_by
        join order_details on order_details.order_id = orders.id
        join food on food.id = order_details.food_id
        join categories cs on cs.id = food.category_id
        
    where orders.order_status like '%canceled'  
        and orders.created_at >= CURDATE() - INTERVAL 1 MONTH  
        # and orders.created_at between '2025-01-01' and '2025-01-15'
        -- >= "2023-11-01" and orders.ccodeFor Delivery Data fiber_manual_recordreated_at < "2023-11-23"
        and orders.cancelation_reason  = 'R4' -- Distance to long
        and orders.restaurant_id not in (1329 , 999);
    
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_pos_discount():
    """
    Fetch data for Pos Discount 
    """
    query = """
        select
            CAST(orders.id AS CHAR) AS orderId,
            date(orders.placed_at) order_Date,
            orders.order_status,
            orders.pos_discount_amount,
            concat(admins.f_name , " " , admins.l_name) Admin_Name,
            restaurants.name Rest_Name,
            orders.order_note,
            res_fee.restaurant_fee,
            res_fee.commission_value,
            (res_fee.restaurant_fee + res_fee.commission_value) as rf_cv,
            orders.original_delivery_charge,
            (orders.original_delivery_charge + 11) as delivery_fee_plus_11,
            (res_fee.restaurant_fee+res_fee.commission_value+orders.original_delivery_charge+11) as tot

        from orders
        join restaurants on restaurants.id = orders.restaurant_id
        left join  admins on orders.created_by = admins.id
        left join restaurant_fee_details as res_fee on res_fee.order_id = orders.id

    where 
        orders.created_at  >= CURDATE() - INTERVAL 1 MONTH
        and orders.pos_discount_amount > 0
        and orders.order_status = 'delivered'
        and admins.id != 471
        ;
        


    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_handover():
    """
    Fetch data for Handover not null but cancelled
    """
    query = """
    select
        CAST(orders.id AS CHAR) AS orderId,
        # orders.created_at,
        date(orders.created_at) order_Date,
        orders.confirmed,
        orders.handover,
        orders.accepted,
        orders.canceled,
        orders.delivery_charge,
        orders.order_status,
        concat(delivery_men.f_name , "-" , delivery_men.l_name) Delivery_Man,
        concat(A2.f_name , "-" , A2.l_name ) Dispatcher_Name,
        concat(A1.f_name , "-" , A1.l_name ) CRM_Name,
        restaurants.name Rest_Name,
        concat(A3.f_name," ",A3.l_name) cancelled_by,
        cancellation_reasons.message Cancel_reason,
        orders.cancelation_note cancellation_note


    from orders
        left join delivery_men  on orders.delivery_man_id = delivery_men.id
        left join admins as A2 on A2.id = orders.dispatcher_id
        left join admins as A1 on A1.id = orders.responsible_person
        left join admins as A3 on A3.id = orders.canceled_by
        join restaurants on orders.restaurant_id = restaurants.id
        join cancellation_reasons on orders.cancelation_reason = cancellation_reasons.id

    where orders.restaurant_id not in (999 , 1329)
        and orders.handover is not null
        and orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        # and orders.created_at >= "2025-01-01" and orders.created_at < "2025-01-12"
        and orders.order_status = 'canceled'
        # group by orders.id
        ;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_pick_up_35min():
    """
    Fetch data for created to picked up more than 35 min 
    """
    query = """
            
    select
        date(orders.created_at) order_Date,
        CAST(orders.id AS CHAR) AS ID,
        orders.delivery_charge Delivery_charge,
        concat(delivery_men.f_name," ",delivery_men.l_name) Driver_man,
        concat(admins.f_name," ",admins.l_name) Dispatcher_name,
        json_unquote(
        JSON_Extract(orders.delivery_address,"$.address")
        ) Delivery_address,
        restaurants.name Restaurant,
        count(if(timestampdiff(second,orders.placed_at,orders.picked_up)/60 > 35,orders.id,Null)) Morethan_35,
        round(timestampdiff(second,orders.placed_at,orders.picked_up) / 60, 2) created_pickedup_min,
        -- round(timestampdiff(second,orders.accepted,orders.delivery_charge) / 60, 2) accepted_delivered_min,
           orders.delivery_distance,
        dz.name
        

    from orders
        join restaurants on restaurants.id = orders.restaurant_id
        left join delivery_men on delivery_men.id = orders.delivery_man_id
        left join admins on admins.id = orders.dispatcher_id
        left join delivery_zones dz on dz.id = delivery_men.z_id

    where orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        and orders.restaurant_id not in ( '999' , '1329' , '317', '1202' , '39' ,'315' , '316' , '319',1477,1535,1585,1586,1587,1588,1589,1590,46,387,1221,348,1202,1729,1617)
        and orders.order_status = "delivered" 
        and timestampdiff(second,orders.placed_at,orders.picked_up) / 60 > 35
        and orders.delivery_charge < 150

        group by order_Date,orders.id
        order by 7 desc;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_delivery_timestamp():
    """
    Fetch data for All delivery timestamp 
    """
    query = """
        
    select
        CAST(orders.id AS CHAR) AS "order ID",
        # orders.created_at,
        date(orders.created_at) order_Date,
        orders.accepted,
        orders.delivered,
        concat(A1.f_name," ",A1.l_name) CRM_name,
        concat(A2.f_name," ",A2.l_name) Dispatcher,
        concat(delivery_men.f_name," ",delivery_men.l_name) Driver,
        timestampdiff(second,orders.placed_at,orders.confirmed) / 60 Created_Confirmed,
        timestampdiff(second,orders.placed_at, orders.accepted) / 60 placed_accepted,
        timestampdiff(second,orders.confirmed,orders.handover) / 60 Confirmed_Handover,
        timestampdiff(second,orders.handover,orders.accepted) / 60 Handover_Accepted,
        timestampdiff(second,orders.accepted,orders.picked_up) / 60 Accepted_Pickedup,
        timestampdiff(second,orders.picked_up,orders.delivered) / 60 Pickedup_Delivered,
        timestampdiff(second,orders.created_at,orders.delivered) / 60 Created_Delivered

    from orders
        left join admins as A1 on A1.id = orders.responsible_person
        left join admins as A2 on A2.id = orders.dispatcher_id
        left join delivery_men on delivery_men.id = orders.delivery_man_id

    where orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        #  >= "2025-01-01" and orders.created_at <  "2025-01-12"
        # and (timestampdiff(second,orders.created_at,orders.delivered) / 60 <= 45)
        and orders.order_status = 'delivered'
        and orders.restaurant_id not in (1329, 999,1585,1586,1587,1588,1589,1590)
        ;    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_men_ratings():
    """
    Fetch data for Delivery men Ratings Daily
    """
    query = """

    select
        date(d_m_reviews.created_at) order_Date,
        concat(
            monthname(d_m_reviews.created_at),
            " ",
            day(d_m_reviews.created_at)
        ) Date,
        d_m_reviews.order_id OrderId,
        delivery_men.area Area,
        concat(delivery_men.f_name, " ", delivery_men.l_name) Driver,
        (d_m_reviews.rating) Rating,
        d_m_reviews.comment Comment
    from
        d_m_reviews
        join delivery_men on d_m_reviews.delivery_man_id = delivery_men.id
    where
        d_m_reviews.created_at >= CURDATE() - INTERVAL 1 MONTH
        #   d_m_reviews.created_at >= '2025-01-01' and d_m_reviews.created_at < '2025-01-12'
        # and  d_m_reviews.comment not like "%comment%"
        order by
        5 asc;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_resturant_rating():
    """
    Fetch data for Restaurant Rating
    """
    query = """

        # 19_Restaurant Rating
        #
    select
        date(reviews.created_at) order_Date,
        concat(
            monthname(reviews.created_at),
            " ",
            day(reviews.created_at)
        ) Date,
        reviews.order_id,
        json_unquote(
            JSON_Extract(order_details.food_details, "$.name")
        ) as Item,
        restaurants.name Restaurant,
        reviews.rating Rating,
        reviews.comment Comment #  categories.name,
        from
        reviews
        join order_details on reviews.order_id = order_details.order_id
        join restaurants on reviews.restaurant_id = restaurants.id # join categories on restaurants.category_id = categories.id
    where
        reviews.created_at >= CURDATE() - INTERVAL 1 MONTH # reviews.created_at >= '2022-11-12' and reviews.created_at < '2022-11-19'
        #   reviews.created_at >= '2025-01-01' and reviews.created_at < '2025-01-12'
        #   and reviews.comment not like '%No comment%'
    group by
        # #   categories.id
        order_Date, order_details.order_id
    order by
        5 asc;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_order_after_2():
    """
    Fetch data for Order after 20:00:00
    """
    query = """
                                # 22_Orders after 20:00:00      
        #
    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        orders.placed_at order_time,
        orders.order_status orderStatus,
        orders.order_amount,
        restaurants.name restaurantName,
        restaurants.address restaurantAddress,
        (json_extract(delivery_address, '$.address')) deliveryAddress,
        orders.delivery_charge deliveryCharge,
        orders.responsible_person responsiblePersonId,
        concat(A1.f_name, " ", A1.l_name) responsiblePerson,
        concat(A2.f_name," ",A2.l_name) Dispatcher,
        concat(delivery_men.f_name," ",delivery_men.l_name) driverName,
        orders.cancelation_reason cancellation,
        cancellation_reasons.message cancellationReason,
        orders.cancelation_note cancellationNote

    from orders
        join restaurants
        on orders.restaurant_id = restaurants.id
        left join delivery_men
        on delivery_men.id = orders.delivery_man_id
        left join admins as A1
        on A1.id = orders.responsible_person
        left join admins as A2 
        on A2.id = orders.dispatcher_id
        left join cancellation_reasons 
        on cancellation_reasons.id = orders.cancelation_reason

    where 
        orders.placed_at >= CURDATE() - INTERVAL 1 MONTH
        # orders.created_at >= "2025-01-01" and orders.created_at < "2025-01-12"
        and time(orders.placed_at) >= "20:00:00"
        # and time(orders.created_at) >= "19:00:00" and time(orders.created_at) <= "20:00:00"
        and orders.order_status != 'failed'
        and orders.restaurant_id not in (1329, 999)
        ;

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_morethan_90():
    """
    Fetch data for More than 90min
    """
    query = """
            # 23_Morethan 90 min
        #
    select
        date(orders.created_at) order_Date,
        CAST(orders.id AS CHAR) AS "order ID",
        orders.delivery_charge,
        concat(delivery_men.f_name, "-" , delivery_men.l_name) Driver_Name,
        concat(admins.f_name," ",admins.l_name) Dispatcher_Name,
        restaurants.name Rest_Name,
        restaurants.address,
        json_unquote(
            JSON_Extract(orders.delivery_address, "$.address")
        ) as Delivery_address,
        count(if( timestampdiff(second, orders.placed_at, orders.delivered)/60 >= 90 , orders.id , null )) Morethan_90,
        round(timestampdiff(second,orders.created_at , orders.delivered)/60 , 2) created_delivered_min,
        round(timestampdiff(second,orders.accepted , orders.delivered)/60,2) accepted_delivered_min,
        case
        when (timestampdiff(second,orders.accepted,orders.delivered) / 60 > 45 and orders.picked_up is not null) then 'late driver'
            when (timestampdiff(second,orders.handover,orders.accepted) / 60 > 35 and orders.picked_up is not null) then 'late assignment'
            when (timestampdiff(second,orders.created_at,orders.handover) / 60 > 5 and orders.picked_up is not null) then 'late crm'
            when orders.picked_up is null then 'drivers ontime fixed'
        when ((timestampdiff(second,orders.handover,orders.accepted) / 60 < 0 or timestampdiff(second,orders.accepted,orders.delivered) / 60 < 0
                    or timestampdiff(second,orders.created_at,orders.handover) / 60 < 0) and orders.picked_up is not null) then 'Negative'    
            else 'other'
        end as late_reason

    from orders
        join restaurants on orders.restaurant_id = restaurants.id
        left join delivery_men on orders.delivery_man_id = delivery_men.id
        left join admins on orders.dispatcher_id = admins.id

    where orders.order_status = "delivered" 
        and  orders.delivery_charge > 150
        and orders.restaurant_id not in ( '999' , '1329' , '317', '1202' , '39' ,'315' , '316' , '319',1535,1585,1586,1587,1588,1589,1590,46,387,1221,348,1202,1729,1617)
        and orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        # and orders.placed_at >= "2025-01-01" and orders.placed_at < "2025-01-12"
        and timestampdiff(second,orders.placed_at , orders.delivered)/ 60 >= 90


        group by order_Date, orders.id  -- More than 90 Min Orders
        order by 7 desc;

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_incomplete_driver():
    """
    Fetch data for Incomplete Orders with driver unassigned
    """
    query = """
            # 24_Incomplete Orders with driver unassigned
        #
    select 
        CAST(orders.id AS CHAR) AS order_id,
        date(orders.placed_at) order_Date,
        orders.placed_at order_time,
        restaurants.name restaurant_name,
        restaurant_fee_details.restaurant_fee Restaurant_fee,
        orders.order_amount orderAmount,
        orders.delivery_charge deliveryCharge,
        json_unquote(
                JSON_Extract(
                orders.log_details,
                "$.service_charges.restaurant_service_charge_amount"
                )
            )as  serviceCharge,
        restaurants.address restaurants_address,
        concat(delivery_men.f_name,"-",delivery_men.l_name) delivery_men,
        concat(admins.f_name,"-",admins.l_name) responsible_person,
        (json_extract(delivery_address, '$.address')) Delivery_address,
        orders.order_status,
        concat(a1.f_name," ",a1.l_name) cancelled_by,
        orders.cancelation_reason,
        cancellation_reasons.message cancellation_message,
        orders.cancelation_note Cancel_Note



    From orders
        left join restaurant_fee_details on restaurant_fee_details.order_id = orders.id
        left join delivery_men 
        on delivery_men.id = orders.delivery_man_id
        join restaurants 
        on restaurants.id = orders.restaurant_id
        join cancellation_reasons 
        on cancellation_reasons.id = orders.cancelation_reason
        join admins
        on admins.id = orders.responsible_person
        join admins as a1
        on a1.id = orders.canceled_by
        
    where 
        orders.placed_at >= CURDATE() - INTERVAL 1 MONTH
        # orders.created_at >= "2025-01-01" and orders.created_at < "2025-01-12"
        and orders.restaurant_id not in (1329 , 999)
        and orders.order_status = 'canceled'
        and cancellation_reasons.id in ('I01', 'I02', 'I03', 'I04', 'I05', 'I06', 'I07', 'I08', 'I09','I10','I11','I12','I13','I14','I15','I16','I17','I18','I19','I20','I21','I22','I23','I24', 'R41', 'R42', 'R28')
        and delivery_men.id is null
        ;

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_possible_spammer():
    """
    Fetch data for Possible Spammer
    """
    query = """
            # 25_Possible Spammer
        # 
    select
        date(orders.created_at) order_Date,
        orders.placed_at,
        users.phone,
        CAST(orders.id AS CHAR) AS "order ID",
        orders.order_status,
        orders.cancelation_reason,
        cancellation_reasons.message,
        concat(admins.f_name," ",admins.l_name) Responsible_Person

    from orders
        join users on users.id = orders.user_id
        join admins on orders.responsible_person = admins.id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason

    where 
        orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        # orders.created_at >= "2025-01-01" and orders.created_at < "2025-01-12"
        and orders.restaurant_id not in (1329,999)
        and users.customer_classification = 'Possible Spammer'
        ;

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_placed_at_morethan_40min():
    """
    Fetch data for Placed at to accepted in morethan 40 min
    """
    query = """
            # 26_Placed at to accepted in morethan 40 min
        #
    select
        #orders.placed_at,
        date(orders.created_at) order_Date,
        CAST(orders.id AS CHAR) AS ID,
        restaurants.name Restaurant,
        concat(admins.f_name," ",admins.l_name) Dispatcher,
        concat(delivery_men.f_name," ",delivery_men.l_name) Driver,
        round(timestampdiff(second,orders.placed_at,orders.accepted) / 60,2) Placed_accepted,
        round(timestampdiff(second,orders.accepted,orders.delivered) / 60,2) Accepted_delivered,
        case
        when (timestampdiff(second,orders.accepted,orders.delivered) / 60) < 3 then 'driver ontime fixed'
        end as driverOntimeFixed,
        orders.delivery_charge,
        orders.order_status,
        orders.delivery_distance,
        dz.name
        

    from orders
        join restaurants on restaurants.id = orders.restaurant_id
        left join delivery_men on delivery_men.id = orders.delivery_man_id
        left join admins on admins.id = orders.dispatcher_id
        left join delivery_zones dz on dz.id = delivery_men.z_id


    where orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        and orders.order_status = "delivered"
        and orders.restaurant_id not in (1535,1585,1586,1587,1588,1589,1590)
        and (timestampdiff(second,orders.placed_at,orders.accepted) / 60) > 35

        order by 6 desc
        ;

    """
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_c6():
    """
    Fetch data for c6
    """
    query = """
    select
        date(orders.created_at) order_Date,
        users.phone "User Phone",
        CAST(orders.id AS CHAR) AS "order ID",
        concat(admins.f_name, " ", admins.l_name) "Responsible Person",
        message "Cancellation Reason",
        orders.handover,
        orders.order_amount,
        orders.delivery_charge,
        orders.cancelation_note,
        canceled_by_admin.f_name as "Canceled By"
    from
        orders
        left join cancellation_reasons cr on cr.id = orders.cancelation_reason
        left join admins on admins.id = orders.responsible_person
        left join users on users.id = orders.user_id
        left join admins as canceled_by_admin on canceled_by_admin.id = orders.canceled_by
        
    where
        orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        #   orders.created_at between '2025-01-17' and '2025-01-21'
        and orders.restaurant_id not in (1329 , 999)
        and orders.cancelation_reason =
        #       'R5'
        #       'R12'
        #       'R9'
        'C6';

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_c9():
    """
    Fetch data for c9
    """
    query = """
    select
        date(orders.created_at) order_Date,
        users.phone "User Phone",
        CAST(orders.id AS CHAR) AS "order ID",
        concat(admins.f_name, " ", admins.l_name) "Responsible Person",
        message "Cancellation Reason",
        orders.handover,
        orders.order_amount,
        orders.delivery_charge
    from
        orders
        left join cancellation_reasons cr on cr.id = orders.cancelation_reason
        left join admins on admins.id = orders.responsible_person
        left join users on users.id = orders.user_id
    where
        orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        #   orders.created_at between '2025-01-17' and '2025-01-22'
        and orders.restaurant_id not in (1329 , 999)
        and orders.cancelation_reason =  'C9'
        and orders.order_status != 'delivered'
        ;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_mube():
    """
    Fetch data for c6
    """
    query = """
        SELECT
            DATE(o.placed_at) AS order_date,
            o.placed_at AS "Placed At",
            o.canceled AS "Cancelled At",
            CAST(o.id AS CHAR) AS "order ID",
            u.f_name AS "Customer name",
            u.phone AS "Customer phone",
            cr.message AS "Cancellation reason",
            TIMESTAMPDIFF(SECOND, o.placed_at, o.canceled) / 60 AS cancel_time,
            CASE
                WHEN nu.first_order_id = o.id THEN 'NEW USER'
                ELSE 'EXISTING USER'
            END AS user_type
        FROM orders o
        JOIN users u
            ON u.id = o.user_id
        JOIN cancellation_reasons cr
            ON cr.id = o.cancelation_reason
        LEFT JOIN (
            SELECT
                ho.user_phone,
                MIN(ho.order_id) AS first_order_id
            FROM history_orders ho
            WHERE ho.created_at >= CURDATE() - INTERVAL 3 MONTH
            GROUP BY ho.user_phone
        ) nu
            ON nu.first_order_id = o.id
        WHERE o.placed_at >= CURDATE() - INTERVAL 1 MONTH
        AND o.order_status = 'canceled'
        AND u.customer_classification NOT LIKE '%Possible%'
        AND TIMESTAMPDIFF(SECOND, o.placed_at, o.canceled) >= 3000;

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_crm():
    """
    CRM not receiving phone call
    """
    query = """
    select
        date(orders.placed_at)  order_Date,
        users.phone,
        CAST(orders.id AS CHAR) AS orderId,
        concat(admins.f_name, " ", admins.l_name) responsiblePerson,
        cancellation_reasons.message CancellationMessage
    from
        orders
        join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        join users on users.id = orders.user_id
        left join admins on admins.id = orders.responsible_person
    where
        orders.order_status = 'canceled' # and  cancellation_reasons.message like '%(CRM) Not receiving phone call | BEFORE%'  -- CRM Cancellation
        and orders.cancelation_reason = 'R5'
        and orders.restaurant_id not in (
            999,
            1329,
            1477,
            1536,
            1527,
            1585,
            1586,
            1587,
            1588,
            1589,
            1590
        )
        and orders.placed_at  >= CURDATE() - INTERVAL 1 MONTH
        #   and orders.created_at >= "2025-01-17" and orders.created_at < "2025-01-23"
        ;

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_acc_ass():   
    """
    CRM not receiving phone call
    """
    query = """
    # Assigned & Accepted Percentage
    select
        date(orders.created_at) order_Date,
       delivery_zones.name as area,
        count(
            distinct if(orders.is_assign = 1, orders.id, null)
        ) assigned,
        count(
            distinct if(orders.is_assign = 0, orders.id, null)
        ) accepted,
        count(distinct orders.id) total_count,
        round(
            (
            count(
                distinct if(orders.is_assign = 1, orders.id, null)
            ) / count(distinct orders.id)
            ) * 100,
            2
        ) assigned_percent,
        round(
            (
            count(
                distinct if(orders.is_assign = 0, orders.id, null)
            ) / count(distinct orders.id)
            ) * 100,
            2
        ) accepted_percent
    from
        orders
        left join delivery_men driver on driver.id = orders.delivery_man_id
        join delivery_zones on delivery_zones.id =driver.z_id
    where
        orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        and orders.order_status = 'delivered'
    group by
        delivery_zones.id,date(orders.created_at);
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_accive_status():
    """
    CRM not receiving phone call
    """
    query = """
        SELECT 
                
                delivery_men.is_package,
                CONCAT(delivery_men.f_name, ' ', delivery_men.l_name) AS full_name,
                delivery_men.phone,
                delivery_men.id,
                delivery_zones.name as area,
                delivery_men.status
                
            FROM 
                delivery_men
                join delivery_zones on delivery_zones.id =delivery_men.z_id
            WHERE 
                delivery_men.status = 1;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_arif_pay_edited():
    """
        telebirr paid, edited and delivered
    """
    query = """
    
    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        if(
            users.l_name is null,
            users.f_name,
            concat(users.f_name, " ", users.l_name)
        ) Customer,
        users.phone,
        orders.order_amount,
        customer_transactions.order_amount user_paid,
        orders.tip,
        orders.payment_method,
        orders.payment_status,
        orders.cancelation_reason,
        cancellation_reasons.message
            
        #   orders.cancelation_note,
        #   orders.order_status
    from
    orders
        join users on users.id = orders.user_id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        left join customer_transactions on customer_transactions.order_id = orders.id
        
    where
        date(orders.placed_at) >= CURDATE() - INTERVAL 1 MONTH
        and orders.payment_method = 'arifpay'
        and orders.order_status = 'delivered'
        and orders.payment_status != 'unpaid'
        and orders.edited = 1
        ;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_chapa_edited():
    """
        telebirr paid, edited and delivered
    """
    query = """
    
    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        if(
            users.l_name is null,
            users.f_name,
            concat(users.f_name, " ", users.l_name)
        ) Customer,
        users.phone,
        orders.order_amount,
        customer_transactions.order_amount user_paid,
        orders.tip,
        orders.payment_method,
        orders.payment_status,
        orders.cancelation_reason,
        cancellation_reasons.message
            
        #   orders.cancelation_note,
        #   orders.order_status
    from
    orders
        join users on users.id = orders.user_id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        left join customer_transactions on customer_transactions.order_id = orders.id
        
    where
        date(orders.placed_at) >= CURDATE() - INTERVAL 1 MONTH
        and orders.payment_method = 'chapa'
        and orders.order_status = 'delivered'
        and orders.payment_status != 'unpaid'
        and orders.edited = 1
        ;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_telebirr_edited():
    """
        telebirr paid, edited and delivered
    """
    query = """
    
    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        if(
            users.l_name is null,
            users.f_name,
            concat(users.f_name, " ", users.l_name)
        ) Customer,
        users.phone,
        orders.order_amount,
        customer_transactions.order_amount user_paid,
        orders.tip,
        orders.payment_method,
        orders.payment_status,
        orders.cancelation_reason,
        cancellation_reasons.message
            
        #   orders.cancelation_note,
        #   orders.order_status
    from
    orders
        join users on users.id = orders.user_id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        left join customer_transactions on customer_transactions.order_id = orders.id
        
    where
        date(orders.placed_at) >= CURDATE() - INTERVAL 1 MONTH
        and orders.payment_method = 'telebirr'
        and orders.order_status = 'delivered'
        and orders.payment_status != 'unpaid'
        and orders.edited = 1
        ;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_telebirr_canceled():
    """
    telebirr paid but canceled

    """
    query = """
  
    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        if(
            users.l_name is null,
            users.f_name,
            concat(users.f_name, " ", users.l_name)
        ) Customer,
        users.phone,
        orders.order_amount,
        customer_transactions.order_amount user_paid,
        orders.tip,
        orders.payment_method,
        orders.payment_status,
        orders.cancelation_reason,
        cancellation_reasons.message
            
        #   orders.cancelation_note,
        #   orders.order_status
    from
    orders
        join users on users.id = orders.user_id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        left join customer_transactions on customer_transactions.order_id = orders.id
        
    where
        date(orders.placed_at) >= CURDATE() - INTERVAL 1 MONTH
        and orders.payment_method = 'telebirr'
        and orders.order_status = 'canceled'
        and orders.payment_status != 'unpaid'
        #   and orders.id = 1627441
        #   and users.phone = '+251910861386'
        #   and cancellation_reasons.message like "%Incomplete%"
        ;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_split_edited():
    """
        telebirr paid, edited and delivered
    """
    query = """
    
    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        if(
            users.l_name is null,
            users.f_name,
            concat(users.f_name, " ", users.l_name)
        ) Customer,
        users.phone,
        orders.order_amount,
        orders.order_point,
        customer_transactions.order_amount user_paid,
        orders.tip,
        orders.payment_method,
        orders.payment_status,
        orders.cancelation_reason,
        cancellation_reasons.message
            
        #   orders.cancelation_note,
        #   orders.order_status
    from
    orders
        join users on users.id = orders.user_id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        left join customer_transactions on customer_transactions.order_id = orders.id
        
    where
        date(orders.placed_at) >= CURDATE() - INTERVAL 1 MONTH
        and orders.payment_method = 'split'
        and orders.order_status = 'delivered'
        and orders.payment_status != 'unpaid'
        and orders.edited = 1
        ;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_split_canceled():
    """
    telebirr paid but canceled

    """
    query = """
  
    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        if(
            users.l_name is null,
            users.f_name,
            concat(users.f_name, " ", users.l_name)
        ) Customer,
        users.phone,
        orders.order_amount,
        orders.order_point,
        customer_transactions.order_amount user_paid,
        orders.tip,
        orders.payment_method,
        orders.payment_status,
        orders.cancelation_reason,
        cancellation_reasons.message
            
        #   orders.cancelation_note,
        #   orders.order_status
    from
    orders
        join users on users.id = orders.user_id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        left join customer_transactions on customer_transactions.order_id = orders.id
        
    where
        date(orders.placed_at) >= CURDATE() - INTERVAL 1 MONTH
        and orders.payment_method = 'split'
        and orders.order_status = 'canceled'
        and orders.payment_status != 'unpaid'
        #   and orders.id = 1627441
        #   and users.phone = '+251910861386'
        #   and cancellation_reasons.message like "%Incomplete%"
        ;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_chapa_canceled():
    """
        chapa paid but canceled
    """
    query = """
    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        if(
            users.l_name is null,
            users.f_name,
            concat(users.f_name, " ", users.l_name)
        ) Customer,
        users.phone,
        orders.order_amount,
        customer_transactions.order_amount user_paid,
        orders.tip,
        orders.payment_method,
        orders.payment_status,
        orders.cancelation_reason,
        cancellation_reasons.message
        #   orders.cancelation_note,
        #   orders.order_status
    from
    orders
        join users on users.id = orders.user_id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        left join customer_transactions on customer_transactions.order_id = orders.id
        
    where
        date(orders.placed_at) >= CURDATE() - INTERVAL 1 MONTH
        and orders.payment_method = 'chapa'
        and orders.order_status = 'canceled'
        and orders.payment_status != 'unpaid'
        #   and users.phone = '+251910861386'
        #   and cancellation_reasons.message like "%Incomplete%"
        ;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_arifpay_canceled():
    """
        arifpay paid but canceled
    """
    query = """
    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        if(
            users.l_name is null,
            users.f_name,
            concat(users.f_name, " ", users.l_name)
        ) Customer,
        users.phone,
        orders.order_amount,
        customer_transactions.order_amount user_paid,
        orders.tip,
        orders.payment_method,
        orders.payment_status,
        orders.cancelation_reason,
        cancellation_reasons.message
        #   orders.cancelation_note,
        #   orders.order_status
    from
    orders
        join users on users.id = orders.user_id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        left join customer_transactions on customer_transactions.order_id = orders.id

    where
        date(orders.placed_at) >= CURDATE() - INTERVAL 1 MONTH
        and orders.payment_method = 'arifpay'
        and orders.order_status = 'canceled'
        and orders.payment_status != 'unpaid'
        #   and users.phone = '+251910861386'
        #   and cancellation_reasons.message like "%Incomplete%"
        ;

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_R9():
    """
    Fetch data for R9
    """
    query = """
    select
        date(orders.created_at) order_Date,
        users.phone "User Phone",
        CAST(orders.id AS CHAR) AS "order ID",
        concat(admins.f_name, " ", admins.l_name) "Responsible Person",
        message "Cancellation Reason",
        orders.handover,
        orders.order_amount,
        orders.delivery_charge,
        orders.cancelation_note,
        canceled_by_admin.f_name as "Canceled By"
    from
        orders
        left join cancellation_reasons cr on cr.id = orders.cancelation_reason
        left join admins on admins.id = orders.responsible_person
        left join users on users.id = orders.user_id
        left join admins as canceled_by_admin on canceled_by_admin.id = orders.canceled_by
        
    where
        orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        #   orders.created_at between '2025-01-17' and '2025-01-21'
        and orders.restaurant_id not in (1329 , 999)
        and orders.cancelation_reason =
        #       'R5'
        #       'R12'
              'R9';

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_R12():
    """
    Fetch data for R12
    """
    query = """
    select
        date(orders.created_at) order_Date,
        users.phone "User Phone",
        CAST(orders.id AS CHAR) AS "order ID",
        concat(admins.f_name, " ", admins.l_name) "Responsible Person",
        message "Cancellation Reason",
        orders.handover,
        orders.order_amount,
        orders.delivery_charge,
        orders.cancelation_note,
        canceled_by_admin.f_name as "Canceled By"
    from
        orders
        left join cancellation_reasons cr on cr.id = orders.cancelation_reason
        left join admins on admins.id = orders.responsible_person
        left join users on users.id = orders.user_id
        left join admins as canceled_by_admin on canceled_by_admin.id = orders.canceled_by
        
    where
        orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        #   orders.created_at between '2025-01-17' and '2025-01-21'
        and orders.restaurant_id not in (1329 , 999)
        and orders.cancelation_reason =
        #       'R5'
              'R12';

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_R47():
    """
    Fetch data for R47
    """
    query = """
    select
        date(orders.created_at) order_Date,
        users.phone "User Phone",
        CAST(orders.id AS CHAR) AS "order ID",
        concat(admins.f_name, " ", admins.l_name) "Responsible Person",
        message "Cancellation Reason",
        orders.handover,
        orders.order_amount,
        orders.delivery_charge,
        orders.cancelation_note,
        canceled_by_admin.f_name as "Canceled By"
    from
        orders
        left join cancellation_reasons cr on cr.id = orders.cancelation_reason
        left join admins on admins.id = orders.responsible_person
        left join users on users.id = orders.user_id
        left join admins as canceled_by_admin on canceled_by_admin.id = orders.canceled_by
        
    where
        orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        #   orders.created_at between '2025-01-17' and '2025-01-21'
        and orders.restaurant_id not in (1329 , 999)
        and orders.cancelation_reason =
              'R47';

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_R54():
    """
    Fetch data for R47
    """
    query = """
    select  
        date(orders.created_at) order_Date,
        CAST(orders.id AS CHAR) AS "order ID",
        restaurants.name as Restaurant_Name,
        concat(delivery_men.f_name," ",delivery_men.l_name),
        message "Cancellation Reason",
        orders.original_delivery_charge,
        dm_earnings.earning,
        dm_earnings.cut
        
    from
        orders
        left join cancellation_reasons cr on cr.id = orders.cancelation_reason
        left join restaurants on restaurants.id = orders.restaurant_id
        left join delivery_men on delivery_men.id = orders.delivery_man_id
        left join dm_earnings on dm_earnings.dm_id = delivery_men.id
        
    where
        orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        and orders.restaurant_id not in (1329 , 999)
        and orders.cancelation_reason =  'R54';


    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_CRM_conve_agent():
    """
    Fetch data for CRM Conversion by agent 
    """
    query = """
    select
        date(orders.created_at) order_Date,
        admins.id,
        concat(admins.f_name, " ", admins.l_name) CRM,
        
        #   count(distinct orders.id) TotalAlert,
        count(
            distinct if(order_status = 'delivered', orders.id, null)
        ) TotalDelivered,
        #   count(
        #     distinct if(order_status = 'canceled', orders.id, null)
        #   ) TotalCancelled,
        count(
            if(
            orders.order_status = 'delivered'
            and timestampdiff(second, orders.placed_at, orders.handover) / 60 <= 5,
            orders.id,
            null
            )
        ) OnTimeCount,
        round(
            (
            count(
                if(
                orders.order_status = 'delivered'
                and timestampdiff(second, orders.placed_at, orders.handover) / 60 <= 5,
                orders.id,
                null
                )
            ) / count(
                if(
                orders.order_status = 'delivered',
                orders.id,
                null
                )
            )
            ) * 100,
            1
        ) OnTimePercent,
        round(
            (
            count(
                distinct if(order_status = 'delivered', orders.id, null)
            ) / (
                count(
                distinct if(order_status = 'delivered', orders.id, null)
                ) + count(
                distinct if(
                    orders.cancelation_reason in ('R12', 'R5', 'C9', 'R47','R9'),
                    orders.id,
                    null
                )
                )
            )
            ) * 100,
            1
        ) CRMConversion
        from
        orders
        join admins on admins.id = orders.responsible_person
        join restaurants r on r.id = orders.restaurant_id
    where
         orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        #   orders.created_at like '2025-02-13%'
        and r.name not like '%Donate%'
        and (
            orders.cancelation_reason not like 'Telebirr User canceled order%'
            or orders.cancelation_reason is null
        )
        and order_status != 'failed'
    group by
        admins.id,Date(orders.created_at)
    having
        TotalDelivered > 1
        order by orders.created_at ;

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_CRM_total():
    """
    Fetch data for CRM group by date 
    """
    query = """
    select
        concat(
            monthname(orders.created_at),
            ' ',
            day(orders.created_at)
        ) created_at,
        count(
            if(
            orders.order_status = 'delivered',
            orders.id,
            null
            )
        ) all_delivered,
        count(
            if(
            orders.order_status = 'delivered'
            and timestampdiff(second, orders.created_at, orders.handover) / 60 <= 5,
            orders.id,
            null
            )
        ) percentage_less_equal_five,
        round(
            (
            count(
                if(
                orders.order_status = 'delivered'
                and timestampdiff(second, orders.created_at, orders.handover) / 60 <= 5,
                orders.id,
                null
                )
            ) / count(
                if(
                orders.order_status = 'delivered',
                orders.id,
                null
                )
            )
            ) * 100,
            2
        ) percentage_from_total,
        round(
            (
                count(
                distinct if(order_status = 'delivered', orders.id, null)
                ) / (
                count(
                    distinct if(order_status = 'delivered', orders.id, null)
                ) + count(
                    distinct if(
                    orders.cancelation_reason in ('R5', 'R12', 'R9','C9', 'R47'),
                    orders.id,
                    null
                    )
                )
                )
            ) * 100,
            1
            ) CRMConversion,
        COUNT(IF(
            orders.cancelation_reason IN ('R12', 'R5', 'C9', 'R47','R9'), 
            orders.id, 
            NULL
        )) AS cancelation_reason_count,
        count(if(orders.cancelation_reason = 'R12',orders.id,NULL)) as R12,
        count(if(orders.cancelation_reason = 'R5',orders.id,NULL)) as R5,
        count(if(orders.cancelation_reason = 'C9',orders.id,NULL)) as C9,
        count(if(orders.cancelation_reason = 'R47',orders.id,NULL)) as R47,
        count(if(orders.cancelation_reason = 'R9',orders.id,NULL)) as R9
    from
        orders
        join restaurants on restaurants.id = orders.restaurant_id
        where
        orders.restaurant_id not in(999, 1329)
        #     and orders.created_at like '2025-02-13%'
        AND orders.created_at >= DATE_FORMAT(NOW(), '%Y-%m-01') 
        AND orders.created_at < LAST_DAY(NOW()) + INTERVAL 1 DAY
        and restaurants.name not like 'Ethio-post%'
        and orders.order_status != 'failed'
        group by
        date(orders.created_at)
        order by
        orders.created_at asc;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_CRM_total_month():
    """
    Fetch data for CRM group by date 
    """
    query = """
    select
        count(
            if(
            orders.order_status = 'delivered',
            orders.id,
            null
            )
        ) all_delivered,
        count(
            if(
            orders.order_status = 'delivered'
            and timestampdiff(second, orders.created_at, orders.handover) / 60 <= 5,
            orders.id,
            null
            )
        ) percentage_less_equal_five,
        round(
            (
            count(
                if(
                orders.order_status = 'delivered'
                and timestampdiff(second, orders.created_at, orders.handover) / 60 <= 5,
                orders.id,
                null
                )
            ) / count(
                if(
                orders.order_status = 'delivered',
                orders.id,
                null
                )
            )
            ) * 100,
            2
        ) percentage_from_total,
        round(
            (
                count(
                distinct if(order_status = 'delivered', orders.id, null)
                ) / (
                count(
                    distinct if(order_status = 'delivered', orders.id, null)
                ) + count(
                    distinct if(
                    orders.cancelation_reason in ('R5', 'R12', 'R9','C9', 'R47'),
                    orders.id,
                    null
                    )
                )
                )
            ) * 100,
            1
            ) CRMConversion,
        COUNT(IF(
            orders.cancelation_reason IN ('R12', 'R5', 'C9', 'R47','R9'), 
            orders.id, 
            NULL
        )) AS cancelation_reason_count,
        count(if(orders.cancelation_reason = 'R12',orders.id,NULL)) as R12,
        count(if(orders.cancelation_reason = 'R5',orders.id,NULL)) as R5,
        count(if(orders.cancelation_reason = 'C9',orders.id,NULL)) as C9,
        count(if(orders.cancelation_reason = 'R47',orders.id,NULL)) as R47,
        count(if(orders.cancelation_reason = 'R9',orders.id,NULL)) as R9
    from
        orders
        join restaurants on restaurants.id = orders.restaurant_id
        where
        orders.restaurant_id not in(999, 1329)
        #     and orders.created_at like '2025-02-13%'
        and orders.created_at >= DATE_FORMAT(NOW(), '%Y-%m-01') 
        AND orders.created_at < LAST_DAY(NOW()) + INTERVAL 1 DAY
        and restaurants.name not like 'Ethio-post%'
        and orders.order_status != 'failed'
        order by
        orders.created_at asc;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_mube_compensation():
    """
    Fetch data for mube compensation 
    """
    query = """
    
    SELECT 
        DATE(orders.created_at) AS order_date,
        orders.id AS Id,
        orders.coupon_discount_title,
        orders.coupon_code,
        orders.order_status,
        users.phone,
        orders.coupon_discount_amount
    FROM 
        orders
    JOIN 
        users ON orders.user_id = users.id
    WHERE 
        orders.coupon_discount_title IN ("Muba compensation", "Mube Compensation")
        AND orders.created_at >= DATE_FORMAT(NOW(), '%Y-%m-01') 
        AND orders.created_at < LAST_DAY(NOW()) + INTERVAL 1 SECOND
        AND orders.order_status = "delivered";


    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_removeed_deduction():
    """
    Fetch data for Removed Deductions
    """
    query = """
    select
        date(orders.created_at) order_Date,
        CAST(orders.id AS CHAR) AS "order ID",
        orders.delayed_delivery,
        orders.accepted	,
        orders.delivered	,
        round(timestampdiff(second,orders.placed_at,orders.accepted) / 60,2) Placed_accepted,
        round(timestampdiff(second,orders.accepted,orders.delivered) / 60,2) Accepted_delivered,
        orders.delivery_distance,
        orders.original_delivery_charge,
        orders.late_delivery
    from

        orders

    where 
        orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        and orders.restaurant_id not in (1329 , 999)
        and orders.order_status = "delivered"
        and orders.delayed_delivery = 1

    order by orders.late_delivery

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_ussd_canceled():
    """
    Fetch data for telebirr ussd payment canceled
    """
    query = """

    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        if(
            users.l_name is null,
            users.f_name,
            concat(users.f_name, " ", users.l_name)
        ) Customer,
        users.phone,
        orders.order_amount,
        customer_transactions.order_amount user_paid,
        orders.order_status,
        orders.tip,
        orders.payment_method,
        orders.payment_status,
        orders.cancelation_reason,
        cancellation_reasons.message,
            
        orders.cancelation_note
        #   orders.order_status
    from
        orders
        join users on users.id = orders.user_id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        left join customer_transactions on customer_transactions.order_id = orders.id


    where orders.payment_method = "telebirr-ussd"
        and orders.created_at >= CURDATE() - INTERVAL 1 MONTH
        and orders.order_status = "canceled";



    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_telebirr_ussd_edited():
    """
        telebirr-ussd paid, edited and delivered
    """
    query = """
    
    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        if(
            users.l_name is null,
            users.f_name,
            concat(users.f_name, " ", users.l_name)
        ) Customer,
        users.phone,
        orders.order_amount,
        customer_transactions.order_amount user_paid,
        orders.tip,
        orders.payment_method,
        orders.payment_status,
        orders.cancelation_reason,
        cancellation_reasons.message
            
        #   orders.cancelation_note,
        #   orders.order_status
    from
    orders
        join users on users.id = orders.user_id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        left join customer_transactions on customer_transactions.order_id = orders.id
        
    where
        date(orders.placed_at) >= CURDATE() - INTERVAL 1 MONTH
        and orders.payment_method = 'telebirr-ussd'
        and orders.order_status = 'delivered'
        and orders.payment_status != 'unpaid'
        and orders.edited = 1
        ;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_timestamp(order_id):
    """
    Fetches timestamp data for a single order ID.
    """
    query = """
        SELECT
            CAST(orders.id AS CHAR) AS "order ID",
            orders.created_at,
            placed_at,
            confirmed,
            processing,
            handover,
            accepted,
            driver_arrived,
            picked_up,
            delivered,
            canceled,
            TIMESTAMPDIFF(SECOND, orders.placed_at, orders.delivered) / 60 AS late,
            orders.order_status,
            concat(a1.f_name," ",a1.l_name) cancelled_by,
            concat(a2.f_name," ",a2.l_name) responsible_person,
            concat(a3.f_name," ",a3.l_name) delivered_by,
            concat(a4.f_name," ",a4.l_name) dispacher_by,
            
            orders.delivery_initiator

        from orders
            left join admins a1 on a1.id = orders.canceled_by
            left join admins a2 on a2.id = orders.responsible_person
            left join admins a4 on a4.id = orders.dispatcher_id
            left join admins a3 on a3.id = orders.delivered_by
        WHERE
            orders.id = %s
    """

    # Ensure `order_id` is passed as a tuple
    if isinstance(order_id, list) or isinstance(order_id, tuple):
        order_id = int(order_id[0])  # Take the first element if it's a list or tuple

    with engine.connect() as connection:
        result = pd.read_sql(query, connection, params=(order_id,))  # Pass as a tuple

    return result

def get_unique_bds():
    query = """
    SELECT DISTINCT CONCAT(admins.f_name, '-', admins.l_name) AS bd_name
    FROM restaurants
    JOIN admins ON admins.id = restaurants.business_developer_id
    WHERE restaurants.id NOT IN (999, 1329)
    AND restaurants.name NOT LIKE 'Ethio-post%'
    """
    with engine.connect() as connection:
        return pd.read_sql(query, connection)['bd_name'].dropna().sort_values().tolist()


def get_unique_restaurants():
    query = """
    SELECT DISTINCT name
    FROM restaurants
    WHERE id NOT IN (999, 1329)
    AND name NOT LIKE 'Ethio-post%'
    """
    with engine.connect() as connection:
        return pd.read_sql(query, connection)['name'].dropna().sort_values().tolist()


def fetch_filtered_data(start_date, end_date, bd_list=None, restaurant_list=None, order_ids=None):
    filters = [
        f"orders.created_at BETWEEN '{start_date}' AND '{end_date}'",
        """(orders.order_status = 'delivered' OR 
            (orders.order_status = 'canceled' AND 
                (orders.cancelation_reason IN ('R41', 'R42', 'R28') OR orders.cancelation_reason LIKE 'I%')
            )
        )""",
        "restaurants.id NOT IN (999, 1329)",
        "restaurants.name NOT LIKE 'Ethio-post%'"
    ]

    if bd_list:
        bd_str = ", ".join([f"'{bd}'" for bd in bd_list])
        filters.append(f"CONCAT(admins.f_name, '-', admins.l_name) IN ({bd_str})")

    if restaurant_list:
        rest_str = ", ".join([f"'{rest}'" for rest in restaurant_list])
        filters.append(f"restaurants.name IN ({rest_str})")

    if order_ids:
        ids_str = ", ".join([f"'{oid}'" for oid in order_ids])
        filters.append(f"orders.id IN ({ids_str})")

    where_clause = " AND ".join(filters)

    query = f"""
    SELECT
        orders.id,
        orders.created_at,
        restaurants.name,
        JSON_Extract(order_details.food_details, "$.name") AS product,
        order_details.price,
        order_details.quantity,
        orders.order_status,
        categories.name AS category,
        CONCAT(admins.f_name, '-', admins.l_name) AS bd_name,
        orders.delivery_charge
    FROM orders
        JOIN restaurants ON restaurants.id = orders.restaurant_id
        LEFT JOIN restaurant_fee_details fee ON fee.order_id = orders.id
        LEFT JOIN order_details ON order_details.order_id = orders.id
        LEFT JOIN categories ON categories.id = restaurants.category_id
        LEFT JOIN admins ON admins.id = restaurants.business_developer_id
    WHERE {where_clause}
    GROUP BY order_details.id
    ORDER BY orders.created_at ASC;
    """

    with engine.connect() as connection:
        return pd.read_sql(query, connection)
    
def fetch_data_to_download():
    """
    Fetch data for R47
    """
    query = """
            
        
SELECT
    orders.id,
    res.name,
    orders.created_at,
    orders.order_amount,
    orders.coupon_discount_amount,
    orders.restaurant_discount_amount,
    orders.delivery_charge,

    rfd.total_price,
    rfd.quantity,
    rfd.restaurant_discount,
    rfd.restaurant_discount_on_food,
    rfd.beu_discount,
    rfd.beu_discount_on_food,
    rfd.price_after_restaurant_discount,
    rfd.restaurant_fee,
    rfd.commission_value,

    orders.order_status,
    orders.cancelation_reason,
    orders.service_charge,

    res.comission,

    users.id AS user_id,
    users.app_language,
    users.phone,

    orders.created_by,
    orders.language_pref_fee,

    orders.delivery_address ->> '$.dz_name' AS customer_district,
    orders.delivery_address ->> '$.address' AS customer_addresses,

    dz.name AS restaurant_district,

    CONCAT(admins.f_name, ' ', admins.l_name) AS `BD NAME`,

    CASE
        WHEN admins.f_name IN (
            'Wase',
            'Yohannes',
            'Chernet',
            'Abreham',
            'Bereket',
            'Haregewyn'
        ) THEN 'Team 1'

        WHEN admins.f_name IN (
            'Mifta',
            'Meseret',
            'Abel',
            'Rekik'
        ) THEN 'Team 2'

        ELSE 'NO TEAM'
    END AS Team

FROM orders

JOIN users
    ON users.id = orders.user_id

JOIN restaurants res
    ON res.id = orders.restaurant_id

JOIN restaurant_fee_details rfd
    ON rfd.order_id = orders.id

JOIN delivery_zones dz
    ON dz.id = res.z_id

JOIN admins
    ON admins.id = res.business_developer_id

WHERE DATE(orders.created_at)
    BETWEEN '2026-04-01' AND '2026-04-30'

AND orders.order_status = 'canceled'
;





  



    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_ontime():
    """
    Fetch data Did not order after cancellation 
    """
    query = """
       
    SELECT
        CASE
            WHEN (orders.delivery_distance < 6 AND TIMESTAMPDIFF(SECOND, orders.placed_at, orders.delivered) / 60 > 59) THEN 'late_60'
            WHEN (orders.delivery_distance >= 6 AND TIMESTAMPDIFF(SECOND, orders.placed_at, orders.delivered) / 60 > 90) THEN 'late_90'
            ELSE 'ontime'
        END AS delivery_status,
        COUNT(*) AS order_count
    FROM orders
    JOIN restaurants ON restaurants.id = orders.restaurant_id
    WHERE
        orders.order_status = 'delivered'
        AND orders.created_at >= 	DATE_FORMAT(NOW(), '%Y-%m-01')
            AND orders.created_at < LAST_DAY(NOW()) + INTERVAL 1 DAY
        AND restaurants.store_type != 'courier'
        AND restaurant_id NOT IN (
            317, 1202, 39, 315, 316, 319,
            1221, 1477, 1509, 1527, 348, 46, 387
        )
    GROUP BY
        CASE
            WHEN (orders.delivery_distance < 6 AND TIMESTAMPDIFF(SECOND, orders.placed_at, orders.delivered) / 60 > 59) THEN 'late_60'
            WHEN (orders.delivery_distance >= 6 AND TIMESTAMPDIFF(SECOND, orders.placed_at, orders.delivered) / 60 > 90) THEN 'late_90'
            ELSE 'ontime'
        END;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_all_cancellation_byorder():
    """
        telebirr-ussd paid, edited and delivered
    """
    query = """
    SELECT
        date(orders.placed_at) order_Date,
        (orders.created_at) as order_time,
        CONCAT(admins.f_name, ' ', admins.l_name) AS 'BD NAME',
         CAST(orders.id AS CHAR) AS order_id,
        restaurants.name as res_name,
        cancellation_reasons.message as cancelation_reason

    from orders
    left join restaurants on restaurants.id = orders.restaurant_id
    join cancellation_reasons  on cancellation_reasons.id = orders.cancelation_reason
    join admins on admins.id = restaurants.business_developer_id
    where
        date(orders.created_at)  >= CURDATE() - INTERVAL 1 MONTH
        and orders.order_status = 'canceled'
        and orders.restaurant_id not in(999, 1329)
        and (
            cancellation_reasons.message like '(Restaurant)%' or orders.cancelation_reason in ('C5', 'C2', 'C7', 'C8', 'R15')
        ) 
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_failed_order():
    """
    Fetch data Did not order after cancellation 
    """
    query = """
        WITH failed_orders_ranked AS (
            SELECT
                o.id,
                o.user_id,
                o.order_amount,
                r.name AS restaurant_name,
                o.created_at,
                o.payment_method,

                ROW_NUMBER() OVER (
                    PARTITION BY o.user_id
                    ORDER BY o.created_at DESC
                ) AS rn,

                COUNT(*) OVER (
                    PARTITION BY o.user_id, DATE(o.created_at)
                ) AS failed_order_count_on_date

            FROM orders o
            JOIN restaurants r 
                ON r.id = o.restaurant_id
            WHERE DATE(o.created_at) >= CURDATE() - INTERVAL 1 MONTH
            AND o.order_status = 'Failed'
        ),
        delivered_orders AS (
            SELECT
                o.id,
                o.user_id,
                o.order_amount,
                r.name AS restaurant_name,
                o.created_at,
                o.order_status,
                cr.message AS cancellation_reasons
            FROM orders o
            JOIN restaurants r 
                ON r.id = o.restaurant_id
            LEFT JOIN cancellation_reasons cr 
                ON cr.id = o.cancelation_reason
            WHERE DATE(o.created_at) >= CURDATE() - INTERVAL 1 MONTH
            AND o.order_status != 'Failed'
        )
        SELECT
            u.f_name,
            u.phone,
            DATE(fo.created_at) AS order_Date,

            CAST(fo.id AS CHAR) AS failed_order_id,
            fo.order_amount AS failed_order_amount,
            fo.restaurant_name AS failed_restaurant,
            fo.created_at AS failed_date,
            fo.payment_method AS failed_payment_method,
            fo.failed_order_count_on_date,   -- ✅ per-day count

            CAST(do.id AS CHAR) AS delivered_order_id,
            do.order_amount AS delivered_order_amount,
            do.restaurant_name AS delivered_restaurant,
            do.created_at AS delivered_date,
            do.order_status,
            do.cancellation_reasons

        FROM failed_orders_ranked fo
        JOIN users u 
            ON fo.user_id = u.id
        LEFT JOIN delivered_orders do 
            ON do.user_id = u.id
        AND DATE(do.created_at) >= DATE(fo.created_at)

        WHERE fo.rn = 1
        # AND do.id IS NULL
        ORDER BY u.id;

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_campaing_code(code, date):
    query = """
        SELECT 
            o.user_id,
            MIN(o.id) AS example_order_id,
            MIN((
                SELECT MIN(h.created_at)
                FROM history_orders h
                JOIN orders o2 ON o2.id = h.order_id
                WHERE o2.user_id = o.user_id
            )) AS first_order_date,
            CASE 
                WHEN DATE((
                    SELECT MIN(h.created_at)
                    FROM history_orders h
                    JOIN orders o2 ON o2.id = h.order_id
                    WHERE o2.user_id = o.user_id
                )) = %s THEN 'Yes'
                ELSE 'No'
            END AS is_new_user,
            COUNT(o.id) AS order_count
        FROM orders o
        WHERE o.coupon_code = %s
          AND DATE(o.created_at) = %s
          AND o.order_status = 'delivered'
        GROUP BY o.user_id;
    """

    with engine.connect() as connection:
        # date is passed twice: once for is_new_user check, once for order filter
        result = pd.read_sql(query, connection, params=(date, code, date))

    return result


def fetch_data_driver_rating():
    query = """
       SELECT 
            date(d_m_reviews.created_at) order_Date,
            CONCAT(delivery_men.f_name, " ", delivery_men.l_name) AS driver_name,
            cast(d_m_reviews.order_id AS CHAR) AS order_id,
            d_m_reviews.rating,
            d_m_reviews.comment
        FROM d_m_reviews
        JOIN delivery_men 
            ON d_m_reviews.delivery_man_id = delivery_men.id
        WHERE d_m_reviews.comment IS NOT NULL
        AND TRIM(d_m_reviews.comment) <> ''
        AND d_m_reviews.comment <> 'No comment'
        And date(d_m_reviews.created_at) >= CURDATE() - INTERVAL 1 MONTH
        ORDER BY d_m_reviews.order_id DESC
    """



    with engine.connect() as connection:
        # date is passed twice: once for is_new_user check, once for order filter
        result = pd.read_sql(query, connection)
    return result


def fetch_data_m_pesa_edited():
    """
        Mpessa paid, edited and delivered
    """
    query = """
    
    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        if(
            users.l_name is null,
            users.f_name,
            concat(users.f_name, " ", users.l_name)
        ) Customer,
        users.phone,
        orders.order_amount,
        customer_transactions.order_amount user_paid,
        orders.tip,
        orders.payment_method,
        orders.payment_status,
        orders.cancelation_reason,
        cancellation_reasons.message
            
        #   orders.cancelation_note,
        #   orders.order_status
    from
    orders
        join users on users.id = orders.user_id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        left join customer_transactions on customer_transactions.order_id = orders.id
        
    where
        date(orders.placed_at) >= CURDATE() - INTERVAL 1 MONTH
        and orders.payment_method = 'm-pesa'
        and orders.order_status = 'delivered'
        and orders.payment_status != 'unpaid'
        and orders.edited = 1
        ;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_m_pesa_canceled():
    """
    Mpessa paid but canceled

    """
    query = """
  
    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        if(
            users.l_name is null,
            users.f_name,
            concat(users.f_name, " ", users.l_name)
        ) Customer,
        users.phone,
        orders.order_amount,
        customer_transactions.order_amount user_paid,
        orders.tip,
        orders.payment_method,
        orders.payment_status,
        orders.cancelation_reason,
        cancellation_reasons.message
            
        #   orders.cancelation_note,
        #   orders.order_status
    from
    orders
        join users on users.id = orders.user_id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        left join customer_transactions on customer_transactions.order_id = orders.id
        
    where
        date(orders.placed_at) >= CURDATE() - INTERVAL 1 MONTH
        and orders.payment_method = 'm-pesa'
        and orders.order_status = 'canceled'
        and orders.payment_status != 'unpaid'
        #   and orders.id = 1627441
        #   and users.phone = '+251910861386'
        #   and cancellation_reasons.message like "%Incomplete%"
        ;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_failed_transactions():
    """
    Mpessa paid but canceled

    """
    query = """
  
    select
        date(delivery_man_transactions.created_at) order_Date,
        delivery_man_transactions.created_at order_time,
        concat(delivery_men.f_name," ",delivery_men.l_name) Driver_name,
        delivery_man_transactions.deposit_amount,
        delivery_men.phone,
        delivery_man_transactions.msisdn,
        delivery_man_transactions.transaction_status
        

    from delivery_men
    join delivery_man_transactions on delivery_men.id = delivery_man_transactions.delivery_man_id

    where delivery_man_transactions.transaction_status = "SESSION-CREATED"
        and delivery_man_transactions.created_at  >= CURDATE() - INTERVAL 1 MONTH
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

# def fetch_retention():
#     """
#     retention
#     """
#     # Calculate previous month in 'YYYY-MM' format using pandas (no additional imports)
#     today = pd.Timestamp.today()
#     first_of_this_month = today.replace(day=1)
#     prev_month_last_day = first_of_this_month - pd.Timedelta(days=1)
#     prev_month_str = prev_month_last_day.strftime("%Y-%m")

#     query = f"""    
#         # User retention
#         WITH
#         first_orders AS (
#             -- Get the first order date for each user
#             SELECT
#             user_phone,
#             MIN(DATE(created_at)) AS first_order_date
#             FROM
#             history_orders
#             GROUP BY 
#             user_phone
#         ),
#         new_users_by_month AS (
#             -- Find the first order month for each user
#             SELECT
#             user_phone,
#             DATE_FORMAT(first_order_date, '%Y-%m') AS first_order_month
#             FROM
#             first_orders
#         ),
#         orders_by_month AS (
#             -- Get all orders grouped by user and month
#             SELECT
#             user_phone,
#             DATE_FORMAT(DATE(created_at), '%Y-%m') AS order_month
#             FROM
#             history_orders
#         ),
#         new_user_counts AS (
#             -- Get the number of new users in each month (Month 0)
#             SELECT
#             first_order_month,
#             COUNT(DISTINCT user_phone) AS new_users
#             FROM
#             new_users_by_month
#             GROUP BY
#             first_order_month
#         )
#         SELECT
#         new_users.first_order_month AS "New Users Month",
#         orders.order_month AS "Retention Month",
#         COUNT(DISTINCT orders.user_phone) AS "Retained Users",
#         round(
#             COUNT(DISTINCT orders.user_phone) / new_user_counts.new_users  * 100
#         ,1) AS "Retention Rate (%)"
#         FROM
#         new_users_by_month new_users
#         LEFT JOIN orders_by_month orders ON new_users.user_phone = orders.user_phone
#         JOIN new_user_counts ON new_users.first_order_month = new_user_counts.first_order_month
#         WHERE
#         orders.order_month >= new_users.first_order_month
#         and new_users.first_order_month = '{prev_month_str}'
#         GROUP BY
#         new_users.first_order_month,
#         orders.order_month,
#         new_user_counts.new_users
#         ORDER BY
#         new_users.first_order_month,
#         orders.order_month;
#         #   User Retention
#     """
    
#     with engine.connect() as connection:
#         result = pd.read_sql(query, connection)
#     return result

def fetch_new_user():
    """
    Mpessa paid but canceled

    """
    query = """
        WITH new_users_daily AS (
            SELECT 
                DATE(MIN(ho.created_at)) AS order_Date,
                ho.user_phone
            FROM 
                history_orders ho
            LEFT JOIN orders 
                ON orders.id = ho.order_id
            LEFT JOIN users 
                ON users.id = orders.user_id
            
            GROUP BY 
                ho.user_phone
        )
        SELECT 
            order_Date,
            COUNT(*) AS new_users,
            SUM(COUNT(*)) OVER (ORDER BY order_Date) AS cumulative_new_users
        FROM 
            new_users_daily
        WHERE 
            order_Date >= DATE_FORMAT(CURDATE(), '%Y-%m-01')  -- from month start
            AND order_date <= CURDATE()
        GROUP BY 
            order_date
        ORDER BY 
            order_date;
                    
          
                    
            
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

# >= CURDATE() - INTERVAL 1 MONTH
# date(orders.placed_at) order_Date,

def fetch_today_order():
    """
    Mpessa paid but canceled

    """
    query = """
        select
            users.f_name,
            users.phone,
            count(orders.id)
        from orders
        join users on users.id = orders.user_id

        where date(orders.created_at) = CURDATE()
            and orders.order_status = "delivered"
        group by users.id;
        
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_cancel_no_order():
    """
    Mpessa paid but canceled

    """
    query = """
        SELECT 
            date(o.placed_at) order_Date,
            CAST(o.id AS CHAR) AS order_id,
            o.user_id,
            u.f_name,
            u.phone,
            DATE(o.created_at) AS order_date,
            COUNT(o.id) AS canceled_orders,
            max(o.created_at) AS order_time,
            max(o.canceled) as order_cancle_time,
            o.order_amount,
            cr.message
            
        FROM orders o
        JOIN users u ON u.id = o.user_id
        join cancellation_reasons cr on cr.id = o.cancelation_reason
        WHERE 
            o.order_status = 'canceled'
            AND DATE(o.created_at)  >= CURDATE() - INTERVAL 1 MONTH
            AND TIMESTAMPDIFF(MINUTE, o.created_at, o.canceled) > 30
            -- ✅ Ensure they did NOT have any delivered order AFTER this canceled one on the same day
            AND NOT EXISTS (
                SELECT 1 
                FROM orders o2
                WHERE 
                    o2.user_id = o.user_id
                    AND DATE(o2.created_at) = DATE(o.created_at)
                    AND o2.order_status != 'canceled'
                    AND o2.created_at > o.created_at
            )
        GROUP BY 
            o.user_id, DATE(o.created_at)
        ORDER BY 
            order_date DESC;
        
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_pos_orders():
    """
   Normal pos orders

    """
    query = """
        SELECT
            date(orders.placed_at) order_Date,
            CONCAT(admins.f_name, ' ', admins.l_name) AS created_by,
            sum(orders.pos_discount_amount),
            count(orders.id)
            
        FROM orders
        JOIN admins  ON admins.id = orders.created_by
        WHERE DATE(orders.created_at) >= CURDATE() - INTERVAL 1 MONTH
        and orders.created_by > 0
        GROUP BY
            order_Date,
            admins.id;

        
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_order_after_4_30():
    """
    Fetch data for Order after 20:00:00
    """
    query = """
                  
    select
        date(o.placed_at) order_Date,
        CAST(o.id AS CHAR) AS order_id,
        o.order_amount,
        o.coupon_discount_title,
        o.coupon_discount_amount,
       (o.placed_at),
        o.order_status,
        cr.message,
        r.name as r_name,
        dz.name as area,
        concat(admins.f_name," ",admins.l_name)


        from orders o
        left join cancellation_reasons cr on cr.id = o.cancelation_reason
        join restaurants r on r.id = o.restaurant_id
        join delivery_zones dz on dz.id = r.z_id
        join admins on admins.id = r.business_developer_id
        where
        
        date(o.created_at) >= CURDATE() - INTERVAL 1 MONTH
        
        and time(o.created_at) > "22:30:00";



    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

# date(orders.placed_at) order_Date,
def fetch_data_cancled_on_not_samed_date():
    """
    ccancled order not on the same date 
    """
    query = """
                  
        SELECT
        
            orders.id,
            date(orders.placed_at) order_Date,
            cr.message as cancelation_reason    ,
            orders.created_at,
            orders.canceled,
            CONCAT(a1.f_name, " ", a1.l_name) AS cancelled_by
        FROM orders
        LEFT JOIN admins a1 
            ON a1.id = orders.canceled_by
        JOIN cancellation_reasons cr  
            ON cr.id = orders.cancelation_reason
        WHERE DATE(orders.created_at) < DATE(orders.canceled)
        AND TIMESTAMPDIFF(HOUR, orders.created_at, orders.canceled) > 3
        AND DATE(orders.canceled) >= CURDATE() - INTERVAL 1 MONTH
        AND orders.order_status = 'canceled';


    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_cancled_after_22():
    """
    ccancled order not on the same date 
    """
    query = """
                  
                
        SELECT
            CAST(orders.id AS CHAR) AS order_number,
            orders.created_at,
            u.phone AS customer_phone,
            r.name AS restaurant_name,
            CONCAT(a1.f_name, " ", a1.l_name) AS cancelled_by,
            orders.canceled AS cancellation_time,
            cr.message AS cancellation_reason,
            orders.cancelation_note
        from orders      
        JOIN users u  ON u.id = orders.user_id
        JOIN restaurants r  ON r.id = orders.restaurant_id
        LEFT JOIN admins a1  ON a1.id = orders.canceled_by
        JOIN cancellation_reasons cr   ON cr.id = orders.cancelation_reason
        WHERE orders.order_status = 'canceled'
        AND (
                TIME(orders.canceled) >= '22:00:00' 
                OR TIME(orders.canceled) < '04:00:00'
            )
            
        AND orders.created_at >= DATE_FORMAT(NOW(), '%Y-%m-01') 
        AND orders.created_at < LAST_DAY(NOW()) + INTERVAL 1 SECOND    


    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_data_Assigned():
    """
    Fetch data for orders that have been assigned
    """
    query = """
                  
                
       SELECT
        CAST(o.id AS CHAR) AS order_id,
        res.name,
        o.order_type,
        DATE(o.created_at) AS order_Date,
        dz.name AS Res_location,
        o.delivery_address ->> '$.dz_name' AS Customer_location,
        o.delivery_distance,
        TIMESTAMPDIFF(MINUTE, o.created_at, o.accepted) AS prep_time_minutes,
        o.created_at,
        o.accepted,

        CASE 
            WHEN EXISTS (
                SELECT 1
                FROM order_details od
                JOIN food f ON f.id = od.food_id
                JOIN categories c ON c.id = f.category_id
                WHERE od.order_id = o.id
                AND (
                     c.id = 44
                    or c.parent_id = 44
                )
            ) THEN 1 ELSE 0
        END AS has_pizza

    FROM orders o

    LEFT JOIN delivery_men d ON d.id = o.delivery_man_id
    JOIN restaurants res  ON res.id = o.restaurant_id
    JOIN delivery_zones dz  ON dz.id = res.z_id

    WHERE 
        o.created_at >= CURDATE() - INTERVAL 1 MONTH
        AND o.order_status = 'delivered'
        AND o.is_assign = 1;   


    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_time_stamp():
    """
    Fetch data for orders that have been assigned
    """
    query = """
                  
                            
        SELECT 
   
            DATE(a_log.activated_at) AS order_Date,
            CONCAT(a.f_name, " ", a.l_name) AS res_name,

            a_log.activated_at,
            a_log.inactivated_at,

            TIMESTAMPDIFF(MINUTE, a_log.activated_at, a_log.inactivated_at) AS active_time

        FROM admin_active_duration_logs a_log
        JOIN admins a ON a.id = a_log.admin_id

        WHERE a_log.activated_at >= CURDATE() - INTERVAL 1 MONTH
         and  a.role_id = 4 
        ;

    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

def fetch_driver_bag_check(phone_number=None):
    """
    Fetch data for Drivers to check their active date in last 3 months.
    Optionally filter by phone number.
    
    Args:
        phone_number (str, optional): Driver's phone number to filter results
    """
    query = """
        SELECT 
            CONCAT(dm.f_name, " ", dm.l_name) AS full_name,
            dm.phone,
            COUNT(orders.id) AS total_orders,
            COUNT(DISTINCT DATE(orders.created_at)) AS days_worked
        FROM orders 
        JOIN delivery_men dm ON dm.id = orders.delivery_man_id
        WHERE 
            orders.order_status = "delivered"
            AND orders.created_at >= DATE_SUB(NOW(), INTERVAL 3 MONTH)
    """
    
    params = None
    if phone_number:
        query += " AND dm.phone = %s"
        params = (phone_number,)
    
    query += """
        GROUP BY dm.id, dm.phone, dm.f_name, dm.l_name
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection, params=params if params else None)
    return result


def fetch_customer_transactions_by_session(session_id):
    """
    Fetch customer transactions by session id.
    """
    query = """
    SELECT 
        customer_transactions.*
    FROM customer_transactions
    WHERE customer_transactions.session_id = %s
    """
    with engine.connect() as connection:
        result = pd.read_sql(query, connection, params=(session_id,))
    return result


def fetch_customer_transactions_by_session(session_id):
    """
    Fetch customer transactions by session id.
    """
    query = """
    SELECT 
    users.f_name,
    users.phone,
            customer_transactions.*
        FROM customer_transactions
    join users on users.id = customer_transactions.user_id
    WHERE customer_transactions.session_id = %s
    """
    with engine.connect() as connection:
        result = pd.read_sql(query, connection, params=(session_id,))
    return result

def fetch_Driver_transactions_by_session(session_id):
    """
    Fetch driver transactions by session id.
    """
    query = """
    SELECT 
      concat(dm.f_name," ",dm.l_name),
        dm.phone,
        delivery_man_transactions.*
         
    from delivery_man_transactions
    join delivery_men dm on dm.id = delivery_man_transactions.delivery_man_id
    WHERE delivery_man_transactions.session_id = %s
    """
    with engine.connect() as connection:
        result = pd.read_sql(query, connection, params=(session_id,))
    return result

def fetch_data_CRM_total(first_date, last_date):
    """
    Fetch CRM total data.
    """
    query = """
    SELECT
  concat(admins.f_name, " ", admins.l_name) admin_name,
  COUNT(orders.id) AS TotalOrdersPeragent,
  count(
    if(
      orders.order_status = 'delivered',
      orders.id,
      NULL
    )
  ) Deliveredperagent,
  count(
    if(
      orders.order_status = 'canceled'
      AND orders.cancelation_reason NOT IN ('C2', 'C6', 'C8', 'C7', 'R42', 'R25', 'R21'),
      orders.id,
      NULL
    )
  ) canceled,
  round(
    (
      count(
        if(
          orders.order_status = 'delivered',
          orders.id,
          NULL
        )
      ) / (
        count(
          if(
            orders.order_status = 'delivered',
            orders.id,
            NULL
          )
        ) + count(
          if(
            orders.order_status = 'canceled'
            AND orders.cancelation_reason NOT IN ('C2', 'C6', 'C8', 'C7', 'R42', 'R25', 'R21'),
            orders.id,
            NULL
          )
        )
      )
    ) * 100,
    2
  ) Conversion
  ,count(if(orders.order_type='delivery' and orders.order_status='delivered',orders.id,null)) as total_food_order,
  count(if(orders.restaurant_id=1561 and orders.order_status='delivered',orders.id,null)) as total_beu_indivdual_order
FROM
  orders
  JOIN admins ON admins.id = orders.created_by
  LEFT JOIN restaurants ON restaurants.id = orders.restaurant_id
  LEFT JOIN categories ON categories.id = restaurants.category_id
WHERE
  orders.created_by is not null
  AND orders.order_status != 'failed'
  AND date(orders.placed_at) BETWEEN %s AND %s
  AND orders.restaurant_id NOT IN (1329, 999, 1585, 1586, 1587, 1588, 1589, 1590)
  AND (
    orders.order_type = 'delivery'
    OR orders.restaurant_id = 1561
  )
GROUP BY
  orders.created_by
ORDER BY
  2 DESC;
    """
    with engine.connect() as connection:
        result = pd.read_sql(query, connection, params=(first_date, last_date))
    return result

def fetch_data_BD_report():
    """
    Fetch data for orders that have been assigned
    """
    query = """
                    
    SELECT 
        date(o.placed_at) order_Date,

        CONCAT(admin.f_name, ' ', admin.l_name) AS business_developer_name,        
        -- Active and inactive restaurant counts (Now capturing ALL restaurants)
        COUNT(DISTINCT IF(res.active = 0, res.id, NULL)) AS inactive_restaurants,
        COUNT(DISTINCT IF(res.active = 1, res.id, NULL)) AS active_restaurants,

        -- Order metrics 
        COUNT(IF(o.order_status = 'delivered', o.id, NULL)) AS total_delivered_orders,
        SUM(res_fee.commission_value) AS revenue,
        COUNT(DISTINCT IF(o.order_status = 'canceled' and o.cancelation_reason in (
            'c2', 'c5', 'c7', 'c8', 'R15', 'R16', 'R17', 'R18', 'R19', 'R20', 'R21', 'R22', 'R23',
            'R34', 'R35', 'R36', 'R37', 'R38', 'R39', 'R40', 'R48', 'R49', 'R50', 'R53', 'R54'
    ), o.id, NULL)) AS total_cancelled_orders,
        -- Restaurant cancellation reasons
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'C2', o.id, NULL)) AS `Restaurant didnt prepare item on time.`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'C5', o.id, NULL)) AS `Restaurant didnt receive the order properly`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'C7', o.id, NULL)) AS `BD didn't pass this order to the restaurant`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'C8', o.id, NULL)) AS `Restaurant did not prepare food after confirmed`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R15', o.id, NULL)) AS `Restaurant is closed | Before`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R16', o.id, NULL)) AS `(Restaurant) Restauran's packaging problem | BEFORE`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R17', o.id, NULL)) AS `(Restaurant) restaurant that are not working with us | BEFORE`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R18', o.id, NULL)) AS `(Restaurant) Item not available | BEFORE`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R19', o.id, NULL)) AS `(Restaurant) Restaurant not picking up the phone | BEFORE`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R20', o.id, NULL)) AS `(Restaurant) Wrong number of restaurant`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R21', o.id, NULL)) AS `(Restaurant) No electricity | BEFORE`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R22', o.id, NULL)) AS `(Restaurant) Order will be late on restaurant | BEFORE`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R23', o.id, NULL)) AS `(Restaurant) Wrong Number`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R34', o.id, NULL)) AS `(Restaurant) It's not working hour of the restaurants | AFTER`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R35', o.id, NULL)) AS `(Restaurant) Restauran's packaging problem | AFTER`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R36', o.id, NULL)) AS `(Restaurant) restaurant that are not working with us | AFTER`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R37', o.id, NULL)) AS `(Restaurant) Item not available | AFTER`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R38', o.id, NULL)) AS `(Restaurant) Restaurant not picking up the phone | AFTER`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R39', o.id, NULL)) AS `(Restaurant) No electricity | AFTER`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R40', o.id, NULL)) AS `(Restaurant) Order will be late on restaurant | AFTER`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R48', o.id, NULL)) AS `(Restaurant) Restaurant changed price | BEFORE`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R49', o.id, NULL)) AS `(Restaurant) Restaurant asking for payment | BEFORE`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R50', o.id, NULL)) AS `(Restaurant) Restaurant under renovation | BEFORE`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R53', o.id, NULL)) AS `(Restaurant) asking for pad`,
        COUNT(DISTINCT IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R54', o.id, NULL)) AS `(Restaurant) quality issue`
            
    FROM admins admin
    JOIN restaurants res ON admin.id = res.business_developer_id
    JOIN orders o ON res.id = o.restaurant_id AND DATE(o.created_at) >= CURDATE() - INTERVAL 1 MONTH
    LEFT JOIN restaurant_fee_details res_fee ON res_fee.order_id = o.id
    LEFT JOIN cancellation_reasons ca ON ca.id = o.cancelation_reason

    GROUP BY admin.id, date(o.placed_at)
    ORDER BY admin.id;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

# >= CURDATE() - INTERVAL 1 MONTH
# date(orders.placed_at) order_Date,


def fetch_data_starpay_canceled():
    """
    telebirr paid but canceled

    """
    query = """
  
    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        if(
            users.l_name is null,
            users.f_name,
            concat(users.f_name, " ", users.l_name)
        ) Customer,
        users.phone,
        orders.order_amount,
        customer_transactions.order_amount user_paid,
        orders.tip,
        orders.payment_method,
        orders.payment_status,
        orders.cancelation_reason,
        cancellation_reasons.message
            
        #   orders.cancelation_note,
        #   orders.order_status
    from
    orders
        join users on users.id = orders.user_id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        left join customer_transactions on customer_transactions.order_id = orders.id
        
    where
        date(orders.placed_at) >= CURDATE() - INTERVAL 1 MONTH
        and orders.payment_method = 'starpay'
        and orders.order_status = 'canceled'
        and orders.payment_status != 'unpaid'
        ;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result
def fetch_data_starpay_edited():
    """
        telebirr paid, edited and delivered
    """
    query = """
    
    select
        CAST(orders.id AS CHAR) AS "order ID",
        date(orders.placed_at) order_Date,
        if(
            users.l_name is null,
            users.f_name,
            concat(users.f_name, " ", users.l_name)
        ) Customer,
        users.phone,
        orders.order_amount,
        customer_transactions.order_amount user_paid,
        orders.tip,
        orders.payment_method,
        orders.payment_status,
        orders.cancelation_reason,
        cancellation_reasons.message
            
        #   orders.cancelation_note,
        #   orders.order_status
    from
    orders
        join users on users.id = orders.user_id
        left join cancellation_reasons on cancellation_reasons.id = orders.cancelation_reason
        left join customer_transactions on customer_transactions.order_id = orders.id
        
    where
        date(orders.placed_at) >= CURDATE() - INTERVAL 1 MONTH
        and orders.payment_method = 'starpay'
        and orders.order_status = 'delivered'
        and orders.payment_status != 'unpaid'
        and orders.edited = 1
        ;
    """
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result
