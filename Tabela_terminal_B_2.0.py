import serial
import csv

# Configuração da porta serial
serial_port = 'COM3'  # Substitua 'COM3' pela porta serial do seu Arduino
baud_rate = 9600  # Ajuste para a taxa de transmissão do seu Arduino

# Configuração do arquivo CSV
csv_file_path = 'dados_sensor.csv'

# Função para receber e processar os dados
def receber_dados(arduino_serial):
    dados = arduino_serial.readline().decode().strip().split(',')
    return dados

# Função para salvar os dados no arquivo CSV
def salvar_dados_csv(dados):
    with open(csv_file_path, mode='a', newline='') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerow(dados)

# Função principal
def main():
    # Abre a porta serial
    try:
        porta_serial = serial.Serial(serial_port, baud_rate, timeout=1)
    except serial.SerialException as e:
        print(f"Erro ao abrir a porta serial: {e}")
        return

    # Espera pela mensagem de início do Arduino
    while True:
        mensagem_inicio = porta_serial.readline().decode().strip()
        if mensagem_inicio == "Começar123":
            print("Iniciando recebimento de dados.")
            break

    try:
        while True:
            # Recebe e processa os dados
            dados = receber_dados(porta_serial)

            # Exibe os dados no terminal
            print(dados)

            # Salva os dados no arquivo CSV
            salvar_dados_csv(dados)

    except KeyboardInterrupt:
        print("Programa encerrado pelo usuário.")
    finally:
        porta_serial.close()

if __name__ == "__main__":
    main()
