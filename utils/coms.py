import serial
import time

class Coms:
    def __init__(self, comport, baud) -> None:
        self.comport = comport
        self.baud = baud
        self.ser = serial.Serial()
        pass

    def openPort(self):
        try:
            print(f"Iniciando comunicação com Arduino.")        
            self.ser = serial.Serial(self.comport, self.baud, timeout=None)
            return True
        except serial.SerialException as e:
            print(f"[ERRO 1] Erro ao abrir a porta serial: {e}")
            return False

    def handShake(self):
        while True:
            try:
                incoming = self.ser.readline().decode().strip()
    
                if incoming.lower() == "Começar123".lower():
                    print("[INFO] Iniciando recebimento de dados.")
                    break
            except UnicodeDecodeError:
                pass

    def process(self, aoReceber):
        try:
            while True:
                # Recebe e processa os dados
                dados = self.ser.readline().decode().strip().split(',')
                if(not dados[0] == ''):
                    dados.insert(0, time.strftime("%H:%M:%S", time.localtime(time.time())))
                    dados.insert(0, time.strftime("%d/%m/%Y", time.localtime(time.time())))

                    aoReceber(dados)
    
        except Exception as e:
            print(f"[ERRO 2] Erro de comunicação: {e}")
            pass
        finally:
            self.ser.close()