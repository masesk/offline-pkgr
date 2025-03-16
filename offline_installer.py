import os
import subprocess
import sys
import tarfile
import configparser
import subprocess
import shutil
class GenericInstaller:
    def __init__(self):
        pass

    def install(self, tar_file_path: str) -> None:
        tar = tarfile.open(tar_file_path)
        tar.extractall(path="/tmp/")
        config = configparser.ConfigParser()
        config.read("/tmp/install.ini")
        install_command = config.get("install", "install_command")
        directory = config.get("install", "directory")
        os.chdir(directory)
        print("Executing: ", install_command)
        process = subprocess.Popen(
            install_command, 
            shell=True, stdin=None, 
            stdout=subprocess.PIPE, # Capture stdout in a pipe
            stderr=subprocess.PIPE,
            executable="/bin/sh",
            text=True
        )
        while process.poll() is None:  # While the process is running
            # Read stdout
            stdout_line = process.stdout.readline()
            if stdout_line:
                sys.stdout.write(stdout_line)
                sys.stdout.flush()  # Ensure it prints immediately

            # Read stderr
            stderr_line = process.stderr.readline()
            if stderr_line:
                sys.stderr.write(stderr_line)
                sys.stderr.flush()

        # Capture any remaining output after the process ends
        stdout_remainder, stderr_remainder = process.communicate()

        if stdout_remainder:
            sys.stdout.write(stdout_remainder)
            sys.stdout.flush()
        if stderr_remainder:
            sys.stderr.write(stderr_remainder)
            sys.stderr.flush()
        shutil.rmtree(directory)
def prompt_sudo():
    ret = 0
    if os.geteuid() != 0:
        msg = "[sudo] password for %u:"
        ret = subprocess.check_call("sudo -v -p '%s'" % msg, shell=True)
    return ret

if __name__ == "__main__":
    if prompt_sudo() != 0:
        # the user wasn't authenticated as a sudoer, exit?
        exit(1)
    installer = GenericInstaller()
    if len(sys.argv) < 2 or sys.argv[1] is None:
        print("No file provided. Pass file path as first argument.")
        exit(1)
    file = sys.argv[1]
    installer.install(file)