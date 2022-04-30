# ICS32
# Author: Solar Shao
# UCI ICS32 Material
A simple social network GUI based on temporary socket server created by ICS32 summer2020 instructer: Mark S. Baldwin. 
We implemented the Direct Messaging Protocol created by the instructor and design the interface on our own.
The GUI requires user to have a unique username and password to login. 

<p align="center"><img width="480" alt="1" src="https://user-images.githubusercontent.com/62400474/166119515-2d40bf5b-0d86-40ae-8e7e-967327df2da1.png"></p>

<p align="center"><img width="481" alt="2" src="https://user-images.githubusercontent.com/62400474/166119710-dba6ae7c-af99-4a4c-8cc5-30a1a7ae7247.png"></p>

If the username has already been taken(the usernamme exists but the input password does not match what it's saved, an error message will appear on the login page). 
If the username aren't taken, then the interface will consider the user's action as creating a new account and saved the information. 

![InvalidUsername](https://user-images.githubusercontent.com/62400474/166119729-1b31eb7b-28ca-4c21-a8ca-1f22af95d1f7.jpg)

This is how the window looks like after user successfully logged in.
The add user button could add a new chat window(to the specified receiver's name). If user has sent messages to the receiver, new window will not be added.
Messages has been sorted in a 24h time format with new message appears at the bottom.
Hitting the send button, the message will be sent to the selected user and that message will be pushed to the chat window. If the receiver login their account successfully, they will see this message. 
One thing not support: when sending message, the GUI would not check if the user exists or not but sending the message anyway. 

![FinalVersion](https://user-images.githubusercontent.com/62400474/166119521-139dcd33-8957-4e77-809c-d4d733e14f5c.jpg)

