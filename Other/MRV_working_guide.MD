# Matthew's working area

## Content Scope
- Steps on how to provision OpenEMR in AWS
- Links to articles and documentation that helped me proof out an AWS devops concept

## Redis Sessions

(Memcached in Elasticache has failed me: http://stackoverflow.com/questions/43825089/elasticache-session-start-failed-to-create-session-id (sadface.jpg). Therefore, I'm going to take a different approach entirely...)

The default `$_SESSION['...']` data storage mechanism in PHP is the disk of the web server. This is an acceptable solution for OpenEMR until many users and patients are in the system and scaling is needed. For example, load balancing between 4 servers, all with their own `$_SESSION['...']` data, instead of a central cluster will result in errorneous state in the application. AWS Elasticache solves this by providing a Memcached or Redis cache store that can be used by an application to store ephemeral session state such as this.

0) Steps to create a VPC, redis security group, keypair, ssh, etc go here!
1) In the AWS console, navigate to Services > EC2 and click "Launch Instance"
2) Under "Quick Start", select "Ubuntu Server 16.04 LTS (HVM), SSD Volume Type" (ami-80861296)
3) Under "Choose an Instance Type", select your instance size (the bigger the better because this cache is scaled vertically), then click "Next: Configure Instance Details"
4) Under "Network", select VPC from step 0 then click "Next: Add Storage"
5) Under "Size", select the disk GBs (Redis saves data to disk from time to time, so consider your scale and select the size accordingly) then click "Review and Launch"
6) When "Select an existing key pair or create a new key pair" dialog shows up, select your key pair and click "Launch Instances"
7) Navigate to Services > EC2 > Running Instances and identify the new instance being initialized.
8) Click the edit icon in the "Name" column and call the instance "Redis"
9) Wait for the instance to be fully running
10) Navigate to Services > VPC and click "Elastic IPs"
11) Click "Allocate new address" and then "Allocate"
12) After a moment a green "New address request succeeded" message will appear. Note the IP and click "Close".
13) Check the recent created IP, click the "Actions" dropdown, and click "Associate address"
14) Under "Instance" select the "Redis" instance
15) Under "Private IP" select the first dropdown value and note this address
16) Click "Associate" and then "Close"
17) Using the Public DNS at the bottom right, ssh into the instance with the `ubuntu` user
18) Run `sudo apt-get install -y docker.io && sudo usermod -aG docker ubuntu && sudo gpasswd -a $USER docker && sudo service docker restart && newgrp docker` to install Docker and associate it with the system user
19) Run `docker pull docker.io/redis && docker run -d --name redis_server -p 6379:6379 redis` to spin up a redis image
20) Run `sudo vi /etc/systemd/system/redis-container.service` and then enter the following content

```
[Unit]
Description=Redis container
After=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker start -a redis_server
ExecStop=/usr/bin/docker stop -t 2 redis_server

[Install]
WantedBy=local.target
```

21) Once complete run `sudo systemctl enable redis-container.service && sudo systemctl start redis-container.service` and wait a moment
22) Run `sudo lsof -i :6379` and check for and make sure `docker-pr` is shown under the `COMMAND` column
21) Navigate to Services > EC2 > Running Instances and select the Redis instance
22) Under "Security groups" in the bottom pane (note: this step is not referring to the "Security Groups" link in the left pane), click the security group starting with "launch-wizard-"
23) Note the "Group ID"
24) Click the "Actions" dropdown and click "Edit inbound rules"
25) Under Type, select "Custom TCP Port" (will originally be "SSH")
26) Under Port Range, enter 6379 and click "Save"
27) Click the "Security Groups" link in the left pane and locate the row with the Group ID noted in step 23
28) Click the "Actions" dropdown and click "Copy to new"
29) Under "Security group name", enter "redis-security-group"
30) Under "Description", enter "Restricted Redis security group", click "Create", and note the Group ID
31) Navigate to Services > EC2 > Running Instances and select the Redis instance
32) Click the "Actions" dropdown and click "Networking" > "Change Security Groups"
33) Uncheck the Security Group noted in step 23
34) Check the Security Group noted in step 29
35) Click "Assign Security Group"
36) Open your local OpenEMR project and add `redis-sessions.config` to the `.ebextensions` directory (replace `{{REDIS_IP}}` with the address noted in step 15)

