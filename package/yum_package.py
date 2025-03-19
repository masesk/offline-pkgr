class YumPackage():
    def __init__(self):
        self.default_install_command = "yum install -y --cacheonly --nobest --skip-broken --disablerepo=* *.rpm"
        self.default_download_command = """yum update -y && yum install -y --downloadonly --installroot=/var/tmp/rpminstallroot --releasever=$(rpm -q --provides $(rpm -q --whatprovides "system-release(releasever)") | grep "system-release(releasever)" | cut -d ' ' -f 3) --downloaddir=$DOWNLOAD_DIR"""
    def generate_download_command(self, packages: list[str], install_command: str = None, prepend_command: str = "", append_command: str = "") -> str:
        pkgs = " ".join(packages)
        if install_command is None: 
            install_command = self.default_download_command
        command = f""" {prepend_command} {install_command} {pkgs} {append_command}"""
        return command
    
    def generate_install_command(self, install_command: str = None, append_command: str = "", prepend_command: str = "") -> str:
        if install_command is None: 
            install_command = self.default_install_command
        return f"{prepend_command} {install_command} {append_command}"