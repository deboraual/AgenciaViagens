import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import json

from PIL import Image, ImageTk
from model.Cliente import *
from model.LinkedClient import *
import os
class View:
    def __init__(self, master):
        self.master = master

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
    
    def registo(self):
        janela_registo = tk.Toplevel(self.master)
        janela_registo.title("Registo")
        janela_registo.configure(background = "#696969", width=500, height=500)

        nova_frame = tk.Frame(janela_registo, bg="#696969")
        nova_frame.pack(fill="both", expand=True)
        
        nova_frame.columnconfigure(1, weight=1)#permite que a coluna da etxt espanda

        tk.Label(nova_frame, text="Nome:", font=("Arial", 14), bg="#696969", fg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        nome_entry = tk.Entry(nova_frame, font=("Arial",14))
        nome_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        tk.Label( nova_frame, text="Password:", font=("Arial", 14), bg="#696969", fg="white").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        password_entry = tk.Entry(nova_frame, show="*", font=("Arial",14))
        password_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        tk.Label(  nova_frame, text="Repita a password:", font=("Arial", 14), bg="#696969", fg="white").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        password_repetida_entry = tk.Entry(nova_frame, show="*", font=("Arial",14))
        password_repetida_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        tk.Button( nova_frame,text="Registar",command=lambda: self.registar_cliente(janela_registo, nome_entry.get(),password_entry.get(),password_repetida_entry.get(),
            ),).grid(row=3, column=3,padx=10, pady=5)
        
        tk.Button(nova_frame,text="Voltar", command=janela_registo.destroy ).grid(row=3, column=4, pady=10)
        

    def registar_cliente(self, janela_registo, nome, password, password_repetida):
        if nome and password :
            posicao = self.clientes.find_username(nome)
            if posicao != -1: #ja esta registado
                messagebox.showerror("Erro!!","Cliente existente")
            else:
                if password == password_repetida:
                    self.clientes.insert_last(Cliente(nome, password))
                    janela_registo.destroy()
                    messagebox.showinfo("Sucesso!!","Cliente criado com sucesso")
                else:
                    messagebox.showerror("erro", "as passwords nao sao iguais")
        else:
            messagebox.showerror("Erro", "Todos os campos teem de estar preenchidos")
            


    def login(self):
        janela_login = tk.Toplevel(self.master)
        janela_login.title("Login")
        janela_login.configure(background = "#696969", width=500, height=500)

        nova_frame = tk.Frame(janela_login, bg="#696969")
        nova_frame.pack(fill="both", expand=True)
        
        nova_frame.columnconfigure(1, weight=1)#permite que a coluna da etxt espanda

        tk.Label(nova_frame, text="Nome:", font=("Arial", 14), bg="#696969", fg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        nome_entry = tk.Entry(nova_frame, font=("Arial",14))
        nome_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        tk.Label( nova_frame, text="Password:", font=("Arial", 14), bg="#696969", fg="white").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        password_entry = tk.Entry(nova_frame, show="*", font=("Arial",14))
        password_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        tk.Button(nova_frame, text="Entrar", font=("Arial", 10), command=lambda: self.ir_para_home(janela_login, nome_entry.get(), password_entry.get())).grid(row=2, column=1, pady=(20, 10))
    
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
        
        
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        mensagem = f"Bem-vindo(a), {self.cliente_login.get_nome()}!"
        tk.Label(self.frame, text=mensagem, font=("Arial", 15), bg="#696969", fg="#C6C6DC").grid(row=0, column=0, columnspan=2, padx=10, pady=30, sticky='ew')
        
        # Lista de caminhos de imagens e países
        imagens_info = [
            {"caminho": "imagem1.jpg", "pais": "Portugal"},
            {"caminho": "imagem2.jpg", "pais": "Espanha"},
            {"caminho": "imagem3.jpg", "pais": "França"},
            {"caminho": "imagem4.jpg", "pais": "Itália"},
        ]

        self.imagens_tk = []  # Guardar referências para evitar garbage collection

        for i, info in enumerate(imagens_info):
            row = i // 2
            col = i % 2

            try:
                img = Image.open(info["caminho"])
                img = img.resize((100, 100), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                self.imagens_tk.append(img_tk)

                tk.Label(self.frame, image=img_tk, bg="#696969").grid(row=row*2+1, column=col, padx=20, pady=(10, 5), sticky='n')
            except Exception:
                # Caso não tenha imagem ainda
                tk.Label(self.frame, text="Sem imagem", width=15, height=6, bg="#999").grid(row=row*2+1, column=col, padx=20, pady=(10, 5), sticky='n')

            tk.Label(self.frame, text=info["pais"], bg="#696969", fg="white", font=("Arial", 12)).grid(row=row*2+2, column=col, padx=40, pady=(0, 20),sticky='n')