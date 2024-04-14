import csv
from prettytable import PrettyTable
import os

csvFile = 'tabela.csv'
variaveis = ["A", "B"]

tabelaconsole = PrettyTable()
tabelaconsole.field_names = variaveis

def saveToCSV(dados):
    try:
        existe = os.path.exists(csvFile)
        with open(csvFile, 'a', newline='') as file: # Iremos adicionar algo na última linha, e não substiur o arquivo inteiro.
            tabelacsv = csv.writer(file)
            if not existe: # Se não existe, vamos criar os parametros, caso contrário vamos apenas adicionar linhas
                tabelacsv.writerow(variaveis)
            
            if not file.closed:
                tabelacsv.writerow(dados)
                tabelaconsole.add_row(dados)
                print(tabelaconsole)
            
                file.close()
            else:
                print(f"!!!! [ERRO] !!!!\nO arquivo {csvFile} estava fechado enquanto tentei salvar dados!\n")
                
    except OSError as e:
        print(f"!!!! [ERRO] !!!!\nOcorreu um erro enquanto tentava salvar a tabela!\n{e.winerror}\n")
        print(e)
        pass

def load():
    existe = os.path.exists(csvFile)
    if not existe:
        return
    
    with open(csvFile, 'r', newline='') as file:
        tabelacsv = csv.reader(file)
        cabecalho = next(tabelacsv)
        tabelaconsole.field_names = cabecalho
        for linha in tabelacsv:
            tabelaconsole.add_row(linha)
        print(tabelaconsole)

        file.close()

load()

for i in range(0, 10):
    saveToCSV([i, pow(i, 2)])