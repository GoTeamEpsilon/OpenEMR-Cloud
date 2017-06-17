_[next chapter >](02-Private-Cloud.md)_

# 🚴 Getting Started

### Start by getting a local copy of OpenEMR v5

1. Download the latest [tarball](http://sourceforge.net/projects/openemr/files/OpenEMR%20Current/5.0.0/openemr-5.0.0.tar.gz/download) to your computer.
2. Extract the contents with your favorite archive extractor.
3. Rename the downloaded "**openemr-5.0.0**" directory to "**openemr**".
4. Enter into the "**openemr**" directory.
5. Create an AWS specific directory called "**.ebextensions**".
6. Download all files in [this](https://github.com/GoTeamEpsilon/OpenEMR-AWS-Guide/tree/master/assets/eb) area to the newly created "**.ebextensions**" directory.

### Create an AWS Account

1. Navigate to [https://aws.amazon.com/](https://aws.amazon.com/), and then click **Create an AWS Account**.
2. Follow along with the signup wizard.

### Add yourself as an administrative user

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

### Restrict permissions to your Root account

_TODO: Revert the **AdministratorAccess** step from above once this is in place :)_

0. Explanation of why this is important since it sometimes confuses me
1. Steps Steps Steps XYZ XYZ XYZ (this includes setting up an individual account, right?)

### Generate an AWS SSH keypair

1. In the AWS Management Console, click **Services** and then click **EC2**.
2. In the lefthand pane, click **Keypairs**.
3. Click **Create Key Pair**.
4. When the **"Create Key Pair"** dialog appears, enter your username for the **Key pair name** field and click **Create**.
5. When the **Save As** dialog appears, save the key to a safe place.
