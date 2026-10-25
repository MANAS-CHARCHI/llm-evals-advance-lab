import json
import os
from datetime import datetime
from langchain_core.messages import AIMessage

LOG_FILE = "conversation_logs.jsonl"

def extract_tokens_and_tools(messages: list) -> dict:
    """Extracts input/output tokens and tool calls from all AIMessages in this turn."""
    input_tokens = 0
    output_tokens = 0
    tools_called = []

    for msg in messages:
        if isinstance(msg, AIMessage):
            # Extract token usage from LangChain metadata
            usage = getattr(msg, "usage_metadata", None)
            if usage:
                input_tokens += usage.get("input_tokens", 0)
                output_tokens += usage.get("output_tokens", 0)
            elif hasattr(msg, "response_metadata") and "usage" in msg.response_metadata:
                u = msg.response_metadata["usage"]
                input_tokens += u.get("input_tokens", 0)
                output_tokens += u.get("output_tokens", 0)
            # Extract any tools the model decided to execute
            if getattr(msg, "tool_calls", None):
                for tc in msg.tool_calls:
                    tools_called.append({
                        "name": tc.get("name"),
                        "args": tc.get("args")
                    })

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "tools_called": tools_called
    }

def log_turn(
    conversation_id: str,
    turn: int,
    user_question: str,
    model_response: str,
    turn_messages: list,
    cumulative_tokens: int,
    log_file: str = LOG_FILE
) -> int:
    """Appends an interaction record to the JSONL log file and returns updated cumulative tokens."""
    token_data = extract_tokens_and_tools(turn_messages)
    new_cumulative = cumulative_tokens + token_data["total_tokens"]

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "conversation_id": conversation_id,
        "turn": turn,
        "user_question": user_question,
        "model_response": model_response,
        "tools_called": token_data["tools_called"],
        "tokens": {
            "input_tokens": token_data["input_tokens"],
            "output_tokens": token_data["output_tokens"],
            "turn_total_tokens": token_data["total_tokens"]
        },
        "session_cumulative_tokens": new_cumulative
    }
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
    return new_cumulative