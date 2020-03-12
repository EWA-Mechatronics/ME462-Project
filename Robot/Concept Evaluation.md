### Evaluation Criteria
- Cost
- Size
- Weight
- Reliability
- Reparability
- Replaceability
- Power Consumption
- Energy Density (Wh/L)
- Processing Capability
- Wireless Capability
- Number of GPIO Pins
- Time to Implement
- Functionality<br><br>

### Concept Evaluation
***1. Actuating the wheels to move***

|                  |                   | DC Geared Motor   | RC Servo Motor | Stepper Motor |
| ---              | :---:             | :---:             | :---:          | :---:         |
| **Criteria**     | **Weight Factor** | Score/Rating      | Score/Rating   | Score/Rating  |
| Cost             |               0.1 |           4 / 0.4 |        3 / 0.3 |       2 / 0.2 |
| Size             |              0.15 |          3 / 0.45 |       3 / 0.45 |       2 / 0.3 |
| Weight           |               0.1 |           4 / 0.4 |        4 / 0.4 |       2 / 0.2 |
| Reliability      |              0.15 |           4 / 0.6 |       3 / 0.45 |       4 / 0.6 |
| Replaceability   |               0.1 |           4 / 0.4 |        3 / 0.3 |       4 / 0.4 |
| Power Consumption|               0.2 |           4 / 0.8 |        3 / 0.6 |       2 / 0.4 |
| Time to Implement|               0.2 |           3 / 0.6 |        4 / 0.8 |       4 / 0.8 |
| *Total*          |                 1 |              3.65 |            3.3 |           2.9 |

<br><br>
**2. To store power**

|                  |                 |18650 Li-ion Battery|14500 Li-ion Battery|Li-Po Battery|
| ---              | :---:           | :---:              | :---:              | :---:       |
| **Criteria**     |**Weight Factor**| Score/Rating       | Score/Rating       | Score/Rating|
| Cost             |            0.15 |            4 / 0.6 |            4 / 0.6 |    3 / 0.45 |
| Size             |             0.2 |            3 / 0.6 |            4 / 0.8 |     4 / 0.8 |
| Reliability      |            0.15 |           3 / 0.45 |           3 / 0.45 |     4 / 0.6 |
| Replaceability   |            0.15 |            4 / 0.6 |            4 / 0.6 |     4 / 0.6 |
| Energy Density   |             0.2 |            4 / 0.8 |            4 / 0.8 |     3 / 0.6 |
| Time to Implement|            0.15 |            4 / 0.6 |            4 / 0.6 |     4 / 0.6 |
| *Total*          |               1 |               3.65 |               3.85 |        3.65 |

<br><br>
**3. Microcontroller**
|  |  | Arduino Nano | Raspberry Pi Zero | NodeMCU | ESP-12E |
| --- | :---: | :---: | :---: | :---: | :---: |
| **Criteria** | **Weight Factor** | Score/Rating | Score/Rating | Score/Rating | Score/Rating |
| Cost | 0.15 | 4 / 0.6 | 2 / 0.3 | 3 / 0.45 | 4 / 0.6 |
| Size | 0.15 | 4 / 0.6 | 3 / 0.45 | 3 / 0.45 | 4 / 0.6 |
| Reliability | 0.1 | 4 / 0.4 | 4 / 0.4 | 4 / 0.4 | 4 / 0.4 |
| Replaceability | 0.05 | 4 / 0.2 | 4 / 0.2 | 4 / 0.2 | 4 / 0.2 |
| Power Consumption | 0.1 | 4 / 0.4 | 1 / 0.1 | 2 / 0.2 | 3 / 0.3 |
| Wireless Capability | 0.2 | 0 / 0 | 2 / 0.4 | 4 / 0.8 | 4 / 0.8 |
| Number of GPIO Pins | 0.05 | 3 / 0.15 | 4 / 0.2 | 3 / 0.15 | 3 / 0.15 |
| Time to Implement | 0.1 | 2 / 0.2 | 1 / 0.1 | 4 / 0.4 | 3 / 0.3 |
| Functionality | 0.1 | 1 / 0.1 | 2 / 0.2 | 4 / 0.4 | 4 / 0.4 |
| Total | 1 | 2.65 | 2.35 | 3.45 | 3.75 |

<br><br>
**4. To recharge itself**

|                  |                 |Wireless charger|Physical Contact Charge|
| ---              | :---:           | :---:          | :---:                 |
| **Criteria**     |**Weight Factor**| Score/Rating   | Score/Rating          |
| Cost             |            0.25 |       3 / 0.75 |               4 / 1.0 |
| Reliability      |             0.3 |        3 / 0.9 |               3 / 0.9 |
| Reparability     |            0.25 |        2 / 0.5 |               4 / 1.0 |
| Time to Implement|             0.2 |        2 / 0.4 |               2 / 0.4 |
| Total            |               1 |           2.55 |                   3.3 |

<br><br>
**5. To indicate status**

|  |  | Addressable LED | RGB LED | Buzzer |
| --- | :---: | :---: | :---: | :---: |
| **Criteria** | **Weight Factor** | Score/Rating | Score/Rating | Score/Rating |
| Cost | 0.15 | 2 / 0.3 | 4 / 0.6 | 4 / 0.6 |
| Size | 0.2 | 4 / 0.8 | 4 / 0.8 | 3 / 0.6 |
| Reliability | 0.15 | 3 / 0.45 | 4 / 0.6 | 3 / 0.45 |
| Replaceability | 0.15 | 4 / 0.6 | 4 / 0.6 | 4 / 0.6 |
| Power Consumption | 0.1 | 4 / 0.4 | 4 / 0.4 | 4 / 0.4 |
| Time to Implement | 0.1 | 3 / 0.3 | 2 / 0.2 | 3 / 0.3 |
| Functionality | 0.15 | 4 / 0.6 | 2 / 0.3 | 1 / 0.15 |
| Total | 1 | 3.45 | 3.5 | 3.1 |
