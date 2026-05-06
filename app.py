import customtkinter as ctk
import pyautogui
import pandas as pd
import threading
import time
import os
import hashlib
from tkinter import filedialog

# ===== CONFIG =====
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1000x600")
app.title("AutoCadastro Pro 🚀")

pyautogui.FAILSAFE = True

dados_excel = None
rodando = False

# ===== LICENÇA =====
ARQUIVO_LICENCA = "licenca.key"
SEGREDO = "autofill_pro_2026"

def gerar_hash(chave):
    return hashlib.sha256((chave + SEGREDO).encode()).hexdigest()

def validar_licenca(chave):
    return gerar_hash(chave).startswith("00")

def salvar_licenca(chave):
    with open(ARQUIVO_LICENCA, "w") as f:
        f.write(chave)

def carregar_licenca():
    if os.path.exists(ARQUIVO_LICENCA):
        with open(ARQUIVO_LICENCA, "r") as f:
            return f.read().strip()
    return None

# ===== AUTOMAÇÃO =====
def automacao():
    global rodando

    if dados_excel is None:
        status_dash.configure(text="Importe um Excel primeiro!", text_color="red")
        return

    rodando = True
    status_dash.configure(text="Iniciando em 5 segundos...", text_color="yellow")

    time.sleep(5)

    try:
        for _, linha in dados_excel.iterrows():
            if not rodando:
                break

            for valor in linha:
                pyautogui.write(str(valor))
                pyautogui.press("tab")
                time.sleep(0.2)

            pyautogui.press("enter")
            time.sleep(0.3)

        if rodando:
            status_dash.configure(text="Automação finalizada 🚀", text_color="green")
        else:
            status_dash.configure(text="Automação parada ⛔", text_color="orange")

    except Exception as e:
        status_dash.configure(text=f"Erro: {str(e)}", text_color="red")

    rodando = False

def iniciar_automacao():
    threading.Thread(target=automacao).start()

def parar_automacao():
    global rodando
    rodando = False

# ===== EXCEL =====
def importar_excel():
    global dados_excel

    caminho = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])

    if caminho:
        try:
            dados_excel = pd.read_excel(caminho)
            label_excel.configure(text="Excel carregado ✅")
        except:
            label_excel.configure(text="Erro ao carregar ❌")

# ===== LOGIN =====
def fazer_login():
    if entry_user.get() == "admin" and entry_senha.get() == "123":
        frame_login.pack_forget()
        frame_dashboard.pack(fill="both", expand=True)
    else:
        status_login.configure(text="Login inválido", text_color="red")

# ===== LICENÇA UI =====
def ativar_licenca():
    chave = entry_licenca.get()

    if validar_licenca(chave):
        salvar_licenca(chave)
        status_licenca.configure(text="Licença válida ✅", text_color="green")
        abrir_login()
    else:
        status_licenca.configure(text="Licença inválida ❌", text_color="red")

def abrir_login():
    frame_licenca.pack_forget()
    frame_login.pack(fill="both", expand=True)

# ===== TELA LICENÇA =====
frame_licenca = ctk.CTkFrame(app)

ctk.CTkLabel(frame_licenca, text="Ativação do Sistema", font=("Arial", 24)).pack(pady=20)

entry_licenca = ctk.CTkEntry(frame_licenca, placeholder_text="Digite sua licença", width=300)
entry_licenca.pack(pady=10)

ctk.CTkButton(frame_licenca, text="Ativar", command=ativar_licenca).pack(pady=10)

status_licenca = ctk.CTkLabel(frame_licenca, text="")
status_licenca.pack()

# ===== LOGIN UI =====
frame_login = ctk.CTkFrame(app)

ctk.CTkLabel(frame_login, text="AutoCadastro Pro", font=("Arial", 28)).pack(pady=30)

entry_user = ctk.CTkEntry(frame_login, placeholder_text="Usuário")
entry_user.pack(pady=10)

entry_senha = ctk.CTkEntry(frame_login, placeholder_text="Senha", show="*")
entry_senha.pack(pady=10)

ctk.CTkButton(frame_login, text="Entrar", command=fazer_login).pack(pady=20)

status_login = ctk.CTkLabel(frame_login, text="")
status_login.pack()

# ===== DASHBOARD =====
frame_dashboard = ctk.CTkFrame(app)

ctk.CTkLabel(frame_dashboard, text="Painel de Automação", font=("Arial", 20)).pack(pady=20)

ctk.CTkButton(frame_dashboard, text="📂 Importar Excel", command=importar_excel).pack(pady=10)

label_excel = ctk.CTkLabel(frame_dashboard, text="Nenhum arquivo carregado")
label_excel.pack()

ctk.CT
