class RpmPackage():
    def __init__(self):
        self.default_command = "yum install -y --cacheonly --nobest --skip-broken --disablerepo=* *.rpm"
    def generate_download_command(self, packages: list[str], prepend_command: str = "", append_command: str = "") -> str:
        pkgs = " ".join(packages)
        command = f""" {prepend_command}
            yum update -y && \
            yum install -y --downloadonly --installroot=/var/tmp/rpminstallroot --releasever=$(rpm -q --provides $(rpm -q --whatprovides "system-release(releasever)") | grep "system-release(releasever)" | cut -d ' ' -f 3) --downloaddir=$DOWNLOAD_DIR {pkgs}
              {append_command}"""
        return command
    
    def generate_install_command(self, install_command: str = None, append_command: str = "", prepend_command: str = "") -> str:
        if install_command is None: 
            install_command = self.default_command
        print("Returning: ", f"{prepend_command} {install_command} {append_command}")
        return f"{prepend_command} {install_command} {append_command}"