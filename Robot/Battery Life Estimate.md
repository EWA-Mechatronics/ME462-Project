### Estimate Battery Life Calculation
According to our concept evaluation, following components are choosen to be best concepts for the robot.
* DC Gear Motor
* 14500 Li-Ion Battery
* ESP-12E
* Physical contact charge
* RGB Led

#### For this configuration, following battery life estimate for the robot can be made;

Battery &rightarrow; 750 mAh  
DC Motor &rightarrow; ~100 mA x 2  
ESP-12E &rightarrow; 170 mA (max)  
RGB Led &rightarrow; 30 mA  

Total Consumption = 400 mA

Assume a combined 75% efficieny for motor driver and voltage converter &rightarrow; 533 mA consumption

Then the life of the robot becomes;

>**Life** = 750 mAh / 533 mA = 1.4 hours

This life time can easily be doubled if two batteries are used instead of one.
