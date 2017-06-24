_[< previous chapter](05-Session-Management.md) | [next chapter >](07-Secure-Domain-Setup.md)_

# 🖥 Application Servers

### Configure the servers to use your timezone

1. Open "**openemr/.ebextensions/05-php-configuration.config**" and replace "**<<TIME_ZONE_HERE>>**" with your timezone from the [following list](http://php.net/manual/en/timezones.php). Do not enter spaces (e.g.: "**America\\/New_York**" is valid while "**America\\/New York**" is not - note the "\\" is required for sed escaping).

### Prepare your first deployment

1. Archive **openemr** as "**openemr.zip**".

### Establish fully managed web server infrastructure

1. In the AWS Management Console, click **Services**, **Elastic Beanstalk**, and then click **Create New Application** to the top right.
2. Enter "**openemr**" for the **Application Name**
3. Click **Create web server**.
4. Under **Preconfigured platform**, select "**PHP**".
5. Click **Next**.

### Upload your first deployment
1. Under **Application code**, radio check **Upload your code**.
2. Click **Upload** and select "**openemr.zip**". Note that the name of the file must be exact.
3. Click **Next**.

### Name the environment

1. Under **Environment name**, enter **"<<your_practice>>"**.
2. Click **Next**.

### Lock down your environment

1. Under **Additional Resources**, checkbox **"Create this environment inside a VPC"**.
2. Click **Next**.

### Configure Instance Servers

1. Select an instance size under **Instance type**. If you're not sure, select **"t1.micro"**.
2. Under **EC2 key pair**, select your keypair.
3. Under **Email address**, enter your email.
4. Click **Next** twice.

### Attach environment to VPC

1. Under **VPC**, select the VPC that includes **"10.0.0.0/16"**.
2. Under the subnet table, checkbox all rows.
3. Under **VPC security group**, select the **"openemr-vpc"** default security group id.
4. Click **Next** twice and then click **Launch**.
5. Wait many moments for the environment to be created.

### Establish the environment's initial capacity

1. Click **Configuration**.
2. Under **Scaling**, click the gear icon.
3. Under **Auto Scaling**, enter "**1**" for **Minimum instance count** and "**1**" for **Maximum instance count** values. These values will be changed later, a single instance will be used to set the baseline for the EFS.
4. Click **Apply**.

### Extend the load balancer idle timeout

1. In the AWS Management Console, click **EC2** and then click **Load Balancer** in the left hand pane.
2. Checkbox the first load balancer.
3. In the the bottom hand pane, scroll down to the **Attributes** area.
4. Click **Edit idle timeout**.
5. For **Idle timeout**, enter **"3600"**.
6. Click **Save**.

### OpenEMR setup

1. Visit your Elastic Beanstalk URL. It should look look like **"your_practice.my-area-1.elasticbeanstalk.com"**.
2. At the end of the address bar in your browser, append **"/openemr"** and press enter to start the signup wizard.
3. Go through each step of the signup wizard, using the MySQL credentials noted in previous steps.

### Post-install security update

1. In the AWS Management Console, click **EC2** and then click **Instances** in the left hand pane.
2. Clickbox the running **your_practice** instance and note the **Public DNS (IPv4)** in the bottom pane.
3. Using this IP, SSH into the server. If you aren't sure, please review [How do I SSH into Instances](#how-do-i-ssh-into-instances) section.
4. Run `sudo /opt/elasticbeanstalk/hooks/appdeploy/post/09-post-install-setup-file-deletion.sh` to manually remove public setup files (will be ran automatically when subsequent instances are created by ElasticBeanstalk).

### Establish the environment's maximum capacity

1. In the AWS Management Console, click **Services**, **Elastic Beanstalk**, and then choose **openemr/your_practice**.
2. Click **Configuration**.
3. Under **Scaling**, click the gear icon.
4. Under **Auto Scaling**, enter your desired **Minimum instance count** and **Maximum instance count** values. If you aren't sure, enter "**2**" and "**4**", respectively.
5. Click **Apply**.
