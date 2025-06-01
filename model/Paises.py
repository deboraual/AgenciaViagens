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
    def __init__(self, nome):
        self.nome = nome
        self.cidades = []

    def adicionar_cidade(self, cidade):
        self.cidades.append(cidade)

    def __str__(self):
        cidades_str = "\n\n".join(str(cidade) for cidade in self.cidades)
        return f"País: {self.nome}\nCusto da Viagem: €{self.custo_viagem}\n{cidades_str}"


portugal = Pais("Portugal")
lisboa = Cidade("Lisboa")
lisboa.adicionar_ponto_turistico(PontoTuristico("Torre de Belém", "Fortificação icônica à beira do Tejo."))
lisboa.adicionar_ponto_turistico(PontoTuristico("Mosteiro dos Jerónimos", "Obra-prima do estilo manuelino."))
portugal.adicionar_cidade(lisboa)

espanha = Pais("Espanha")
barcelona = Cidade("Barcelona")
barcelona.adicionar_ponto_turistico(PontoTuristico("Sagrada Família", "Basílica desenhada por Gaudí."))
barcelona.adicionar_ponto_turistico(PontoTuristico("Parque Güell", "Parque com mosaicos coloridos de Gaudí."))
espanha.adicionar_cidade(barcelona)

franca = Pais("França")
paris = Cidade("Paris")
paris.adicionar_ponto_turistico(PontoTuristico("Torre Eiffel", "Símbolo icônico de Paris."))
paris.adicionar_ponto_turistico(PontoTuristico("Museu do Louvre", "Famoso museu de arte com a Mona Lisa."))
franca.adicionar_cidade(paris)

italia = Pais("Itália")
roma = Cidade("Roma")
roma.adicionar_ponto_turistico(PontoTuristico("Coliseu", "Antigo anfiteatro romano."))
roma.adicionar_ponto_turistico(PontoTuristico("Fontana di Trevi", "Fonte barroca famosa."))
italia.adicionar_cidade(roma)

alemanha = Pais("Alemanha")
berlim = Cidade("Berlim")
berlim.adicionar_ponto_turistico(PontoTuristico("Portão de Brandemburgo", "Monumento histórico em Berlim."))
berlim.adicionar_ponto_turistico(PontoTuristico("Muro de Berlim", "Remanescente da divisão da cidade."))
alemanha.adicionar_cidade(berlim)

egito = Pais("Egito")
cairo = Cidade("Cairo")
cairo.adicionar_ponto_turistico(PontoTuristico("Pirâmides de Gizé", "Um dos marcos mais icônicos do mundo, construído há mais de 4.500 anos."))
egito.adicionar_cidade(cairo)
luxor = Cidade("Luxor")
luxor.adicionar_ponto_turistico(PontoTuristico("Templo de Karnak", "Um imenso complexo de templos dedicado aos deuses egípcios, especialmente Amon-Rá."))
egito.adicionar_cidade(luxor)

japao = Pais("Japão")
toquio = Cidade("Tóquio")
toquio.adicionar_ponto_turistico(PontoTuristico("Templo Senso-ji", "O templo budista mais antigo da cidade, localizado em Asakusa."))
japao.adicionar_cidade(toquio)
kyoto = Cidade("kyoto")
kyoto.adicionar_ponto_turistico(PontoTuristico("Pavilhão Dourado", "Um templo zen coberto de folhas de ouro, rodeado por um lago sereno."))
japao.adicionar_cidade(kyoto)

tailandia = Pais("Tailândia")
bangkok = Cidade("Bangkok")
bangkok.adicionar_ponto_turistico(PontoTuristico("Grande Palácio", "Complexo real com arquitetura tailandesa tradicional e o Buda de Esmeralda."))
tailandia.adicionar_cidade(bangkok)
chiang_mai = Cidade("Chiang Mai")
chiang_mai.adicionar_ponto_turistico(PontoTuristico("Wat Phra That Doi Suthep", "Templo sagrado em uma montanha com vista para a cidade"))
tailandia.adicionar_cidade(chiang_mai)

brasil = Pais("Brasil")
rio_de_janeiro = Cidade("Rio de Janeiro")
rio_de_janeiro.adicionar_ponto_turistico(PontoTuristico("Cristo Redentor", "Estátua icônica de Jesus Cristo no topo do Corcovado."))
brasil.adicionar_cidade(rio_de_janeiro)
foz_do_iguaçu = Cidade("Foz do Iguaçu")
foz_do_iguaçu.adicionar_ponto_turistico(PontoTuristico("Cataratas do Iguaçu", "Conjunto de quedas d'água na fronteira com a Argentina"))
brasil.adicionar_cidade(foz_do_iguaçu)

paises = [portugal, espanha, franca, italia, alemanha, egito, japao, tailandia, brasil]
