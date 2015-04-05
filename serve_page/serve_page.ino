/**
 * @example TCPServer.ino
 * @brief The TCPServer demo of library WeeESP8266. 
 * @author Wu Pengfei<pengfei.wu@itead.cc> 
 * @date 2015.02
 * 
 * @par Copyright:
 * Copyright (c) 2015 ITEAD Intelligent Systems Co., Ltd. \n\n
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of
 * the License, or (at your option) any later version. \n\n
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include "ESP8266.h"

ESP8266 wifi(Serial1);

void setup(void)
{
  Serial.begin(9600);
  while(!Serial){
    //do nothing 
  }
  Serial.print("setup begin\r\n");

  pinMode(ESP_GPIO0,OUTPUT);
  pinMode(ESP_GPIO2,OUTPUT);
  pinMode(ESP_RESET,OUTPUT);
  pinMode(ESP_CH_PD,OUTPUT);

  digitalWrite(ESP_GPIO0,HIGH);
  digitalWrite(ESP_GPIO2,HIGH);
  digitalWrite(ESP_RESET,LOW);
  digitalWrite(ESP_CH_PD,HIGH);
  delay(100);
  digitalWrite(ESP_RESET,HIGH);
  
  delay(1000);
  wifi.restart();
  delay(1000);

  Serial.print("FW Version:");
  Serial.println(wifi.getVersion().c_str());

  if (wifi.setOprToSoftAP()) {
    Serial.print("to station + softap ok\r\n");
  } 
  else {
    Serial.print("to station + softap err\r\n");
  }
  wifi.setSoftAPParam("MR THERMOSTAT", "", 7, 0);

  /*if (wifi.joinAP("TySock2.4G", "lolamani")) {
    Serial.print("Join AP success\r\n");*/
    Serial.print("IP: ");
    Serial.println(wifi.getLocalIP().c_str());    
  /*} 
  else {
    Serial.print("Join AP failure\r\n");
  }*/

  if (wifi.enableMUX()) {
    Serial.print("multiple ok\r\n");
  } 
  else {
    Serial.print("multiple err\r\n");
  }

  if (wifi.startTCPServer(80)) {
    Serial.print("start tcp server ok\r\n");
  } 
  else {
    Serial.print("start tcp server err\r\n");
  }

  if (wifi.setTCPServerTimeout(10)) { 
    Serial.print("set tcp server timout 10 seconds\r\n");
  } 
  else {
    Serial.print("set tcp server timout err\r\n");
  }
  Serial1.setTimeout(1000);

  Serial.print("setup end\r\n");
}

int generateResponse(uint8_t* buffer) {
  const uint8_t html[189] = "<html><h1>Mr Thermostat Setup</h1><form>Network SSID:<input type=\"text\" name=\"ssid\"><br>Password:<input type=\"password\" name=\"pw\"><br><br><input type=\"submit\" value=\"Submit\"></form></html>";
  int pos;

  for (pos = 0; pos < 188; pos++) {
    buffer[pos] = html[pos];
    delay(1);
  }
  buffer[pos] = 0;
  return pos + 1;
}

void loop(void)
{
  pinMode(ESP_GPIO0,OUTPUT);
  pinMode(ESP_GPIO2,OUTPUT);
  pinMode(ESP_RESET,OUTPUT);
  pinMode(ESP_CH_PD,OUTPUT);

  digitalWrite(ESP_GPIO0,HIGH);
  digitalWrite(ESP_GPIO2,HIGH);
  digitalWrite(ESP_RESET,HIGH);
  digitalWrite(ESP_CH_PD,HIGH);
  
  
  uint8_t buffer[200] = {
    0  };
  uint8_t mux_id;
  uint32_t len = wifi.recv(&mux_id, buffer, sizeof(buffer), 10000);
  //Serial.println("created vars");
  if (len > 0) {
    Serial.print("Status:[");
    Serial.print(wifi.getIPStatus().c_str());
    Serial.println("]");

    Serial.print("Received from :");
    Serial.print(mux_id);
    Serial.print("[");
    for(uint32_t i = 0; i < len; i++) {
      Serial.print((char)buffer[i]);
    }
    Serial.print("]\r\n");
    len = generateResponse(buffer);
    if(wifi.send(mux_id, buffer, len)) {
      Serial.print("send back ok\r\n");
    } 
    else {
      Serial.print("send back err\r\n");
    }

    if (wifi.releaseTCP(mux_id)) {
      Serial.print("release tcp ");
      Serial.print(mux_id);
      Serial.println(" ok");
    } 
    else {
      Serial.print("release tcp");
      Serial.print(mux_id);
      Serial.println(" err");
    }

    Serial.print("Status:[");
    Serial.print(wifi.getIPStatus().c_str());
    Serial.println("]");
  }
}


