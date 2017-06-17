_[< previous chapter](04-Database-System.md) | [next chapter >](06-Application-Servers.md)_

# 💻 Session Management

### Setup Redis cache for user session data storage across servers

1. In the AWS Management Console, click **Services**, **EC2**, and then click **Launch Instance**.
2. Under **Quick Start**, select "**Ubuntu Server 16.04 LTS (HVM), SSD Volume Type**" (ami-80861296).
3. Under **Choose an Instance Type**, select your preferred instance size. If you aren't sure, select "**t2.medium**".
4. Click **Next: Configure Instance Details**.

### Associate cache with your private network

1. Under **Network**, select "**openemr-vpc**".

### Provide disk space for the cache when occasional writes are made outside of memory

1. Click **Next: Add Storage**.
2. Under **Size**, select your preferred disk size. If you aren't sure, enter "**8GB**".

### Launch the instance
1. Click **Review and Launch** and then click **Launch**.
2. Wait a few moments.
3. When **Select an existing key pair or create a new key pair** dialog shows up, select your key pair, accept the terms, and click **Launch Instances**.

### Specify the name and location of instance

1. In the AWS Management Console, click **EC2** and then click **Running Instances**.
2. Wait a few moments.
3. Identify the recently created instance.
4. Click the icon in the **Name** column and name the instance "**openemr-redis**".
5. In the AWS Management Consule, click **Services**, **VPC**, and then click **Elastic IPs**.
6. Click **Allocate new address** and then click **Allocate**.
7. Wait a few moments.
8. A **New address request succeeded** appear. Note the Elastic IP in a safe place.
9. Click **Close**.
10. Checkbox the recent created IP.
11. Click the **Actions** dropdown.
12. Click **Associate address**.
13. Under **Instance**, select "**openemr-redis**".
14. Under **Private IP**, select the first dropdown value and note the IP in a safe place.
15. Click **Associate**.
16. Click **Close**.

### Provision the server

1. Using the Elastic IP noted from before, SSH into the server. If you aren't sure, please review [How do I SSH into Instances](#how-do-i-ssh-into-instances) section.
2. Setup the server by running the following `curl -s https://raw.githubusercontent.com/GoTeamEpsilon/OpenEMR-AWS-Guide/master/AWS-Guide/Assets/ec2/redis-setup.sh | sh`.

### Lock down the server
1. In the AWS Management Console, click **EC2** and then click **Running Instances**.
2. Select the "**openemr-redis**" instance.
3. Under **Security groups** in the bottom pane, click the group starting with "**launch-wizard-"**.
4. Note the **Group IP** in a safe place.
5. Click the **Actions** dropdown.
6. Click **Edit inbound rules**.
7. Under **Type**, select "**Custom TCP Rule**" (will originally be "**SSH**").
8. Under **Port Range**, enter 6379 and click **Save**.

### Configure OpenEMR servers to point at the cache

1. Open "**openemr/.ebextensions/06-redis-configuration.config**" and replace "**<<REDIS_IP>>**" with your noted Elastic ID from before.