```
files:
  "/etc/php.d/project.ini" :
    mode: "000644"
    owner: root
    group: root
    content: |
      [Session]
      session.save_handler = redis
      session.save_path = "tcp://{{REDIS_IP}}:6379"
container_commands:
  01_install_redis_php_extension:
    command: "wget http://rpms.famillecollet.com/enterprise/remi-release-6.rpm && rpm -Uvh remi-release-6.rpm && sudo yum -y --enablerepo=remi,remi-test install php70-pecl-redis"
```

37) Deploy the application

TODO:
- When rebooting the Redis instance, Dockerized Redis Systemd does NOT start
- Need to lock down the redis security group source (current it's 0.0.0.0/0)

NOTES:
This is the test program I am using to test this (make sure you have the .ebextensions folder in place):

```
<?php
    header('Content-Type: text/plain');
    session_start();
    if(!isset($_SESSION['visit']))
    {
        echo "This is the first time you're visiting this server\n";
        $_SESSION['visit'] = 0;
    }
    else
            echo "Your number of visits: ".$_SESSION['visit'] . "\n";

    $_SESSION['visit']++;

    echo "Server IP: ".$_SERVER['SERVER_ADDR'] . "\n";
    echo "Client IP: ".$_SERVER['REMOTE_ADDR'] . "\n";
    print_r($_COOKIE);
	
	session_write_close();
```

## Elastic File System

In OpenEMR, an administrator can add a site to achieve a multi-tenant EMR solution (note that this is _not_ the same as having multiple facilities). By default, OpenEMR ships with the `default` site found in `openemr/sites/default/`. This folder contains uploaded documents, templates, and admin templates.

Our AWS solution calls for a load balanced environment, therefore, this default folder must be shared across instances. This can be achieved with the AWS Elastic File System service. Here is a demonstration of how to set up a simple PHP/Apache application that shares a common file system:

1) In the AWS console, navigate to Services > VPC and click "Start VPC Wizard"
2) Select "VPC with a Single Public Subnet" and click "Select"
3) Enter "openemr-vpc" for the VPC name, select your preferred Availability Zone, and click "Create VPC"
4) Navigate to Services > Elastic Beanstalk and click "Create New Application"
5) Enter "openemr" for the Application Name and click "Create"
6) Under "Environments", click "Create one now"
7) Select "Web server environment" and click "Select"
8) Under "Preconfigured platform", select "PHP"
9) At the button of the page, click "Configure more options"
10) Under "Configuration presets", select "Custom configuration"
11) Under "Network", click "Modify"
12) Under "Virtual private cloud (VPC)", select "OpenEMR VPC", check all items in "Load balancer subnets", "Instance subnets", and "Instance security groups", and click "Save"
13) Under "Environment settings", click "Modify"
14) Under "Name", enter "OpenEMR" and click "Save"
15) Under "Capacity", click "Modify"
16) Under "Auto Scaling Group", enter "2" for "min" and click "Save"
17) Click "Create environment"
18) Navigate to "Services" > "EFS" and click "Create file system"
19) Under "VPC", select the "OpenEMR" VPC, check all items in "Create mount targets", and click "Next Step"
20) Under "Add tags", enter "OpenEMR-EFS" for the "Key" and "Documents" for the "Value"
21) Select the right performance mode for your use case "Choose performance mode" and click "Next Step" and then "Create File System"
22) Take note of the "File system ID"
23) On your local computer, create a directory named `sample` with an `index.php` file with the following contents:
```
<?php
echo "OK";
```

24) Create `.ebextensions` and `documents` directories in the `sample` directory
25) Save https://upload.wikimedia.org/wikipedia/commons/d/d9/Test.png to the `documents` directory
26) Create file `storage-efs-mountfilesystem.config` in the `.ebextensions` directory with the following contents (replace `{{FS_ID_HERE}}` with your noted file system id): 

