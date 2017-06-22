_[< previous chapter](03-Network-File-System.md) | [next chapter >](05-Session-Management.md)_

# 💽 Database System

### Create a fully managed MySQL database

1. In the AWS Management Console, click **Services** and then click **RDS**.
2. Under **Create Instance**, click **Launch a DB Instance**. If you are using a brand new account, you'll have to click **Instances** in the left-hand pane to get around the marketing screen.
3. Click **MySQL**.
4. Click **Select**.
5. Under **Production**, click **MySQL**.
6. Click **Next Step**.
7. Apply the following under **Instance Specifications**:
    1. In **DB Engine Version**, select "**MySQL 5.6.27**".
    2. In **DB Instance Class**, select your preferred instance size. If you aren't sure, select "**db.t2.large**".
    3. In **Select Multi-AZ Deployment**, select your preferred AZ configuration. If you aren't sure, select "**No**".
    4. In **Storage Type**, select "**General Purpose (SSD)**".
    5. In **Allocated Storage**, select your preferred size. If you aren't sure, enter "**500GB**".
8. Apply the following under **Settings**:
    1. In **DB Instance Identifier**, enter "**openemr-db**".
    2. In **Master User**, enter "**openemr_db_user**".
    3. In **Master Password**, enter a [strong password](https://www.random.org/passwords/?num=1&len=16&format=html&rnd=new). Make sure this is recorded in a safe place.
9. Click **Next Step**.

### Restrict database access to its own private network

1. Apply the following under **Network & Security**
    1. In **VPC**, select "**Create new VPC**".
    2. In **Subnet Group**, select "**Create new DB Subnet Group**".
    3. In **Publicly Accessible**, select "**No**".
    4. In **Availability Zone**, select your preferred zone. If you aren't sure, select "**No Preference**".
    5. In **VPC Security Group(s)**, select "**Create new Security Group**".
2. Apply the following under **Database Options**:
    1. In **Database Name**, enter "**openemr**".
    2. In **Database Port**, enter "**3306**".
    3. In **DB Parameter Group**, select "**default.mysql5.6**".
    4. In **Option Group**, select "**default:mysql-5-6**".
    5. In **Copy Tags To Snapshots**, uncheck box.

### Setup a data backup strategy

1. Apply the following under **Backup**:
    1. In **Backup Retention Period**, select your preferred days. If you aren't sure, select "**7**".
    2. In **Backup Window**, select "**Select Window**" and choose your preferred window. If you aren't sure, select "**00:00**".

### Allow for system health checks

1. Apply the following under **Monitoring**:
    1. In **Enable Enhanced Monitoring**, select "**Yes**".
    2. In **Monitoring Role**, select "**Default**".
    3. In **Granularity**, select your preferred second(s). If you aren't sure, select "**60**".

### Permit minor safety updates to your database engine

1. Apply the following under **Maintenance**:
    1. In **Auto Minor Version Upgrade**, select your preferred strategy. If you aren't sure, select "**Yes**".
    2. In **Maintenance Window**, and choose your preferred window. If you aren't sure, select "**00:00**".

### Launch your fully configured database

1. Click **Launch Instance**.
2. Click **View your db instances**.
3. Wait many moments for the database to be created.
4. Click on the first row of the **Instances** table.
5. Record the **Endpoint** in a safe place.

### Permit access to other instances

__TODO: This should be limited to only the other VPC__

1. Click the tab handle with the magnifying glass icon.
2. Under **Security Groups**, click the first link.
3. Click the **Actions** dropdown.
4. Click **Edit inbound rules**.
5. Under the entry, select **"Anywhere"** for **Source** and click **Save**.
