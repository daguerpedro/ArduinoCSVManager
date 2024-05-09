#define ANALOGICO_R1 A0 //Pino analógico conectado com o resistor 1
#define ANALOGICO_R2 A1 //Pino analógico conectado com o resistor 2

#define RESISTOR1 10 //O valor em Ohms do resistor conectado com o ANALOGICO_R1 
#define RESISTOR2 10 //O valor em Ohms do resistor conectado com o ANALOGICO_R2 

#define ONE_WIRE_BUS 6 //Pino digital conectado com o sensor de temperatura DS18B20

#define TEMPO_DE_ESPERA 300000 //O Tempo de espera entre as leituras, em milissegundos




#include <OneWire.h>
#include <DallasTemperature.h>


OneWire oneWire(ONE_WIRE_BUS); // Configuramos uma instancia de comunicação oneWire para os dispositivos que suportam esse tipo de comunicação
DallasTemperature sensors(&oneWire); // Passa a referência oneWire para o sensor de temperatura Dallas


void setup() {
  Serial.begin(9600);  // Inicializa a comunicação serial
  analogReference(INTERNAL); //Muda a tensão de referência para interna de 1.1 V para melhorar a resolução, ative essa linha para leituras na faixa de 0 a 1 V.
  
  sensors.begin(); //Chama a biblioteca referente ao sensor de temperatura

  // Envia a mensagem para começar
  Serial.println("Começar123");
}

void loop() {
  int Val_Leitura_R1, Val_Leitura_R2;
  float Tens_R1, Tens_R2, Resist_R1, Resist_R2, Corrente_R1, Corrente_R2, Potencia_R1, Potencia_R2;

  //Lê os valores de tensão pelas portas analógicas do arduino
  Val_Leitura_R1 = analogRead(ANALOGICO_R1);
  Val_Leitura_R2 = analogRead(ANALOGICO_R2);

  //Converte os valores lidos em valor de tensão em milivolts e salva na variável de tensão
  Tens_R1 = (Val_Leitura_R1 * 1.1 / 1023.0) * 1000;
  Tens_R2 = (Val_Leitura_R2 * 1.1 / 1023.0) * 1000;

  //Calcula o valor da corrente com base na primeira lei de ohm e salva na variável de corrente
  Corrente_R1 = Tens_R1 / RESISTOR1;
  Corrente_R2 = Tens_R2 / RESISTOR2;

  //Calcula o valor da potência e converte de microwatts para miliwatts dividindo por mil
  Potencia_R1 = (Tens_R1 * Corrente_R1) / 1000;
  Potencia_R2 = (Tens_R2 * Corrente_R2) / 1000;


  //Envia os dados separados por vírgulas
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

  sensors.requestTemperatures(); // A função sensors.requestTemperature emite uma temperatura global e faz o requirimento para todos os dispositivos na linha de transmissão
  Serial.println(sensors.getTempCByIndex(0)); //A função sensors.getTempCByIndex(0) é chamada para obter a temperatura do primeiro sensor no barramento. 0 se refere ao primeiro sensor no barramento

  delay((unsigned long)TEMPO_DE_ESPERA);  // Aguarda antes de fazer a próxima leitura
}
