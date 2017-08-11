#!/usr/bin/python
# -*- coding: utf-8 -*-

from troposphere import Base64, FindInMap, GetAtt, GetAZs, Join, Select, Split, Output
from troposphere import Parameter, Ref, Tags, Template
from troposphere import ec2, route53, kms, s3, efs, elasticache, cloudtrail, rds, iam, cloudformation

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
                'rtPrivate1Attach',
                SubnetId = Ref('PrivateSubnet1'),
                RouteTableId = Ref('rtTablePrivate')
            )
        )

        t.add_resource(
            ec2.SubnetRouteTableAssociation(
                'rtPrivate2Attach',
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
                "Version": "2012-10-17",
                "Id": "key-default-1",
                "Statement": [{
                    "Sid": "1",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": [
                            Join(':', ['arn:aws:iam:', ref_account, 'root'])
                        ]
                    },
                    "Action": "kms:*",
                    "Resource": "*"
                }]
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
        cloudtrail.Trail(
            'CloudTrail',
            DependsOn = 'BucketPolicy',
            IsLogging = True,
            IncludeGlobalServiceEvents = True,
            IsMultiRegionTrail = True,
            S3BucketName = Ref('S3Bucket')
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

def buildEFS(t, dev):
    t.add_resource(
        ec2.SecurityGroup(
            'EFSSecurityGroup',
            GroupDescription = 'Webworker NFS Access',
            VpcId = Ref('VPC'),
            Tags = Tags(Name='NFS Access')
        )
    )

    t.add_resource(
        ec2.SecurityGroupIngress(
            'EFSSGIngress',
            GroupId = Ref('EFSSecurityGroup'),
            IpProtocol = '-1',
            SourceSecurityGroupId = Ref('ApplicationSecurityGroup')
        )
    )

    t.add_resource(
        efs.FileSystem(
            'ElasticFileSystem',
            DeletionPolicy = 'Delete' if dev else 'Retain',
            FileSystemTags = Tags(Name='OpenEMR Codebase')
        )
    )

    t.add_resource(
        efs.MountTarget(
            'EFSMountPrivate1',
            FileSystemId = Ref('ElasticFileSystem'),
            SubnetId = Ref('PrivateSubnet1'),
            SecurityGroups = [Ref('EFSSecurityGroup')]
        )
    )

    t.add_resource(
        efs.MountTarget(
            'EFSMountPrivate2',
            FileSystemId = Ref('ElasticFileSystem'),
            SubnetId = Ref('PrivateSubnet2'),
            SecurityGroups = [Ref('EFSSecurityGroup')]
        )
    )

    t.add_resource(
        route53.RecordSetType(
            'DNSEFS',
            DependsOn = ['EFSMountPrivate1', 'EFSMountPrivate2'],
            HostedZoneId = Ref('DNS'),
            Name = 'nfs.openemr.local',
            Type = 'CNAME',
            TTL = '900',
            ResourceRecords = [Join("", [Ref('ElasticFileSystem'), '.efs.', ref_region, ".amazonaws.com"])]
        )
    )

    return t

def buildRedis(t, dualAZ):
    t.add_resource(
        ec2.SecurityGroup(
            'RedisSecurityGroup',
            GroupDescription = 'Webworker Session Store',
            VpcId = Ref('VPC'),
            Tags = Tags(Name='Redis Access')
        )
    )

    t.add_resource(
        ec2.SecurityGroupIngress(
            'RedisSGIngress',
            GroupId = Ref('RedisSecurityGroup'),
            IpProtocol = '-1',
            SourceSecurityGroupId = Ref('ApplicationSecurityGroup')
        )
    )

    t.add_resource(
        elasticache.SubnetGroup(
            'RedisSubnets',
            Description = 'Redis node locations',
            SubnetIds = [Ref('PrivateSubnet1'), Ref('PrivateSubnet2')]
        )
    )

    t.add_resource(
        elasticache.CacheCluster(
            'RedisCluster',
            CacheNodeType = 'cache.t2.small',
            VpcSecurityGroupIds = [GetAtt('RedisSecurityGroup', 'GroupId')],
            CacheSubnetGroupName = Ref('RedisSubnets'),
            Engine = 'redis',
            NumCacheNodes = '2' if dualAZ else '1'
        )
    )

    t.add_resource(
        route53.RecordSetType(
            'DNSRedis',
            HostedZoneId = Ref('DNS'),
            Name = 'redis.openemr.local',
            Type = 'CNAME',
            TTL = '900',
            ResourceRecords = [GetAtt('RedisCluster', 'RedisEndpoint.Address')]
        )
    )

    return t

def buildMySQL(t, args):
    # TODO: verify dual-AZ
    t.add_resource(
        ec2.SecurityGroup(
            'DBSecurityGroup',
            GroupDescription = 'Patient Records',
            VpcId = Ref('VPC'),
            Tags = Tags(Name='MySQL Access')
        )
    )

    t.add_resource(
        ec2.SecurityGroupIngress(
            'DBSGIngress',
            GroupId = Ref('DBSecurityGroup'),
            IpProtocol = '-1',
            SourceSecurityGroupId = Ref('ApplicationSecurityGroup')
        )
    )

    t.add_resource(
        rds.DBSubnetGroup(
            'RDSSubnetGroup',
            DBSubnetGroupDescription = 'MySQL node locations',
            SubnetIds = [Ref('PrivateSubnet1'), Ref('PrivateSubnet2')]
        )
    )

    ### RDSInstance
    t.add_resource(
        rds.DBInstance(
            'RDSInstance',
            DeletionPolicy = 'Delete' if args.dev else 'Snapshot',
            DBName = 'openemr',
            AllocatedStorage = Ref('PatientRecords'),
            DBInstanceClass = 'db.t2.small',
            Engine = 'MySQL',
            EngineVersion = FindInMap('RegionData', ref_region, 'MySQLVersion'),
            MasterUsername = 'openemr',
            MasterUserPassword = Ref('RDSPassword'),
            PubliclyAccessible = False,
            DBSubnetGroupName = Ref('RDSSubnetGroup'),
            VPCSecurityGroups = [Ref('DBSecurityGroup')],
            KmsKeyId = Ref('OpenEMRKey'),
            StorageEncrypted = True,
            MultiAZ = args.dualAZ,
            Tags = Tags(Name='Patient Records')
        )
    )

    t.add_resource(
        route53.RecordSetType(
            'DNSMySQL',
            HostedZoneId = Ref('DNS'),
            Name = 'mysql.openemr.local',
            Type = 'CNAME',
            TTL = '900',
            ResourceRecords = [GetAtt('RDSInstance', 'Endpoint.Address')]
        )
    )

    return t

def buildCertWriter(t, dev):
    t.add_resource(
        iam.ManagedPolicy(
            'CertWriterPolicy',
            Description='Policy for initial CA writer',
            PolicyDocument = {
                "Version": "2012-10-17",
                "Statement": [
                {
                  "Sid": "Stmt1500612724000",
                  "Effect": "Allow",
                  "Action": [
                      "s3:*"
                  ],
                  "Resource": [
                    Join('', ['arn:aws:s3:::', Ref('S3Bucket'), "/CA/*"])
                  ]
                },
                {
                  "Sid": "Stmt1500612724001",
                  "Effect": "Allow",
                  "Action": [
                      "s3:ListBucket"
                  ],
                  "Resource": [
                      Join('', ['arn:aws:s3:::', Ref('S3Bucket')])
                  ]
                },
                {
                  "Sid": "Stmt1500612724002",
                  "Effect": "Allow",
                  "Action": [
                      "kms:GenerateDataKey*"
                  ],
                  "Resource": [
                    GetAtt("OpenEMRKey", "Arn")
                  ]
                }
                ]
            }
        )
    )

    t.add_resource(
        iam.Role(
            'CertWriterRole',
            AssumeRolePolicyDocument = {
               "Version" : "2012-10-17",
               "Statement": [ {
                  "Effect": "Allow",
                  "Principal": {
                     "Service": [ "ec2.amazonaws.com" ]
                  },
                  "Action": [ "sts:AssumeRole" ]
               } ]
            },
            Path='/',
            ManagedPolicyArns= [Ref('CertWriterPolicy')]
        )
    )

    t.add_resource(
        iam.InstanceProfile(
            'CertWriterInstanceProfile',
            Path = '/',
            Roles = [Ref('CertWriterRole')]
        )
    )

    instanceScript = [
        "#!/bin/bash -xe\n",
        "cd /root\n",
        "mkdir -m 700 CA CA/certs CA/keys CA/work\n",
        "cd CA\n",
        "openssl genrsa -out keys/ca.key 8192\n",
        "openssl req -new -x509 -extensions v3_ca -key keys/ca.key -out certs/ca.crt -days 3650 -subj '/CN=OpenEMR Backend CA'\n",
        "openssl req -new -nodes -newkey rsa:2048 -keyout keys/beanstalk.key -out work/beanstalk.csr -days 3648 -subj /CN=beanstalk.openemr.local\n",
        "openssl x509 -req -in work/beanstalk.csr -out certs/beanstalk.crt -CA certs/ca.crt -CAkey keys/ca.key -CAcreateserial\n",
        "openssl req -new -nodes -newkey rsa:2048 -keyout keys/couch.key -out work/couch.csr -days 3648 -subj /CN=couchdb.openemr.local\n",
        "openssl x509 -req -in work/couch.csr -out certs/couch.crt -CA certs/ca.crt -CAkey keys/ca.key\n",
        "aws s3 sync keys s3://", Ref('S3Bucket'), "/CA/keys --sse aws:kms --sse-kms-key-id ", Ref('OpenEMRKey'), " --acl private\n",
        "aws s3 sync certs s3://", Ref('S3Bucket'), "/CA/certs --acl public-read\n",
        "/opt/aws/bin/cfn-signal -e 0 ",
        "         --stack ", ref_stack_name,
        "         --resource CertWriterInstance ",
        "         --region ", ref_region, "\n",
        "shutdown -h now", "\n"
    ]

    t.add_resource(
        ec2.Instance(
            'CertWriterInstance',
            DependsOn = 'rtPrivate1Attach',
            ImageId = FindInMap('RegionData', ref_region, 'AmazonAMI'),
            InstanceType = 't2.nano',
            SubnetId = Ref('PrivateSubnet1'),
            KeyName = Ref('EC2KeyPair'),
            IamInstanceProfile = Ref('CertWriterInstanceProfile'),
            Tags = Tags(Name='Backend CA Processor'),
            InstanceInitiatedShutdownBehavior = 'stop' if args.dev else 'terminate',
            UserData = Base64(Join('', instanceScript)),
            CreationPolicy = {
              "ResourceSignal" : {
                "Timeout" : "PT5M"
              }
            }
        )
    )

    return t

def buildNFSBackup(t):
    t.add_resource(
        ec2.SecurityGroup(
            'NFSBackupSecurityGroup',
            GroupDescription = 'NFS Backup Access',
            VpcId = Ref('VPC'),
            Tags = Tags(Name='NFS Backup Access')
        )
    )

    t.add_resource(
        ec2.SecurityGroupIngress(
            'NFSSGIngress',
            GroupId = Ref('EFSSecurityGroup'),
            IpProtocol = '-1',
            SourceSecurityGroupId = Ref('NFSBackupSecurityGroup')
        )
    )

    t.add_resource(
        iam.ManagedPolicy(
            'NFSBackupPolicy',
            Description='Policy for ongoing NFS backup instance',
            PolicyDocument = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                      "Sid": "Stmt1500699052003",
                      "Effect": "Allow",
                      "Action": ["s3:ListBucket"],
                      "Resource" : Join("", ["arn:aws:s3:::", Ref('S3Bucket')])
                    },
                    {
                        "Sid": "Stmt1500699052000",
                        "Effect": "Allow",
                        "Action": [
                          "s3:PutObject",
                          "s3:GetObject",
                          "s3:DeleteObject"
                        ],
                        "Resource": [
                            Join("", ["arn:aws:s3:::", Ref('S3Bucket'), '/Backup/*'])
                        ]
                    },
                    {
                        "Sid": "Stmt1500612724002",
                        "Effect": "Allow",
                        "Action": [
                          "kms:Encrypt",
                          "kms:Decrypt",
                          "kms:GenerateDataKey*"
                        ],
                        "Resource": [ GetAtt("OpenEMRKey", "Arn") ]
                    }
                ]
            }
        )
    )

    t.add_resource(
        iam.Role(
            'NFSBackupRole',
            AssumeRolePolicyDocument = {
               "Version" : "2012-10-17",
               "Statement": [ {
                  "Effect": "Allow",
                  "Principal": {
                     "Service": [ "ec2.amazonaws.com" ]
                  },
                  "Action": [ "sts:AssumeRole" ]
               } ]
            },
            Path='/',
            ManagedPolicyArns= [Ref('NFSBackupPolicy')]
        )
    )

    t.add_resource(
        iam.InstanceProfile(
            'NFSInstanceProfile',
            Path = '/',
            Roles = [Ref('NFSBackupRole')]
        )
    )

    bootstrapScript = [
        "#!/bin/bash -xe\n",
        "exec > /tmp/part-001.log 2>&1\n",
        "apt-get -y update\n",
        "apt-get -y install python-pip\n",
        "pip install https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz\n",
        "cfn-init -v ",
        "         --stack ", ref_stack_name,
        "         --resource NFSBackupInstance ",
        "         --configsets Setup ",
        "         --region ", ref_region, "\n",
        "cfn-signal -e 0 ",
        "         --stack ", ref_stack_name,
        "         --resource NFSBackupInstance ",
        "         --region ", ref_region, "\n"
    ]

    setupScript = [
        "#!/bin/bash\n",
        "S3=", Ref('S3Bucket'), "\n",
        "KMS=", Ref('OpenEMRKey'), "\n",
        "apt-get -y update\n",
        "DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y -o Dpkg::Options::=\"--force-confdef\" -o Dpkg::Options::=\"--force-confold\" --force-yes\n",
        "apt-get -y install duplicity python-boto nfs-common awscli\n",
        "mkdir /mnt/efs\n",
        "echo \"nfs.openemr.local:/ /mnt/efs nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 0 0\" >> /etc/fstab\n",
        "mount /mnt/efs\n",
        "touch /tmp/mypass\n",
        "chmod 500 /tmp/mypass\n",
        "openssl rand -base64 32 >> /tmp/mypass\n",
        "aws s3 cp /tmp/mypass s3://$S3/Backup/passphrase.txt --sse aws:kms --sse-kms-key-id $KMS\n",
        "rm /tmp/mypass\n"
    ]

    backupScript = [
        "#!/bin/bash\n",
        "S3=", Ref('S3Bucket'), "\n",
        "KMS=", Ref('OpenEMRKey'), "\n",
        "PASSPHRASE=`aws s3 cp s3://$S3/Backup/passphrase.txt - --sse aws:kms --sse-kms-key-id $KMS`\n",
        "export PASSPHRASE\n",
        "duplicity --full-if-older-than 1M /mnt/efs s3://s3.amazonaws.com/$S3/Backup\n",
        "duplicity remove-all-but-n-full 2 --force s3://s3.amazonaws.com/$S3/Backup\n"
    ]

    recoveryScript = [
        "#!/bin/bash\n",
        "S3=", Ref('S3Bucket'), "\n",
        "KMS=", Ref('OpenEMRKey'), "\n",
        "PASSPHRASE=`aws s3 cp s3://$S3/Backup/passphrase.txt - --sse aws:kms --sse-kms-key-id $KMS`\n",
        "export PASSPHRASE\n",
        "duplicity --force s3://s3.amazonaws.com/$S3/Backup /mnt/efs\n"
    ]

    bootstrapInstall = cloudformation.InitConfig(
        files = {
            "/root/setup.sh" : {
                "content" : Join("", setupScript),
                "mode"  : "000500",
                "owner" : "root",
                "group" : "root"
            },
            "/etc/cron.daily/backup.sh" : {
                "content" : Join("", backupScript),
                "mode"  : "000500",
                "owner" : "root",
                "group" : "root"
            },
            "/root/recovery.sh" : {
                "content" : Join("", recoveryScript),
                "mode"  : "000500",
                "owner" : "root",
                "group" : "root"
            }
        },
        commands = {
            "01_setup" : {
              "command" : "/root/setup.sh"
            }
        }
    )

    bootstrapMetadata = cloudformation.Metadata(
        cloudformation.Init(
            cloudformation.InitConfigSets(
                Setup = ['Install']
            ),
            Install=bootstrapInstall
        )
    )

    t.add_resource(
        ec2.Instance(
            'NFSBackupInstance',
            DependsOn = ['rtPrivate2Attach', 'DNSEFS'],
            Metadata = bootstrapMetadata,
            ImageId = FindInMap('RegionData', ref_region, 'UbuntuAMI'),
            InstanceType = 't2.nano',
            SubnetId = Ref('PrivateSubnet2'),
            KeyName = Ref('EC2KeyPair'),
            IamInstanceProfile = Ref('NFSInstanceProfile'),
            Tags = Tags(Name='NFS Backup Agent'),
            InstanceInitiatedShutdownBehavior = 'stop',
            UserData = Base64(Join('', bootstrapScript)),
            CreationPolicy = {
              "ResourceSignal" : {
                "Timeout" : "PT5M"
              }
            }
        )
    )
    return t

setInputs(t,args)
setMappings(t)
buildVPC(t, args.dualAZ)
buildFoundation(t, args.dev)
if (args.dev):
    buildDeveloperBastion(t)
buildEFS(t, args.dev)
buildRedis(t, args.dualAZ)
buildMySQL(t, args)
buildCertWriter(t, args.dev)
buildNFSBackup(t)

print(t.to_json())
