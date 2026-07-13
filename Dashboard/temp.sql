SELECT 
    CONCAT(admin.f_name, ' ', admin.l_name) AS business_developer_name,
    admin.id AS business_developer_id,
    
    -- Active and inactive restaurant counts (Now capturing ALL restaurants)
    COUNT(DISTINCT IF(res.active = 0, res.id, NULL)) AS inactive_restaurants,
    COUNT(DISTINCT IF(res.active = 1, res.id, NULL)) AS active_restaurants,

    -- Order metrics 
    COUNT(IF(o.order_status = 'delivered', o.id, NULL)) AS total_delivered_orders,
    SUM(res_fee.commission_value) AS revenue,
    COUNT(IF(o.order_status = 'canceled' and o.cancelation_reason in (
        'c2', 'c5', 'c7', 'c8', 'R15', 'R16', 'R17', 'R18', 'R19', 'R20', 'R21', 'R22', 'R23',
        'R34', 'R35', 'R36', 'R37', 'R38', 'R39', 'R40', 'R48', 'R49', 'R50', 'R53', 'R54'
  ), o.id, NULL)) AS total_cancelled_orders,
    -- Restaurant cancellation reasons
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'C2', o.id, NULL)) AS `Restaurant didn’t prepare item on time.`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'C5', o.id, NULL)) AS `Restaurant didn’t receive the order properly`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'C7', o.id, NULL)) AS `BD didn't pass this order to the restaurant`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'C8', o.id, NULL)) AS `Restaurant did not prepare food after confirmed`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R15', o.id, NULL)) AS `Restaurant is closed | Before`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R16', o.id, NULL)) AS `(Restaurant) Restauran's packaging problem | BEFORE`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R17', o.id, NULL)) AS `(Restaurant) restaurant that are not working with us | BEFORE`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R18', o.id, NULL)) AS `(Restaurant) Item not available | BEFORE`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R19', o.id, NULL)) AS `(Restaurant) Restaurant not picking up the phone | BEFORE`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R20', o.id, NULL)) AS `(Restaurant) Wrong number of restaurant`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R21', o.id, NULL)) AS `(Restaurant) No electricity | BEFORE`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R22', o.id, NULL)) AS `(Restaurant) Order will be late on restaurant | BEFORE`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R23', o.id, NULL)) AS `(Restaurant) Wrong Number`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R34', o.id, NULL)) AS `(Restaurant) It's not working hour of the restaurants | AFTER`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R35', o.id, NULL)) AS `(Restaurant) Restauran's packaging problem | AFTER`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R36', o.id, NULL)) AS `(Restaurant) restaurant that are not working with us | AFTER`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R37', o.id, NULL)) AS `(Restaurant) Item not available | AFTER`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R38', o.id, NULL)) AS `(Restaurant) Restaurant not picking up the phone | AFTER`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R39', o.id, NULL)) AS `(Restaurant) No electricity | AFTER`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R40', o.id, NULL)) AS `(Restaurant) Order will be late on restaurant | AFTER`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R48', o.id, NULL)) AS `(Restaurant) Restaurant changed price | BEFORE`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R49', o.id, NULL)) AS `(Restaurant) Restaurant asking for payment | BEFORE`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R50', o.id, NULL)) AS `(Restaurant) Restaurant under renovation | BEFORE`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R53', o.id, NULL)) AS `(Restaurant) asking for pad`,
    COUNT(IF(o.order_status = 'canceled' AND o.cancelation_reason = 'R54', o.id, NULL)) AS `(Restaurant) quality issue`
        
FROM admins admin
JOIN restaurants res ON admin.id = res.business_developer_id
JOIN orders o ON res.id = o.restaurant_id AND DATE(o.created_at) >= CURDATE() - INTERVAL 1 MONTH
LEFT JOIN restaurant_fee_details res_fee ON res_fee.order_id = o.id
LEFT JOIN cancellation_reasons ca ON ca.id = o.cancelation_reason

GROUP BY admin.id 
-- HAVING revenue IS NOT NULL
ORDER BY admin.id;