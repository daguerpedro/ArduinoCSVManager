import serial.tools.list_ports

def listCOMPORTS():
    print(f"Listando portas disponíveis: ")
    for i in serial.tools.list_ports.comports():
        print(f"{i}")

if __name__ == "__main__":
    listCOMPORTS()
