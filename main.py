from fsist_bot import FSistBot

if __name__ == "__main__":
    print("Iniciando automação FSist...")
    bot = FSistBot()
    try:
        bot.executar_fluxo_completo()
        print("Processo finalizado com sucesso.")
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        bot.fechar()
