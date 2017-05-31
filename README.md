![img](http://www.textfiles.com/underconstruction/HeHeartlandBluffs8237Photo_2000construction5_anim.gif)

# OpenEMR AWS Guide

A production grade solution for small facilities and hospitals to run their OpenEMR v5 installation in the AWS cloud.

Many OpenEMR users run their system on premise and have not yet realized the benefits of cloud technologies. This step-by-step guide provides a straightforward approach in getting OpenEMR deployed to the cloud in a secure, reliable, and cloud first way.

This entire process should take about 1 to 2 hours. Be sure to follow the steps exactly and if any instruction confuses you, [enter a bug](https://github.com/GoTeamEpsilon/OpenEMR-AWS-Guide/issues) so our open source team can improve the wording and provide you with support.

_NOTE: A [follow-along YouTube video](https://www.youtube.com/watch?v=foobar) is provided for non-technical users that can benefit from beginner-friendly, enhanced instructions._

## 🚴 Getting Started

#### Start by getting a local copy of OpenEMR v5

1. Download the latest [tarball](http://sourceforge.net/projects/openemr/files/OpenEMR%20Current/5.0.0/openemr-5.0.0.tar.gz/download) to your computer.
2. Extract the contents with your favorite archive extractor.
3. Rename the downloaded "**openemr-5.0.0**" directory to "**openemr**".
4. Enter into the "**openemr**" directory.
5. Create an AWS specific directory called "**.ebextensions**".
6. Download all files in [this](https://github.com/GoTeamEpsilon/OpenEMR-AWS-Guide/tree/master/assets/eb) area to the newly created "**.ebextensions**" directory.

#### Create an AWS Account

1. Navigate to [https://aws.amazon.com/](https://aws.amazon.com/), and then click **Create an AWS Account**.
2. Follow along with the signup wizard.

#### Add yourself as an administrative user

1. Now that you are logged into the AWS Management Console, click **Services** and then click **IAM**.
2. In the left pane, click **Users**.
3. Click **Add user**.
4. Under **Set user details**, enter your username in the **User name** field.
5. Under **Select AWS access type**, select **Programmatic access** and **AWS Management Console access** in the **Access type** area.
6. Click **Next: Permissions**.
7. Under **Set permissions for ...**, click the **Attach existing policies directly**  box.
8. With the table at the bottom of the page in view, select **AdministratorAccess** (will be the first row).
9. Click **Next: Review**.
10. Under **Review**, ensure all information reflects the above steps.
11. Click **Next: Create user**.

#### Restrict permissions to your Root account

_TODO: Revert the **AdministratorAccess** step from above once this is in place :)_

0. Explanation of why this is important since it sometimes confuses me
1. Steps Steps Steps XYZ XYZ XYZ (this includes setting up an individual account, right?)

#### Generate an AWS SSH keypair

1. In the AWS Management Console, click **Services** and then click **EC2**.
2. In the lefthand pane, click **Keypairs**.
3. Click **Create Key Pair**.
4. When the **"Create Key Pair"** dialog appears, enter your username for the **Key pair name** field and click **Create**.
5. When the **Save As** dialog appears, save the key to a safe place.

## ☁ Private Cloud

#### Lock down your system components with a private virtual network

1. In the AWS Management Console, click **Services** and then click **Start VPC Wizard**.
2. Click **VPC with a Single Public Subnet** and click **Select**.
3. In **VPC Name**, enter "**openemr-vpc**".
4. In **Availability Zone**, select your preferred zone. If you aren't sure, select "**No Preference**".
5. Click **Create VPC**.

## 📁 Network File System

#### Provide a network file system to store patient documents and site configuration across systems

1. In the AWS Management Console, click **Services** and then click **EFS**.
2. Click **Create file system**.
3. Under **VPC**, select **"openemr-vpc"**.
4. Under **Create mount targets**, checkbox all items.
5. Click **Next Step**.
6. Under **Add tags**, enter "**openemr-efs**" for the **Key** and "**sys**" for **Value**.
7. Under **Choose performance mode**, select your preferred performance setting. If you aren't sure, select "**General Purpose**".
8. Click **Next Step**.
9. Click **Create File System**.
10. Wait a few moments.
11. Note the **File System ID** in a safe place.

#### Configure OpenEMR servers to mount the shared drive on bootup

1. Open "**openemr/.ebextensions/07-efs-mount-install.config**" and replace "**<<FS ID HERE>>**" with your noted **File System ID** from before.

## 💽 Database System

#### Create a fully managed MySQL database

1. In the AWS Management Console, click **Services** and then click **RDS**.
2. Under **Create Instance**, click **Launch a DB Instance**. If you are using a brand new account, you'll have to click **Instances** in the left-hand pane to get around the marketing screen.
3. Click **MySQL**.
4. Click **Select**.
5. Under **Production**, click **MySQL**.
6. Click **Next Step**.
7. Apply the following under **Instance Specifications**:
    1. In **DB Engine Version**, select "**MySQL 5.6.27**".
    2. In **DB Instance Class**, select your preferred instance size. If you aren't sure, select "**db.t2.large**".
    3. In **Select Multi-AZ Deployment**, select your preferred AZ configuration. If you aren't sure, select "**No**".
    4. In **Storage Type**, select "**General Purpose (SSD)**".
    5. In **Allocated Storage**, select your preferred size. If you aren't sure, enter "**500GB**".
8. Apply the following under **Settings**:
    1. In **DB Instance Identifier**, enter "**openemr-db**".
    2. In **Master User**, enter "**openemr_db_user**".
    3. In **Master Password**, enter a [strong password](https://www.random.org/passwords/?num=1&len=16&format=html&rnd=new). Make sure this is recorded in a safe place.
9. Click **Next Step**.

#### Restrict database access to your private network

1. Apply the following under **Network & Security**
    1. In **VPC**, select "**openemr-vpc**".
    2. In **Subnet Group**, select "**default**".
    3. In **Publicly Accessible**, select "**No**".
    4. In **Availability Zone**, select your preferred zone. If you aren't sure, select "**No Preference**".
    5. In **VPC Security Group(s)**, select "**Create new Security Group**".
2. Apply the following under **Database Options**:
    1. In **Database Name**, enter "**openemr**".
    2. In **Database Port**, enter "**3306**".
    3. In **DB Parameter Group**, select "**default.mysql5.6**".
    4. In **Option Group**, select "**default:mysql-5-6**".
    5. In **Copy Tags To Snapshots**, uncheck box.

#### Setup a data backup strategy

1. Apply the following under **Backup**:
    1. In **Backup Retention Period**, select your preferred days. If you aren't sure, select "**7**".
    2. In **Backup Window**, select "**Select Window**" and choose your preferred window. If you aren't sure, select "**00:00**".

#### Allow for system health checks

1. Apply the following under **Monitoring**:
    1. In **Enable Enhanced Monitoring**, select "**Yes**".
    2. In **Monitoring Role**, select "**Default**".
    3. In **Granularity**, select your preferred second(s). If you aren't sure, select "**60**".

#### Permit minor safety updates to your database engine

1. Apply the following under **Maintenance**:
    1. In **Auto Minor Version Upgrade**, select your preferred strategy. If you aren't sure, select "**Yes**".
    2. In **Maintenance Window**, and choose your preferred window. If you aren't sure, select "**00:00**".

#### Launch your fully configured database

1. Click **Launch Instance**.
2. Click **View your db instances**.
3. Wait many moments for the database to be created.
4. Click on the first row of the **Instances** table.
5. Record the **Endpoint** in a safe place.

## 💻 Session Management

#### Setup Redis cache for user session data storage across servers

1. In the AWS Management Console, click **Services**, **EC2**, and then click **Launch Instance**.
2. Under **Quick Start**, select "**Ubuntu Server 16.04 LTS (HVM), SSD Volume Type**" (ami-80861296).
3. Under **Choose an Instance Type**, select your preferred instance size. If you aren't sure, select "**t2.medium**".
4. Click **Next: Configure Instance Details**.

#### Associate cache with your private network

1. Under **Network**, select "**openemr-vpc**".

#### Provide disk space for the cache when occasional writes are made outside of memory

1. Click **Next: Add Storage**.
2. Under **Size**, select your preferred disk size. If you aren't sure, enter "**8GB**".

#### Launch the instance
1. Click **Review and Launch** and then click **Launch**.
2. Wait a few moments.
3. When **Select an existing key pair or create a new key pair** dialog shows up, select your key pair, accept the terms, and click **Launch Instances**.

#### Specify the name and location of instance

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

#### Provision the server

1. Using the Elastic IP noted from before, SSH into the server. If you aren't sure, please review [How do I SSH into Instances](#how-do-i-ssh-into-instances) section.
2. Call the following script [assets/ec2/redis-setup.sh](assets/ec2/redis-setup.sh) by running it via `curl -s https://raw.githubusercontent.com/GoTeamEpsilon/OpenEMR-AWS-Guide/master/assets/ec2/redis-setup.sh | sh`.
3. Once the script has completed, run `echo $?` and make sure the value printed to the screen is "**0**".

#### Lock down the server
1. In the AWS Management Console, click **EC2** and then click **Running Instances**.
2. Select the "**openemr-redis**" instance.
3. Under **Security groups** in the bottom pane, click the group starting with "**launch-wizard-"**.
4. Note the **Group IP** in a safe place.
5. Click the **Actions** dropdown.
6. Click **Edit inbound rules**.
7. Under **Type**, select "**Custom TCP Rule**" (will originally be "**SSH**").
8. Under **Port Range**, enter 6379 and click **Save**.

#### Configure OpenEMR servers to point at the cache

1. Open "**openemr/.ebextensions/06-redis-configuration.config**" and replace "**<<REDIS_IP>>**" with your noted Elastic ID from before.

## 🖥 Application Servers

#### Configure the servers to use your timezone

1. Open "**openemr/.ebextensions/05-php-configuration.config**" and replace "**<<TIME_ZONE_HERE>>**" with your timezone from the [following list](http://php.net/manual/en/timezones.php). Do not enter spaces (e.g.: "**America\/New_York**" is valid while "**America\/New York**" is not - note the "\\" is required for sed escaping).

#### Prepare your first deployment
1. Archive **openemr** as "**openemr.zip**".

#### Establish fully managed web server infrastructure

1. In the AWS Management Console, click **Services**, **Elastic Beanstalk**, and then click **Create New Application**.
2. Enter "**openemr**" for the **Application Name**
3. Click **Create**.
4. Under **Environments**, click **Create one now**.
5. Select **Web server environment** and click **Select**.
6. Under **Preconfigured platform**, select "**PHP**".

#### Upload your first deployment
1. Under **Application code**, radio check **Upload your code**.
2. Click **Upload** and select "**openemr.zip**". Note that the name of the file must be exact.

#### Lock down your environment

_... TODO ... Assign EC2 instances to their own custom "Instance security groups"_

1. At the bottom of the page, click **Configure more options**.
2. Under **Configuration presets**, radio check "**Custom configuration**".
3. Under **Network**, click **Modify**.
4. Under **Virtual private cloud (VPC)**, select "**openemr-vpc**".
5. Under **Load balancer subnets**, check all entries.
6. Under **Instance subnets**, check all entries.
7. Click **Save**.

#### Establish the environment's capacity

1. Under **Capacity**, click **Modify**.
2. Under **Instances**, enter your desired **Min** and **Max** values. If you aren't sure, enter "**2**" and "**4**", respectively.
3. Under **Placement**, select all entries.
4. Click **Save**.

#### Launch the initial deployment and configure OpenEMR

1. Click **Create environment**.
2. Wait many moments for the environment to build.
3. Click the the URL that looks like **"openemr.abcde12345.my-area-1.elasticbeanstalk.com"** at the top of the screen.
4. At the end of the address bar in your browser, append **"/openemr"** and press enter to start the signup wizard.
5. Go through each step of the signup wizard, using the MySQL credentials noted in previous steps.

#### Post install security updates

1. In the AWS Management Console, click **Services**, **Elastic Beanstalk**, and then click **openemr/openemr**.
2. Click the **Actions** dropdown to the top right and click **Restart App Server(s)** so each instance can perform post-install security updates.

## ▶ Secure Domain Setup

_this section is under construction!!!_
#### Route53 stuff
1. Go to Route53, and in the text box near the middle of the page enter the domain name you'd like to register. This will be what you type in your browser to access your OpenEMR instance.
2. Click "Add To Cart" if the domain is available.
3. If it is n to available, check for another site or choose one of the "Related domain suggestions".
4. Click "Continue"
5. Enter your "Registrant Contact" information. XYZ XYZ XYZ
6. Click Continue
7. Click "Complete Purchase"
8. You should be directed back to the main dashboard.

#### Certificate Manager
1. Go to AWS Certificate Manager
2. Click on "Get Started"
3. In the text box in the middle of the screen type in "yourdomain.com" and then click XYZ and in the new box type "*.yourdomain.com". The asterisk followed by a dot (and then followed by your domain name) is important because it enables SSL for various versions how your site is typed into a browser and later subdomains.
4. Click "Review and request".
5. Click "Confirm and request".
6. The request has now been made. Click "Continue" to head to the next screen where you will see your domain in the "Pending verification" state.
7. Go to the email associated with your account.
8. You might have multiple emails from AWS. Don't worry and simply click the link in each of them and approve.
9. You should now be approved and you have enabled SSL/TLS for your sites on AWS!!!

## 🎛 Administration

#### How do I deploy custom changes to my cloud?

The most robust and maintainable approach for deployments is to keep an internal changelog of your changes along with associated [version control tags](https://git-scm.com/book/en/v2/Git-Basics-Tagging). Not only will this help you stay organized, but you can also reference it in the case you wish to rollback to a previous deployment and aid in reapplying your custom changes when a newer version of OpenEMR is available.

1. In the AWS Management Console, click **Services**, **Elastic Beanstalk**, and then choose **openemr/openemr**.
2. Click the **Upload and Deploy** button in the center of the screen.
3. Click **Choose File** and select "**openemr.zip**". Note that the name of this file must be exact.
4. Under **Label**, enter in **"openemr-deployment-N"** where **N** is most recent version of your deployment.
5. Click **Deploy**.

#### How do I access system logs?

1. In the AWS Management Console, click **Services**, **Elastic Beanstalk**, and then choose **openemr/openemr**.
2. In the lefthand pane, click **Logs**.
3. Click the **Request Logs** button to the to pright of the screen.
4. Click **Full Logs** and wait a moment for the logs to download.
5. Extract the contents with your favorite archive extractor to view each instance's Apache logs in **logs_directory/var/log/httpd**.

#### How do I restore a database backup?

1. In the AWS Management Console, click **Services**, **RDS**.
2. In the lefthand pane, click **Instances**.
3. Checkbox your database instance.
4. Click the **Instance Actions** button in the center of the screen.
5. Click **Restore to Point in Time**.
6. Enter the date and time for your restore under **Use Custom Restore Time**.
7. Configure the database restore instance as you did when [creating the initial system](#-database-system).
8. SSH into any EC2 instance associated with the Elastic Beanstalk environment and note the values in **openemr/sites/default/sqlconf.php**.
9. Update your local **openemr/sites/default/sqlconf.php** with these noted values, but with the new MySQL restore endpoint information.
10. Reploy the application via [the instructions in the deployment section](#how-do-i-deploy-custom-changes-to-my-cloud).

#### How do I Access the Database?

_TODO: Shouldn't this be using the pem file for added security?_

1. In the AWS Management Console, click **Services**, **RDS**.
2. In the lefthand pane, click **Instances**.
3. Checkbox your database instance.
4. Note the database **Endpoint** including the port number.
5. Click the **Instance Actions** button in the center of the screen.
6. Click **Modify**.
7. Under **Network & Security**, select **"Yes"** for **Publicly Accessible**.
8. Click **Continue** and then **Modify DB Instance**.
9. Perform your MySQL work by running `mysql -u (stored database username) -p (stored database password) -h (noted endpoint:port) openemr` on your local computer. If you aren't sure, [download and install MySQL](https://dev.mysql.com/downloads/mysql/) and [familiarize yourself with interacting with data](https://www.google.com/search?q=learn+mysql).
10. Back in the AWS Management Console, reset **Publicly Accessible** to **"No"**, using the previous steps as a guide.

#### How do I SSH Into Instances?

Accessing your instances with SSH is one of the more challenging tasks in this guide. As such, be sure to treat this as a learning opportunity and pay close attention to the instructions to ensure the most seamless experience.

##### Prerequisites

1. Download and install the latest [PuTTY MSI](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) software suite. If you aren't sure, click [here](https://the.earth.li/~sgtatham/putty/latest/w64/putty-64bit-0.69-installer.msi).
2. Using your AWS SSH keypair that is saved as **"your-username.pem"**, convert it to a **ppk** file by following [these instructions](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html#putty-private-key).

##### Redis Access

_TODO: The security group should have a name and not use default launch wizard_

_TODO: Test SSH out with the "my ip address" as source_

1. In the AWS Management Console, click **EC2** and then click **Running Instances**.
2. Select the "**openemr-redis**" instance.
3. Under **Elastic IPs**, note the address.
4. Under **Security groups** in the bottom pane, click the group starting with "**launch-wizard-"**.
5. Click the **Actions** dropdown.
6. Click **Edit inbound rules**.
7. Click **Add Rule**.
8. Under **Type**, select "**SSH**".
9. Under **Source**, select "**Anywhere**".
10. Click **Save**.
11. Using your **"your-username.ppk"** keypair, access your instance by following [these instructions](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html#putty-ssh). Note that step 1 can be skipped and that **"user_name@public_dns_name"** is **"ubuntu@(your previously noted elastic ip)"**.
12. Perform your SSH work.
13. Back in the AWS Management Console, remove the **SSH** inbound rule, using the previous steps as a guide.

##### Elastic Beanstalk Instance Access

_TODO: The security group should have a name and not use default generated group_

_TODO: The security group already have the SSH revoked... currently it is there by default_

_TODO: Test SSH out with the "my ip address" as source_

1. In the AWS Management Console, click **Services**, **EC2**, and then **Running Instances**.
2. Select the **openemr** instance you are interested in accessing.
3. Under **Public DNS (IPv4)**, note the address.
4. Under **Security groups** in the bottom pane, click the first group.
5. Click the **Actions** dropdown.
6. Click **Edit inbound rules**.
7. Click **Add Rule**.
8. Under **Type**, select "**SSH**".
9. Under **Source**, select "**Anywhere**".
10. Click **Save**.
11. Using your **"your-username.ppk"** keypair, access your instance by following [these instructions](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html#putty-ssh). Note that step 1 can be skipped and that **"user_name@public_dns_name"** is **"ec2-user@(your previously noted public dns ip)"**.
12. Perform your SSH work.
13. Back in the AWS Management Console, remove the **SSH** inbound rule, using the previous steps as a guide.

## 📓 Notes

- This is an *alpha* release of the guide. Version 1 proper will be HIPAA/BAA compliant.
- Version 2 will be a fully automated "turnkey" solution that allows users to choose any cloud provider they want, including the option to set up a "local cloud" on premise.

## License

MIT
