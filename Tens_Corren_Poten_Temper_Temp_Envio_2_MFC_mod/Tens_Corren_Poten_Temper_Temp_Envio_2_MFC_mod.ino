#include <OneWire.h>
#include <DallasTemperature.h>
//Sensor DS18B20 de Temperatura
/*Aqui iremos definir em qual pino digital sera a leitura dos daods no Arduino, 
iremos configurar o pino digital 6, mas esse pode ser alterado*/
#define ONE_WIRE_BUS 6
/*Configuramos uma instancia de comunicação oneWire para os dispositivos que suportam esse tipo de comunicação*/
OneWire oneWire(ONE_WIRE_BUS);
/*Passa a referência oneWire para o sensor de temperatura Dallas*/
DallasTemperature sensors(&oneWire);


const int Pino_Leitura_R1 = A0, Pino_Leitura_R2 = A1;  // Pino analógico onde o sensor está conectado
int Val_Leitura_R1, Val_Leitura_R2;
float Tens_R1, Tens_R2, Resist_R1, Resist_R2, Corrente_R1, Corrente_R2, Potencia_R1, Potencia_R2;
bool Valor_Correto;
char resposta;
unsigned long tempo_inicial = 0; // Variável para armazenar o tempo inicial
unsigned long tempo_atual = 0;   // Variável para armazenar o tempo corrente
unsigned int horas, minutos, segundos;  // Variável unsigned só deve armazenar valores não negativos (zero ou positivos).


void setup() {
  Serial.begin(9600);  // Inicializa a comunicação serial
  analogReference(INTERNAL); //Muda a tensão de referência para interna de 1.1 V para melhorar a resolução, ative essa linha para leituras na faixa de 0 a 1 V.
  Resist_R1 = 560;     //Adicione o valor da resistência externa utilizado no circuito
  Resist_R2 = 560;
  sensors.begin(); //Chama a biblioteca referente ao sensor de temperatura

  // Envia a mensagem para começar
  Serial.println("Começar123");

  tempo_inicial = millis(); //Registra o tempo inicial, ultimo passo antes de entrar no loop para começar as leituras
}

void loop() {
  tardis();
  
  //Lê os valores de tensão pelas portas analógicas do arduino
  Val_Leitura_R1 = analogRead(Pino_Leitura_R1);
  Val_Leitura_R2 = analogRead(Pino_Leitura_R2);

  //Converte os valores lidos em valor de tensão em milivolts e salva na variável de tensão
  Tens_R1 = (Val_Leitura_R1 * 1.1 / 1023.0) * 1000;
  Tens_R2 = (Val_Leitura_R2 * 1.1 / 1023.0) * 1000;

  //Calcula o valor da corrente com base na primeira lei de ohm e salva na variável de corrente
  Corrente_R1 = Tens_R1 / Resist_R1;
  Corrente_R2 = Tens_R2 / Resist_R2;

  //Calcula o valor da potência e converte de microwatts para miliwatts dividindo por mil
  Potencia_R1 = (Tens_R1 * Corrente_R1) / 1000;
  Potencia_R2 = (Tens_R2 * Corrente_R2) / 1000;


  //Cria uma string (sequência de caracteres) com as informações de tempo
  String resultado_Tempo = String(horas) + ":" + String(minutos) + ":" + String(segundos);


  //Envia os dados separados por vírgulas
  Serial.print(resultado_Tempo);
  Serial.print(",");
  Serial.print(Tens_R1, 4);
  Serial.print(",");
  Serial.print(Corrente_R1, 4);
  Serial.print(",");
  Serial.print(Potencia_R1, 4);
  Serial.print(",");
  Serial.print(Tens_R2, 4);
  Serial.print(",");
  Serial.print(Corrente_R2, 4);
  Serial.print(",");
  Serial.print(Potencia_R2, 4);
  Serial.print(",");
  temperatura(); // Função para obter temperatura do sensor DS18B20
  

  delay(300000);  // Aguarda 5 minutos antes de fazer a próxima leitura

}

void tardis() {
  tempo_atual = millis(); // Obtém o tempo atual
  unsigned long tempo_decorrido = (tempo_atual - tempo_inicial) / 1000; // Calcula o tempo decorrido em segundos
  horas = tempo_decorrido / 3600; // Calcula as horas
  minutos = (tempo_decorrido % 3600) / 60; // Calcula os minutos
  segundos = (tempo_decorrido % 3600) % 60; // Calcula os segundos
}

void temperatura() {
  // A função sensors.requestTemperature emite uma temperatura global e faz o requirimento para todos os dispositivos na linha de transmissão
  sensors.requestTemperatures();
  //A função sensors.getTempCByIndex(0) é chamada para obter a temperatura do primeiro sensor no barramento. 0 se refere ao primeiro sensor no barramento
  Serial.println(sensors.getTempCByIndex(0));
}
