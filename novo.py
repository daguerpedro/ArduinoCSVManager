import csv, os, time
import serial, serial.tools.list_ports

variaveis = ["HORA", "mV", "mA", "mW", "mV", "mA", "mW"]
digits = 16 # Quantos digitos vamos alinhar

comport = "/dev/ttyUSB0" # Altere para a porta desejada
baud = 9600 

def printtable(data):
    if(len(data) == 0):
        return
     
    last = (len(data) - 1)

    print('|', end = '')
    for d in data:
        position = data.index(d)     

        divisor = ','
        
        stringsize = len(str(d)) #Tamanho do dado recebido
        strtoprint = str(d) #Dado formatado como string
        strformatado = strtoprint # Temporario, se o tamanho for >= digitos de alinhamento é so imprimir essa variavel

        if stringsize < digits: #Precisa alinhar
            missing = digits - stringsize #Quantos faltam para alinhar com 7digitos

            prefix = sufix = ''

            for i in range(0, missing // 2):
                prefix += ' '
                sufix += ' '

            if not (missing % 2) == 0: # Se o tamanho do dado nao for par, vamos adicionar um espaço para alinhar corretamente
                sufix += ' '

            strformatado = prefix + strtoprint + sufix
             

        if position >= last: # Quebrar a linha
            divisor = '|\n'

        # Flush força imprimir o buffer na hora.
        # Apenas usei para testar quando nao tinha o comport
        # Caso tenha dúvidas: https://pt.stackoverflow.com/questions/291779/o-que-%C3%A9-o-par%C3%A2metro-flush-da-fun%C3%A7%C3%A3o-print
        print(strformatado, end = divisor)

# Isso é uma função pois toda vez que for guardar algo na tabela, irá ler essa função que por vez separa as 
# tabelas por dias, semanas ou meses (Ajustável via código), assim como imprime o cabeçalho nela caso ela ainda não exista.
def arquivoCSV() -> str:
    mes_ano = time.strftime("%m_%Y", time.localtime(time.time()))
    semana = time.strftime("%W", time.localtime(time.time()))

    c = f'{mes_ano}_semana{semana}.csv' # Separar por dias.
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

def saveToCSV(data):
    if(len(data) == 0):
        return
    try:
        with open(arquivoCSV(), 'a', newline='\n') as file: # Iremos adicionar algo na última linha, e não substiur o arquivo inteiro.
            tabelacsv = csv.writer(file)
            if not file.closed:
                tabelacsv.writerow(data)
                file.close()
            else:
                print(f"[AVISO]\nO arquivo {csvFile} estava fechado enquanto tentei salvar dados!\n")
                
    except (OSError, Exception) as e:
        print(f"[ERRO]\nOcorreu um erro enquanto tentava salvar a tabela!\n{e}\n")
        pass

def loadCSV():
    try:
        with open(arquivoCSV(), 'r', newline='\n') as file:
            tabelacsv = csv.reader(file)

            for linha in tabelacsv:
                printtable(linha)
            
            file.close()
    except (OSError, Exception) as e:
        print(f"[ERRO]\nOcorreu um erro enquanto tentava carregar a tabela que já existia!\n{e}\n")
        pass

def listenCOMPORT():
    try:
        ser = serial.Serial(comport, baud, timeout=1)
    except serial.SerialException as e:
        print(f"[ERROR] Erro ao abrir a porta serial: {e}")
        return
    
    pong = False
    while not pong:
        handshake = ser.readline().decode().strip()
        
        if handshake.lower() == "Comecar123".lower():
            print("[INFO] Iniciando recebimento de dados.")
            pong = True

    loadCSV()
    
    try:
        while True:
            # Recebe e processa os dados
            dados = ser.readline().decode().strip().split(',')

            dados.insert(0, time.strftime("%H:%M:%S", time.localtime(time.time())))

            saveToCSV(dados)
            printtable(dados)

    except Exception as e:
        print("[ERRO DE COMUNICAÇÃO] {e}")
        pass
    finally:
        ser.close()


def listCOMPORTS():
    print(f"Listando portas disponíveis: ")
    for i in serial.tools.list_ports.comports():
        print(f"   ({(serial.tools.list_ports.comports().index(i)) + 1}) {i}")

# O CODIGO A SEGUIR ESTA DESATIVADO E PODE SER USADO PARA SUBSTITUIR A NECESSIDADE DE EDITAR COMPORT TODA VEZ QUE ABRE, NO ENTANTO FARIA NECESSÁRIO DIGITAR UM NÚMERO NO CONSOLE 
"""
    port = -1

    while port == -1 or (port > (len(ports.comports())-1)):
        try:
            port = int(input(f"Digite o numero da porta desejada: "))
        except (ValueError, Exception):
            pass
    
    comport += port
"""

def init():
    try:
        listCOMPORTS()
        listenCOMPORT()
    except KeyboardInterrupt:
        print("\nPrograma finalizado.")

if __name__ == "__main__":
    init()
