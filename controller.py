from view import *
from model.Paises import *

import tkinter as tk
import os
from PIL import Image, ImageTk

class Controller:
    def __init__(self, master):
       
        self.carrinho = []
        self.view = View(master, self)
        self.cart_icon = None
    
    def criar_scrollable_frame(self, frame):
        canvas = tk.Canvas(frame, bg='#696969', highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scrollable_frame = tk.Frame(canvas, bg='#696969')

        def atualizar_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", atualizar_scrollregion)

        frame.update_idletasks()  # Garante a largura correta
        canvas.create_window((frame.winfo_width() // 2, 0), window=scrollable_frame, anchor="n")

        return canvas, scrollable_frame


    def pesquisar(self, termo):
        termo = termo.lower()
        for pais in self.lista_paises:
            if termo in pais.nome.lower():
                self.view.pag_paises(pais)
                return
            for cidade in pais.cidades:
                if termo in cidade.nome.lower():
                    self.view.pag_paises(pais)
                    return
                for ponto in cidade.pontos_turisticos:
                    if termo in ponto.nome.lower():
                        self.view.pag_paises(pais)
                        return
        messagebox.showinfo("Pesquisa", "Nenhum resultado encontrado.")

    def barra_carrinho(self, frame, is_home = False):
            top_bar = tk.Frame(frame, bg="#505050", height=100)
            top_bar.place(relx=0, rely=0, relwidth=1.0)
            voltar_btn = tk.Button(top_bar, text="❌", command=self.voltar_home, bg="red", fg="white")
            voltar_btn.pack(side="left", padx=10, pady=10)

            if is_home:
                #adicionar barra de pesquisa
                self.pesquisa_entry= tk.Entry(top_bar, font=('Arial',12))
                self.pesquisa_entry.pack(side='left', padx=5, pady=10)

                pesquisar_btn= tk.Button(top_bar, text='Pesquisar', command=lambda: self.pesquisar(self.pesquisa_entry.get()))
                pesquisar_btn.pack(side='left', padx=10, pady=10)

                #botao para compra 
                comprar_btn = tk.Button(top_bar, text="Comprar", command=self.abrir_carrinho, bg="green", fg="white")
                comprar_btn.pack(side="right", padx=10, pady=10)

                #botao abrir carrinho
                carrinho_btn = tk.Button(top_bar, text="🛒", command=self.abrir_carrinho)
                carrinho_btn.pack(side="right", padx=10, pady=10)
            else:
                #adicionar para coprar nos paises  
                comprar_btn = tk.Button(top_bar, text="Comprar", command=self.abrir_carrinho, bg="green", fg="white")
                comprar_btn.pack(side="right", padx=10, pady=10)

                #botao abrir carrinho
                carrinho_btn = tk.Button(top_bar, text="🛒", command=self.abrir_carrinho)
                carrinho_btn.pack(side="right", padx=10, pady=10)


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

    def comprar_viagem(self, pais):
        quantidade = simpledialog.askinteger(
            "Compra de Passagens",
            f"Quantas passagens deseja comprar para {pais.nome}?",
            minvalue=1,
            parent=self.view.master
        )

        if quantidade:
            total = pais.custo_viagem * quantidade
            self.carrinho.append({
                "pais": pais.nome,
                "quantidade": quantidade,
                "total": total
            })

            messagebox.showinfo(
                "Compra Realizada",
                f"{quantidade} passagem(ns) para {pais.nome} adicionada(s) ao carrinho.\nTotal: €{total:.2f}"
            )

    def voltar_home(self):
        self.view.home()


