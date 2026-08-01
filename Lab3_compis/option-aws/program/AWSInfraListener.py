import boto3
from antlr4 import *
from InfraLangListener import InfraLangListener

class AWSInfraListener(InfraLangListener):
    def __init__(self):
        self.variables = {}
        self.provider_config = {}
        self.instance_config = {}

    def enterVariable(self, ctx):
        var_name = ctx.STRING().getText().strip('"')
        for kv in ctx.body().keyValue():
            key = kv.IDENTIFIER().getText()
            if key == "default":
                value = kv.expr().getText().strip('"')
                self.variables[var_name] = value
                print(f"[var] {var_name} = {'*' * len(value) if 'key' in var_name or 'secret' in var_name else value}")

    def enterProvider(self, ctx):
        provider_name = ctx.STRING().getText().strip('"')
        if provider_name != "aws":
            raise Exception(f"Expected 'aws' provider, got '{provider_name}'.")
        for kv in ctx.body().keyValue():
            key = kv.IDENTIFIER().getText()
            self.provider_config[key] = kv.expr().getText()

    def enterResource(self, ctx):
        resource_type = ctx.STRING(0).getText().strip('"')
        if resource_type != "aws_instance":
            return
        for kv in ctx.body().keyValue():
            key = kv.IDENTIFIER().getText()
            self.instance_config[key] = kv.expr().getText()

    def resolve(self, expr):
        if expr.startswith("var."):
            var_name = expr.split(".")[1]
            if var_name in self.variables:
                return self.variables[var_name]
            raise Exception(f"Undefined variable '{var_name}'.")
        return expr.strip('"')

    def deploy(self):
        if not self.provider_config:
            raise Exception("Missing provider block.")
        if not self.instance_config:
            raise Exception("Missing aws_instance resource block.")

        region = self.resolve(self.provider_config.get("region", '"us-east-1"'))
        access_key = self.resolve(self.provider_config.get("access_key", '""'))
        secret_key = self.resolve(self.provider_config.get("secret_key", '""'))

        name = self.resolve(self.instance_config.get("name", '"my-instance"'))
        ami = self.resolve(self.instance_config.get("ami", '""'))
        instance_type = self.resolve(self.instance_config.get("instance_type", '"t2.micro"'))

        print(f"[*] Connecting to AWS ({region})...")
        ec2 = boto3.client(
            'ec2',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

        print(f"[*] Launching EC2 instance '{name}' ({instance_type})...")
        response = ec2.run_instances(
            ImageId=ami,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': name}]
            }]
        )

        instance_id = response['Instances'][0]['InstanceId']
        print(f"[✓] EC2 instance launched: {instance_id}")
        print(f"[!] Remember to terminate it: aws ec2 terminate-instances --instance-ids {instance_id} --region {region}")
