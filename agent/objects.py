from pydantic import BaseModel, Field

class Answer(BaseModel):
    answer: str = Field(description="The answer that is needed for the user question.")
    conversation: bool = Field(description="This is indication to know if the conversation"\
                              "should still continue or no. If the agent has made the decision about the refund this should be false"\
                                "If the conversation still need more talk then it's true", default=True)

class PurchaseItem(BaseModel):
    name: str = Field(description="The name of the item that the user has purchased.")