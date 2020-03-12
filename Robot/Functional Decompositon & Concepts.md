**Mobile Robot Functional Decomposition**
1. Actuating the wheels to move
2. To store power
3. Microcontroller
4. To recharge itself
5. To indicate status

**Concepts**
1. Actuating the wheels to move
    * DC Geared Motor  
    A very common DC motor with a metal gearbox.
    [Sample-1](https://www.jsumo.com/mp12-micro-gear-motor-6v-500rpm) 
    [Sample-2](https://www.robotistan.com/6v-350rpm-reduktorlu-mikro-dc-motor)
    * RC Servo Motor  
    [FS90R](https://www.pololu.com/product/2820) is considered. Additionally, [SG90](http://www.towerpro.com.tw/product/sg90-7/) can be used but requires a simple hack to make it rotate continuously.
    * Stepper Motor  
    Bipolar, NEMA 8 sized stepper motor is considered([Sample](https://www.robotistan.com/nema-8-200-adim-20x30mm-39v-step-motor-pl-1204)). [28BYJ-48](https://components101.com/motors/28byj-48-stepper-motor) which is a very common unipolar stepper motor could have been considered as a solution but it provides a rotational speed of approximately 10-15 RPM. This speed is not satisfactory for this project. 


2. To store power
    * 18650 Li-ion Battery
    * 14500 Li-ion Battery
    * Li-Po Battery of appropriate size


3. Microcontroller
    * Arduino Nano
    * Raspberry Pi Zero
    * NodeMCU
    * ESP-12E


4. To recharge itself
    * Wireless charger
    * Physical Contact Charge
 

5. To indicate status
    * Addressable LED (NeoPixel)
    * RGB LED
    * Buzzer


**Concepts**

| **Functions / Solutions** | 1 | 2 | 3 | 4 |
| --- | :---: | :---: | :---: | :---: |
| 1. Actuating the wheels to move | DC Geared Motor | RC Servo Motor |Stepper Motor|
| 2. To store power | 18650 Li-ion Battery | 14500 Li-ion Battery | Li-Po Battery |  
| 3. Microcontroller | Arduino Nano | Raspberry Pi Zero | NodeMCU | ESP-12E |
| 4. To recharge itself | Wireless charger | Physical Contact Charge |
| 5. To indicate status | Addressable LED | RGB LED | Buzzer |
