import argparse
from container.docker.docker_client import DockerClient
from package.apt_package import AptPackage
from container.host.host_client import HostClient
SUPPORTED_PACKAGE_MANAGERS = ["apt"]
SUPPORTED_CONTAINER_CLIENTS = ["host", "docker"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pkg-manager", help="Package manager to use", choices=SUPPORTED_PACKAGE_MANAGERS, required=True)
    parser.add_argument("--distro", type=str, help="Distro to install packages for. Use docker/podman image tags (ie ubuntu:18.04)", default="host", required=False)
    parser.add_argument("--container-client", type=str, help=f"Either {SUPPORTED_CONTAINER_CLIENTS}. If non-host is passed, distro must also be non-host", default="host", required=False, choices=SUPPORTED_CONTAINER_CLIENTS)
    parser.add_argument("--install-command", type=str, help="Custom install command command. Defaults based on distro", default=None, required=False)
    parser.add_argument("--post-command", type=str, help="Command to append to install command", default="", required=False)
    parser.add_argument("--pre-command", type=str, help="Command to prepend to install command", default="", required=False)
    parser.add_argument("--packages", help="Packages to install", required=True)
    args = parser.parse_args()
    if(args.pkg_manager == "apt"):
        package_mgr = AptPackage()
    if(args.distro == "host" and args.container_client == "host"):
        print("Using Host")
        client = HostClient()
    elif(args.container_client == "docker" and args.distro != "host"):
        print("Using Docker")
        client = DockerClient(args.distro)
    else:
        print("Unsupported combination of --distro and --container-client. Use --help for more information")
        exit(1)
    client.run(package_mgr.generate_download_command(packages=["tshark"]), package_mgr.generate_install_command(prepend_command=args.pre_command, append_command=args.post_command, install_command=args.install_command), output_file="output.tar.gz")