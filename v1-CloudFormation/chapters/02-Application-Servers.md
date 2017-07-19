_[< previous chapter](01-Getting-Started.md) | [next chapter >](03-Secure-Domain-Setup.md)_

# 🖥 Application Servers

### OpenEMR setup

1. In the AWS Management Console, click **CloudFormation** and review the list of stacks. One will have the name you assigned &mdash; click that stack, and the content in the tabs on the bottom half of the screen will populate. Once the status of your stack is a green **CREATE_COMPLETE**, the stack is built and you are ready to proceed.
2. Click the **Outputs** now, and click the link labeled **OpenEMR Setup**.
3. Go through each step of the signup wizard using the MySQL credentials noted in previous steps.
 * The MySQL host will be "mysql.oemr.local".
 * The database password will be what you originally gave the stack in the last chapter.
 * Make sure to enter a [strong password](https://www.random.org/passwords/?num=1&len=16&format=html&rnd=new) for the initial user and record it in a safe place. Note that the first step of the wizard will take a few minutes. Although the page will be white and not have any loading indicators, please do not attempt to refresh the page or resubmit the request.
4. Once the setup process completes, log in to OpenEMR with your administrative credentials.
5. Select **Administration**, then **Globals**, then **Documents**. From the dropdown, select **CouchDB**, then make the following changes:
 * For **CouchDB HostName**, enter "couchdb.oemr.local".
 * For **CouchDB Database**, enter "couchdb".
 * Check the box marked **CouchDB Log Enable**.
6. Save.
