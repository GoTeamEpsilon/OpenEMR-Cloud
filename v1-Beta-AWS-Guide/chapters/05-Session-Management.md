_[< previous chapter](04-Database-System.md) | [next chapter >](06-Application-Servers.md)_

# 💻 Session Management

### Setup Redis cache for user session data storage across servers

1. In the AWS Management Console, click **Services**, **EC2**, and then click **Launch Instance**.
2. Under **Quick Start**, select "**Ubuntu Server 16.04**".
3. Under **Choose an Instance Type**, select your preferred instance size. If you aren't sure, select "**t2.medium**".
4. Click **Next: Configure Instance Details**.

### Associate cache with your private network

1. Under **Network**, select "**openemr-vpc**".
2. Under **Subnet**, select one the "Private" subnet.
3. Select **Protect against accidental termination**.

### Provide disk space for the cache when occasional writes are made outside of memory

1. Click **Next: Add Storage**.
2. Under **Size**, select your preferred disk size. If you aren't sure, enter "**8**".

### Configure security group

1. Click **Next: Add Tags**.
2. **Click to add a Name tag** and call it "Redis".
3. Click **Next: Configure Security Group**.
4. Under **Assign a security group** checkbox **Select an existing security group**.
5. Checkbox **"default"** under **Name**.
6. Click **Review and Launch**.

### Launch the instance
1. Click **Launch**.
2. When **Select an existing key pair or create a new key pair** dialog shows up, select your key pair, accept the terms, and click **Launch Instances**.
3. Wait a few moments.

### Specify the name and location of instance

1. In the AWS Management Console, click **EC2** and then click **Running Instances**.
2. Wait a few moments.
3. Identify the recently created instance.
4. Click the icon in the **Name** column and name the instance "**openemr-redis**".
5. Note the internal IP of the instance.

### Provision the server

1. Using the IP noted from before, SSH into the server as user 'ubuntu'. If you aren't sure, please review [How do I SSH into Instances](../chapters/08-Administration.md#how-do-i-ssh-into-instances) section. Be sure you're logged into the VPN!
2. Setup the server by running the following `curl -s https://raw.githubusercontent.com/GoTeamEpsilon/OpenEMR-Cloud/master/v1-Beta-AWS-Guide/assets/ec2/redis-setup.sh | sh`.

### Configure OpenEMR servers to point at the cache

1. Open "**openemr/.ebextensions/00-options.config**" and replace "**&lt;&lt;enter redis IP here&gt;&gt;**" with your noted internal IP from before.
