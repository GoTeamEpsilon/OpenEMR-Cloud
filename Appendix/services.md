![picture of AWS services as of April 2017](https://www.dropbox.com/s/y0atpw7agpbmksq/Screenshot%202017-04-22%2019.52.47.png?dl=1)

# Which groups will we use?

## Compute
- EC2
- Elastic Beanstalk

## Storage
- S3 (strong yes)
- EFS (strong yes)
- Glacier (not sure yet, but it seems likely some data would have to be archived??)

## Networking & Content Delivery
- VPC (strong yes)
- Route 53 (strong yes, they need domain name for SSL)

## Management Tools 
- CloudWatch (strong yes)
- CloudFormation (strong yes)
- CloudTrail (strong yes)
- Config (strong yes)

## Security, Identity & Compliance:
- IAM (strong yes)
- Certificate Manager (strong yes)
- Directory Service (for replicating on-premise AD, probably going to delete)
- WAF & Shield (yes)

## Messaging
- Simple Notification Service (I believe you need this for CloudWatch notifications)

## Business Productivity (extremely optional)
- (opinion here is they should probably host their email and have a Dropbox like solution, why not choose AWS)
- WorkDocs
- WorkMail
