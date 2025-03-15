from installer.generic_installer import GenericInstaller
import os, subprocess
import sys

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