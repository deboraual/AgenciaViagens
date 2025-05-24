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
    
    def barra_carrinho (self,frame, pais=None):
        top_bar = tk.Frame(frame, bg="#505050", height=40)
        top_bar.pack(side="top", fill="x")


        try:
            cart_img = Image.open("imagens/carrinho.png")  # Caminho para tua imagem
            cart_img = cart_img.resize((24, 24), Image.LANCZOS)
            self.cart_icon = ImageTk.PhotoImage(cart_img)

            cart_btn = tk.Button(
                top_bar,
                image=self.cart_icon,
                bg="#505050",
                relief="flat",
                command=self.abrir_carrinho
            )
            cart_btn.pack(side="right", padx=10, pady=5)
        except Exception:
            cart_btn = tk.Button(
                top_bar,
                text="🛒",
                bg="#505050",
                fg="white",
                font=("Arial", 16),
                relief="flat",
                command=self.abrir_carrinho
            )
            cart_btn.pack(side="right", padx=10, pady=5)
        if pais is not None:
            comprar_btn = tk.Button(top_bar,text="Comprar Viagem",font=("Arial", 10, "bold"),bg="#4CAF50",fg="white",command=lambda: self.comprar_viagem(pais))
            comprar_btn.pack(side="right", padx=10, pady=5)
            btn_voltar = tk.Button(top_bar,text="X",font=("Arial", 12, "bold"),bg="#505050",fg="white",relief="flat",command=self.voltar_home)
            btn_voltar.pack(side="left", padx=10, pady=5)


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
            parent=self.view.master  # Usa o master da view
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