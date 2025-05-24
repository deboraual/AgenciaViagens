import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
import mysql.connector
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import json
import requests
import hashlib
import os

from PIL import Image, ImageTk
from model.Cliente import *
from model.LinkedClient import *
from model.Paises import *
from controller import *

class View:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.carrinho = controller.carrinho
        #self.carrinho = []

        #criar linked list
        self.clientes = LinkedClient()
        print(self.clientes)
        self.cliente_login = None

        #página inicial
        self.frame = tk.Frame(self.master, bg='#696969')
        self.frame.pack(fill="both", expand = True)
        
        self.logo = Image.open("imagens/plane.jpg")
        self.logo = self.logo.resize((200, 200), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_label = tk.Label(self.frame, image=self.logo, bg="Black")
        self.logo_label.pack(pady=(50, 20))

        self.registo_button = ttk.Button(self.frame, text="Registo", style="TButton", command=self.registo )
        self.registo_button.pack(pady=(20,10), ipadx=20, ipady=5)
        self.login_button = ttk.Button(self.frame, text="Login", style="TButton", command=self.login )
        self.login_button.pack(pady=(5,10), ipadx=20, ipady=5)

    # ----------- Ligar à base de dados -----------
    def ligar_base_dados(self):
        try:
            conexao = mysql.connector.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='5218Debora',
                database='travelbuddy',
                auth_plugin='mysql_native_password'
            )
            return conexao
        except mysql.connector.Error as erro:
            messagebox.showerror("Erro", f"Erro na ligação:\n{erro}")
            return None
    

        #API -> ligação 
    def autenticar_amadeus(self):
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.amadeus_key,
            "client_secret": self.amadeus_secret
        }
        try:
            response = requests.post(url, data=data)    
            self.amadeus_token = response.json().get("access_token")
        except Exception as e:
            messagebox.showerror("Erro Amadeus", f"Erro ao autenticar: {e}")

    def registo(self):
        janela_registo = tk.Toplevel(self.master)
        janela_registo.title("Registo")
        janela_registo.configure(background="#696969", width=500, height=500)

        nova_frame = tk.Frame(janela_registo, bg="#696969")
        nova_frame.pack(fill="both", expand=True)

        nova_frame.columnconfigure(1, weight=1)

        tk.Label(nova_frame, text="Nome:", font=("Arial", 14), bg="#696969", fg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        nome_entry = tk.Entry(nova_frame, font=("Arial",14))
        nome_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        tk.Label(nova_frame, text="Email:", font=("Arial", 14), bg="#696969", fg="white").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        email_entry = tk.Entry(nova_frame, font=("Arial",14))
        email_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        tk.Label(nova_frame, text="Password:", font=("Arial", 14), bg="#696969", fg="white").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        password_entry = tk.Entry(nova_frame, show="*", font=("Arial",14))
        password_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        tk.Label(nova_frame, text="Repita a password:", font=("Arial", 14), bg="#696969", fg="white").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        password_repetida_entry = tk.Entry(nova_frame, show="*", font=("Arial",14))
        password_repetida_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

        
        tk.Button(
            nova_frame,
            text="Registar",
            command=lambda: self.registar_cliente(
                janela_registo,
                nome_entry,
                email_entry,
                password_entry,
                password_repetida_entry
            )
        ).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(nova_frame, text="Voltar", command=janela_registo.destroy).grid(row=5, column=0, columnspan=2, pady=10)
        

    def registar_cliente(self, janela_registo, entry_nome, entry_email, entry_password, entry_password_repetida):
        nome = entry_nome.get().strip()
        email = entry_email.get().strip()
        password = entry_password.get()
        password_repetida = entry_password_repetida.get()

        # Verificações básicas
        if not nome or not email or not password or not password_repetida:
            messagebox.showerror("Erro", "Todos os campos têm de estar preenchidos")
            return

        if "@" not in email or "." not in email:
            messagebox.showwarning("Email inválido", "Por favor insere um email válido.")
            return

        if password != password_repetida:
            messagebox.showerror("Erro", "As passwords não são iguais")
            return

        # Verifica se o cliente já existe
        if self.clientes.find_username(nome) != -1:
            messagebox.showerror("Erro", "Cliente já existente")
            return

        # Guarda na estrutura de dados local
        self.clientes.insert_last(Cliente(nome, password))

        # Hash da password
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Guarda na base de dados
        conexao = self.ligar_base_dados()
        if conexao is None:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO utilizadores (nome, email, password) VALUES (%s, %s, %s)",
                (nome, email, password_hash)
            )
            conexao.commit()
            messagebox.showinfo("Sucesso", "Utilizador registado com sucesso!")
            janela_registo.destroy()
        except mysql.connector.Error as erro:
            messagebox.showerror("Erro", f"Erro ao registar na base de dados:\n{erro}")
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()


    def login(self):
        janela_login = tk.Toplevel(self.master)
        janela_login.title("Login")
        janela_login.configure(background = "#696969", width=500, height=500)

        nova_frame = tk.Frame(janela_login, bg="#696969")
        nova_frame.pack(fill="both", expand=True)
        
        nova_frame.columnconfigure(1, weight=1)#permite que a coluna da etxt espanda

        tk.Label(nova_frame, text="Email:", font=("Arial", 14), bg="#696969", fg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        nome_entry = tk.Entry(nova_frame, font=("Arial",14))
        nome_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        tk.Label( nova_frame, text="Password:", font=("Arial", 14), bg="#696969", fg="white").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        password_entry = tk.Entry(nova_frame, show="*", font=("Arial",14))
        password_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        tk.Button(nova_frame, text="Entrar", font=("Arial", 10),command=lambda: self.login_cliente(janela_login, nome_entry.get(), password_entry.get())).grid(row=2, column=1, pady=(20, 10))
    
    def login_cliente(self, janela_login, email, password):
        if not email or not password:
            messagebox.showwarning("Aviso", "Preenche todos os campos.")
            return

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conexao = self.ligar_base_dados()
        if conexao is None:
            return

        try:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT * FROM utilizadores WHERE email = %s AND password = %s",
                (email, password_hash)
            )
            resultado = cursor.fetchone()
            if resultado:
                messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {resultado[1]}!")
                janela_login.destroy()
                self.frame.destroy()
                self.cliente_login = Cliente(resultado[1], "")  # nome, password vazia
                self.home()
            else:
                messagebox.showerror("Erro", "Email ou password incorretos.")
        except mysql.connector.Error as erro:
            messagebox.showerror("Erro", f"Erro ao autenticar: {erro}")
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

        
    def ir_para_home(self, janela_login, nome, password):

        if nome and password:
            posicao = self.clientes.find_username(nome)
            if posicao == -1:
                messagebox.showerror("Erro!!")
                return
            cliente = self.clientes.get(posicao)
            if password == cliente.get_password():
                self.cliente_login = cliente
                janela_login.destroy()
                self.frame.destroy()#fechar as janelas anteriores
                self.home()
            else:
                messagebox.showerror("erro","password errada")

    def home(self):
        if self.frame:
            self.frame.destroy()
            
        self.frame = tk.Frame(self.master, bg='#696969')
        self.frame.master.title('Home')
        self.frame.master.geometry('500x500')
        self.frame.pack(fill='both', expand=True)    
        
        #puxar para sima 
        canvas = tk.Canvas(self.frame, bg='#696969', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        self.frame.update_idletasks()

        scrollable_frame = tk.Frame(canvas, bg='#696969')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="n", width=self.frame.winfo_width())

        self.controller.barra_carrinho(self.frame)



        mensagem = f"Bem-vindo(a), {self.cliente_login.get_nome()}!"
        tk.Label(scrollable_frame, text=mensagem, font=("Arial", 15), bg="#696969", fg="#C6C6DC").grid(row=0, column=0, columnspan=2, padx=10, pady=30, sticky='ew')

        # Lista de imagens e países
        imagens_info = [
            {"caminho": "imagens/portugal.jpg", "pais_obj": paises[0]},
            {"caminho": "imagens/espanha.jpg", "pais_obj": paises[1]},
            {"caminho": "imagens/franca.jpg", "pais_obj": paises[2]},
            {"caminho": "imagens/italia.jpg", "pais_obj": paises[3]},
            {"caminho": "imagens/alemanha.jpg", "pais_obj": paises[4]},
            # Adiciona mais aqui se necessário
        ]

        self.imagens_tk = []

        for col in range(2):
            scrollable_frame.columnconfigure(col, weight=1)

        for i, info in enumerate(imagens_info):
            row = i // 2
            col = i % 2

            try:
                img = Image.open(info["caminho"])
                img = img.resize((100, 100), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                self.imagens_tk.append(img_tk)

                tk.Label(scrollable_frame, image=img_tk, bg="#696969").grid(
                    row=row*3+1, column=col, padx=60, pady=(10, 5), sticky='n'
                )

            except Exception:
                tk.Label(scrollable_frame, text="Sem imagem", width=15, height=6, bg="#999").grid(
                    row=row*3+1, column=col, padx=60, pady=(10, 5), sticky='n'
                )

            nome_pais = info["pais_obj"].nome
            custo = info["pais_obj"].custo_viagem
            texto = f"{nome_pais}\nCusto: €{custo}"

            tk.Label(scrollable_frame, text=texto, bg="#696969", fg="white", font=("Arial", 12)).grid(row=row*3+2, column=col, padx=60, pady=(0, 20), sticky='n')
            btn = tk.Button(scrollable_frame, text="Entrar", font=("Arial", 10), command=lambda pais=info["pais_obj"]: self.pag_paises(pais))
            btn.grid(row=row*3+3, column=col, padx=60, pady=(0, 20), sticky='n')


    def pag_paises(self, paises):
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(self.master, bg="#696969")
        self.frame.pack(fill='both', expand=True)
        self.controller.barra_carrinho(self.frame, paises)


        self.frame.master.title(f"{paises.nome} - Pontos Turísticos")

        tk.Label(
            self.frame,
            text=f"Pontos turísticos em {paises.nome}",
            font=("Arial", 16),
            bg="#696969",
            fg="white"
        ).pack(pady=20)

        self.imagens_tk_pontos = []  # lista para manter referências

        for cidade in paises.cidades: 
            tk.Label(
                self.frame,
                text=f"Cidade: {cidade.nome}",
                font=("Arial", 14, "bold"),
                bg="#696969",
                fg="white"
            ).pack(pady=(10, 0))

            for ponto in cidade.pontos_turisticos:

                #criar o cartao dos pontos tutisticos 
                cartao_frame = tk.Frame(self.frame, bg='#808080', bd=1, relief='solid',padx=10, pady=10)
                cartao_frame.pack(padx=20, pady=20, fill = 'x')

                caminho_base = "imagens/pontos/" #carregar imagens 
                nome_formatado = (
                    ponto.nome.lower()
                    .replace(" ", "_")
                    .replace("ã", "a")
                    .replace("á", "a")
                    .replace("â", "a")
                    .replace("é", "e")
                    .replace("ê", "e")
                    .replace("í", "i")
                    .replace("ó", "o")
                    .replace("õ", "o")
                    .replace("ç", "c")
                    .replace("ü","u")
                )
                extensoes = [".jpg", ".jpeg", ".png"]
                img_tk = None

                for ext in extensoes:
                    caminho = os.path.join(caminho_base, nome_formatado + ext)
                    if os.path.exists(caminho):
                        try:
                            img = Image.open(caminho)
                            img = img.resize((200, 120), Image.LANCZOS)
                            img_tk = ImageTk.PhotoImage(img)
                            self.imagens_tk_pontos.append(img_tk)  
                            break
                        except Exception as e:
                            print(f"Erro ao carregar imagem '{caminho}': {e}")

                if img_tk:
                    tk.Label(cartao_frame, image=img_tk, bg="#808080").pack(side= 'left', padx=(0,10))
                else:
                    tk.Label(cartao_frame, text="[Imagem não disponível]", width=15, height=5, bg='#999').pack(side='left', padx=(0,10))

                texto_frame = tk.Frame(cartao_frame, bg='#808080')
                texto_frame.pack(side="left", fill="both", expand=True)

                tk.Label(texto_frame, text=ponto.nome, font=("Arial", 12, "bold"), bg="#808080", fg="white").pack(anchor="w")
                tk.Label(texto_frame, text=f"Localização: {cidade.nome}", font=("Arial", 10), bg="#808080", fg="#DDDDDD").pack(anchor="w", pady=2)
                tk.Label(texto_frame, text=ponto.descricao, font=("Arial", 10), bg="#808080", fg="#DDDDDD", wraplength=300, justify="left").pack(anchor="w", pady=(5, 0))

    

    
    def abrir_carrinho(self):
        if not self.carrinho:
            messagebox.showinfo("Carrinho", "O carrinho está vazio.")
            return

        conteudo = ""
        total_geral = 0
        for item in self.carrinho:
            conteudo += f"{item['quantidade']}x {item['pais']} — €{item['total']:.2f}\n"
            total_geral += item["total"]

        conteudo += f"\nTotal geral: €{total_geral:.2f}"
        messagebox.showinfo("Carrinho", conteudo)
    