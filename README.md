# ICS32
# Author: Solar Shao
# UCI ICS32 Material
A simple social network GUI based on temporary socket server created by ICS32 summer2020 instructer: Mark S. Baldwin. 
We implemented the Direct Messaging Protocol created by the instructor and design the interface on our own.
The GUI requires user to have a unique username and password to login. 
If the username has already been taken(the usernamme exists but the input password does not match what it's saved, an error message will appear on the login page). 
If the username aren't taken, then the interface will consider the user's action as creating a new account and saved the information. 
<img width="480" alt="1" src="https://user-images.githubusercontent.com/62400474/166119515-2d40bf5b-0d86-40ae-8e7e-967327df2da1.png">

![Uploading 2.p<img width="480" alt="1" src="https://user-images.githubusercontent.com/62400474/166119506-3d92b822-762d-4086-a1fe-5551f5c4ee68.png">
ng…]()
This is how the window looks like after user successfully logged in.
The add user button could add a new chat window(to the specified receiver's name). If user has sent messages to the receiver, new window will not be added.
Messages has been sorted in a 24h time format with new message appears at the bottom.
Hitting the send button, the message will be sent to the selected user and that message will be pushed to the chat window. If the receiver login their account successfully, they will see this message. 
One thing not support: when sending message, the GUI would not check if the user exists or not but sending the message anyway. 
![FinalVersion](https://user-images.githubusercontent.com/62400474/166119521-139dcd33-8957-4e77-809c-d4d733e14f5c.jpg)
