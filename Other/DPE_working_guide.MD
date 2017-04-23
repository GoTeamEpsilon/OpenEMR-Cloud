# This will be Daniel Ehrlich's current contribution area for this repo.

## Resources below will:
- be random but properly formatted into many different groups
- include helpful links about HIPAA daniel provides
- include helpful links about HIPAA in AWS and HIPAA in the cloud in general
- include help security links and Linux-hardening guidelines
- start providing AWS-specific directions on setting up OpenEMR


## Prenotes:
- For your Elastic Beanstalk app, you will use the Amazon Linux AMI. This Linux AMI auto-updates, so a lot of security patching is taken care of for you. There will still need to be things you should do to "harden" the instance and this will be covered in this guide. Some examples will be optional.

## Proto-Guide:
0. Set up users???
1. Upload Code.
2. Set up networks and the necessary security
3. Launch DB separetely from Elastic Beanstalk??
4. Launch Elastic Beanstalk app
5. Encrypt EBS volumes
6. Harden your Linux instance
7. Add WAF (it's so cheap!)
8. Set up Alerts
9. Something something CouchDB
10. Add SSL Cert
11. Other random security services AWS offers

## Resources:
- Great series: https://aws.amazon.com/blogs/security/how-to-automate-hipaa-compliance-part-1-use-the-cloud-to-protect-the-cloud/
- Good intro: http://cloudacademy.com/blog/how-to-build-hipaa-compliant-applications-on-aws/
