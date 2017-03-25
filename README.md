![img](http://www.textfiles.com/underconstruction/HeHeartlandBluffs8237Photo_2000construction5_anim.gif)

# OpenEMR AWS Guide

## ☁ Overview

Our team will demonstrate how a small facility or hospital can run their OpenEMR v5 installation in the AWS cloud in a way that is peformant, scalable, secure (HIPAA-compliant), and cost-effective.

Many OpenEMR users host their server instances on premise and have not yet realized the benefits of cloud technologies. While users can hire a professional vendor for cloud deployment services or simply learn AWS and do it themselves, our team has identified a need for a more cost effective option.

## 🕊️ Version 1

This first release (codename "Dove") will use AWS services in a way that can be described as a "PaaS-buffet". This is to say that the choosen technologies will "lock" the user to many opinionated AWS services.

Services include Elastic Beanstalk, RDS, Route53, IAM, TurnKey CouchDB, Cloudwatch, CloudFormation, and SES.

## 🐨 Version 2

This second release (codename "Dolphin") will focus on using generic services so users may choose any cloud provider they want. Ideally, users can stand up a "local cloud" should they choose to benefit from cloud technologies but want to run their own data centers.

## License & Credits

MIT
