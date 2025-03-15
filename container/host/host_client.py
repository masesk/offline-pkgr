import tempfile
import os
import subprocess
from container.generic_client import GenericClient
class HostClient(GenericClient):
    def __init__(self):
        pass
    def run(self, command: str, install_command: str, output_file: str = "output.tar.gz"):
        with tempfile.TemporaryDirectory() as tmpdirname:
            command = f"cd {tmpdirname} && {command}"
            proc = subprocess.Popen(["bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.wait() 
            self.__generate_tar__(tmpdirname, install_command, output_file)
