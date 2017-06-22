_[< previous chapter](01-Getting-Started.md) | [next chapter >](03-Network-File-System.md)_

# ☁ Private Cloud

### Lock down your system components with a private virtual network

1. In the AWS Management Console, click **Services** and then click **Start VPC Wizard**.
2. Click **VPC with a Single Public Subnet** and click **Select**.
3. In **VPC Name**, enter "**openemr-vpc**".
4. In **Availability Zone**, select your preferred zone. If you aren't sure, select the first entry (selecting an entry at the bottom of the list may not be supported in ElasticBeanstalk, such as with us-east-1e).
5. Click **Create VPC**.
6. In the lefthand pane, click **Security Groups**.
7. Note the Group ID for the recently created **"default"** VPC.
