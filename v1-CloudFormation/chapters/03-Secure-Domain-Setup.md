_[< previous chapter](02-Application-Servers.md) | [next chapter >](04-VPN-Access.md)_

# ▶ Secure Domain Setup

### Purchase Custom Domain

1. In the AWS Management Console, click **Services** and then **Route 53**.
2. Under **Register domain**, enter your desired domain name and then click **Check**.
3. Assuming the domain is available, click **Add to cart** next to your desired domain name. Note the domain name in a safe place.
4. Scroll down to the bottom of the page and click **Continue**.
5. Enter your **Registrant**, **Administrative**, and **Technical** contact information and then click **Continue** at the bottom of the page.
6. Under **Terms and Conditions**, checkbox the agreement then click **Complete Purchase**.
7. Wait around 10 minutes for an AWS email to be sent to you entited **Verification of your contact data**. Click the confirmation link in the message body.

### Create Hosted Zone

1. In the AWS Management Console, click **Services** and then **Route 53**.
2. Click **Go To Domains** in the center of the screen.
3. In the left hand pane, click **Hosted zones**.
4. Click **Create Hosted Zone** to the top left.
5. Checkbox your recently created domain name and then click **Create Hosted Zone** to the top left.
6. In the new **Create Hosted Zone** right hand pane, enter your noted domain name in for **Domain Name** and then click **Create**.

_If your domain isn't registered through Amazon, you can still host it with Route 53 by changing your domain's "NS" entries at your registrar to the NS records showing on your domain here at Amazon. That will tell the world that Amazon is the one responsible for the content of the zone file, and will let the changes you're about to make be publically visible. Alternately, you can leave your domain hosted off-Amazon entirely, but the automated SES-to-Route-53 setup in a few sections won't be available, and you'll have to modify records manually._

### Configure public access to OpenEMR

1. In the AWS Management Console, click **Services** and then **Route 53**.
2. In the left hand pane, click **Hosted zones**, then select your domain.
3. Click **Create Record Set** to the top.
4. In the new **Create Record Set** right hand pane, enter "**www**" for **Name** and "**A - IPv4 address**" for **Type**.
5. Checkbox **"Yes"** for **Alias**.
6. Under **Alias Target**, select the only entry under **Elastic Beanstalk Environments**.
7. Click **Create**.

### Associate Domain with a SSL Certificate

1. In the AWS Management Console, click **Services** and then **Certificate Manager**.
2. Click **Request a certificate** to the top left.
3. Under **Domain name**, enter your domain without a "**www.**" prefix.
4. Click **Add another name to this certificate**.
5. Enter another domain entry with a **"*."** prefix.
6. Click **Review and request**.
7. Click **Confirm and request**.
8. Wait around 10 minutes for multiple AWS emails to be sent to you. Click the confirmation link in each message body.
9. Navigate to "**https://www.your_practice_domain.ext/openemr**" and inform your user base of the link.

### Configure Amazon Simple Email Service

1. In the AWS Management Console, click **Services** and then **SES**.
2. Click **Domains**, then **Verify a New Domain**.
3. Enter the domain (without any 'www' but with the '.com' or similar extension), click the **DKIM** box, and click **Verify This Domain**.
4. Click **Route 53**.
5. Click **Create Record Sets**. As soon as Amazon sees the records on your domain, the SES verification process will complete.
6. In the sidebar, click **SMTP Settings**. Copy down the **Server Name**, which is probably "email-smtp.&lt;region&gt;.amazonaws.com".
7. Click **Create My SMTP Credentials**, then **Create**, then **Show User SMTP Security Credentials**.
8. Copy down your SMTP username and password now. Store them in a safe place &mdash; there will never be another chance to see them.
9. Log in to OpenEMR via the URL you used in chapter 2.
10. Go to **Administration**, **Globals**, **Notifications**, and configure the mail server:
 * Email Transport Method: **SMTP**
 * SMTP Server Hostname: &lt;the server from step 6&gt;
 * SMTP Server Port Number: 587
 * SMTP User for Authentication, SMTP Password for Authentication: &lt;the credentials from step 8&gt;
 * SMTP Security Protocol: **TLS**
11. Click **Save**.
