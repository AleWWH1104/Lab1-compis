from google.cloud import compute_v1
from google.oauth2 import service_account
from antlr4 import *
from InfraLangListener import InfraLangListener

class GCPInfraListener(InfraLangListener):
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
                print(f"[var] {var_name} = {value}")

    def enterProvider(self, ctx):
        provider_name = ctx.STRING().getText().strip('"')
        if provider_name != "gcp":
            raise Exception(f"Expected 'gcp' provider, got '{provider_name}'.")
        for kv in ctx.body().keyValue():
            key = kv.IDENTIFIER().getText()
            self.provider_config[key] = kv.expr().getText()

    def enterResource(self, ctx):
        resource_type = ctx.STRING(0).getText().strip('"')
        if resource_type != "gcp_instance":
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
            raise Exception("Missing gcp_instance resource block.")

        project = self.resolve(self.provider_config.get("project", '""'))
        zone = self.resolve(self.provider_config.get("zone", '"us-central1-a"'))
        credentials_file = self.resolve(self.provider_config.get("credentials", '"credentials.json"'))

        print(f"[*] Loading GCP credentials from {credentials_file}...")
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

        name = self.resolve(self.instance_config.get("name", '"my-instance"'))
        machine_type = self.resolve(self.instance_config.get("machine_type", '"e2-micro"'))
        image_family = self.resolve(self.instance_config.get("image", '"debian-cloud/debian-11"'))

        image_parts = image_family.split("/")
        image_project, image_family_name = image_parts[0], image_parts[1]

        image_client = compute_v1.ImagesClient(credentials=credentials)
        image = image_client.get_from_family(project=image_project, family=image_family_name)

        instance = compute_v1.Instance()
        instance.name = name
        instance.machine_type = f"zones/{zone}/machineTypes/{machine_type}"

        disk = compute_v1.AttachedDisk()
        disk.boot = True
        disk.auto_delete = True
        params = compute_v1.AttachedDiskInitializeParams()
        params.source_image = image.self_link
        disk.initialize_params = params
        instance.disks = [disk]

        nic = compute_v1.NetworkInterface()
        access_config = compute_v1.AccessConfig()
        access_config.name = "External NAT"
        access_config.type_ = compute_v1.AccessConfig.Type.ONE_TO_ONE_NAT
        nic.access_configs = [access_config]
        instance.network_interfaces = [nic]

        instance_client = compute_v1.InstancesClient(credentials=credentials)
        print(f"[*] Creating GCP instance '{name}' ({machine_type}) in {zone}...")
        operation = instance_client.insert(project=project, zone=zone, instance_resource=instance)
        operation.result()
        print(f"[✓] Instance '{name}' created in project '{project}', zone '{zone}'.")
        print(f"[!] Remember to delete it to avoid charges.")
