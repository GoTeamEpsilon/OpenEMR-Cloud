_[< previous chapter](04-Database-System.md) | [next chapter >](06-Application-Servers.md)_

# 💻 Session Management

### Create environment security group

1. In the AWS Management Consule, click **Services**, **VPC**, and then click **Security Groups**.
2. Click **Create Security Group**.
3. Under **Name tag**, **Description**, and **Group name** enter **"redis"**.
4. Under **VPC**, select the recently created **"openemr-vpc"**.
5. Click **Yes, Create**.
6. Wait a moment.
7. Note the Group ID.
8. In the bottom pane, click **Inbound Rules** and then **Edit**.
9. For the first row, select **"CUSTOM TCP Rule"**, protocol **"TCP"**, port **"6379"**, and source of the Security Group ID of the recently created VPC.
10. For the second row, select **"SSH"**, protocol **"TCP"**, port **"22"**, and source of **"0.0.0.0/0"**. Note this source will be locked down at a later time in the setup.
11. Click **Save**.

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

### Configure security group

1. Click **Next: Add Tags**.
2. Click **Next: Configure Security Group**.
3. Under **Assign a security group** checkbox **Select an existing security group**.
4. Checkbox **"redis"** under **Name**.
5. Click **Review and Launch**. Note that you can ignore the "Improve your instances' security..." message for now.

### Launch the instance
1. Click **Launch**.
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
14. Under **Private IP**, select the first dropdown value and note this internal IP in a safe place.
15. Click **Associate**.
16. Click **Close**.

### Provision the server

1. Using the Elastic IP noted from before, SSH into the server. If you aren't sure, please review [How do I SSH into Instances](#how-do-i-ssh-into-instances) section.
2. Setup the server by running the following `curl -s https://raw.githubusercontent.com/GoTeamEpsilon/OpenEMR-AWS-Guide/master/AWS-Guide/Assets/ec2/redis-setup.sh | sh`.

### Lock down the server

1. In the AWS Management Console, click **Services**, **VPC**, and then click **Security Groups**.
2. Click **redis**.
3. In the bottom pane, click **Inbound Rules** and then **Edit**.
4. Click the **x** on the **SSH** row.
5. For the **"CUSTOM TCP Rule"** row, edit the **source** to be the **openemr-vpc** default security group id.
6. Click **Save**.

### Configure OpenEMR servers to point at the cache

1. Open "**openemr/.ebextensions/06-redis-configuration.config**" and replace "**<<REDIS_IP>>**" with your noted internal IP from before.
