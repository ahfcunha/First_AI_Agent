import time 
from google import genai
from google.genai import types
from ferramentas import TOOL, executar_ferramenta
from config import SYSTEM_PROMPT, MODELO, API_KEY, MAX_VOLTAS, DEBUG, NIVEL_PENSAMENTO

class Agente:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)
        self.historico = []
        self.config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[TOOL],
            thinking_config=types.ThinkingConfig(
                include_thoughts=DEBUG,           
                thinking_level=NIVEL_PENSAMENTO, 
            ),
        )

    def consultar_modelo(self):
        inicio = time.perf_counter()
        resposta = self.client.models.generate_content(
            model=MODELO,
            contents=self.historico,
            config=self.config
        )
        duracao = time.perf_counter() - inicio
 
        if DEBUG:
            self.mostrar_debug(resposta, duracao)
        return resposta

    def mostrar_debug(self, resposta, duracao):
        uso = resposta.usage_metadata
        pensamento = (uso.thoughts_token_count or 0) if uso else 0
        saida = (uso.candidates_token_count or 0) if uso else 0
        print(
            f"\n[Debug] Chamada ao modelo: {duracao:.1f}s | "
            f"tokens de pensamento: {pensamento} | tokens de saída: {saida}"
        )
 
        for parte in resposta.candidates[0].content.parts:
            if parte.thought and parte.text:
                print(f"[Pensamento] {parte.text}")


    def enviar_mensagem(self, mensagem):
        voltas = 0

        # parts é a lista de conteúdos daquela mensagem
        # Part representa cada conteudo individualmente (texto, imagem aúdio)
        self.historico.append(
            types.Content(
                role="user",
                parts=[types.Part(text=mensagem)]
            )
        )


        resposta = self.consultar_modelo()

        # verifica se o modelo solicitou alguma ferramenta
        while resposta.function_calls and voltas < MAX_VOLTAS:

            # armazena a mensagem de solicitação enviada pelo modelo
            self.historico.append(resposta.candidates[0].content)

            #  armazenará os resultados das ferramentas solicitadas
            partes_resposta = []

            for chamada in resposta.function_calls:

                resultado = executar_ferramenta(chamada)

                #  transforma o resultado python em em uma mensagem que o modelo consegue interpretar como retorno da ferramenta 
                partes_resposta.append(
                    types.Part.from_function_response(
                        name=chamada.name,
                        response={
                            "result": resultado
                        }
                    )
                )

            # coloca o retorno das funções no histórico
            self.historico.append(
                types.Content(
                    role="user",
                    parts=partes_resposta
                )
            )

            # consulta novamente o modelo
            resposta = self.consultar_modelo()

            voltas += 1

        # armazena a resposta final do modelo no histórico
        self.historico.append(
            types.Content(
                role="model",
                parts=[types.Part(text=resposta.text)]
            )
        )

        return resposta.text
