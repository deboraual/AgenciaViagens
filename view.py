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

from datetime import datetime
from PIL import Image, ImageTk
from model.Cliente import *
from model.LinkedClient import *
from model.Paises import *
from model.CompanhiaAeria import *
from controller import *

class View:
    def __init__(self, master, controller):
        
        self.master = master
        self.controller = controller
        self.frame = None
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
        
        #puxar para sima _ faz com que ignore o canvas 
        _, scrollable= self.controller.criar_scrollable_frame(self.frame)
        self.controller.barra_carrinho(self.frame, is_home=True)

        mensagem = f"Bem-vindo(a), {self.cliente_login.get_nome()}!"
        tk.Label(scrollable, text=mensagem, font=("Arial", 15), bg="#696969", fg="#C6C6DC").grid(row=0, column=0, columnspan=2, padx=10, pady=(100,30), sticky='ew')

        # Lista de imagens e países
        imagens_info = [
            {"caminho": "imagens/portugal.jpg", "pais_obj": paises[0]},
            {"caminho": "imagens/espanha.jpg", "pais_obj": paises[1]},
            {"caminho": "imagens/franca.jpg", "pais_obj": paises[2]},
            {"caminho": "imagens/italia.jpg", "pais_obj": paises[3]},
            {"caminho": "imagens/alemanha.jpg", "pais_obj": paises[4]},
            {"caminho": "imagens/egito.jpg", "pais_obj": paises[5]},
            {"caminho": "imagens/japao.jpg", "pais_obj": paises[6]},
            {"caminho": "imagens/tailandia.jpg", "pais_obj": paises[7]},
            {"caminho": "imagens/brasil.jpg", "pais_obj": paises[8]},
        ]

        self.imagens_tk = []

        for col in range(2):
            scrollable.columnconfigure(col, weight=1)

        for i, info in enumerate(imagens_info):
            row = i // 2
            col = i % 2

            try:
                img = Image.open(info["caminho"])
                img = img.resize((100, 100), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                self.imagens_tk.append(img_tk)

                tk.Label(scrollable, image=img_tk, bg="#696969").grid(
                    row=row*3+1, column=col, padx=60, pady=(10, 5), sticky='n'
                )

            except Exception:
                tk.Label(scrollable, text="Sem imagem", width=15, height=6, bg="#999").grid(
                    row=row*3+1, column=col, padx=60, pady=(10, 5), sticky='n'
                )

            nome_pais = info["pais_obj"].nome
            custo = info["pais_obj"].custo_viagem
            texto = f"{nome_pais}\nCusto: €{custo}"

            tk.Label(scrollable, text=texto, bg="#696969", fg="white", font=("Arial", 12)).grid(row=row*3+2, column=col, padx=60, pady=(0, 20), sticky='n')
            btn = tk.Button(scrollable, text="Pontos Turisticos", font=("Arial", 10), command=lambda pais=info["pais_obj"]: self.pag_paises(pais))
            btn.grid(row=row*3+3, column=col, padx=60, pady=(0, 20), sticky='n')


    def pag_paises(self, paises):
        if self.frame:
            self.frame.destroy()

        self.frame = tk.Frame(self.master, bg="#696969")
        self.frame.pack(fill='both', expand=True)
        _, scroll_frame = self.controller.criar_scrollable_frame(self.frame)
        self.controller.barra_carrinho(self.frame, is_home=False, pais=paises)


        self.master.title(f"{paises.nome} - Pontos Turísticos")

        tk.Label(scroll_frame,text=f"Pontos turísticos em {paises.nome}",font=("Arial", 16),bg="#696969",fg="white").pack(pady=20)

        self.imagens_tk_pontos = []  # lista referências

        for cidade in paises.cidades: 
            tk.Label(scroll_frame,text=f"Cidade: {cidade.nome}",font=("Arial", 14, "bold"),bg="#696969",fg="white").pack(pady=(10, 0))

            for ponto in cidade.pontos_turisticos:

                #criar o cartao dos pontos tutisticos 
                cartao_frame = tk.Frame(scroll_frame, bg='#808080', bd=1, relief='solid',padx = 5, pady= 5)
                cartao_frame.pack(padx=10, pady=10, fill = 'x')

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
                            img = img.resize((150, 90), Image.LANCZOS)
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

                tk.Label(texto_frame, text=ponto.nome, font=("Arial", 11, "bold"), bg="#808080", fg="white").pack(anchor="w")
                tk.Label(texto_frame, text=f"Localização: {cidade.nome}", font=("Arial", 9 ), bg="#808080", fg="#DDDDDD").pack(anchor="w")
                tk.Label(texto_frame, text=ponto.descricao, font=("Arial", 9), bg="#808080", fg="#DDDDDD", wraplength=250, justify="left").pack(anchor="w", pady=(2, 0))


    
    def pag_voos(self, pais):

        # Cria nova janela para consulta de voos
        self.janela_voos = tk.Toplevel(self.master)
        self.janela_voos.title(f'Consulta de Voos para {pais.nome}')

        tk.Label(self.janela_voos, text=f"Voos disponíveis para {pais.nome}", font=("Arial", 16)).pack(pady=10)

        self.pais_atual_voo=pais
        # Widgets de filtro
        filtro_frame = tk.Frame(self.janela_voos)
        filtro_frame.pack(pady=5)

        tk.Label(filtro_frame, text="Preço máximo (€):").grid(row=0, column=0, padx=5)
        self.preco_max_entry = tk.Entry(filtro_frame, width=8)
        self.preco_max_entry.grid(row=0, column=1)

        self.direto_var = tk.BooleanVar()
        tk.Checkbutton(filtro_frame, text="Somente voos diretos", variable=self.direto_var).grid(row=0, column=2, padx=10)

        tk.Button(filtro_frame, text="Filtrar", command=self.atualizar_voos_filtrados).grid(row=0, column=3)

        # Espaço para resultados
        self.resultado_voos_frame = tk.Frame(self.janela_voos)
        self.resultado_voos_frame.pack(pady=10)

        self.atualizar_voos_filtrados()  # exibe resultados iniciais

    def atualizar_voos_filtrados(self):
        for widget in self.resultado_voos_frame.winfo_children():
            widget.destroy()

        # Leitura de filtros
        preco_max = self.preco_max_entry.get()
        direto = self.direto_var.get()
        try:
            preco_max = float(preco_max) if preco_max else None
        except ValueError:
            preco_max = None

        # Aplica filtros
        voos_filtrados = self.controller.buscar_voos(
            pais=self.pais_atual_voo.nome,
            preco_max=preco_max,
            direto=direto
        )

        if not voos_filtrados:
            tk.Label(self.resultado_voos_frame, text="Nenhum voo disponível com os critérios selecionados.").pack()
            return

        # Agrupa por companhia
        companhias = sorted(set(voo.companhia for voo in voos_filtrados))

        self.companhia_var = tk.StringVar(value=companhias[0])
        self.data_preco_var = tk.StringVar()

        tk.Label(self.resultado_voos_frame, text="Escolha a companhia aérea:").pack()
        ttk.OptionMenu(self.resultado_voos_frame, self.companhia_var, self.companhia_var.get(), *companhias, command=self.atualizar_datas_voos).pack(pady=5)

        tk.Label(self.resultado_voos_frame, text="Escolha data e preço:").pack()
        self.menu_datas = ttk.OptionMenu(self.resultado_voos_frame, self.data_preco_var, '')
        self.menu_datas.pack(pady=5)

        self.voos_filtrados = voos_filtrados
        self.atualizar_datas_voos(self.companhia_var.get())

        tk.Button(self.resultado_voos_frame, text='Confirmar voo', command=self.confirmar_voo_escolhido).pack(pady=10)

    def atualizar_datas_voos(self, companhia_nome):
        opcoes = [
            f'{voo.data} - €{voo.preco}'
            for voo in self.voos_filtrados
            if voo.companhia == companhia_nome
        ]

        self.menu_datas['menu'].delete(0, 'end')

        if not opcoes:
            self.data_preco_var.set('Sem datas disponíveis')
            return

        self.data_preco_var.set(opcoes[0])
        for opcao in opcoes:
            self.menu_datas['menu'].add_command(
                label=opcao,
                command=lambda value=opcao: self.data_preco_var.set(value)
            )

    def confirmar_voo_escolhido(self):
        companhia = self.companhia_var.get()
        data_preco_str = self.data_preco_var.get()

        if '€' not in data_preco_str:
            messagebox.showwarning('Aviso', 'Por favor, selecione uma data válida.')
            return

        data_voo, preco = data_preco_str.split("- €")
        preco = float(preco.strip())
        messagebox.showinfo('Confirmação', f'Voo confirmado:\nCompanhia: {companhia}\nData: {data_voo}\nPreço: {preco:.2f}€')
        self.janela_voos.destroy()
        self.janela_voos.destroy()
    
    def buscar_voos_por_pais(self, pais):
        return [voo for voo in self.voos if voo.pais.lower() == pais.lower()]

    def buscar_voos_ate_preco(self, preco_max):
        return [voo for voo in self.voos if voo.preco <= preco_max]

    def ordenar_voos_por_preco(self):
        return sorted(self.voos, key=lambda v: v.preco)
    

    def ordenar_voos_por_data(self):
        return sorted(self.voos, key=lambda v: datetime.strptime(v.data, "%d/%m/%Y"))

    def voos_diretos(self):
        return [voo for voo in self.voos if not voo.escala]

    def buscar_voos(self, pais=None, preco_max=None, direto=None):
        resultado = self.voos
        if pais:
            resultado = [v for v in resultado if v.pais.lower() == pais.lower()]
        if preco_max is not None:
            resultado = [v for v in resultado if v.preco <= preco_max]
        if direto is not None:
            resultado = [v for v in resultado if v.escala != direto]
        return resultado