import csv, os, time

class FileSaver:
    def __init__(self, variaveis) -> None:
        self.vars = variaveis
        pass

    def __createIfNot(self, path):     
        if not os.path.exists(path):   
            try:
                with open(path, 'a', newline='\n') as file: # Iremos adicionar algo na última linha, e não substiur o arquivo inteiro.
                    tabelacsv = csv.writer(file)
                    tabelacsv.writerow(self.vars)
                    file.close()          
            except (Exception) as e:
                print(f"[ERRO 5] Ocorreu um erro enquanto tentava salvar o cabeçalho na tabela nova: {c}!\n{e}\n")
                pass

    def __nomeArquivoCSV(self) -> str:
        mes_ano = time.strftime("%m_%Y", time.localtime(time.time()))
        semana = time.strftime("%W", time.localtime(time.time()))
    
        c = f'{mes_ano}_semana{semana}.csv' # Separar por dias.
        
        self.__createIfNot(c)

        return c
    
    def saveToCSV(self, data):
        if(len(data) == 0):
            return
        try:
            with open(self.__nomeArquivoCSV(), 'a', newline='\n') as file: # Iremos adicionar algo na última linha, e não substiur o arquivo inteiro.
                tabelacsv = csv.writer(file)
                if not file.closed:
                    tabelacsv.writerow(data)
                    file.close()
                else:
                    print("[AVISO]\nO arquivo estava fechado enquanto tentei salvar dados!\n")
    
        except (Exception) as e:
            print(f"[ERRO 4] Ocorreu um erro enquanto tentava salvar a tabela!\nDado a ser salvo: \"{data}\" \nErro: {e}\n")
            pass
    
    def loadCSV(self, lineCallBack):
        try:
            with open(self.__nomeArquivoCSV(), 'r', newline='\n') as file:
                tabelacsv = csv.reader(file)
    
                for linha in tabelacsv:
                    lineCallBack(linha)
    
                file.close()
        except (Exception) as e:
            print(f"[ERRO 3] Ocorreu um erro enquanto tentava carregar a tabela que já existia!\n{e}\n")
            pass
    