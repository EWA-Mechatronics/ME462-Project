# About Updates File

Main aim of this file is recording solved problems, recorded at 
the [Problems](https://github.com/EWA-Mechatronics/ME462-Project/blob/master/Software/Problems_and_Updates/Problems.md) file,  of the software part by dates.

### 26.05.2020

- Instances of Robot subclasses, such as Lion() and Deer(), can be created with specified initial coordinates.

- Fixed the issue where the push buttons lost their original colors, when the Game Map Window was opened again after being closed.

- Initial position selection button for **Robot** is added to Game Map Window.

- Initial position selection button for **Target** is added to Game Map Window.

### 27.05.2020

- Fixed the issue where the push buttons lost their functions after,Robot and Target initial positions are assigned.

- Previous **Game Manager** is deleted, because of design considerations.

- In order to create a sustainable design
**Game Manager** is now created as a class, which includes general funcitons that will be used by all game scenarios.
