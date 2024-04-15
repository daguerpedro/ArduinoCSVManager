import csv, os, random
from time import sleep
import time

variaveis = ["H", "V1", "A1", "P1", "V2", "A2", "P2"]
digits = 18 #Quantos digitos vamos alinhar

def printtable(data):
    last = (len(data) - 1)

    print('|', end = '')
    for d in data:
        pos = data.index(d)     

        divisor = ','
        
        stringsize = len(str(d)) #Tamanho do dado recebido
        strtoprint = str(d) #Dodo formatado como string
        strformatado = strtoprint

        if stringsize < digits: #Precisa alinhar
            missing = digits - stringsize #Quantos faltam para alinhar com 7digitos

            prefix = sufix = ''

            for i in range(0, missing // 2):
                prefix += ' '
                sufix += ' '

            if not (missing % 2) == 0:
                sufix += ' '

            strformatado = prefix + strtoprint + sufix
             

        if pos >= last:
            divisor = '|\n'

        print(strformatado, end = divisor, flush=True)

def arquivoCSV() -> str:
    c = f'tabela{time.strftime("_%d_%m_%Y", time.localtime(time.time()))}.csv'
    if not os.path.exists(c):
        try:
            with open(c, 'a', newline='\n') as file: # Iremos adicionar algo na última linha, e não substiur o arquivo inteiro.
                tabelacsv = csv.writer(file)
                tabelacsv.writerow(variaveis)
                file.close()          
        except (OSError, Exception) as e:
            print(f"[ERRO]\nOcorreu um erro enquanto tentava salvar o cabeçalho na tabela nova: {c}!\n{e}\n")
            pass
    return c

def saveToCSV(dados):
    try:
        with open(arquivoCSV(), 'a', newline='\n') as file: # Iremos adicionar algo na última linha, e não substiur o arquivo inteiro.
            tabelacsv = csv.writer(file)
            if not file.closed:
                tabelacsv.writerow(dados)
                file.close()
            else:
                print(f"[AVISO]\nO arquivo {csvFile} estava fechado enquanto tentei salvar dados!\n")
                
    except (OSError, Exception) as e:
        print(f"[ERRO]\nOcorreu um erro enquanto tentava salvar a tabela!\n{e}\n")
        pass

def load():
    try:
        with open(arquivoCSV(), 'r', newline='\n') as file:
            tabelacsv = csv.reader(file)

            for linha in tabelacsv:
                printtable(linha)
            
            file.close()
    except (OSError, Exception) as e:
        print(f"[ERRO]\nOcorreu um erro enquanto tentava carregar a tabela que já existia!\n{e}\n")
        pass
    
def read():
    for i in range(0, 15): # ADICIONAR COMUNICACAO SERIAL:
        data = [time.strftime("%H:%M:%S;%d/%m", time.localtime(time.time())), random.randint(1, 255), random.randint(1, 255), random.randint(1, 255), random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]
        saveToCSV(data)
        printtable(data)
        sleep(.5)

def init():
    try:
        load()
        read()
    except KeyboardInterrupt:
        print("Programa finalizado.")

if __name__ == "__main__":
    init()