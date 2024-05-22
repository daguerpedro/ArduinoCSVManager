#define ANALOGICO_R1 A0 //Pino analógico conectado com o resistor 1
#define ANALOGICO_R2 A1 //Pino analógico conectado com o resistor 2

#define RESISTOR1 10 //O valor em Ohms do resistor conectado com o ANALOGICO_R1 
#define RESISTOR2 10 //O valor em Ohms do resistor conectado com o ANALOGICO_R2 

#define ONE_WIRE_BUS 7 //Pino digital conectado com o sensor de temperatura DS18B20

#define TEMPO_DE_ESPERA 1000 //O Tempo de espera entre as leituras, em milissegundos

#include <OneWire.h>
#include <DallasTemperature.h>

#include "ADS1X15.h" // Incluir a biblioteca do ADS
// Construtor do ADS, o parametro é o valor do endereço I2C, configurado pelo pino ADDR na placa do ADS1115.
// https://github.com/RobTillaart/ADS1X15?tab=readme-ov-file#i2c-address
ADS1115 ADS(0x48);

OneWire oneWire(ONE_WIRE_BUS); // Configuramos uma instancia de comunicação oneWire para os dispositivos que suportam esse tipo de comunicação
DallasTemperature sensors(&oneWire); // Passa a referência oneWire para o sensor de temperatura Dallas


void setup() {
  Serial.begin(9600);  // Inicializa a comunicação serial
  Serial.println(__FILE__);
  
  Wire.begin(); // Protocolo I2C
  ADS.begin(); // ADS1115

  sensors.begin(); //Chama a biblioteca referente ao sensor de temperatura

  // Envia a mensagem para começar
  Serial.println("Começar123");
}

/*
| GAIN /  RANGE  | 
|  0  / ±6.144V  | default
|  1  / ±4.096V  |
|  2   / ±2.048V  |  
|  4  / ±1.024V  |  
|  8  / ±0.512V  |  
| 16  / ±0.256V  |
*/ 
void loop() {
  ADS.setGain(4);

  int16_t leitura_tensao_r1 = ADS.readADC(ANALOGICO_R1); 
  int16_t leitura_tensao_r2 = ADS.readADC(ANALOGICO_R2); 
  
  double fator = ADS.toVoltage(1000); // mV

  double tens1 = leitura_tensao_r1 * fator;
  double tens2 = leitura_tensao_r2 * fator;
  
  //Calcula o valor da corrente com base na primeira lei de ohm e salva na variável de corrente
  double Corrente_R1 = tens1 / RESISTOR1;
  double Corrente_R2 = tens2 / RESISTOR2;

  //Calcula o valor da potência e converte de microwatts para miliwatts dividindo por mil
  double Potencia_R1 = (tens1 * Corrente_R1) / 1000;
  double Potencia_R2 = (tens2 * Corrente_R2) / 1000;


  //Envia os dados separados por vírgulas
  Serial.print(tens1, 4);
  Serial.print(",");
  Serial.print(Corrente_R1, 4);
  Serial.print(",");
  Serial.print(Potencia_R1, 4);
  Serial.print(",");
  Serial.print(tens2, 4);
  Serial.print(",");
  Serial.print(Corrente_R2, 4);
  Serial.print(",");
  Serial.print(Potencia_R2, 4);
  Serial.print(",");

  sensors.requestTemperatures(); // A função sensors.requestTemperature emite uma temperatura global e faz o requirimento para todos os dispositivos na linha de transmissão
  Serial.println(sensors.getTempCByIndex(0)); //A função sensors.getTempCByIndex(0) é chamada para obter a temperatura do primeiro sensor no barramento. 0 se refere ao primeiro sensor no barramento

  delay((unsigned long)TEMPO_DE_ESPERA);  // Aguarda antes de fazer a próxima leitura
}
