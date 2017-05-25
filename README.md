![img](http://www.textfiles.com/underconstruction/HeHeartlandBluffs8237Photo_2000construction5_anim.gif)

# OpenEMR AWS Guide

A turnkey solution for small facilities and hospitals to run their OpenEMR v5 installation in the AWS cloud.

Many OpenEMR users run the system on premise and have not yet realized the benefits of cloud technologies. This step-by-step guide provides a straightforward approach in getting OpenEMR deployed to the cloud in a secure and reliable way.

This entire process should take about an hour. Be sure to follow the steps exactly and if any instruction confuses you, [enter a bug](https://github.com/GoTeamEpsilon/OpenEMR-AWS-Guide/issues) so our team can improve the wording.

## 🚴 Getting Started

#### Start by getting a local copy of OpenEMR v5

1. Download the latest [tarball](http://sourceforge.net/projects/openemr/files/OpenEMR%20Current/5.0.0/openemr-5.0.0.tar.gz/download).
2. Extract the contents with your favorite archive extractor (If you aren't sure, install [7Zip](http://www.7-zip.org/a/7z1700-x64.exe) program and right click the downloaded file to access [7Zip extraction](https://www.youtube.com/watch?v=Z73m14PGs88)).
3. Enter into the "**openemr-5.0.0**" directory.
4. Create the "**.ebextensions**" AWS specific directory for the purposes of this guide with (If you aren't sure, follow [this approach](https://superuser.com/a/331924) to create such a directory).

#### Create an AWS Account

1. Navigate to [https://aws.amazon.com/](https://aws.amazon.com/), and then choose **Create an AWS Account**.
2. Follow along with the signup wizard.

#### Add yourself as an administrative user

1. Now that you are logged into the AWS Management Console, click **Services** and then choose **IAM**.
2. In the left pane, click **Users**.
3. Click **Add user**.
4. Under **Set user details**, enter your username in the **User name** field.
5. Under **Select AWS access type**, select **Programmatic access** in the **Access type** area.
6. Click **Next: Permissions**.
7. Under **Set permissions for ...**, click the **Attach existing policies directly**  box.
8. With the table at the bottom of the page in view, select **AdministratorAccess** (will be the first row).
9. Click **Next: Review**.
10. Under **Review**, ensure all information reflects the above steps.
11. Click **Next: Create user**.

## ☁️ Private Cloud

#### Lock down your system components with a private virtual network

1. In the AWS Management Console, click **Services** and then choose **Start VPC Wizard**.
2. Click **VPC with a Single Public Subnet** and click **Select**.
3. In **VPC Name**, enter "**openemr-vpc**".
4. In **Availability Zone**, select your preferred zone. If you aren't sure, select "**No Preference**".

## 📁 Network File System

#### Provide a network file system to store patient documents and site configuration across systems

1. In the AWS Management Console, click **Services** and then choose **EFS**.
2. Click **Create file system**.
3. Under **VPC**, select **"openemr-vpc"**.
4. Under **Create mount targets**, check all items.
5. Click **Next Step**.
6. Under **Add tags**, enter "**openemr-efs**" for the **Key** and "**sys**" for **Value**.
7. Under **Choose performance mode**, select your preferred performance setting. If you aren't sure, select "**General Purpose**".
8. Click **Next Step**.
9. Click **Create File System**.
10. Wait a few moments.
11. Note the **File System ID**. Make sure this is recorded in a safe place.

#### Configure OpenEMR servers to mount the shared drive on bootup

1. Download the [assets/storage-efs-mountfilesystem.config](assets/storage-efs-mountfilesystem.config) to your local "**openemr-5.0.0/.ebextensions/**" directory.
2. Open "**openemr-5.0.0/.ebextensions/storage-efs-mountfilesystem.config**" and replace "**{{FS_ID_HERE}}**" with your noted ID from before. If you aren't sure, Install [Notepad++](https://notepad-plus-plus.org/repository/7.x/7.3.3/npp.7.3.3.Installer.exe) and right click the file to access Notepad++ editing.

## 💽 Database System

#### Create a fully managed MySQL database

1. In the AWS Management Console, click **Services** and then choose **RDS**.
2. Under **Create Instance**, click **Launch a DB Instance**.
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
    3. In **Master Password**, enter a [strong password](https://www.random.org/passwords/). Make sure this is recorded in a safe place.
9. Click **Next Step**.

#### Restrict database access to your private network

1. Apply the following under **Network & Security**
    1. In **VPC**, select "**openemr-vpc**".
    2. In **Subnet Group**, select "**default**".
    3. In **Publicly Accessible**, select "**No**".
    4. In **Availability Zone**, select your preferred zone. If you aren't sure, select "**No Preference**".
    5. In **VPC Security Group(s)**, select "**Create new Security Group**".
2. Apply the following under **Database Options**:
    1. In **Database Name**, enter "**openemr-db**".
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
3. Wait a few moments.
4. Click on the first row of the **Instances** table.
5. Record the **Endpoint** in a safe place.

## 💻 Session Management

#### Setup Redis cache for user session data storage across servers

1. In the AWS Management Console, click **Services**, **EC2**, and then choose **Launch Instance**.
2. Under **Quick Start**, select "**Ubuntu Server 16.04 LTS (HVM), SSD Volume Type**" (ami-80861296).
3. Under **Choose an Instance Type**, select your preferred instance size. If you aren't sure, select "**t2.medium**".
4. Click **Next: Configure Instance Details**.

#### Associate cache with your private network

1. Under **Network**, select "**openemr-vpc**".

#### Provide disk space for the cache when occasional writes are made outside of memory

1. Click **Next: Add Storage**.
2. Under **Size**, select your preferred disk size. If you aren't sure, enter "**10GB**".

#### Launch the instance
1. Click **Review and Launch**.
2. Wait a few moments.
3. When **Select an existing key pair or create a new key pair** dialog shows up, select your key pair and click **Launch Instances**.

#### Specify the name and location of instance

1. In the AWS Management Console, click **EC2** and then click **Running Instances**.
2. Wait a few moments.
3. Identify the recently created instance.
4. Click the icon in the **Name** column and call the instance "**openemr-redis**".
5. In the AWS Management Consule, click **Services**, **VPC**, and then choose **Elastic IPs**.
6. Click **Allocate new address** and then click **Allocate**.
7. Wait a few moments.
8. A **New address request succeeded** appear. Note the IP in a safe place.
9. Click **Close**.
10. Checkbox the recent created IP.
11. Click the **Actions** dropdown.
12. Click **Associate address**.
13. Under **Instance**, select "**openemr-redis**".
14. Under **Private IP**, select the first dropdown value and note the IP in a safe place.
15. Click **Associate**.
16. Click **Close**.

#### Provision the server

1. SSH into the Redis server and copy/paste [assets/redis-setup.sh](assets/redis-setup.sh) to an executable file and run it. If you aren't sure, watch [this video](www.youtube.com).

#### Lock down the server
1. In the AWS Management Console, click **EC2** and then click **Running Instances**.
2. Select the "**openemr-redis**" instance.
3. Under **Security groups** in the bottom pane, click the group starting with "**launch-wizard-"**.
4. Note the **Group IP** in a safe place.
5. Click the **Actions** dropdown.
6. Click **Edit inbound rules**.
7. Under **Type**, select "**Custom TCP Port**" (will originally be "**SSH**").
8. Under **Port Range**, enter 6379 and click **Save**.

#### Configure OpenEMR servers to point at the cache

1. Download [assets/redis-sessions.config](assets/redis-sessions.config) to your local "**openemr-5.0.0/.ebextensions/**" directory.
2. Open "**openemr-5.0.0/.ebextensions/redis-sessions.config**" and replace "**{{REDIS_IP}}**" with your noted ID from before. If you aren't sure, Install [Notepad++](https://notepad-plus-plus.org/repository/7.x/7.3.3/npp.7.3.3.Installer.exe) and right click the file to access Notepad++ editing.

## 🖥️ Application Servers

_this section is under construction!!!_

#### Configure OpenEMR servers to satify system dependencies on startup

1. Download the [assets/openemr-dependencies.config](assets/openemr-dependencies.config) to your local "**openemr-5.0.0/.ebextensions/**" directory.

#### Prepare your first deployment
1. Archive **openemr-5.0.0** as "**openemr-5.0.0-deployment-1.zip**". If you aren't sure, install [7Zip](http://www.7-zip.org/a/7z1700-x64.exe) program and right click the folder to access [7Zip archival](https://www.youtube.com/watch?v=Z73m14PGs88).

#### Establish fully managed web server infrastructure

1. In the AWS Management Console, click **Services**, **Elastic Beanstalk**, and then choose **Create New Application**.
2. Enter "**openemr**" for the **Application Name**
3. Click **Create**.
4. Under **Environments**, click **Create one now**.
5. Select **Web server environment** and click **Select**.
6. Under **Preconfigured platform**, select "**PHP**".

#### Upload your first deployment
1. Under **Application code**, radio check **Upload your code**.
2. Click **Upload** and select "**openemr-5.0.0-deployment-1.zip**".

#### Lock down your environment
1. At the bottom of the page, click **Configure more options**.
2. Under **Configuration presets**, radio check "**Custom configuration**".
3. Under **Network**, click **Modify**.
4. Under **Virtual private cloud (VPC)**, select "**openemr-vpc**".
14. _... TODO ... Check all items in "Load balancer subnets",_
15. _... TODO ... "Instance subnets", and "Instance security groups", and click "Save"_
16. _... TODO ...  Under "Environment settings", click "Modify"_
17. _... TODO ...  Under "Name", enter "OpenEMR" and click "Save"_
18. _... TODO ...  Under "Capacity", click "Modify"_
19. _... TODO ...  Under "Auto Scaling Group", enter "2" for "min" and click "Save"_
20. _... TODO ...  Click "Create environment"_

#### Configure OpenEMR for use
1. _... TODO ... some general install steps to make sure everything is working_

## ▶️ Secure Domain Setup

_this section is under construction!!!_
### Route53 stuff
Talk about purchasing a domain

### Certificate Manager
using https.

1. Go to AWS Certificate Manager
2. Click on “Get Started”
3. In the text box in the middle of the screen type in “yourdomain.com” and then click XYZ and in the new box type “*.yourdomain.com”. The asterisk followed by a dot (and then followed by your domain name) is important because it enables SSL for various versions how your site is typed into a browser and later subdomains.
4. Click “Review and request”.
5. Click “Confirm and request”.
6. The request has now been made. Click “Continue” to head to the next screen where you will see your domain in the “Pending verification” state.
7. Go to the email associated with your account.
8. You might have multiple emails from AWS. Don’t worry and simply click the link in each of them and approve.
9. You should now be approved and you have enabled SSL/TLS for your sites on AWS!!!

## 🎛️ Administration

_this section is under construction!!!_

Should answer the questions:
- _... TODO ... How do I access the logs?_
- _... TODO ... How do I configure and see my backups?_
- _... TODO ... How do I make changes to my OpenEMR instance and redeploy it to my cloud?_
- _... TODO ... How do I add other system users?_
- _... TODO ... How do I access the database?_

## 📓 Notes

- This is an *alpha* release of the guide. Version 1 proper will be HIPAA/BAA compliant.
- Version 2 will be fully automated and allow users choose any cloud provider they want, including the option to set up a "local cloud".

## License

MIT
