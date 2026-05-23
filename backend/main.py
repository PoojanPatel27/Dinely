# Author: Dhaval Patel. Codebasics YouTube Channel

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper

app = FastAPI()

# Stores current session orders
inprogress_orders = {}


@app.post("/")
async def handle_request(request: Request):

    payload = await request.json()

    # Extract intent and parameters
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult'].get('outputContexts', [])

    # Safe session id extraction
    session_id = "default" 

    if len(output_contexts) > 0:
        session_id = generic_helper.extract_session_id(
            output_contexts[0]["name"]
        )

    print(f"Intent Detected: {intent}")
    print(f"Parameters: {parameters}")
    print(f"Session ID: {session_id}")

    # Updated intent mapping
    intent_handler_dict = {

        # New Order
        'new.order': new_order,
        'new order': new_order,

        # Add To Order
        'order.add': add_to_order,
        'add to order': add_to_order,
        'order.add - context: ongoing-order': add_to_order,

        # Remove From Order
        'order.remove': remove_from_order,
        'remove from order': remove_from_order,
        'order.remove - context: ongoing-order': remove_from_order,

        # Complete Order
        'order.complete': complete_order,
        'complete order': complete_order,
        'order.complete - context: ongoing-order': complete_order,

        # Track Order
        'track.order': track_order,
        'track order': track_order,
        'track.order - context: ongoing-tracking': track_order
    }

    # Intent validation
    if intent not in intent_handler_dict:
        return JSONResponse(content={
            "fulfillmentText": f"Intent '{intent}' is not configured in backend."
        })

    return intent_handler_dict[intent](parameters, session_id)


# ---------------- NEW ORDER ---------------- #

def new_order(parameters: dict, session_id: str):

    inprogress_orders[session_id] = {}

    fulfillment_text = (
        "Ok, starting a new order. "
        "You can say things like 'I want 2 pizzas and 1 biryani'."
    )

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


# ---------------- SAVE ORDER ---------------- #

def save_to_db(order: dict):

    next_order_id = db_helper.get_next_order_id()

    for food_item, quantity in order.items():

        rcode = db_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )

        if rcode == -1:
            return -1

    db_helper.insert_order_tracking(
        next_order_id,
        "in progress"
    )

    return next_order_id


# ---------------- COMPLETE ORDER ---------------- #

def complete_order(parameters: dict, session_id: str):

    if session_id not in inprogress_orders:

        fulfillment_text = (
            "I'm having trouble finding your order. "
            "Please start a new order."
        )

    else:

        order = inprogress_orders[session_id]

        if len(order.keys()) == 0:
            fulfillment_text = "Your order is empty!"

        else:

            order_id = save_to_db(order)

            if order_id == -1:

                fulfillment_text = (
                    "Sorry, I couldn't process your order "
                    "due to a backend error."
                )

            else:

                order_total = db_helper.get_total_order_price(order_id)

                fulfillment_text = (
                    f"Awesome! Your order has been placed successfully. "
                    f"Your order id is #{order_id}. "
                    f"Total amount is ₹{order_total}."
                )

        del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


# ---------------- ADD TO ORDER ---------------- #

def add_to_order(parameters: dict, session_id: str):

    food_items = parameters.get("food-item", [])
    quantities = parameters.get("number", [])

    # Convert single values into list
    if not isinstance(food_items, list):
        food_items = [food_items]

    if not isinstance(quantities, list):
        quantities = [quantities]

    if len(food_items) != len(quantities):

        fulfillment_text = (
            "Sorry, please specify food items "
            "with quantities clearly."
        )

    else:

        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_orders:

            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict

        else:

            inprogress_orders[session_id] = new_food_dict

        order_str = generic_helper.get_str_from_food_dict(
            inprogress_orders[session_id]
        )

        fulfillment_text = (
            f"So far you have ordered: {order_str}. "
            f"Do you need anything else?"
        )

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


# ---------------- REMOVE FROM ORDER ---------------- #

def remove_from_order(parameters: dict, session_id: str):

    if session_id not in inprogress_orders:

        return JSONResponse(content={
            "fulfillmentText":
            "I can't find your current order."
        })

    food_items = parameters.get("food-item", [])

    if not isinstance(food_items, list):
        food_items = [food_items]

    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:

        if item not in current_order:
            no_such_items.append(item)

        else:
            removed_items.append(item)
            del current_order[item]

    fulfillment_text = ""

    if len(removed_items) > 0:
        fulfillment_text += (
            f"Removed {', '.join(removed_items)} from your order. "
        )

    if len(no_such_items) > 0:
        fulfillment_text += (
            f"Items not found: {', '.join(no_such_items)}. "
        )

    if len(current_order.keys()) == 0:

        fulfillment_text += "Your order is now empty."

    else:

        order_str = generic_helper.get_str_from_food_dict(
            current_order
        )

        fulfillment_text += (
            f"Current order: {order_str}"
        )

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


# ---------------- TRACK ORDER ---------------- #

def track_order(parameters: dict, session_id: str):

    order_id = parameters.get('order_id')

    if not order_id:

        order_id = parameters.get('number')

    try:
        order_id = int(order_id)

    except:
        return JSONResponse(content={
            "fulfillmentText":
            "Please provide a valid order id."
        })

    order_status = db_helper.get_order_status(order_id)

    if order_status:

        fulfillment_text = (
            f"Your order status for order id "
            f"{order_id} is: {order_status}"
        )

    else:

        fulfillment_text = (
            f"No order found with order id {order_id}"
        )

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })