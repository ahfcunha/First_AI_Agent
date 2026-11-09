import requests
from google.genai import types

TIMEOUT = 10

# códigos WMO usados pela Opne-Meteo, traduzidos
CODIGOS_CLIMA = {
    0: "céu limpo", 1: "predominantemente limpo", 2: "parcialmente nublado",
    3: "nublado", 45: "neblina", 48: "neblina com geada",
    51: "garoa fraca", 53: "garoa", 55: "garoa forte",
    61: "chuva fraca", 63: "chuva moderada", 65: "chuva forte",
    80: "pancadas de chuva fracas", 81: "pancadas de chuva moderadas",
    82: "pancadas de chuva fortes", 95: "trovoada",
    96: "trovoada com granizo", 99: "trovoada com granizo forte",
}

def buscar_coordenadas(cidade):
    resp = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": cidade, "count": 1, "language": "pt"},
        timeout=TIMEOUT
    )
    # verifica o código se status http da resposta a API
    resp.raise_for_status()
    resultados = resp.json().get("results")

    if not resultados:
        return {"erro": f"Cidade '{cidade}' não encontrada"}

    r = resultados[0]
    return {
        "cidade": r["name"],
        "pais": r.get("country"),
        "latitude": r["latitude"],
        "longitude": r["longitude"]
    }

def buscar_clima(latitude, longitude):
    resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,weather_code,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,"
                     "precipitation_probability_max,weather_code",
            "timezone": "auto",
            "forecast_days": 7,
        },
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    dados = resp.json()

    atual = dados["current"]
    diario = dados["daily"]

    previsao = []
    for i, data in enumerate(diario["time"]):
        previsao.append({
            "data": data,
            "condicao": CODIGOS_CLIMA.get(diario["weather_code"][i], "desconhecida"),
            "temp_min": diario["temperature_2m_min"][i],
            "temp_max": diario["temperature_2m_max"][i],
            "prob_chuva_%": diario["precipitation_probability_max"][i],
        })

    return {
        "agora": {
            "temperatura": atual["temperature_2m"],
            "condicao": CODIGOS_CLIMA.get(atual["weather_code"], "desconhecida"),
            "vento_kmh": atual["wind_speed_10m"],
        },
        "previsao_7_dias": previsao,
    }

DECLARACAO_COORDENADAS = types.FunctionDeclaration(
    name="buscar_coordenadas",
    description="Converte o nome de uma cidade em latitude e longitude. "
                "Necessário antes de consultar o clima.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "cidade": {"type": "string", "description": "Nome da cidade, ex.: 'São Paulo'."}
        },
        "required": ["cidade"],
    },
)
 
DECLARACAO_CLIMA = types.FunctionDeclaration(
    name="buscar_clima",
    description="Retorna o clima atual e a previsão dos próximos 7 dias "
                "para uma coordenada geográfica.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "latitude": {"type": "number", "description": "Latitude do local."},
            "longitude": {"type": "number", "description": "Longitude do local."},
        },
        "required": ["latitude", "longitude"],
    },
)