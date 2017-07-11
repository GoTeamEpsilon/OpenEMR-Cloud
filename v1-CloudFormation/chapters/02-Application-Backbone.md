_[< previous chapter](01-Geting-Started.md) | [next chapter >](03-Application-Servers.md)_

# 📝 Application Backbone

_CloudFormation is used for setting up OpenEMR._

### Set up CloudFormation

1. Download the **OpenEMR.json** file [here](https://github.com/GoTeamEpsilon/OpenEMR-Cloud/tree/master/v1-Beta-AWS-Guide/assets/cf) in your local **openemr** folder. Be careful to save the file as `.json` and not `.json.txt`.
2. In the AWS Management Console, click **Services** and then click **CloudFormation**.
3. Click **Create Stack**.
4. In the **Choose a template** section, click the **upload file** button and select the **OpenEMR.json** file downloaded in step 1.
5. Click **Next**.
6. Define the parameters of the application stack here.
..* For Stack name, answer "OpenEMR".
..* For EC2KeyPair, select the EC2 key you created in chapter 1 from the dropdown.
..* For Time Zone, set your [PHP timezone](http://php.net/manual/en/timezones.php).
..* For RDSPassword, this is the administrator's password to the MySQL database we'll create for OpenEMR. Pick a secure password and store it in a safe place.
9. Click **Next**.
10. Click **Next** again.
11. Click **Create** and wait for the stack to finish creating.

### Examine audit logs

1. Once the stack has a status of **CREATE_COMPLETE**, click on **Services** and then click **S3**.
2. Find the new bucket that CloudFormation created. The bucket will have a name with this format: **openemr-<hexadecimal uuid>**.
3. Click into the bucket, then **AWSLogs**, then **\<_your account ID_\>**, then **CloudTrail**.
4. Here, CloudTrail will store your AWS activity with a hierarchy of **region/year/month/day**. The data saved in these logs will be useful to administrators and auditors. Note this location in a safe place.
