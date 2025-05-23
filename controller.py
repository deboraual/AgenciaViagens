from view import *
from model.Paises import *

import os
from PIL import Image, ImageTk

class Controller:
    def __init__(self, master):
        self.view = View(master)
    
    def carregar_imagem_ponto(self, nome_ponto):
        import os
        from PIL import Image, ImageTk

        caminho_base = "imagens/"
        nome_formatado = nome_ponto.lower().replace(" ", "_").replace("ã", "a").replace("é", "e").replace("ç", "c")
        extensoes = [".jpg", ".jpeg", ".png"]

        for ext in extensoes:
            caminho = os.path.join(caminho_base, nome_formatado + ext)
            if os.path.exists(caminho):
                try:
                    img = Image.open(caminho)
                    img = img.resize((200, 120), Image.LANCZOS)
                    return ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Erro ao carregar imagem de {nome_ponto}: {e}")
        return None
