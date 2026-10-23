from langchain.tools import tool
from data import users_data
from dotenv import load_dotenv
import logging
from objects import PurchaseItem
from datetime import date

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s "
)

@tool
def get_user_purchase_history(user: str) -> dict:
    """This tool is used to get the purchase history of a user. 
    It takes the username as input and returns the purchase history of that user if exist."""
    logging.info(f"Getting purchase history for user: {user}")
    if users_data.get(user):
        return users_data[user] 
    return {"status": "There is not username found"}

@tool
def calculate_right_refund(user:str, items:list[PurchaseItem]) -> str:
    """This tool take a list of items to be returned and the username and will return how much the refund is worth"""

    logging.info(f"Calculating refund for user: {user} and items: {items}")
    if users_data.get(user):
        total_refund = 0
        for item in items:
            if users_data[user].get(item.name):
                total_refund += users_data[user][item.name]["price"]

        return f"The total refund for the items is: {total_refund}" 

    return {"status": "There is not username found"}

@tool
def issue_refund_ticket(user:str, refund_amount: int) -> str:
    """this tool will send a ticket to the right team to return the refund"""

    logging.info(f"using issue_refund_ticket for user: {user}")
    return f"a refund ticket has been issued successfully with the amount of {refund_amount}"

@tool
def get_today_date() -> str:
    """Return today's date in YYYY-MM-DD format
    This tool takes no arguments
    only use if a user exist and an item is present for refund"""
    logging.info(f"using the date tool")
    return date.today().isoformat()


# print(get_user_purchase_history.invoke({"user": "user126"}))
# print(calculate_right_refund.invoke(
#     {"user": "user126", "items": [
#         {"name": "lunch_box"},
#         {"name": "backpack"},
#         {"name": "water_bottle"}
#         ]
#     }
# ))

# print(issue_refund_ticket.invoke({"user": "user126", "refund_amount": 10}))
# print(get_today_date.invoke({}))