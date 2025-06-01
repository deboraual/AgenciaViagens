class Voo:
    def __init__(self, pais, data, preco, escala= False, companhia = None):
        self.pais = pais
        self.data = data
        self.preco = preco
        self.escala = escala
        self.companhia = companhia 

    def __repr__(self):
        escala_str = 'com escala' if self.escala else 'direto'
        return f'{self.data} - {self.pais}: {self.preco}€ ({escala_str})'        


class CompanhiaAeria:
    def __init__(self, nome):
        self.nome = nome
        self.destinos = {}
        self.voos = []

    def add_destino(self, destino, data, preco, escala = False):
        voo = Voo( destino, data, preco, escala)
        self.voos.append(voo)


    def resumo_aviao(self):
        destinos = "\n  ".join(str(voo) for voo in self.voos)
        return f"Companhia: {self.nome}\n  Voos:\n  {destinos}"
    
    def add_destino(self, destino, data, preco, escala=False):
        voo = Voo(destino, data, preco, escala)
        self.voos.append(voo)
    
    def carregar_voos(self):
        self.voos = [
            Voo(pais="Brasil", data="2025-06-06", preco=350.0, companhia = 'tap'),
            Voo(pais="Brasil", data="2025-06-07", preco=420.0, companhia= 'tap'),
            Voo(pais="Portugal", data="2025-06-03", preco=200.0, companhia ='tap'),
            Voo(pais="Portugal", data="2025-06-06", preco=240.0, companhia ='tap'),
            Voo(pais="Portugal", data="2025-06-12", preco=140.0, companhia ='tap'),
            Voo(pais="Portugal", data="2025-06-24", preco=140.0, companhia ='tap'),
            Voo(pais="Portugal", data="2025-06-25", preco=130.0, companhia ='tap'),
            Voo(pais="Brasil", data="2025-06-10", preco=980.0, companhia ='tap'),
            Voo(pais="Brasil", data="2025-06-14", preco=980.0, companhia ='tap'),
            Voo(pais="Brasil", data="2025-06-24", preco=980.0, companhia ='tap'),
            Voo(pais="Brasil", data="2025-06-25", preco=920.0, companhia ='tap'),
            Voo(pais="Brasil", data="2025-07-02", preco=1080.0, companhia ='tap'),
            Voo(pais="Franca", data="2025-06-05", preco=195.0, companhia ='tap'),
            Voo(pais="Franca", data="2025-06-06", preco=180.0, companhia ='tap'),
            Voo(pais="Franca", data="2025-06-10", preco=175.0, companhia ='tap'),
            Voo(pais="Franca", data="2025-06-20", preco=100.0, companhia ='tap'),
            Voo(pais="Franca", data="2025-06-25", preco=195.0, companhia ='tap'),
            Voo(pais="Franca", data="2025-06-30", preco=295.0, companhia ='tap'),
            Voo(pais="Franca", data="2025-07-01", preco=195.0, companhia ='tap'),
            Voo(pais="Alemanha", data="2025-06-05", preco=195.0, companhia ='tap'),
            Voo(pais="Alemanha", data="2025-06-06", preco=180.0, companhia ='tap'),
            Voo(pais="Alemanha", data="2025-06-10", preco=175.0, companhia ='tap'),
            Voo(pais="Alemanha", data="2025-06-20", preco=180.0, companhia ='tap'),
            Voo(pais="Alemanha", data="2025-06-25", preco=175.0, companhia ='tap'),
            Voo(pais="Alemanha", data="2025-06-30", preco=100.0, companhia ='tap'),
            Voo(pais="Alemanha", data="2025-07-01", preco=295.0, companhia ='tap'),
            Voo(pais="Espanha", data="2025-06-05", preco=165.0, companhia ='iberia'),
            Voo(pais="Espanha", data="2025-06-06", preco=180.0, companhia ='iberia'),
            Voo(pais="Espanha", data="2025-06-10", preco=175.0, companhia ='iberia'),
            Voo(pais="Espanha", data="2025-06-20", preco=105.0, companhia ='iberia'),
            Voo(pais="Espanha", data="2025-06-25", preco=195.0, companhia ='iberia'),
            Voo(pais="Espanha", data="2025-06-30", preco=205.0, companhia ='iberia'),
            Voo(pais="Espanha", data="2025-07-01", preco=195.0, companhia ='iberia'),
            Voo(pais="Italia", data="2025-06-05", preco=165.0, companhia ='iberia'),
            Voo(pais="Italia", data="2025-06-06", preco=180.0, companhia ='iberia'),
            Voo(pais="Italia", data="2025-06-10", preco=175.0, companhia ='iberia'),
            Voo(pais="Italia", data="2025-06-20", preco=105.0, companhia ='iberia'),
            Voo(pais="Italia", data="2025-06-25", preco=195.0, companhia ='iberia'),
            Voo(pais="Italia", data="2025-06-30", preco=205.0, companhia ='iberia'),
            Voo(pais="Italia", data="2025-07-01", preco=195.0, companhia ='iberia'),
            Voo(pais="Alemanha", data="2025-06-05", preco=265.0, companhia ='iberia'),
            Voo(pais="Alemanha", data="2025-06-06", preco=280.0, companhia ='iberia'),
            Voo(pais="Alemanha", data="2025-06-10", preco=275.0, companhia ='iberia'),
            Voo(pais="Alemanha", data="2025-06-20", preco=205.0, companhia ='iberia'),
            Voo(pais="Alemanha", data="2025-06-25", preco=195.0, companhia ='iberia'),
            Voo(pais="Alemanha", data="2025-06-30", preco=205.0, companhia ='iberia'),
            Voo(pais="Alemanha", data="2025-07-01", preco=195.0, companhia ='iberia'),
            Voo(pais="França", data="2025-06-05", preco=65.0, companhia ='air_france'),
            Voo(pais="França", data="2025-06-06", preco=80.0, companhia ='air_france'),
            Voo(pais="França", data="2025-06-10", preco=100.0, companhia ='air_france'),
            Voo(pais="França", data="2025-06-20", preco=105.0, companhia ='air_france'),
            Voo(pais="França", data="2025-06-25", preco=115.0, companhia ='air_france'),
            Voo(pais="França", data="2025-06-30", preco=50.0, companhia ='air_france'),
            Voo(pais="França", data="2025-07-01", preco=105.0, companhia ='air_france'),
            Voo(pais="Japão", data="2025-06-05", preco=970.0, companhia ='air_france'),
            Voo(pais="Japão", data="2025-06-06", preco=1080.0, companhia ='air_france'),
            Voo(pais="Japão", data="2025-06-10", preco=1075.0, companhia ='air_france'),
            Voo(pais="Japão", data="2025-06-20", preco=1005.0, companhia ='air_france'),
            Voo(pais="Japão", data="2025-06-25", preco=1075.0, companhia ='air_france'),
            Voo(pais="Japão", data="2025-06-30", preco=1005.0, companhia ='air_france'),
            Voo(pais="Japão", data="2025-07-01", preco=1095.0, companhia ='air_france'),
            Voo(pais="Egito", data="2025-06-05", preco=2005.0, companhia ='air_france'),
            Voo(pais="Egito", data="2025-06-06", preco=1095.0, companhia ='air_france'),
            Voo(pais="Egito", data="2025-06-10", preco=310.0, companhia ='air_france'),
            Voo(pais="Egito", data="2025-06-20", preco=380.0, companhia ='air_france'),
            Voo(pais="Egito", data="2025-06-25", preco=375.0, companhia ='air_france'),
            Voo(pais="Egito", data="2025-06-30", preco=305.0, companhia ='air_france'),
            Voo(pais="Egito", data="2025-07-01", preco=295.0, companhia ='air_france'),
            Voo(pais="Tailândia", data="2025-06-05", preco=1010.0, companhia ='air_france'),
            Voo(pais="Tailândia", data="2025-06-06", preco=1080.0, companhia ='air_france'),
            Voo(pais="Tailândia", data="2025-06-10", preco=1075.0, companhia ='air_france'),
            Voo(pais="Tailândia", data="2025-06-20", preco=1005.0, companhia ='air_france'),
            Voo(pais="Tailândia", data="2025-06-25", preco=1905.0, companhia ='air_france'),
            Voo(pais="Tailândia", data="2025-06-30", preco=2005.0, companhia ='air_france'),
            Voo(pais="Tailândia", data="2025-07-01", preco=1095.0, companhia ='air_france'),
            Voo(pais="Alemanha", data="2025-06-05", preco=65.0, companhia ='lufthansa'),
            Voo(pais="Alemanha", data="2025-06-06", preco=80.0, companhia ='lufthansa'),
            Voo(pais="Alemanha", data="2025-06-10", preco=100.0, companhia ='lufthansa'),
            Voo(pais="Alemanha", data="2025-06-20", preco=105.0, companhia ='lufthansa'),
            Voo(pais="Alemanha", data="2025-06-25", preco=115.0, companhia ='lufthansa'),
            Voo(pais="Alemanha", data="2025-06-30", preco=50.0, companhia ='lufthansa'),
            Voo(pais="Alemanha", data="2025-07-01", preco=105.0, companhia ='lufthansa'),
            Voo(pais="Japão", data="2025-06-05", preco=1010.0, companhia ='lufthansa'),
            Voo(pais="Japão", data="2025-06-06", preco=1080.0, companhia ='lufthansa'),
            Voo(pais="Japão", data="2025-06-10", preco=1075.0, companhia ='lufthansa'),
            Voo(pais="Japão", data="2025-06-20", preco=1005.0, companhia ='lufthansa'),
            Voo(pais="Japão", data="2025-06-25", preco=1905.0, companhia ='lufthansa'),
            Voo(pais="Japão", data="2025-06-30", preco=2005.0, companhia ='lufthansa'),
            Voo(pais="Japão", data="2025-07-01", preco=1095.0, companhia ='lufthansa'),
            Voo(pais="Tailândia", data="2025-06-05", preco=970.0, companhia ='lufthansa'),
            Voo(pais="Tailândia", data="2025-06-06", preco=1080.0, companhia ='lufthansa'),
            Voo(pais="Tailândia", data="2025-06-10", preco=1075.0, companhia ='lufthansa'),
            Voo(pais="Tailândia", data="2025-06-20", preco=1005.0, companhia ='lufthansa'),
            Voo(pais="Tailândia", data="2025-06-25", preco=1095.0, companhia ='lufthansa'),
            Voo(pais="Tailândia", data="2025-06-30", preco=2005.0, companhia ='lufthansa'),
            Voo(pais="Tailândia", data="2025-07-01", preco=1095.0, companhia ='lufthansa'),
            Voo(pais="Egito", data="2025-06-05", preco=970.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-06", preco=1080.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-10", preco=1075.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-20", preco=1005.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-25", preco=1095.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-30", preco=2005.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-07-01", preco=1095.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-05", preco=65.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-06", preco=80.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-10", preco=100.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-20", preco=105.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-25", preco=115.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-30", preco=50.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-07-01", preco=105.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-05", preco=65.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-06", preco=80.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-10", preco=100.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-20", preco=105.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-25", preco=115.0, companhia ='egyptair'),
            Voo(pais="Egito", data="2025-06-30", preco=50.0, companhia ='egyptair'),
            Voo(pais="Japão", data="2025-06-05", preco=977.0, companhia ='ana'),
            Voo(pais="Japão", data="2025-06-06", preco=1180.0, companhia ='ana'),
            Voo(pais="Japão", data="2025-06-10", preco=1100.0, companhia ='ana'),
            Voo(pais="Japão", data="2025-06-20", preco=1025.0, companhia ='ana'),
            Voo(pais="Japão", data="2025-06-25", preco=1105.0, companhia ='ana'),
            Voo(pais="Japão", data="2025-06-30", preco=2000.0, companhia ='ana'),
            Voo(pais="Japão", data="2025-07-01", preco=1000.0, companhia ='ana'),
            Voo(pais="Portugal", data="2025-06-05", preco=65.0, companhia ='ana'),
            Voo(pais="Portugal", data="2025-06-06", preco=80.0, companhia ='ana'),
            Voo(pais="Portugal", data="2025-06-10", preco=100.0, companhia ='ana'),
            Voo(pais="Portugal", data="2025-06-20", preco=105.0, companhia ='ana'),
            Voo(pais="Portugal", data="2025-06-25", preco=115.0, companhia ='ana'),
            Voo(pais="Portugal", data="2025-06-30", preco=50.0, companhia ='ana'),
            Voo(pais="Portugal", data="2025-07-01", preco=105.0, companhia ='ana'),
            Voo(pais="Tailândia", data="2025-06-05", preco=970.0, companhia ='ana'),
            Voo(pais="Tailândia", data="2025-06-06", preco=1010.0, companhia ='ana'),
            Voo(pais="Tailândia", data="2025-06-10", preco=1005.0, companhia ='ana'),
            Voo(pais="Tailândia", data="2025-06-20", preco=1080.0, companhia ='ana'),
            Voo(pais="Tailândia", data="2025-06-25", preco=1915.0, companhia ='ana'),
            Voo(pais="Tailândia", data="2025-06-30", preco=2025.0, companhia ='ana'),
            Voo(pais="Tailândia", data="2025-07-01", preco=1005.0, companhia ='ana'),
            Voo(pais="Tailândia", data="2025-06-05", preco=1200.0, companhia ='thai_airways'),
            Voo(pais="Tailândia", data="2025-06-06", preco=1180.0, companhia ='thai_airways'),
            Voo(pais="Tailândia", data="2025-06-10", preco=975.0, companhia ='thai_airways'),
            Voo(pais="Tailândia", data="2025-06-20", preco=1005.0, companhia ='thai_airways'),
            Voo(pais="Tailândia", data="2025-06-25", preco=1205.0, companhia ='thai_airways'),
            Voo(pais="Tailândia", data="2025-06-30", preco=1905.0, companhia ='thai_airways'),
            Voo(pais="Tailândia", data="2025-07-01", preco=1105.0, companhia ='thai_airways'),
            Voo(pais="Japão", data="2025-06-05", preco=1010.0, companhia ='thai_airways'),
            Voo(pais="Japão", data="2025-06-06", preco=1120.0, companhia ='thai_airways'),
            Voo(pais="Japão", data="2025-06-10", preco=1175.0, companhia ='thai_airways'),
            Voo(pais="Japão", data="2025-06-20", preco=1205.0, companhia ='thai_airways'),
            Voo(pais="Japão", data="2025-06-25", preco=1985.0, companhia ='thai_airways'),
            Voo(pais="Japão", data="2025-06-30", preco=2205.0, companhia ='thai_airways'),
            Voo(pais="Japão", data="2025-07-01", preco=1005.0, companhia ='thai_airways'),
            Voo(pais="Brasil", data="2025-06-05", preco=1000.0, companhia ='thai_airways'),
            Voo(pais="Brasil", data="2025-06-06", preco=1050.0, companhia ='thai_airways'),
            Voo(pais="Brasil", data="2025-06-10", preco=1855.0, companhia ='thai_airways'),
            Voo(pais="Brasil", data="2025-06-20", preco=1905.0, companhia ='thai_airways'),
            Voo(pais="Brasil", data="2025-06-25", preco=1955.0, companhia ='thai_airways'),
            Voo(pais="Brasil", data="2025-06-30", preco=1305.0, companhia ='thai_airways'),
            Voo(pais="Brasil", data="2025-07-01", preco=1195.0, companhia ='thai_airways'),
            Voo(pais="Brasil", data="2025-06-05", preco=1100.0, companhia ='latam'),
            Voo(pais="Brasil", data="2025-06-06", preco=1100.0, companhia ='latam'),
            Voo(pais="Brasil", data="2025-06-10", preco=1075.0, companhia ='latam'),
            Voo(pais="Brasil", data="2025-06-20", preco=1185.0, companhia ='latam'),
            Voo(pais="Brasil", data="2025-06-25", preco=1085.0, companhia ='latam'),
            Voo(pais="Brasil", data="2025-06-30", preco=1705.0, companhia ='latam'),
            Voo(pais="Brasil", data="2025-07-01", preco=1325.0, companhia ='latam'),
            Voo(pais="Portugal", data="2025-06-05", preco=165.0, companhia ='latam'),
            Voo(pais="Portugal", data="2025-06-06", preco=180.0, companhia ='latam'),
            Voo(pais="Portugal", data="2025-06-10", preco=190.0, companhia ='latam'),
            Voo(pais="Portugal", data="2025-06-20", preco=155.0, companhia ='latam'),
            Voo(pais="Portugal", data="2025-06-25", preco=105.0, companhia ='latam'),
            Voo(pais="Portugal", data="2025-06-30", preco=150.0, companhia ='latam'),
            Voo(pais="Portugal", data="2025-07-01", preco=170.0, companhia ='latam'),
            Voo(pais="Espanha", data="2025-06-05", preco=95.0, companhia ='latam'),
            Voo(pais="Espanha", data="2025-06-06", preco=70.0, companhia ='latam'),
            Voo(pais="Espanha", data="2025-06-10", preco=90.0, companhia ='latam'),
            Voo(pais="Espanha", data="2025-06-20", preco=175.0, companhia ='latam'),
            Voo(pais="Espanha", data="2025-06-25", preco=135.0, companhia ='latam'),
            Voo(pais="Espanha", data="2025-06-30", preco=120.0, companhia ='latam'),
            Voo(pais="Espanha", data="2025-07-01", preco=145.0, companhia ='latam'),
            
            


        ]
        return self.voos


tap = CompanhiaAeria("TAP Air Portugal")



iberia = CompanhiaAeria("Iberia")
air_france = CompanhiaAeria("Air France")
lufthansa = CompanhiaAeria("Lufthansa")

egyptair = CompanhiaAeria("EgyptAir")

ana = CompanhiaAeria("All Nippon Airways")

thai_airways = CompanhiaAeria("Thai Airways")

latam = CompanhiaAeria("LATAM Airlines")


companhias = [tap, iberia, air_france, lufthansa, egyptair, ana, thai_airways, latam]