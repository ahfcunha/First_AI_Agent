import os
import sys
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

from google.adk.agents import Agent

from config import API_KEY, MODELO, SYSTEM_PROMPT
from ferramentas.adk_tools import FERRAMENTAS_ADK

os.environ.setdefault("GOOGLE_API_KEY", API_KEY)
root_agent = Agent(
    name="assistente",
    model=MODELO,
    instruction=SYSTEM_PROMPT,
    tools=FERRAMENTAS_ADK,
)