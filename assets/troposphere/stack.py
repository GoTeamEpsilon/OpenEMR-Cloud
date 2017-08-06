#!/usr/bin/python
# -*- coding: utf-8 -*-

from troposphere import Base64, FindInMap, GetAtt, GetAZs, Join, Select, Split, Output
from troposphere import Parameter, Ref, Tags, Template
from troposphere import ec2, route53, kms, s3

import argparse

ref_stack_id = Ref('AWS::StackId')
ref_region = Ref('AWS::Region')
ref_stack_name = Ref('AWS::StackName')
ref_account = Ref('AWS::AccountId')

parser = argparse.ArgumentParser(description="OpenEMR stack builder")
parser.add_argument("--dev", help="build [security breaching!] development resources", action="store_true")
parser.add_argument("--dualAZ", help="build AZ-hardened stack", action="store_true")
args = parser.parse_args()

t = Template()

t.add_version('2010-09-09')
t.add_description("""OpenEMR v5.0.0 cloud deployment""")

def setInputs(t, args):
    t.add_parameter(Parameter(
        'EC2KeyPair',
        Description = 'Amazon EC2 Key Pair',
        Type = 'AWS::EC2::KeyPair::KeyName'
    ))

    t.add_parameter(Parameter(
        'RDSPassword',
        NoEcho = True,
        Description = 'The database admin account password',
        Type = 'String',
        MinLength = '8',
        MaxLength = '41'
    ))

    t.add_parameter(Parameter(
        'TimeZone',
        Description = 'The timezone OpenEMR will run in',
        Default = 'America/Chicago',
        Type = 'String',
        MaxLength = '41'
    ))

    t.add_parameter(Parameter(
        'PatientRecords',
        Description = 'Database storage for patient records (minimum 10 GB)',
        Default = '10',
        Type = 'Number',
        MinValue = '10'
    ))

    t.add_parameter(Parameter(
        'DocumentStorage',
        Description = 'Document database for patient documents (minimum 500 GB)',
        Default = '500',
        Type = 'Number',
        MinValue = '10'
    ))

def setMappings(t):
    t.add_mapping('RegionData', {
        "us-east-1" : {
            "RegionBucket": "openemr-useast1",
            "ApplicationSource": "beanstalk/openemr-5.0.0-005.zip",
            "MySQLVersion": "5.6.27",
            "AmazonAMI": "ami-a4c7edb2",
            "UbuntuAMI": "ami-d15a75c7"
        },
        "us-west-2" : {
            "RegionBucket": "openemr-uswest2",
            "ApplicationSource": "beanstalk/openemr-5.0.0-005.zip",
            "MySQLVersion": "5.6.27",
            "AmazonAMI": "ami-6df1e514",
            "UbuntuAMI": "ami-835b4efa"
        },
        "eu-west-1" : {
            "RegionBucket": "openemr-euwest1",
            "ApplicationSource": "beanstalk/openemr-5.0.0-005.zip",
            "MySQLVersion": "5.6.27",
            "AmazonAMI": "ami-d7b9a2b1",
            "UbuntuAMI": "ami-6d48500b"
        },
        "ap-southeast-2" : {
            "RegionBucket": "openemr-apsoutheast2",
            "ApplicationSource": "beanstalk/openemr-5.0.0-005.zip",
            "MySQLVersion": "5.6.27",
            "AmazonAMI": "ami-10918173",
            "UbuntuAMI": "ami-e94e5e8a"
        }
    })
    return t

