![img](http://www.textfiles.com/underconstruction/HeHeartlandBluffs8237Photo_2000construction5_anim.gif)

# OpenEMR AWS Guide

A turnkey solution for small facilities and hospitals to run their OpenEMR v5 installation in the AWS cloud.

Many OpenEMR users run the system on premise and have not yet realized the benefits of cloud technologies. This step-by-step guide provides a straightforward approach in getting OpenEMR deployed to the cloud in a secure and reliable way.

## 🚴 Getting Started

This entire process should take about an hour. Be sure to follow the steps exactly and if any instruction confuses you, [enter a bug](https://github.com/GoTeamEpsilon/OpenEMR-AWS-Guide/issues) so our team can improve the process.

### To start things off, let's clone OpenEMR v5 to the local computer.

1. Download the latest [tarball](http://sourceforge.net/projects/openemr/files/OpenEMR%20Current/5.0.0/openemr-5.0.0.tar.gz/download).
2. Extract the contents with your favorite archive extractor (If you aren't sure, install [7Zip](http://www.7-zip.org/a/7z1700-x64.exe) program and right click the downloaded file to access 7Zip extraction).
3. Enter into the "**openemr-5.0.0**" directory.
4. Create the "**.ebextensions**" AWS specific directory for the purposes of this guide with (If you aren't sure, follow [this approach](https://superuser.com/a/331924) to create such a directory).
5. Download the [openemr-dependencies.config](assets/openemr-dependencies.config) to your local "**openemr-5.0.0/.ebextensions/**" directory.

### Let’s create an AWS account and set you up as an administrative user.

1. Navigate to [https://aws.amazon.com/](https://aws.amazon.com/), and then choose **Create an AWS Account**.
2. Follow along with the signup wizard.
3. Now that you are logged into the AWS Management Console, click **Services** and then choose **IAM**.
4. In the left pane, click **Users**.
5. Click **Add user**.
6. Under **Set user details**, enter your username in the **User name** field.
7. Under **Select AWS access type**, select **Programmatic access** in the **Access type** area.
8. Click **Next: Permissions**.
9. Under **Set permissions for ...**, click the **Attach existing policies directly**  box.
10. With the table at the bottom of the page in view, select **AdministratorAccess** (will be the first row).
11. Click **Next: Review**.
12. Under **Review**, ensure all information reflects the above steps.
13. Click **Next: Create user**.

## ☁️ Private Cloud

Locking down system components to a private virtual network provides an extra layer of security and configurability on the cloud. The following steps will step up a network with outbound access to the public internet.

1. In the AWS Management Console, click **Services** and then choose **Start VPC Wizard**.
2. Click **VPC with a Single Public Subnet** and click **Select**.
3. In **VPC Name**, enter "**openemr-vpc**".
4. In **Availability Zone**, select your preferred zone. If you aren't sure, select "**No Preference**".

## 📁 Network File System

OpenEMR stores patient documents and site-specific data on disk. Setting up a network file system to store these files will provide an access mechanism for each server.

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
12. Download the [storage-efs-mountfilesystem.config](assets/storage-efs-mountfilesystem.config) to your local "**openemr-5.0.0/.ebextensions/**" directory.
13. Open "**openemr-5.0.0/.ebextensions/storage-efs-mountfilesystem.config**" and replace "**{{FS_ID_HERE}}**" with your noted ID from before. If you aren't sure, Install [Notepad++](https://notepad-plus-plus.org/repository/7.x/7.3.3/npp.7.3.3.Installer.exe) and right click the file to access Notepad++ editing.

## 💽 Database System

MySQL is the database of OpenEMR. Fortunately, it is trivial to set up a managed database in the cloud that will scale, self-heal, and backup without manual intervention.

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
10. Apply the following under **Network & Security**:
    1. In **VPC**, select "**openemr-vpc**".
    2. In **Subnet Group**, select "**default**".
    3. In **Publicly Accessible**, select "**No**".
    4. In **Availability Zone**, select your preferred zone. If you aren't sure, select "**No Preference**".
    5. In **VPC Security Group(s)**, select "**Create new Security Group**".
11. Apply the following under **Database Options**:
    1. In **Database Name**, enter "**openemr-db**".
    2. In **Database Port**, enter "**3306**".
    3. In **DB Parameter Group**, select "**default.mysql5.6**".
    4. In **Option Group**, select "**default:mysql-5-6**".
    5. In **Copy Tags To Snapshots**, uncheck box.
12. Apply the following under **Backup**:
    1. In **Backup Retention Period**, select your preferred days. If you aren't sure, select "**7**".
    2. In **Backup Window**, select "**Select Window**" and choose your preferred window. If you aren't sure, select "**00:00**".
13. Apply the following under **Monitoring**:
    1. In **Enable Enhanced Monitoring**, select "**Yes**".
    2. In **Monitoring Role**, select "**Default**".
    3. In **Granularity**, select your preferred second(s). If you aren't sure, select "**60**".
14. Apply the following under **Maintenance**:
    1. In **Auto Minor Version Upgrade**, select your preferred strategy. If you aren't sure, select "**Yes**".
    2. In **Maintenance Window**, and choose your preferred window. If you aren't sure, select "**00:00**".
15. Click **Launch Instance**.
16. Click **View your db instances**.
17. Wait a few moments.
18. Click on the first row of the **Instances** table.
19. Record the **Endpoint** in a safe place.


## 💻 Session Management

In order to support running OpenEMR on many servers, user session data must be stored in a centralized area. Redis will be used for this purpose.

1. In the AWS Management Console, click **Services**, **EC2**, and then choose **Launch Instance**.
2. Under **Quick Start**, select "**Ubuntu Server 16.04 LTS (HVM), SSD Volume Type**" (ami-80861296).
3. Under **Choose an Instance Type**, select your preferred instance size. If you aren't sure, select "**t2.medium**".
4. Click **Next: Configure Instance Details**.
5. Under **Network**, select "**openemr-vpc**".
6. Click **Next: Add Storage**.
7. Under **Size**, select your preferred disk size. If you aren't sure, enter "**10GB**".
8. Click **Review and Launch**.
9. Wait a few moments.
10. When **Select an existing key pair or create a new key pair** dialog shows up, select your key pair and click **Launch Instances**.
11. In the AWS Management Console, click **EC2** and then click **Running Instances**.
12. Wait a few moments.
13. Identify the recently created instance.
14. Click the icon in the **Name** column and call the instance "**openemr-redis**".
15. In the AWS Management Consule, click **Services**, **VPC**, and then choose **Elastic IPs**.
16. Click **Allocate new address** and then click **Allocate**.
17. Wait a few moments.
18. A **New address request succeeded** appear. Note the IP in a safe place.
19. Click **Close**.
20. Checkbox the recent created IP.
21. Click the **Actions** dropdown.
22. Click **Associate address**.
23. Under **Instance**, select "**openemr-redis**".
24. Under **Private IP**, select the first dropdown value and note the IP in a safe place.
25. Click **Associate**.
26. Click **Close**.
27. SSH into the Redis server and copy/paste [redis-setup.sh](assets/redis-setup.sh) to an executable file and run it. if you aren't sure, watch [this video](www.youtube.com).
28. In the AWS Management Console, click **EC2** and then click **Running Instances**.
29. Select the "**openemr-redis**" instance.
30. Under **Security groups** in the bottom pane, click the group starting with "**launch-wizard-"**.
31. Note the **Group IP** in a safe place.
32. Click the **Actions** dropdown.
33. Click **Edit inbound rules**.
34. Under **Type**, select "**Custom TCP Port**" (will originally be "**SSH**").
35. Under **Port Range**, enter 6379 and click **Save**.
36. Download [redis-sessions.config](assets/redis-sessions.config) to your local "**openemr-5.0.0/.ebextensions/**" directory.
37. Open "**openemr-5.0.0/.ebextensions/redis-sessions.config**" and replace "**{{REDIS_IP}}**" with your noted ID from before (step 18). If you aren't sure, Install [Notepad++](https://notepad-plus-plus.org/repository/7.x/7.3.3/npp.7.3.3.Installer.exe) and right click the file to access Notepad++ editing.


## 🖥️ Application Servers

1. Archive **openemr-5.0.0** as "**openemr-5.0.0-deployment-1.zip**". If you aren't sure, install [7Zip](http://www.7-zip.org/a/7z1700-x64.exe) program and right click the folder to access 7Zip archival.
2. In the AWS Management Console, click **Services**, **Elastic Beanstalk**, and then choose **Create New Application**.
3. Enter "**openemr**" for the **Application Name**
4. Click **Create**.
5. Under **Environments**, click **Create one now**.
6. Select **Web server environment** and click **Select**.
7. Under **Preconfigured platform**, select "**PHP**".
8. Under **Application code**, radio check **Upload your code**.
9. Click **Upload** and select "**openemr-5.0.0-deployment-1.zip**".
10. At the bottom of the page, click **Configure more options**.
11. Under **Configuration presets**, radio check "**Custom configuration**".
12. Under **Network**, click **Modify**.
13. Under **Virtual private cloud (VPC)**, select "**openemr-vpc**".
14. _... TODO ... Check all items in "Load balancer subnets",_
15. _... TODO ... "Instance subnets", and "Instance security groups", and click "Save"_
16. _... TODO ...  Under "Environment settings", click "Modify"_
17. _... TODO ...  Under "Name", enter "OpenEMR" and click "Save"_
18. _... TODO ...  Under "Capacity", click "Modify"_
19. _... TODO ...  Under "Auto Scaling Group", enter "2" for "min" and click "Save"_
20. _... TODO ...  Click "Create environment"_

## ▶️ Domain Setup

_... TODO ..._

## 🎛️ Administration

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
