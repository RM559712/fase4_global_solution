#define ldrPin 34      // Pino ADC conectado ao LDR
#define trigPin 5     // Pino GPIO conectado ao Trig do HC-SR04
#define echoPin 18     // Pino GPIO conectado ao Echo do HC-SR04
#define pinLED 23      // Pino GPIO conectado ao resistor de LED
#define pinLEDLight 22      // Pino GPIO conectado ao resistor de LED (lampada)
#define pinLEDLightHome 21 // Pino GPIO conectado ao resistor de LED (interno)
#define pinPIR 17


const float GAMMA = 0.7;
const float RL10 = 50;

void setup() {
    Serial.begin(115200);  // Inicia a comunicação serial
    Serial.println("Inicializando...");

    // Configuração do HC-SR04
    pinMode(trigPin, OUTPUT);   // Define o pino Trig como saída
    pinMode(echoPin, INPUT);    // Define o pino Echo como entrada
    Serial.println("HC-SR04 configurado");

    // Configuração do PIR

    pinMode(pinPIR, INPUT); //Define o pino como entrada
    Serial.println("PIR configurado");

    // Configuração dos LEDs

    pinMode(pinLED, OUTPUT);    // Define o pino do LED como saída
    pinMode(pinLEDLight, OUTPUT);    // Define o pino de lâmpada externa
    pinMode(pinLEDLightHome, OUTPUT);    // Define o pino de lâmpada
    Serial.println("LED configurado"); 
}

float executeMeasurement(int minValue, int maxValue) {

  return minValue + (rand() % (maxValue - minValue + 1)) + (rand() % 100) / 100.0;

}

void loop() {
    Serial.println("Loop iniciado");

    // Leitura do HC-SR04
    long duration;
    int distance;

    // Envia pulso de 10 microsegundos para o trig
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    // Calcula o tempo de duração do pulso de retorno
    duration = pulseIn(echoPin, HIGH);

    //distance = 15;
    distance = executeMeasurement(0, 200);

    // Exibe a distância no monitor serial
    Serial.print("Distância medida: ");
    Serial.print(distance);
    Serial.println(" cm");

    bool isDistance = (distance < 100);

    // Acende o LEDLight se o objeto estiver a uma distância menor que 20 cm
    if (isDistance == true) {
        Serial.println("Objeto se aproximando! Lampada externa ligada!");
        digitalWrite(pinLED, HIGH);
    } else {
        Serial.println("Nenhum objeto próximo. Lampada externa desligada.");
        digitalWrite(pinLED, LOW);
    }

    // Leitura do LDR
    int ldrValue = analogRead(ldrPin); 
    float voltage = ldrValue / 1024. * 5;
    float resistance = 2000 * voltage / (1 - voltage / 5);
    float lux = pow(RL10 * 1e3 * pow(10, GAMMA) / resistance, (1 / GAMMA));

    // Simulação de valores aleatórios
    lux = executeMeasurement(0, 100.000);

    Serial.print("Nível de Luz ( lux ): "); 
    Serial.println(lux); // Exibe o valor lido no monitor serial

    if(lux < 10) {

      float percentualLight = 40.00;

      if(isDistance == true) {

        percentualLight = 100.00;

      }

      // Executar ação para ligar a lâmpada externa
      digitalWrite(pinLEDLight, HIGH); 

      Serial.print("Potência da lâmpada externa: "); 
      Serial.print(percentualLight);
      Serial.println(" %");

    }

    else {

      digitalWrite(pinLEDLight, LOW); 

    }

    // Leitura do PIR
    int pirState = digitalRead(pinPIR);
    if (lux < 10) { // Está escuro
        if (pirState == HIGH) { // Corpo detectado
            digitalWrite(pinLEDLightHome, HIGH); // Liga o LED
            Serial.println("Movimento detectado! Lampada interna ligada.");
        } else { 
            digitalWrite(pinLEDLightHome, LOW); // Desliga o LED
            Serial.println("Sem movimento. Lampada interna desligada.");
        }
    } else { 
        // Está claro, desliga o LED independentemente do movimento
        digitalWrite(pinLEDLightHome, LOW);
        Serial.println("Está claro. Lampada interna desligada.");
    }

   
    delay(1500);
}

