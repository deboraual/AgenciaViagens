class PontoTuristico:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def __str__(self):
        return f"{self.nome}: {self.descricao}"


class Cidade:
    def __init__(self, nome):
        self.nome = nome
        self.pontos_turisticos = []

    def adicionar_ponto_turistico(self, ponto):
        self.pontos_turisticos.append(ponto)

    def __str__(self):
        pontos = "\n    ".join(str(p) for p in self.pontos_turisticos)
        return f"Cidade: {self.nome}\n  Pontos Turísticos:\n    {pontos}"


class Pais:
    def __init__(self, nome, custo_viagem):
        self.nome = nome
        self.custo_viagem = custo_viagem
        self.cidades = []

    def adicionar_cidade(self, cidade):
        self.cidades.append(cidade)

    def __str__(self):
        cidades_str = "\n\n".join(str(cidade) for cidade in self.cidades)
        return f"País: {self.nome}\nCusto da Viagem: €{self.custo_viagem}\n{cidades_str}"


portugal = Pais("Portugal", 150)
lisboa = Cidade("Lisboa")
lisboa.adicionar_ponto_turistico(PontoTuristico("Torre de Belém", "Fortificação icônica à beira do Tejo."))
lisboa.adicionar_ponto_turistico(PontoTuristico("Mosteiro dos Jerónimos", "Obra-prima do estilo manuelino."))
portugal.adicionar_cidade(lisboa)

espanha = Pais("Espanha", 180)
barcelona = Cidade("Barcelona")
barcelona.adicionar_ponto_turistico(PontoTuristico("Sagrada Família", "Basílica desenhada por Gaudí."))
barcelona.adicionar_ponto_turistico(PontoTuristico("Parque Güell", "Parque com mosaicos coloridos de Gaudí."))
espanha.adicionar_cidade(barcelona)

franca = Pais("França", 200)
paris = Cidade("Paris")
paris.adicionar_ponto_turistico(PontoTuristico("Torre Eiffel", "Símbolo icônico de Paris."))
paris.adicionar_ponto_turistico(PontoTuristico("Museu do Louvre", "Famoso museu de arte com a Mona Lisa."))
franca.adicionar_cidade(paris)

italia = Pais("Itália", 220)
roma = Cidade("Roma")
roma.adicionar_ponto_turistico(PontoTuristico("Coliseu", "Antigo anfiteatro romano."))
roma.adicionar_ponto_turistico(PontoTuristico("Fontana di Trevi", "Fonte barroca famosa."))
italia.adicionar_cidade(roma)

alemanha = Pais("Alemanha", 210)
berlim = Cidade("Berlim")
berlim.adicionar_ponto_turistico(PontoTuristico("Portão de Brandemburgo", "Monumento histórico em Berlim."))
berlim.adicionar_ponto_turistico(PontoTuristico("Muro de Berlim", "Remanescente da divisão da cidade."))
alemanha.adicionar_cidade(berlim)

paises = [portugal, espanha, franca, italia, alemanha]
