from models import model
from tools import get_user_purchase_history, calculate_right_refund, issue_refund_ticket, get_today_date
from dotenv import load_dotenv
from langchain.agents import create_agent
from prompts import agent_system_prompt
from objects import Answer
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from uuid import uuid4

load_dotenv()

agent = create_agent(
    model=model,
    system_prompt=agent_system_prompt,
    tools = [get_user_purchase_history, calculate_right_refund, issue_refund_ticket, get_today_date],
    response_format=Answer,
    checkpointer=InMemorySaver()
)

def run_conversation():
    config = {"configurable": {"thread_id": str(uuid4())}}
    question = HumanMessage(content = "I would like to request a refund")
    conversation = True
    while conversation:
        response = agent.invoke({"messages": [question]}, config=config)
        answer = response["structured_response"]

        print(answer.answer)
        conversation = answer.conversation
        if conversation:
            user_input = input("User: ")
            question = HumanMessage(content = user_input)
    print("The Job is Done!")

run_conversation()