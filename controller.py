from view import *
from model.Paises import *
from model.CompanhiaAeria import *

import tkinter as tk
import os
from PIL import Image, ImageTk

class Controller:
    def __init__(self, master):
       
        self.voos = []
        self.companhias = [
            CompanhiaAeria("tap"),
            CompanhiaAeria('iberia'),
            CompanhiaAeria('air_france'),
            CompanhiaAeria('lufthansa'),
            CompanhiaAeria('egyptair'),
            CompanhiaAeria('ana'),
            CompanhiaAeria('thairways'),
            CompanhiaAeria('latam'),
        ]
        for companhia in companhias:
            self.voos.extend(companhia.voos)
        self.carrinho = []
        self.view = View(master, self)
        self.cart_icon = None
        self.lista_paises = paises
        self.voos_disponiveis=self.companhias[0].carregar_voos()
    
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

    def barra_carrinho(self, frame, is_home = False, pais=None):
            top_bar = tk.Frame(frame, bg="#505050", height=100)
            top_bar.place(relx=0, rely=0, relwidth=1.0)

            voltar_btn = tk.Button(top_bar, text="❌", command=self.voltar_home, bg="red", fg="white")
            voltar_btn.pack(side="left", padx=10, pady=10)

            # Carrinho sempre aparece
            carrinho_btn = tk.Button(top_bar, text="🛒", command=self.abrir_carrinho)
            carrinho_btn.pack(side="right", padx=10, pady=10)

            if is_home :
                #adicionar barra de pesquisa
                self.pesquisa_entry= tk.Entry(top_bar, font=('Arial',12))
                self.pesquisa_entry.pack(side='left', padx=5, pady=10)

                pesquisar_btn= tk.Button(top_bar, text='Pesquisar', command=lambda: self.pesquisar(self.pesquisa_entry.get()))
                pesquisar_btn.pack(side='left', padx=10, pady=10)



            if not is_home and pais is not None:
                voos = self.voos_pais(pais.nome)
                #adicionar para coprar nos paises  
                comprar_btn = tk.Button(top_bar, text="voos",command=lambda: self.abrir_pag_voos(pais),bg="green", fg="white")
                comprar_btn.pack(side="right", padx=10, pady=10)

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

    def comprar_viagem(self, pais, voo):
        
        quantidade = simpledialog.askinteger(
            "Compra de voos",
            f"Para quantas pessoas deseja comprar esta viagem para: {voo.pais} com {voo.companhia}?",
            minvalue=1,
            parent=self.view.master
        )

        if quantidade:
            total = voo.preco * quantidade
            self.carrinho.append({
                "pais": voo.pais,
                "companhia": voo.companhia,
                'data': voo.data,
                'quantidade':quantidade,
                'total': total
            })

            messagebox.showinfo(
                "Compra Realizada",
                f"{quantidade} passagem(ns) para {voo.pais} adicionada(s) ao carrinho.\nTotal: €{total:.2f}"
            )

    def voltar_home(self):
        self.view.home()


    def confirmar_voo_para_pais(self, nome_pais):
        nome_companhia = self.companhia_var.get()
        data_voo = self.data_entry.get()

        if not data_voo:
            messagebox.showwarning("Aviso", "Por favor, insira uma data.")
            return

        for companhia in companhias:
            if companhia.nome == nome_companhia:
                preco = companhia.destinos.get(nome_pais)
                if preco:
                    messagebox.showinfo(
                        "Detalhes do Voo",
                        f"Companhia: {nome_companhia}\nDestino: {nome_pais}\nData: {data_voo}\nPreço: €{preco:.2f}"
                    )
                    return

        messagebox.showerror("Erro", "Companhia ou destino não encontrado.")

    def voos_pais(self, nome_pais):
        return [v for v in self.voos_disponiveis if v.pais.lower() == nome_pais.lower()]
   
    def abrir_pag_voos(self, pais):
        voos = self.voos_pais(pais.nome)
        self.view.pag_voos(pais, voos)


    def limpar_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def buscar_voos(self, destino=None, data=None):
        voos_filtrados = []

        for voo in self.voos_disponiveis:
            if destino and destino.lower() not in voo.pais.lower():
                continue
            if data and data != voo.data:
                continue
            voos_filtrados.append(voo)

        return voos_filtrados
