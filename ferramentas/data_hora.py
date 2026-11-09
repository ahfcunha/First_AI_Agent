from datetime import datetime
from google.genai import types

DIAS = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
        "sexta-feira", "sábado", "domingo"]


def obter_data_hora():
    agora = datetime.now()
    return {
        "data": agora.strftime("%Y-%m-%d"),
        "hora": agora.strftime("%H:%M"),
        "dia_da_semana": DIAS[agora.weekday()],
    }


DECLARACAO = types.FunctionDeclaration(
    name="obter_data_hora",
    description="Retorna a data (AAAA-MM-DD), a hora e o dia da semana de hoje. "
                "Use sempre que precisar saber que dia é hoje ou calcular datas relativas "
                "como 'amanhã' ou 'sábado'.",
    parameters_json_schema={"type": "object", "properties": {}},
)