_[next chapter >](02-Application-Servers.md)_

# 🚴 Getting Started

### Create an AWS Account

1. Navigate to [https://aws.amazon.com/](https://aws.amazon.com/), and then click **Create an AWS Account**.
2. Follow along with the signup wizard.

### Select an AWS Region

This guide uses services that are _only_ available in certain AWS regions. As of this writing, you will need to make sure you're in one the of four Amazon regions described below.

1. In the AWS Management Console, click **Services**, and then click **EC2**.
2. In the region dropdown in the top right corner, select either "**N. Virginia**" (least expensive), "**Oregon**", "**Ireland**", or "**Sydney**". Be sure to remain in this region for the remainder of this guide.

### Generate an AWS SSH keypair

1. In the AWS Management Console, click **Services** and then click **EC2**.
2. In the left hand pane, under **Network & Security**, click **Key Pairs**.
3. Click **Create Key Pair**.
4. When the **"Create Key Pair"** dialog appears, enter your username for the **Key pair name** field and click **Create**.
5. When the **Save As** dialog appears, save the .pem keyfile to a safe place. We'll talk more about it in later chapters.

### Begin your installation

_Advanced users: If you're running under an existing AWS account with preconfigured IAM, CloudFormation will require a role with unfettered AdministratorAccess._

1. Pick the region you created your keypair in.
   * [North Virginia, USA](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=OpenEMR&templateURL=https://s3.amazonaws.com/openemr-useast1/OpenEMR.008.json)
   * [Oregon, USA](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=OpenEMR&templateURL=https://s3.amazonaws.com/openemr-uswest2/OpenEMR.008.json)
   * [Dublin, Ireland](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=OpenEMR&templateURL=https://s3.amazonaws.com/openemr-euwest1/OpenEMR.008.json)   
   * [Sydney, Australia](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=OpenEMR&templateURL=https://s3.amazonaws.com/openemr-apsoutheast2/OpenEMR.008.json)  
2. Click **Next**.
3. Define the parameters of the application stack here.
   * For **Stack name**, leave it as **OpenEMR** or change it if you'd like.
   * For **EC2KeyPair**, select the EC2 key you created in chapter 1 from the dropdown.
   * For **TimeZone**, set your [PHP timezone](http://php.net/manual/en/timezones.php).
   * For **RDSPassword**, this is the administrator's password to the MySQL database we'll create for OpenEMR. Pick a secure password and store it in a safe place.
4. Click **Next**.
5. Click **Next** again.
6. Click the acknowledgement near the bottom of the page, under the warning about AWS::IAM::Role.
7. Click **Create** and wait ten to fifteen minutes for OpenEMR to fully install to your account.

### While you're waiting: Secure the account with Identity and Access Management

1. In the AWS Management Console, click **Services** and then click **IAM**.
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
