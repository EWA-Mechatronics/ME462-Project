# Fundemental Work Flow 

1. All written py files will be given to everyone, to provide them a freedom about their study intervals.

2. In the sandbox modes, students will not be able to access to the physical  robot arena. They can only use simulations, which will be 
run on their personal computers.

3. In the competetive mode, game manager file will be run at the labarotory computer, and students will not be able to reach that file.
Only admin can manipulate that game manager file. This competetive mode will be able to access to physical robot arena.
Moreover, if admin allows students to practice at competetive mode, students will be able
to connect labratory computer to study at competetive mode.

# Literature Survey and Outcomes about Network Protocols

1. P2P is not suitable for our system, since one crash at one of the groups' py file may lead total crash of the whole system.

2. HTTP based server-client network protocols may create problems because of synchronized communicaiton between server and client.
 Asynchronous communication is desired in this project. Moreover, needed hardware and network requirements for server may not be able 
 to provided.

3. If HTTP based server-client communicaiton is selected, Django is the best way to create it for this project. Djanga is a high-level web frame,
which uses python.

4. MQTT is publish-subscribe network protocol that transports messages between devices. Suitable for high number of devices. Max data size is 260 MB.
It's easy to learn, and also highly compatible with IOT applications.

5. ROS is an open-source, meta-operating system for robots. It provides the services one would expect from an operating system such as
hardware abstraction, low-level device control,message-passing between processes, and package management.
It also provides tools and libraries for obtaining, 
building, writing, and running code across multiple computers. It uses master-node system which is very similar to mqtt in working principles.
 However, it's very complicated  to learn.

6. Creating a manuel server-client system by using sockets is an option. However, probably that will not be efficient as much as other options.
