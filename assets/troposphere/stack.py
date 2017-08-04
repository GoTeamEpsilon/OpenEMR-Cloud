#!/usr/bin/python
# -*- coding: utf-8 -*-

from troposphere import Base64, FindInMap, GetAtt, GetAZs, Join, Select, Output
from troposphere import Parameter, Ref, Tags, Template
from troposphere import ec2, route53, kms

import argparse

ref_stack_id = Ref('AWS::StackId')
ref_region = Ref('AWS::Region')
ref_stack_name = Ref('AWS::StackName')
ref_account = Ref('AWS::AccountId')

t = Template()

t.add_version('2010-09-09')

t.add_description("""OpenEMR v5.0.0 cloud deployment""")

parser = argparse.ArgumentParser(description="OpenEMR stack builder")
parser.add_argument("--dev", help="build [security breaching!] development resources", action="store_true")
parser.add_argument("--dualAZ", help="build AZ-hardened stack", action="store_true")
args = parser.parse_args()

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
                SubnetId = Ref('SubnetPublic1')
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
                SubnetId = Ref('SubnetPublic2')
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
                SubnetId = Ref('SubnetPublic1')
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

def buildFoundation(t):

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
            DeletionPolicy = 'Delete' if args.dev else 'Retain',
            KeyPolicy = {
                "Sid": "1",
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        Join(':', ['arn:aws:iam:', Ref('AWS::AccountId'), 'root'])
                    ]
                },
                "Action": "kms:*",
                "Resource": "*"
            }
        )
    )

    return t

t = buildVPC(t, args.dualAZ)
t = buildFoundation(t)

print(t.to_json())
