import docker
import tempfile
from container.generic_client import GenericClient

class DockerClient(GenericClient):
    def __init__(self, distro):
        self.distro = distro
    def run(self, command: str, install_command: str, output_file: str = "output.tar.gz"):
        with tempfile.TemporaryDirectory() as tmpdirname:
            client = docker.DockerClient()
            command = f"bash -c 'cd {tmpdirname} && {command}'"
            print("Executing: ", command)
            container =client.containers.run(
                self.distro,
                command=command,
                mounts=[
                    docker.types.Mount(
                        target=tmpdirname,
                        source=tmpdirname,
                        type="bind"
                    )
                ],
                detach=False,  # Run in detached mode
                remove=True   # Automatically remove container after it stops
            )
            self.__generate_tar__(tmpdirname, install_command, output_file)
