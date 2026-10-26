import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / 'agent')
)

from agent import agent
from datasets import dataset
from eval_models import model

from deepeval.metrics import StepEfficiencyMetric
from deepeval.integrations.langchain import CallbackHandler


metrics = [StepEfficiencyMetric(threshold=0.75, model=model, include_reason=True) ]

for golden in dataset.evals_iterator(metrics=metrics):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": golden.input}]},
        config={"configurable": {"thread_id": str(uuid4())},
        "callbacks": [CallbackHandler()]}
    )