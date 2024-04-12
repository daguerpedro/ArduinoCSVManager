import serial
import csv
from prettytable import PrettyTable

# Configurar a porta serial
ser = serial.Serial('COM5', 9600)  # Substitua 'COMx' pela porta serial correta

# Aguardar a mensagem do Arduino para começar
while True:
    mensagem = ser.read().decode().strip()
    if mensagem == "Começar123":
        print("Recebeu a mensagem de início.")
        break

# Abrir um arquivo CSV para salvar os dados
with open('dados.csv', 'w', newline='') as arquivo_csv:
    writer = csv.writer(arquivo_csv)

    # Escrever cabeçalhos no arquivo CSV
    writer.writerow(["Tempo", "Tensão MFC 1 (mV)", "Corrente MFC 1 (mA)", "Potência MFC 1 (mW)", "Tensão MFC 2 (mV)", "Corrente MFC 2 (mA)", "Potência MFC 2 (mW)", "Temperatura (ºC)"])

    # Criar uma tabela para exibir os dados
    tabela = PrettyTable()
    tabela.field_names = ["Tempo", "Tensão MFC 1 (mV)", "Corrente MFC 1 (mA)", "Potência MFC 1 (mW)", "Tensão MFC 2 (mV)", "Corrente MFC 2 (mA)", "Potência MFC 2 (mW)", "Temperatura (ºC)"]

    # Definir o tempo limite da comunicação serial
    ser.timeout = 5

    # Continuar lendo dados da porta serial, salvando-os no CSV e exibindo na tabela
    while True:
        try:
            dados = ser.read().decode().strip()
            tempo, tensao1, corrente1, potencia1, tensao2, corrente2, potencia2, temperatura = dados.split(',')
            writer.writerow([tempo, tensao1, corrente1, potencia1, tensao2, corrente2, potencia2, temperatura])
            tabela.add_row([tempo, tensao1, corrente1, potencia1, tensao2, corrente2, potencia2, temperatura])
            print(tabela)
        except serial.SerialTimeoutException:
            # Ignorar erros de tempo limite da comunicação serial
            pass
