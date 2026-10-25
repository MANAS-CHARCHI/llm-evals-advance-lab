from models import model
from tools import get_user_purchase_history, calculate_right_refund, issue_refund_ticket, get_today_date
from dotenv import load_dotenv
from langchain.agents import create_agent
from prompts import agent_system_prompt
from objects import Answer
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from uuid import uuid4
from logger import log_turn

load_dotenv()

agent = create_agent(
    model=model,
    system_prompt=agent_system_prompt,
    tools = [get_user_purchase_history, calculate_right_refund, issue_refund_ticket, get_today_date],
    response_format=Answer,
    checkpointer=InMemorySaver()
)

EXIT_WORDS = {"exit", "quit", "no", "bye", "stop", "done", "cancel"}

def run_conversation():
    conversation_id = str(uuid4())
    config = {
        "configurable": {"thread_id": conversation_id}, 
        "recursion_limit": 8
    }
    initial_user_prompt = "I would like to request a refund"
    question = HumanMessage(content = initial_user_prompt)
    current_user_text = initial_user_prompt
    conversation = True
    turn_count = 0
    max_turns = 6
    prev_msg_count = 0
    cumulative_tokens = 0
    print(f"[Session Started] ID: {config["configurable"]["thread_id"]}\n")
    while conversation and turn_count < max_turns:
        try:
            response = agent.invoke({"messages": [question]}, config=config)
            turn_count += 1
            answer = response["structured_response"]

            # Get only the new messages created in this turn
            all_messages = response.get("messages", [])
            turn_messages = all_messages[prev_msg_count:]
            prev_msg_count = len(all_messages)

            # Log to file
            cumulative_tokens = log_turn(
                conversation_id=conversation_id,
                turn=turn_count,
                user_question=current_user_text,
                model_response=answer.answer,
                turn_messages=turn_messages,
                cumulative_tokens=cumulative_tokens
            )
            print(answer.answer)
            conversation = answer.conversation
            if conversation:
                user_input = input("User: ")
                if user_input.strip().lower() in EXIT_WORDS:
                    print("Ending conversation. Goodbye!")
                    break
                question = HumanMessage(content = user_input)
        except Exception as e:
            print(f"\n[Error/Guardrail Triggered]: {e}")
            break
    print("The Job is Done!")

run_conversation()