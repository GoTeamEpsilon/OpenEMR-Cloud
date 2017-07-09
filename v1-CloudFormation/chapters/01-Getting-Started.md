_[next chapter >](02-Application-Backbone.md)_

# 🚴 Getting Started

### Start by getting a local copy of OpenEMR v5

1. Download the latest [tarball](http://sourceforge.net/projects/openemr/files/OpenEMR%20Current/5.0.0/openemr-5.0.0.tar.gz/download) to your computer.
2. Extract the contents with your favorite archive extractor. Note that a `tar` file will need to be extracted after the initial extraction if you are using Windows.
3. Rename the downloaded "**openemr-5.0.0**" directory to "**openemr**".
4. Enter into the "**openemr**" directory.
5. Create an AWS-specific directory called "**.ebextensions**".
6. Download [this](https://github.com/GoTeamEpsilon/OpenEMR-Cloud/raw/master/v1-Beta-AWS-Guide/assets/eb/eb.zip) zip file to the newly created "**.ebextensions**" directory. Extract the contents with your favorite archive extractor (make sure files are extracted to "**.ebextensions/**" and not "**.ebextensions/eb/**").

### Create an AWS Account

1. Navigate to [https://aws.amazon.com/](https://aws.amazon.com/), and then click **Create an AWS Account**.
2. Follow along with the signup wizard.

### Add yourself as an administrative user

1. Now that you are logged into the AWS Management Console, click **Services** and then click **IAM**.
2. In the left pane, click **Dashboard**, and copy down the IAM user sign-in link.
3. In the left pane, click **Users**.
4. Click **Add user**.
5. Under **Set user details**, enter your username in the **User name** field.
6. Under **Select AWS access type**, select only **AWS Management Console access** in the **Access type** area.
7. Click **Next: Permissions**.
8. Under **Set permissions for ...**, click the **Attach existing policies directly**  box.
9. With the table at the bottom of the page in view, select **AdministratorAccess** (will be the first row).
10. Click **Next: Review**.
11. Under **Review**, ensure all information reflects the above steps.
12. Click **Next: Create user**.
13. Log out of the AWS console, go to the sign-in link you copied down in step 2, and log in with your new credentials.
14. (_Optional but highly recommended step_): Enable two-factor authentication via the **Security credentials** tab of your user profile in IAM. Click the pencil beside **Assigned MFA Device** to start this process.

### Select an AWS Region

This guide uses services that are _only_ available in certain AWS regions. As of this writing, you will need to make sure you're in one the of five Amazon regions described below.

1. In the AWS Management Console, click **Services**, and then click **EC2**.
2. In the region dropdown in the top right corner, select either "**Ohio**", "**N. Virginia**", "**Oregon**", "**Ireland**", or "**Sydney**". Be sure to remain in this region for the remainder of this guide.

### Generate an AWS SSH keypair

1. In the AWS Management Console, click **Services** and then click **EC2**.
2. In the left hand pane, under **Network & Security**, click **Key Pairs**.
3. Click **Create Key Pair**.
4. When the **"Create Key Pair"** dialog appears, enter your username for the **Key pair name** field and click **Create**.
5. When the **Save As** dialog appears, save the .pem keyfile to a safe place.
