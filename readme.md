Command to install Requirements

pip install -r requirements-file

Here requirements file is named "requirements" without any file extension


To Reply to Thread
-------------------------------

./reply.py message-file THREAD_ID

For example in URL
https://bitcointalk.org/index.php?topic=1628.msg164#msg1649
THREAD_ID is 1628



To Edit First Post
--------------------------------------
./editfirst.py message-file THREAD_ID MESSAGE_ID

For example in URL
https://bitcointalk.org/index.php?topic=1628.msg164#msg1649
THREAD_ID is 1628
MESSAGE_ID is 1649

in message-file:

First line will be considered as "Subject" and rest all lines will be "Message Content"


Configuration
-------------------------------------------
Finally, enter your username and password in config.json file.