```
option_settings:
  aws:elasticbeanstalk:application:environment:
    FILE_SYSTEM_ID: '{{FS_ID_HERE}}'
    MOUNT_DIRECTORY: '/var/app/current/sample/shared'

    REGION: '`{"Ref": "AWS::Region"}`'

packages:
  yum:
    nfs-utils: []
    jq: []

commands:
  create_post_dir:
    command: "mkdir /opt/elasticbeanstalk/hooks/appdeploy/post"
    ignoreErrors: true

files:
  "/opt/elasticbeanstalk/hooks/appdeploy/post/mount-efs.sh":
      mode: "000755"
      content : |
        #!/bin/bash

        EFS_REGION=$(/opt/elasticbeanstalk/bin/get-config environment | jq -r '.REGION')
        EFS_MOUNT_DIR=$(/opt/elasticbeanstalk/bin/get-config environment | jq -r '.MOUNT_DIRECTORY')
        EFS_FILE_SYSTEM_ID=$(/opt/elasticbeanstalk/bin/get-config environment | jq -r '.FILE_SYSTEM_ID')

        echo "Mounting EFS filesystem ${EFS_DNS_NAME} to directory ${EFS_MOUNT_DIR} ..."

        echo 'Stopping NFS ID Mapper...'
        service rpcidmapd status &> /dev/null
        if [ $? -ne 0 ] ; then
            echo 'rpc.idmapd is already stopped!'
        else
            service rpcidmapd stop
            if [ $? -ne 0 ] ; then
                echo 'ERROR: Failed to stop NFS ID Mapper!'
                exit 1
            fi
        fi

        echo 'Checking if EFS mount directory exists...'
        if [ ! -d ${EFS_MOUNT_DIR} ]; then
            echo "Creating directory ${EFS_MOUNT_DIR} ..."
            mkdir -p ${EFS_MOUNT_DIR}
            if [ $? -ne 0 ]; then
                echo 'ERROR: Directory creation failed!'
                exit 1
            fi
            chmod 777 ${EFS_MOUNT_DIR}
            if [ $? -ne 0 ]; then
                echo 'ERROR: Permission update failed!'
                exit 1
            fi
        else
            echo "Directory ${EFS_MOUNT_DIR} already exists!"
        fi

        mountpoint -q ${EFS_MOUNT_DIR}
        if [ $? -ne 0 ]; then
            echo "mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 ${EFS_FILE_SYSTEM_ID}.efs.${EFS_REGION}.amazonaws.com:/ ${EFS_MOUNT_DIR}"
            mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 ${EFS_FILE_SYSTEM_ID}.efs.${EFS_REGION}.amazonaws.com:/ ${EFS_MOUNT_DIR}
            if [ $? -ne 0 ] ; then
                echo 'ERROR: Mount command failed!'
                exit 1
            fi
        else
            echo "Directory ${EFS_MOUNT_DIR} is already a valid mountpoint!"
        fi

        echo 'EFS mount complete.'
```

27) Zip up `sample` folder as `sample.zip`
28) Navigate to Services > Elastic Beanstalk > OpenEMR > openemr > Application versions
29) Click "Upload", enter "OpenEMR" for "Version label", upload the sample.zip file, and click "Upload"
30) Check the newly uploaded "OpenEMR" entry and click "Deploy" and "Deploy" once more
31) Navigate to Services > EC2 and choose an "OpenEMR" instance to connect to
32) `cd` into `/var/app/current/sample/shared` and run `sudo touch foobar.txt`
33) Navigate to Services > Elastic Beanstalk > OpenEMR and click on the URL
34) Navigate to {{URL}}/sample/documents/Test.png to see the initial document on the EFS
35) Navigate to {{URL}}/sample/documents/foobar.txt to see the recently added document on the EFS
36) Refresh the page a number of times to ensure that a 404 isn't thrown (this proves that the load balancer is switching between each instance for each request and the central EFS documents are being served up)

## Resources That Helped Me
  - [Elastic Beanstalk & Elastic File System: So Happy Together](https://medium.com/cohealo-engineering/elastic-beanstalk-elastic-file-system-8be6883bdc7a)
  - [Elastic Beanstalk Post-deployment Scripts](http://junkheap.net/blog/2013/05/20/elastic-beanstalk-post-deployment-scripts/)
