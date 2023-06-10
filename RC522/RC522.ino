//khai báo thư viện
#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <HTTPClient.h>

//khai báo chân
#define SS_PIN 21
#define RST_PIN 22

//wifi kết nối
const char* ssid = "MinhThu";
const char* password = "12345689";

MFRC522 mfrc522(SS_PIN, RST_PIN);  // tạo MFRC522.
HTTPClient http;

//các biến cho việc kết nối server và thôn tin gửi đi
String serverName = "http://192.168.1.166:8000/add";
int readsuccess;
byte readcard[4];
char str[32] = "";
String StrUID;

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  Serial.println(WiFi.localIP());
  SPI.begin();      
  mfrc522.PCD_Init();
}
// --------------------------------------------------------------------
void loop() {
  //nếu đọc thể thành công
  readsuccess = getid();
  if(readsuccess){
    HTTPClient http;    
    String UIDresultSend, postData;
    UIDresultSend = StrUID;  
    //Post Data
    postData = "cardID=" + UIDresultSend;
    http.begin(serverName);  //kết nối tới server   
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");//kiểu kết nối
    int httpCode = http.POST(postData);   //gửi request
    String payload = http.getString();    //lấy dữ liệu phản hồi
    Serial.println(UIDresultSend);
    Serial.println(httpCode);   
    Serial.println(payload);      
    http.end();  //đóng kết nối
    delay(1000);
  }
}
// --------------------------------------------------------------------
int getid(){  
  if(!mfrc522.PICC_IsNewCardPresent()){
    return 0;
  }
  if(!mfrc522.PICC_ReadCardSerial()){
    return 0;
  }
  //lây dữ card ID dưới dạng hex
  for(int i=0;i<4;i++){
    readcard[i]=mfrc522.uid.uidByte[i];
    //từ mảng thành string rồi lưu vào biến StrUID
    array_to_string(readcard, 4, str);
    StrUID = str;
  }
  mfrc522.PICC_HaltA();
  return 1;
}
//lưu các byte của uid kể trên vào 1 mảng rồi từ mảng thành string
void array_to_string(byte array[], unsigned int len, char buffer[])
{
    for (unsigned int i = 0; i < len; i++)
    {
        byte nib1 = (array[i] >> 4) & 0x0F;
        byte nib2 = (array[i] >> 0) & 0x0F;
        buffer[i*2+0] = nib1  < 0xA ? '0' + nib1  : 'A' + nib1  - 0xA;
        buffer[i*2+1] = nib2  < 0xA ? '0' + nib2  : 'A' + nib2  - 0xA;
    }
    buffer[len*2] = '\0';
}
