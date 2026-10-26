import os
from pathlib import Path
from deepeval.models import LiteLLMModel
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

model = LiteLLMModel(
    model="anthropic/claude-haiku-5-5",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=1,
)