from fastapi import APIRouter, Request

router = APIRouter(tags=["restaurant"])


@router.post("/restaurant/sales-details", summary="Sales details")
async def get_sales_details(request: Request):
    return {
        "status": "success",
        "data": {"outlet_code": "FNPCKS82QS", "billed_orders": 122, "restaurant_revenue": 8812.05, "orders_value": 11884.0, "GMV": 8895.0, "AOV": 71.29772157628572, "breakfast_orders": 5, "lunch_orders": 20, "dinner_orders": 53, "snacks_orders": 44, "orders_from_new_customers": 64, "orders_from_repeat_customers": 58, "discount_amount": 4207.999999998, "outlet_visits": 1138, "item_page_showing_count": 470, "add_to_cart_count": 291, "placing_order_count": 122, "avg_rating": 3.5238095237142857, "new_customers_from_ads_count": 3, "repeat_customers_from_ads_count": 0, "impressions_count": 9142, "avg_prep_time": 0.0}
    }