def buildVPC(t, dualAZ):
    t.add_resource(
        ec2.VPC(
            'VPC',
            CidrBlock='10.0.0.0/16',
            EnableDnsSupport='true',
            EnableDnsHostnames='true'
        )
    )

    t.add_resource(
        ec2.Subnet(
            'PublicSubnet1',
            VpcId = Ref('VPC'),
            CidrBlock = '10.0.1.0/24',
            AvailabilityZone = Select("0", GetAZs(""))
        )
    )

    t.add_resource(
        ec2.Subnet(
            'PrivateSubnet1',
            VpcId = Ref('VPC'),
            CidrBlock = '10.0.2.0/24',
            AvailabilityZone = Select("0", GetAZs(""))
        )
    )

    t.add_resource(
        ec2.Subnet(
            'PublicSubnet2',
            VpcId = Ref('VPC'),
            CidrBlock = '10.0.3.0/24',
            AvailabilityZone = Select("1", GetAZs(""))
        )
    )

    t.add_resource(
        ec2.Subnet(
            'PrivateSubnet2',
            VpcId = Ref('VPC'),
            CidrBlock = '10.0.4.0/24',
            AvailabilityZone = Select("1", GetAZs(""))
        )
    )

    t.add_resource(
        ec2.InternetGateway(
            'ig'
        )
    )

    t.add_resource(
        ec2.VPCGatewayAttachment(
            'igAttach',
            VpcId = Ref('VPC'),
            InternetGatewayId = Ref('ig')
        )
    )

    t.add_resource(
        ec2.RouteTable(
            'rtTablePublic',
            VpcId = Ref('VPC')
        )
    )

    t.add_resource(
        ec2.Route(
            'rtPublic',
            RouteTableId = Ref('rtTablePublic'),
            DestinationCidrBlock = '0.0.0.0/0',
            GatewayId = Ref('ig'),
            DependsOn = 'igAttach'
        )
    )

    t.add_resource(
        ec2.SubnetRouteTableAssociation(
            'rtPublic1Attach',
            SubnetId = Ref('PublicSubnet1'),
            RouteTableId = Ref('rtTablePublic')
        )
    )

    t.add_resource(
        ec2.SubnetRouteTableAssociation(
            'rtPublic2Attach',
            SubnetId = Ref('PublicSubnet2'),
            RouteTableId = Ref('rtTablePublic')
        )
    )

    if (dualAZ):
        t.add_resource(
            ec2.RouteTable(
                'rtTablePrivate1',
                VpcId = Ref('VPC')
            )
        )

        t.add_resource(
            ec2.EIP(
                'natIp1',
                Domain = 'vpc'
            )
        )

        t.add_resource(
            ec2.NatGateway(
                'nat1',
                AllocationId = GetAtt('natIp1', 'AllocationId'),
                SubnetId = Ref('PublicSubnet1')
            )
        )

        t.add_resource(
            ec2.Route(
                'rtPrivate1',
                RouteTableId = Ref('rtTablePrivate1'),
                DestinationCidrBlock = '0.0.0.0/0',
                NatGatewayId = Ref('nat1')
            )
        )

        t.add_resource(
            ec2.SubnetRouteTableAssociation(
                'rtPrivate1Attach',
                SubnetId = Ref('PrivateSubnet1'),
                RouteTableId = Ref('rtTablePrivate1')
            )
        )

        t.add_resource(
            ec2.RouteTable(
                'rtTablePrivate2',
                VpcId = Ref('VPC')
            )
        )

        t.add_resource(
            ec2.EIP(
                'natIp2',
                Domain = 'vpc'
            )
        )

        t.add_resource(
            ec2.NatGateway(
                'nat2',
                AllocationId = GetAtt('natIp2', 'AllocationId'),
                SubnetId = Ref('PublicSubnet2')
            )
        )

        t.add_resource(
            ec2.Route(
                'rtPrivate2',
                RouteTableId = Ref('rtTablePrivate2'),
                DestinationCidrBlock = '0.0.0.0/0',
                NatGatewayId = Ref('nat2')
            )
        )

        t.add_resource(
            ec2.SubnetRouteTableAssociation(
                'rtPrivate2Attach',
                SubnetId = Ref('PrivateSubnet2'),
                RouteTableId = Ref('rtTablePrivate2')
            )
        )
    else:
        t.add_resource(
            ec2.RouteTable(
                'rtTablePrivate',
                VpcId = Ref('VPC')
            )
        )

        t.add_resource(
            ec2.EIP(
                'natIp',
                Domain = 'vpc'
            )
        )

        t.add_resource(
            ec2.NatGateway(
                'nat',
                AllocationId = GetAtt('natIp', 'AllocationId'),
                SubnetId = Ref('PublicSubnet1')
            )
        )

        t.add_resource(
            ec2.Route(
                'rtPrivate',
                RouteTableId = Ref('rtTablePrivate'),
                DestinationCidrBlock = '0.0.0.0/0',
                NatGatewayId = Ref('nat')
            )
        )

        t.add_resource(
            ec2.SubnetRouteTableAssociation(
                'rtPrivate1',
                SubnetId = Ref('PrivateSubnet1'),
                RouteTableId = Ref('rtTablePrivate')
            )
        )

        t.add_resource(
            ec2.SubnetRouteTableAssociation(
                'rtPrivate2',
                SubnetId = Ref('PrivateSubnet2'),
                RouteTableId = Ref('rtTablePrivate')
            )
        )

    return t

