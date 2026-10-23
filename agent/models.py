from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
model = init_chat_model(model="claude-haiku-5-5", max_tokens=100)

# response = model.invoke("tell me something about Earth in 2 line.")
# print(response.content)