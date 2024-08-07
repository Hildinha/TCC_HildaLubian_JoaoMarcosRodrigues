#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// Definição dos pinos
#define SS_PIN D4
#define RST_PIN D2

MFRC522 mfrc522(SS_PIN, RST_PIN);

const char *ssid = "<nome_do_wifi>";
const char *password = "<senha>";
const char *serverUrl = "http://<localhostgeralmente>/ler?uid=";

WiFiClient client;

void setup() {
  SPI.begin();
  Serial.begin(9600);
  mfrc522.PCD_Init();
  Serial.println("RFID lendo UID");

  // Conexão com a rede Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }
  Serial.println("Conectado ao WiFi!");
}

void loop() {
  // Verificação se há uma nova tag
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

// Função para obter o UID do cartão como uma string
String getTagUID() {
  String tagUID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    tagUID += (mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
    tagUID += String(mfrc522.uid.uidByte[i], HEX);
  }
  tagUID.toLowerCase();
  return tagUID;
}
