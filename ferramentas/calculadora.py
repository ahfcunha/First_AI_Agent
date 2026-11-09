from google.genai import types

def calcular(a, b, operacao):

    if operacao == "somar":
        return a + b

    elif operacao == "subtrair":
        return a - b

    elif operacao == "multiplicar":
        return a * b

    elif operacao == "dividir":

        if b == 0:
            return "Erro: divisão por zero."

        return a / b

    else:
        return "Operação não reconhecida."

# declaração das ferramentas
# explicação de o que cada uma faz e os argumentos que necessitam
DECLARACAO = types.FunctionDeclaration(
    name="calcular",

    description="Realiza operações matemáticas entre dois números.",

    parameters_json_schema={
        "type": "object",
        "properties": {
            "a": {
                "type": "number",
                "description": "Primeiro número."
            },
            "b": {
                "type": "number",
                "description": "Segundo número."
            },
            "operacao": {
                "type": "string",
                "enum": [
                    "somar",
                    "subtrair",
                    "multiplicar",
                    "dividir"
                ],
                "description": "Operação matemática desejada."
            }
        },
        "required": ["a", "b", "operacao"]
    }
)