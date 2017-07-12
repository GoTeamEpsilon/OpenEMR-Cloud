_[< previous chapter](01-Getting-Started.md) | [next chapter >](03-Secure-Domain-Setup.md)_

# 🖥 Application Servers

### OpenEMR setup

TODO 1. (Explain how to get to the stack output)
2. Go through each step of the signup wizard using the MySQL credentials noted in previous steps. Make sure to enter a [strong password](https://www.random.org/passwords/?num=1&len=16&format=html&rnd=new) for the initial user and record it in a safe place. Note that the first step of the wizard will take a few minutes. Although the page will be white and not have any loading indicators, please do not attempt to refresh the page or resubmit the request.

### Post-install security update

TODO (this can't happen unless VPN is configured)

1. In the AWS Management Console, click **EC2** and then click **Instances** in the left hand pane.
2. Clickbox the running **your_practice** instance and note the **Private DNS (IPv4)** in the bottom pane.
3. Using this IP, SSH into the server. If you aren't sure, please review [How do I SSH into Instances](../chapters/09-Administration.md#how-do-i-ssh-into-instances) section.
4. Run `sudo /opt/elasticbeanstalk/hooks/appdeploy/post/09-post-install-setup-file-deletion.sh` to manually remove public setup files (will be ran automatically when subsequent instances are created by ElasticBeanstalk).
