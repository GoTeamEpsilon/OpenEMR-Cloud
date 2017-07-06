_[< previous chapter](01-Getting-Started.md) | [next chapter >](03-Network-File-System.md)_

# ☁ Private Cloud

### Lock down your system components with a private virtual network

1. In the AWS Management Console, click **Services** and then click **Start VPC Wizard**.
2. Click **VPC with a Single Public Subnet** and click **Select**.
3. In **VPC Name**, enter "**openemr-vpc**".
4. In **Availability Zone**, select your preferred zone. If you aren't sure, select the first entry. In fact, this is strongly encouraged due to issues with selecting entries at the bottom of the list which may not be supported in ElasticBeanstalk.
5. Name the subnet "Public".
6. Click **Create VPC**.
7. In the left pane, click *Subnets*, **Create Subnet**. Select your VPC, supply a name (**Private**) and a CIDR address block (**10.0.1.0/24** should work fine).
8. Supply the Availability Zone you used for the first subnet of the VPC, above.
9. Click **Yes, Create**.
10. Click **Create Subnet**. Select your VPC, supply a new name (**Other Public**) and a CIDR address block (**10.0.2.0/24** should work fine).
11. Supply an Availability Zone *other than* the availability zone you previously noted. Any other AZ will do.
12. Click **Yes, Create**.
13. Click **Create Subnet**. Select your VPC, supply a new name (**Other Private**) and a CIDR address block (**10.0.3.0/24** should work fine).
14. Supply the same Availability Zone you used for "Other Public".
15. Click **Yes, Create**.
16. In the left pane, click **Route Tables** and select the route for your VPC that is not the 'Main' route.
17. Click the **Subnet Associations** tab and observe that the "Public" subnet is already assigned to it.
18. **Edit** the subnet and add the "Other Public", then **Save**.
16. In the left pane, click **NAT Gateways** and click **Create a NAT Gateway**.
17. For the subnet, select the "Public" subnet.
18. Click **Create New EIP**, then note the IP created. This is the IP from which traffic from your private instances will appear from.
19. Click **Create a NAT Gateway**, copy the route target (that starts with "nat-"), and select **Edit Route Tables**.
20. Click the "Main" route table for your VPC, then click the **Routes** tab, then **Edit**.
21. **Add another route** sending destination traffic of 0.0.0.0/0 to target your new NAT gateway, which will appear in the box when it gets focus. **Save**.

### Establish VPN server for network

1. Click **Services**, **EC2**, **Instance**, **Launch Instance**.
2. Click **AWS Marketplace**, search **OpenVPN**, select **OpenVPN Access Server**, specifically the "Bring Your Own License" entry from list.
3. Select **t2.small**, **Next**.
4. Confirm it's launching into "openemr-vpc" VPC, and select the "Public" subnet.
5. Do **Protect against accidental termination**.
6. Click **Next: Add Storage**
7. Click **Next: Add Tags**
8. **Click to add a Name tag** and call it **OpenEMR VPN**.
9. Click **Next: Configure Security Group**
10. Rename the generated security group name to just "**VPN Server**".
11. Click **Review and Launch**.
12. (Is it talking about SSD drives? Go ahead and stick with **Magnetic** for now.)
13. **Launch**, and pick your keyfile from the previous chapter from the list.
14. Wait for the launch to complete, then click **View Your Instances**.
15. On the left pane, under **Network & Security**, click **Elastic IPs**.
16. Click **Allocate new address**, then **VPC**, then **Allocate**.
17. **Close**, check the new address, click **Actions**, **Associate address**.
18. Select the VPN instance from the **Instance** dropdown, and **Associate**. **Close**.

### Configure VPN server for use

1. Click **View Your Instances** and wait for the new instance to finish booting -- the **Status Checks** should read 2/2.
2. Check the instance, and look at the **IPv4 Public IP**. Note this down for later.
3. With the instance selected, click **Actions**, **Networking**, **Change Security Groups**.
4. Add the instance to the **default** security group.
5. With your SSH client, connect to the instance IP we just noted, using the keyfile from the previous steps.
6. Log in as user **openvpnas**.
7. Agree with the license, leave all other answers default.
8. At the shell, run **sudo passwd openvpn**, set an administrative password, and disconnect.
9. Browse **https://&lt;&lt;recently noted server ip&gt;&gt;:943/admin**, user openvpn, password as set, **Agree**, **Logout**. Note that you'll see a warning about an unsafe connection, click, you can proceed despite of this.
10. Browse **https://&lt;&lt;recently noted server ip&gt;&gt;:943/?src=connect**, and follow along with the wizard to download and connect to your VPN.
