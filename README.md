# offline-pkgr

## Packager
### Requirements
1. Python 3
2. Pip3

### Create Package
1. Create virtual environment
```
python3 -m venv .venv
```
2. Activate virutal enviroment
```
. .venv/bin/activate
```

3. Install pip requirements
```
pip install -r requirements.txt
```

4. Run packager
```
python offline_pkgr.py --pkg-manager=apt --distro=ubuntu:18.04 --packages="curl wget" --container-client=docker
```
* This command will package wget and curl for Ubuntu 18.04 using the apt package manager and docker to spin a version of Ubuntu 18.04 in the background to do this. Note that current user should have access to docker.
* --contaienr-client=`podman` needs to run as a service. Run ```podman system service --time=0``` on a different terminal.

5. Copy `output.tar.gz` to the target machine along with either `offline_installer.py` for Python3 supported targets or create a go executable using Go. (Details below)

---

## Installer (Python)

### Requirements
1. Python3
2. Pip3 
3. `offline_installer.py`

### Execute
```
sudo python3 offline_installer.py /path/to/output.tar.gz
```

## Installer (Go)
For non-Python installed systems, you can generate an executable to run on the system.

### Requirements
1. Go

### Create Installer
1. Download dependencies
```
go mod tidy
```

2. Create installer
```
go build
```

3. Copy `offline-installer` to target directory

4. Install
```
sudo ./offline-installer /path/to/output.tar.gz
```
