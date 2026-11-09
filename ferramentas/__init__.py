from google.genai import types
from . import calculadora, data_hora, clima, notas

# registro da ferramentas que o modelo poderá utilizar
FERRAMENTAS = {
    "calcular": calculadora.calcular,
    "obter_data_hora": data_hora.obter_data_hora,
    "buscar_coordenadas": clima.buscar_coordenadas,
    "buscar_clima": clima.buscar_clima,
    "salvar_nota": notas.salvar_nota,
    "listar_notas": notas.listar_notas,
    "apagar_nota": notas.apagar_nota,
}

# agrupa declaração dentro de um objeto Tool
TOOL = types.Tool(function_declarations=[
    calculadora.DECLARACAO,
    data_hora.DECLARACAO,
    clima.DECLARACAO_COORDENADAS,
    clima.DECLARACAO_CLIMA,
    notas.DECLARACAO_LISTAR,
    notas.DECLARACAO_SALVAR,
    notas.DECLARACAO_APAGAR
])

# recebe um objeto que contém as informações da solicitação pedida pelo modelo
def executar_ferramenta(chamada):

    print(f"\n[Agente] Utilizando ferramenta: {chamada.name}")

    if chamada.name not in FERRAMENTAS:
        raise ValueError("Ferramenta não encontrada")

    funcao = FERRAMENTAS[chamada.name]

    # transforma as chaves e os valores de um dicionário em argumentos nomeados de uma função
    try:
        resultado = funcao(**chamada.args)
    except Exception as e:
        resultado = {"erro": f"{type(e).__name__}: {e}"}

    print(f"[Agente] Resultado: {resultado}")

    return resultado