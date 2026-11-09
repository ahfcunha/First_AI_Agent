import json
from pathlib import Path
from google.genai import types

# local onde as notas serão armazenadas
ARQUIVO = Path(__file__).parent/"notas.json"

def _carregar():
    if not ARQUIVO.exists():
        return []
    try:
        return json.loads(ARQUIVO.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    
def _salvar(notas):
    ARQUIVO.write_text(
        json.dumps(notas, ensure_ascii=False, indent=2), encoding="utf-8"
    )

def salvar_nota(titulo, conteudo):
    notas = _carregar()
    novo_id = max((n["id"] for n in notas), default=0) + 1
    notas.append({"id": novo_id, "titulo": titulo, "conteudo": conteudo})
    _salvar(notas)
    return {"status": "nota salva", "id": novo_id}

def listar_notas():
    return {"notas": _carregar()}

def apagar_nota(id_nota):
    notas = _carregar()
    restantes = [n for n in notas if n["id"] != id_nota]

    if len(restantes) == len(notas):
        return {"erro": f"Nota com id {id_nota} não existe."}

    _salvar(restantes)
    return {"status": "nota apagada", "id": id_nota}

DECLARACAO_SALVAR = types.FunctionDeclaration(
    name="salvar_nota",
    description="Salva uma nova nota com título e conteúdo.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "titulo": {"type": "string", "description": "Título curto da nota."},
            "conteudo": {"type": "string", "description": "Texto da nota."},
        },
        "required": ["titulo", "conteudo"],
    },
)
 
DECLARACAO_LISTAR = types.FunctionDeclaration(
    name="listar_notas",
    description="Lista todas as notas salvas, com id, título e conteúdo.",
    parameters_json_schema={"type": "object", "properties": {}},
)
 
DECLARACAO_APAGAR = types.FunctionDeclaration(
    name="apagar_nota",
    description="Apaga uma nota pelo id. Se não souber o id, use listar_notas primeiro.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "id": {"type": "integer", "description": "Id da nota a apagar."}
        },
        "required": ["id"],
    },
)