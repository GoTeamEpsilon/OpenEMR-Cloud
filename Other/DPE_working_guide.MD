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
1. Set up users and KMS
2. Upload Code.
3. Set up networks and the necessary security
4. Launch DB separetely from Elastic Beanstalk??
5. Launch Elastic Beanstalk app
6. Encrypt EBS volumes
7. Harden your Linux instance
8. Add WAF and SSL Cert
9. Set up Alerts and Audit Logging
10. Set up EFS


## Resources:
- Great series: https://aws.amazon.com/blogs/security/how-to-automate-hipaa-compliance-part-1-use-the-cloud-to-protect-the-cloud/
- Good intro: http://cloudacademy.com/blog/how-to-build-hipaa-compliant-applications-on-aws/
