_[< previous chapter](02-Private-Cloud.md) | [next chapter >](04-Database-System.md)_

# 📁 Network File System

### Provide a network file system to store patient documents and site configuration across systems

1. In the AWS Management Console, click **Services** and then click **EFS**.
2. Click **Create file system**.
3. Under **VPC**, select **"openemr-vpc"**.
4. Under **Create mount targets**, checkbox all items.
5. Click **Next Step**.
6. Under **Choose performance mode**, select your preferred performance setting. If you aren't sure, select "**General Purpose**".
7. Click **Next Step**.
8. Click **Create File System**.
9. Wait a few moments.
10. Note the **File System ID** in a safe place.

### Configure OpenEMR servers to mount the shared drive on bootup

1. Open "**openemr/.ebextensions/00-options.config**" and replace "**<<enter EFS file system ID here>>**" with your noted **File System ID** from before.
