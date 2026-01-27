import pulumi
import pulumi_gcp as gcp

from my_components import compute


if __name__ == "__main__":
    config = pulumi.Config()
    gcp_config = pulumi.Config("gcp")

    network = gcp.compute.Network(
        "platform-network",
        auto_create_subnetworks=False,
    )

    subnet = gcp.compute.Subnetwork(
        "platform-subnet",
        ip_cidr_range="10.0.1.0/24",
        network=network.id,
        region=gcp_config.require("region"),
    )

    firewall = gcp.compute.Firewall(
        "platform-firewall",
        network=network.self_link,
        allows=[
            {
                "protocol": "tcp",
                "ports": [
                    "22",
                    "80",
                    "443",
                ],
            },
        ],
        direction="INGRESS",
        source_ranges=[
            "128.59.0.0/16",  # Columbia U Secure
            "160.39.0.0/16",  # Columbia U Secure
            "209.2.0.0/16",  # Columbia U Secure
            "129.236.0.0/16",  # Columbia University
            "67.254.133.105/32",  # Your Home IP
        ],
    )

    vm_config = config.require_object("vmConfig")

    vm_args = compute.MyInstanceArgs(
        region=gcp_config.require("region"),
        zone=gcp_config.require("zone"),
        network_id=network.id,
        subnet_id=subnet.id,
        **vm_config,
    )

    vm = compute.MyInstance("test-vm", vm_args)

    pulumi.export("vm_name", vm.instance_name)
    pulumi.export("vm_public_ip", vm.public_ipv4)
