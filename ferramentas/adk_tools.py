''' O ADK monta o schema (fórmulario que indica ao modelo o que aquela ferramenta faz) da ferramenta a partir da assinatura da função 
(nomes, type hints) e da docstring, excluindo a necessidade de escrever FunctionDeclarations manualmenre'''

import functools

from . import calculadora, clima, data_hora, notas

# embrulha uma função, para caso ocorra algum erro na execução da ferramenta, não trave a aplicação
def _execucao_segura(funcao):
    #  faz interna herdar nome, docstring e type hints de funcao
    @functools.wraps(funcao)
    def interna(*args, **kwargs):
        try:
            return funcao(*args, **kwargs)
        except Exception as e:
            return {"erro": f"{type(e).__name__}: {e}"}
    return interna

@_execucao_segura
def calcular(a: float, b: float, operacao: str) -> dict:
    """Realiza uma operação matemática entre dois números.
 
    Args:
        a: Primeiro número.
        b: Segundo número.
        operacao: Uma entre "somar", "subtrair", "multiplicar" ou "dividir".
 
    Returns:
        Dicionário com o resultado da operação.
    """
    return {"resultado": calculadora.calcular(a, b, operacao)}

@_execucao_segura
def obter_data_hora() -> dict:
    """Retorna a data (AAAA-MM-DD), a hora e o dia da semana de hoje.
 
    Use sempre que precisar saber que dia é hoje ou calcular datas
    relativas como "amanhã" ou "sábado".
    """
    return data_hora.obter_data_hora()

@_execucao_segura
def buscar_coordenadas(cidade: str) -> dict:
    """Retorna a data (AAAA-MM-DD), a hora e o dia da semana de hoje.
 
    Use sempre que precisar saber que dia é hoje ou calcular datas
    relativas como "amanhã" ou "sábado".
    """
    return clima.buscar_coordenadas(cidade)

@_execucao_segura
def buscar_clima(latitude: float, longitude: float) -> dict:
    """Retorna o clima atual e a previsão dos próximos 7 dias para uma coordenada.
 
    Args:
        latitude: Latitude do local.
        longitude: Longitude do local.
    """
    return clima.buscar_clima(latitude, longitude)

@_execucao_segura
def salvar_nota(titulo: str, conteudo: str) -> dict:
    """Salva uma nova nota com título e conteúdo.
 
    Args:
        titulo: Título curto da nota.
        conteudo: Texto da nota.
    """
    return notas.salvar_nota(titulo, conteudo)

@_execucao_segura
def listar_notas() -> dict:
    """Lista todas as notas, com id, título e conteúdo"""
    return notas.listar_notas()

@_execucao_segura
def apagar_nota(id_nota: int) -> dict:
    """Apaga uma nota pelo id. Se não souber o id, use listar_notas primeiro.
 
    Args:
        id_nota: Id da nota a apagar.
    """
    return notas.apagar_nota(id_nota)

FERRAMENTAS_ADK = [calcular, obter_data_hora, buscar_coordenadas, buscar_clima, salvar_nota, listar_notas, apagar_nota]