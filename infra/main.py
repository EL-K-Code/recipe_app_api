#!/usr/bin/env python
from cdktf import App, TerraformOutput, TerraformStack
from constructs import Construct

# Imports pour infra_base
from imports.aws.data_aws_caller_identity import DataAwsCallerIdentity
from imports.aws.db_instance import DbInstance
from imports.aws.db_subnet_group import DbSubnetGroup
from imports.aws.default_subnet import DefaultSubnet
from imports.aws.default_vpc import DefaultVpc
from imports.aws.instance import Instance
from imports.aws.provider import AwsProvider
from imports.aws.security_group import (
    SecurityGroup,
    SecurityGroupEgress,
    SecurityGroupIngress,
)


class MyRdsStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Appel à infra_base(), récupération des ressources réseau par défaut
        account_id, security_group, subnets, default_vpc = self.infra_base()

        # On crée un DbSubnetGroup à partir des subnets par défaut récupérés
        subnet_group = DbSubnetGroup(
            self,
            "DbSubnetGroup",
            name="rds-subnet-group",
            subnet_ids=subnets,
            tags={"Name": "RDS subnet group"},
        )

        # Création de l'instance RDS
        db_instance = DbInstance(
            self,
            "PostgresInstance",
            allocated_storage=20,
            engine="postgres",
            engine_version="17.4",
            instance_class="db.t3.micro",
            db_name="mydb",  # attention db_name et pas name
            username="postgres",
            password="StrongPassword123!",
            db_subnet_group_name=subnet_group.name,
            vpc_security_group_ids=[security_group.id],  # sg créé dans infra_base()
            skip_final_snapshot=True,
            publicly_accessible=True,
            tags={"Name": "MyPostgresDB"},
        )

        instance = Instance(
            self,
            "webservice",
            ami="ami-04b4f1a9cf54c11d0",
            instance_type="t2.micro",
            key_name="ec2-django",
        )

        # Outputs
        TerraformOutput(self, "rds_endpoint", value=db_instance.address)
        TerraformOutput(self, "ec2_public_ip", value=instance.public_ip)
        TerraformOutput(self, "db_name_output", value=db_instance.db_name)

    def infra_base(self):
        """
        Permet de définir une infra de base (provider, VPC par défaut, subnets, sg)
        """
        # Provider AWS pour us-east-1 (important car on récupère VPC par défaut us-east-1)
        AwsProvider(self, "AWSProvider", region="us-east-1")

        # Récupération de l'ID du compte AWS (utile si besoin)
        account_id = DataAwsCallerIdentity(self, "account_id").account_id

        # VPC par défaut (celui créé automatiquement dans chaque région)
        default_vpc = DefaultVpc(self, "default_vpc")

        # Liste des AZ us-east-1 disponibles (a-f)
        az_ids = [f"us-east-1{i}" for i in "abcdef"]

        subnets = []
        for i, az_id in enumerate(az_ids):
            subnet = DefaultSubnet(self, f"default_sub{i}", availability_zone=az_id)
            subnets.append(subnet.id)

        # Création d'un security group avec règles ingress/egress
        security_group = SecurityGroup(
            self,
            "sg-tp",
            ingress=[
                SecurityGroupIngress(
                    from_port=22,
                    to_port=22,
                    cidr_blocks=["0.0.0.0/0"],
                    protocol="TCP",
                ),
                SecurityGroupIngress(
                    from_port=80, to_port=80, cidr_blocks=["0.0.0.0/0"], protocol="TCP"
                ),
                SecurityGroupIngress(
                    from_port=8080,
                    to_port=8080,
                    cidr_blocks=["0.0.0.0/0"],
                    protocol="TCP",
                ),
            ],
            egress=[
                SecurityGroupEgress(
                    from_port=0, to_port=0, cidr_blocks=["0.0.0.0/0"], protocol="-1"
                )
            ],
        )

        return account_id, security_group, subnets, default_vpc


app = App()
MyRdsStack(app, "MyRdsStack")
app.synth()
