from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
from config import FSIST_URL, USUARIO, SENHA
import os
import zipfile
import shutil

class FSistBot:
    def __init__(self):
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.destino_base = os.path.join(os.getcwd(), "XML")

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_experimental_option("prefs", {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "download.default_directory": self.download_path
        })
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 20)

    def login(self):
        self.driver.get(FSIST_URL)
        try:
            print("Página carregada. Capturando campos de login...")
            self.driver.save_screenshot("screenshot_login.png")
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Informe o seu e-mail ou usuário cadastrado']"))).send_keys(USUARIO)
            self.driver.find_element(By.XPATH, "//input[@placeholder='Informe a sua senha']").send_keys(SENHA)
            self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Entrar']").click()
            print("Login realizado com sucesso.")
        except Exception as e:
            print(f"Erro ao tentar logar: {e}")
            self.driver.save_screenshot("erro_login.png")
            raise

    def selecionar_empresa(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, "DivEmpresa"))).click()
            time.sleep(1)
            campo_empresa = self.wait.until(EC.visibility_of_element_located((By.ID, "EmpresaNomeBusca")))
            campo_empresa.clear()
            campo_empresa.send_keys("TODAS")
            time.sleep(1)
            campo_empresa.send_keys(Keys.DOWN)
            time.sleep(1)
            campo_empresa.send_keys(Keys.ENTER)
            time.sleep(2)
            self.driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(1)
            print("Empresa 'TODAS' selecionada e confirmada.")
        except Exception as e:
            print(f"Erro ao selecionar empresa: {e}")
            self.driver.save_screenshot("erro_empresa.png")
            raise

    def selecionar_data_hoje(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, "Periodo"))).click()
            time.sleep(1)

            self.wait.until(EC.element_to_be_clickable((By.ID, "data1"))).click()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//th[@class='today' and text()='Hoje']"))).click()
            time.sleep(1)

            self.wait.until(EC.element_to_be_clickable((By.ID, "data2"))).click()
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//th[@class='today' and text()='Hoje']"))).click()
            time.sleep(1)

            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='CONFIRMAR']"))).click()
            print("Período definido com data de hoje.")
        except Exception as e:
            print(f"Erro ao preencher data: {e}")
            self.driver.save_screenshot("erro_data.png")
            raise

    def buscar_notas(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.ID, "butSelecionadosQtd"))).click()
            print("Notas selecionadas.")
            time.sleep(2)
            self.wait.until(EC.element_to_be_clickable((By.ID, "butDownload"))).click()
            print("Botão de download clicado.")
            time.sleep(3)
            try:
                botao_sim = self.driver.find_element(By.XPATH, "//button[span[text()='Sim, efetuar ciência da operação']]")
                botao_sim.click()
                print("Ciência confirmada.")
            except:
                print("Pop-up de ciência não exibido.")
            time.sleep(30)
            try:
                botao_xml = self.driver.find_element(By.XPATH, "//span[contains(text(),'Apenas XMLs')]/..")
                botao_xml.click()
                print("Download de XMLs iniciado.")
            except:
                print("Botão de 'Apenas XMLs' não encontrado.")
            time.sleep(10)
        except Exception as e:
            print(f"Erro ao buscar notas: {e}")
            self.driver.save_screenshot("erro_busca.png")
            raise

    def processar_download(self):
        try:
            zip_files = [f for f in os.listdir(self.download_path) if f.endswith(".zip") and f.startswith("FSist XMLs")]
            for zip_file in zip_files:
                full_path = os.path.join(self.download_path, zip_file)
                with zipfile.ZipFile(full_path, 'r') as zip_ref:
                    folder_data = datetime.now().strftime('%d-%m-%Y')
                    destino = os.path.join(self.destino_base, folder_data)
                    os.makedirs(destino, exist_ok=True)
                    for file in zip_ref.namelist():
                        caminho_destino = os.path.join(destino, file)
                        if not os.path.exists(caminho_destino):
                            zip_ref.extract(file, destino)
                        else:
                            print(f"Arquivo já existe, ignorando: {file}")
                os.remove(full_path)
                print(f"Arquivo {zip_file} processado para {destino}")
        except Exception as e:
            print(f"Erro ao mover/descompactar XMLs: {e}")
            raise

    def executar_fluxo_completo(self):
        self.login()
        self.selecionar_empresa()
        self.selecionar_data_hoje()
        self.buscar_notas()
        self.processar_download()
        self.fechar()

    def fechar(self):
        self.driver.quit()

if __name__ == "__main__":
    bot = FSistBot()
    bot.executar_fluxo_completo()