def buildFoundation(t, dev):

    t.add_resource(
        route53.HostedZone(
            'DNS',
            Name='openemr.local',
            VPCs = [route53.HostedZoneVPCs(
                VPCId = Ref('VPC'),
                VPCRegion = ref_region
            )]
        )
    )

    t.add_resource(
        kms.Key(
            'OpenEMRKey',
            DeletionPolicy = 'Delete' if dev else 'Retain',
            KeyPolicy = {
                "Sid": "1",
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        Join(':', ['arn:aws:iam:', ref_account, 'root'])
                    ]
                },
                "Action": "kms:*",
                "Resource": "*"
            }
        )
    )

    t.add_resource(
        s3.Bucket(
            'S3Bucket',
            DeletionPolicy = 'Retain',
            BucketName = Join('-', ['openemr', Select('2', Split('/', ref_stack_id))])
        )
    )

    t.add_resource(
        s3.BucketPolicy(
            'BucketPolicy',
            Bucket = Ref('S3Bucket'),
            PolicyDocument = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                      "Sid": "AWSCloudTrailAclCheck",
                      "Effect": "Allow",
                      "Principal": { "Service":"cloudtrail.amazonaws.com"},
                      "Action": "s3:GetBucketAcl",
                      "Resource": { "Fn::Join" : ["", ["arn:aws:s3:::", {"Ref":"S3Bucket"}]]}
                    },
                    {
                      "Sid": "AWSCloudTrailWrite",
                      "Effect": "Allow",
                      "Principal": { "Service":"cloudtrail.amazonaws.com"},
                      "Action": "s3:PutObject",
                      "Resource": { "Fn::Join" : ["", ["arn:aws:s3:::", {"Ref":"S3Bucket"}, "/AWSLogs/", {"Ref":"AWS::AccountId"}, "/*"]]},
                      "Condition": {
                        "StringEquals": {
                          "s3:x-amz-acl": "bucket-owner-full-control"
                        }
                      }
                    }
                ]
            }
        )
    )

    t.add_resource(
        ec2.SecurityGroup(
            'ApplicationSecurityGroup',
            GroupDescription = 'Application Security Group',
            VpcId = Ref('VPC'),
            Tags = [ { "Key" : "Name", "Value" : "Application" } ]
        )
    )

    t.add_resource(
        ec2.SecurityGroupIngress(
            'AppSGIngress',
            GroupId = Ref('ApplicationSecurityGroup'),
            IpProtocol = '-1',
            SourceSecurityGroupId = Ref('ApplicationSecurityGroup')
        )
    )

    return t

def buildDeveloperBastion(t):

    t.add_resource(
        ec2.SecurityGroup(
            'SSHSecurityGroup',
            GroupDescription = 'insecure worldwide SSH access',
            VpcId = Ref('VPC'),
            Tags = [ { "Key" : "Name", "Value" : "Global SSH" } ]
        )
    )

    t.add_resource(
        ec2.SecurityGroupIngress(
            'SSHSGIngress',
            GroupId = Ref('SSHSecurityGroup'),
            IpProtocol = 'tcp',
            CidrIp = '0.0.0.0/0',
            FromPort = '22',
            ToPort = '22'
        )
    )

    t.add_resource(
        ec2.Instance(
            'DeveloperBastion',
            ImageId = FindInMap('RegionData', ref_region, 'AmazonAMI'),
            InstanceType = 't2.nano',
            KeyName = Ref('EC2KeyPair'),
            NetworkInterfaces = [ec2.NetworkInterfaceProperty(
                AssociatePublicIpAddress = True,
                DeviceIndex = "0",
                GroupSet = [ Ref('SSHSecurityGroup'), Ref('ApplicationSecurityGroup') ],
                SubnetId = Ref('PublicSubnet2')
            )]
        )
    )

    t.add_output(
        Output(
            'DeveloperKeyhole',
            Description='direct stack access',
            Value=GetAtt('DeveloperBastion', 'PublicIp')
        )
    )

    return t

setInputs(t,args)
setMappings(t)
buildVPC(t, args.dualAZ)
buildFoundation(t, args.dev)
if (args.dev):
    buildDeveloperBastion(t)


print(t.to_json())
