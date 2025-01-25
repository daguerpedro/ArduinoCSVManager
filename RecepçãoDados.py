from utils.filesaver import *
from utils.coms import *
from utils.pytable import *
from utils.API import *

comport = "COM4" # Altere para a porta desejada
baud = 9600 # Frequência desejada

variaveis = ["DIA", "HORA", "mV (MEC1)", "mA (MEC1)", "mW (MEC1)", "mV (MEC2)", "mA (MEC2)", "mW (MEC2)", "°C"]

table = PyTable()
table.alignmentDigits = 12 # Quantos digitos vamos alinhar a tabela no console

useAPI = False
api = API(apiURL = 'http://localhost:8080/data/add')

fileManager = FileSaver(variaveis=variaveis)
comunicacao = Coms(comport=comport, baud=baud)

def aoReceber(dados):
    fileManager.saveToCSV(dados)
    table.addRow(dados)
    
    recebidos = dados
    recebidos.pop(0) # remover a data

    if useAPI == True:
        try:
            res = api.post({
            "hora": str(dados[0]), 
            "tensao1": str(dados[1]), 
            "corrente1": str(dados[2]), 
            "potencia1": str(dados[3]), 
            "tensao2": str(dados[4]), 
            "corrente2": str(dados[5]), 
            "potencia2": str(dados[6]), 
            "temperatura": str(dados[7])
            })

        except:
            pass

def processarLinhasSalvas(linha):
    table.addRow(linha)
    pass

def init():
    try:
        if comunicacao.openPort():
            comunicacao.handShake()

            fileManager.loadCSV(lineCallBack=processarLinhasSalvas)

            comunicacao.process(aoReceber=aoReceber)

    except KeyboardInterrupt:
        print("\nPrograma finalizado.")
 
if __name__ == "__main__":
 
    init()
 
