class AptPackage():
    def __init__(self):
        self.default_install_command = "dpkg -i *.deb"
    def generate_download_command(self, packages: list[str], install_command: str = None, prepend_command: str = "", append_command: str = "") -> str:
        pkgs = " ".join(packages)
        if install_command is None:
            install_command = f"""apt-get update &&
            apt-get download $(apt-cache depends --recurse --no-recommends --no-suggests \
            --no-conflicts --no-breaks --no-replaces --no-enhances \
            {pkgs} | grep "^\w")"""
        command = f""" {prepend_command} {install_command} {append_command}"""
        return command
    
    def generate_install_command(self, install_command: str = None, append_command: str = "", prepend_command: str = "") -> str:
        if install_command is None: 
            install_command = self.default_install_command
        print("Returning: ", f"{prepend_command} {install_command} {append_command}")
        return f"{prepend_command} {install_command} {append_command}"