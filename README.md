**On Local Computer**

**Program name** - client.py, server1.py, server2.py

Step 1: Set Up the Project Structure
Create a new directory for your project. Inside this directory, create the following subdirectories and files:

distributed_system/
├── server1_files/
│   ├── fileA.txt
│   └── fileB.txt
├── server2_files/
│   ├── fileA.txt
│   └── fileB.txt
├── client.py
├── server1.py
└── server2.py
Step 2: Create Sample Files
    Create a file that is identical on both servers:

    In server1_files/fileA.txt, add the content: This is the original version of file A.

    In server2_files/fileA.txt, add the same content: This is the original version of file A.

    Create a file that is different on the two servers (to simulate a delay in replication):

    In server1_files/fileB.txt, add the content: This is version 1 of file B.

    In server2_files/fileB.txt, add the content: This is version 2 of file B, which is more recent.

    Create a file that only exists on one server (to test availability):

    In server2_files/, create a new file named fileC.txt with the content: This file only exists on SERVER 2.

    Do not create fileC.txt in the server1_files/ directory.

Step 3: Save the code server1.py, server2.py, client.py

Step 4: How to Run the System
    1. Open Terminal 1: Navigate to your distributed_system directory and run server2.py (python server2.py)
    2. Open Terminal 2: Navigate to the same directory and run server1.py (python server1.py)
    3. Open Terminal 3: Navigate to the same directory and run client.py (python client.py)

    4. Now, use the client to test the different conditions of your distributed system.
        Request fileA.txt: The client will request fileA.txt. SERVER 1 will find it locally and also request it from SERVER 2. Since the contents are identical, it will send one copy to the client.


**On AWS Cloud**
Use the same sample files created in above section.

Program name - client_cloud.py, server1_cloud.py, server2_cloud.py

Step 1: Launch three EC2 instance named client_ec2, server1_ec2, server2_ec2
Step 2: while launching the instances, save the pem file to ssh into the ec2 instance.
Step 3: once EC2 launched - ssh into the instance and install python
        sudo yum update -y
        sudo yum install python3 -y
Step 4: secure Copy the server1 files and server1 python program from local to EC2
        scp -i /path/to/my-dist-system-key.pem server1.py ec2-user@<server1-public-ip>:/home/ec2-user/
        scp -i /path/to/my-dist-system-key.pem -r server1_files ec2-user@<server1-public-ip>:/home/ec2-user/

Step 5: secure copy the serever1 files and server1 python program from local to EC1.
        scp -i /path/to/my-dist-system-key.pem server2.py ec2-user@<server2-public-ip>:/home/ec2-user/
        scp -i /path/to/my-dist-system-key.pem -r server2_files ec2-user@<server2-public-ip>:/home/ec2-user/

Step 6: secure copy the client program from the local to EC2
        scp -i /path/to/my-dist-system-key.pem client.py ec2-user@<client-public-ip>:/home/ec2-user/
Step 7: Run the server2 followed by server 1 and then client. client program will prompt to enter the file name and continue with the testing as per the test cases.
