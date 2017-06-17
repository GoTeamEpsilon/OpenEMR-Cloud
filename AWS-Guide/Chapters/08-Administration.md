_[< previous chapter](07-Secure-Domain-Setup.md)_

# 🎛 Administration

### How do I deploy custom changes to my cloud?

The most robust and maintainable approach for deployments is to keep an internal changelog of your changes along with associated [version control tags](https://git-scm.com/book/en/v2/Git-Basics-Tagging). Not only will this help you stay organized, but you can also reference it in the case you wish to rollback to a previous deployment and aid in reapplying your custom changes when a newer version of OpenEMR is available.

1. In the AWS Management Console, click **Services**, **Elastic Beanstalk**, and then choose **openemr/your_practice**.
2. Click the **Upload and Deploy** button in the center of the screen.
3. Click **Choose File** and select "**openemr.zip**". Note that the name of this file must be exact.
4. Under **Label**, enter in **"openemr-deployment-N"** where **N** is most recent version of your deployment.
5. Click **Deploy**.

### How do I access system logs?

1. In the AWS Management Console, click **Services**, **Elastic Beanstalk**, and then choose **openemr/your_practice**.
2. In the lefthand pane, click **Logs**.
3. Click the **Request Logs** button to the to pright of the screen.
4. Click **Full Logs** and wait a moment for the logs to download.
5. Extract the contents with your favorite archive extractor to view each instance's Apache logs in **logs_directory/var/log/httpd**.

### How do I restore a database backup?

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

### How do I Access the Database?

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

### How do I SSH Into Instances?

Accessing your instances with SSH is one of the more challenging tasks in this guide. As such, be sure to treat this as a learning opportunity and pay close attention to the instructions to ensure the most seamless experience.

#### Prerequisites

1. Download and install the latest [PuTTY MSI](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) software suite. If you aren't sure, click [here](https://the.earth.li/~sgtatham/putty/latest/w64/putty-64bit-0.69-installer.msi).
2. Using your AWS SSH keypair that is saved as **"your-username.pem"**, convert it to a **ppk** file by following [these instructions](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html#putty-private-key).

#### Redis Access

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

#### Elastic Beanstalk Instance Access

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
