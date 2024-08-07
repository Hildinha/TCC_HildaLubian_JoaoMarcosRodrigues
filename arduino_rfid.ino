#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// Definicao dos pinos
#define SS_PIN D4
#define RST_PIN D2
#define LED_PIN D1

MFRC522 mfrc522(SS_PIN, RST_PIN);

const char *ssid = "<nomedowifi>";
const char *password = "<senha>";
const char *serverUrl = "http://<localhostgeralmente>/check_permission?sala=101&card_uid=";

WiFiClient client;

void setup() {
  SPI.begin();
  Serial.begin(9600);
  mfrc522.PCD_Init();
  Serial.println("RFID lendo UID");

  // Configuração do pino do LED
  pinMode(LED_PIN, OUTPUT);

  // Conexao com a rede wifi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }
  Serial.println("Conectado!!!");
}

void loop() {
  // Verificacao a respeito de uma nova tag
  if (mfrc522.PICC_IsNewCardPresent()) {
    if (mfrc522.PICC_ReadCardSerial()) {

      String tagUID = getTagUID();
      Serial.print("UID lido: ");
      Serial.println(tagUID);

      if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        String url = String(serverUrl) + tagUID;
        http.begin(client, url);
        int httpCode = http.GET();
        
        if (httpCode > 0) {
          String payload = http.getString();
          Serial.print("Resposta do servidor: ");
          Serial.println(payload);

          payload.trim();
          tagUID.trim();
          Serial.print("Comparando: tagUID = '");
          Serial.print(tagUID);
          Serial.print("' com cartaoUser = '");
          Serial.print(payload);
          Serial.println("'");

          if (tagUID.equalsIgnoreCase(payload)) {
            Serial.println("Acesso Permitido");
            Serial.println("Led piscou duas vezes");
            piscarLED(2); // Pisca o LED duas vezes se o acesso for permitido
          } else {
            Serial.println("Acesso Negado");
          }
        } else {
          Serial.print("Erro na requisição HTTP: ");
          Serial.println(http.errorToString(httpCode));
        }
        
        http.end();
      } else {
        Serial.println("WiFi desconectado");
      }

      mfrc522.PICC_HaltA();
    }
  }
}

// Funcao para obter o UID do cartao como uma string
String getTagUID() {
  String tagUID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    tagUID += (mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
    tagUID += String(mfrc522.uid.uidByte[i], HEX);
  }
  tagUID.toLowerCase();
  return tagUID;
}

// Funcao para piscar o LED
void piscarLED(int vezes) {
  for (int i = 0; i < vezes; i++) {
    digitalWrite(LED_PIN, HIGH); // Acende o LED
    delay(100); // Aguarda 100 milissegundos
    digitalWrite(LED_PIN, LOW); // Apaga o LED
    delay(100); // Aguarda 100 milissegundos
  }
}
