_[< previous chapter](01-Getting-Started.md) | [next chapter >](03-Secure-Domain-Setup.md)_

# 🖥 Application Servers

### OpenEMR Setup

1. In the AWS Management Console, click **Services**, and then click **CloudFormation**.
2. Review the table and checkbox the row with **Stack Name** of **OpenEMR**.
3. With the bottom pane present and the **Overview** tab in focus, observe the **Status** value. Once the value is **CREATE_COMPLETE**, you may proceed.
4. Click the **Outputs** tab and click the link in the **URL** row.
5. Go through each step of the signup wizard.
   * The database password will be what you noted in the last chapter.
   * The MySQL host will be **mysql.openemr.local**.
   * Make sure to enter a [strong password](https://www.random.org/passwords/?num=1&len=16&format=html&rnd=new) for the initial user and record it in a safe place.
   * The first step of the wizard will take about 5 minutes. Although the page will be white and not have any loading indicators, please do not attempt to refresh the page or resubmit the request.

### Connect the Patient Documents Database

1. Login into OpenEMR using your new administrative credentials.
2. At the top, hover over **Administration** and then click **Globals**.
3. Now with the settings area in view, click the **Documents** tab.
4. For the **Document Storage Method** field, select **CouchDB**.
5. For the **CouchDB HostName** field, enter **couchdb.openemr.local**.
6. For the **CouchDB Database** field, enter **couchdb**.
7. For the **CouchDB Log Enable** field, checkbox the input.
8. Click **Save** near the bottom left.
