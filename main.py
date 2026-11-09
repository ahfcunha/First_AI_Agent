from agente import Agente

def main():
    agente = Agente()
    while True:
        mensagem = input("Faça sua pergunta: ").strip()
        if mensagem.lower() in ["sair", "exit"]:
            break
        if mensagem:
            print(agente.enviar_mensagem(mensagem))

if __name__ == "__main__":
    main()