# UESTC SAFE CHECK

## Install

### Linux
Packages: Firefox 60.0+ python3 pip3 curl

```
apt install firefox python3 python3-pip curl git
```
Then
```
bash install.sh
```
### Docker
```
cd docker
docker build -t uestc_check:latest .
docker run -d --name uestc_check -v path/to/config.json:/etc/uestc_check/config.json uestc_check
```

## Usage
set username and passwd at config.py
```
user = '2018220xxxx'
passwd = 'xxx'

```
run the task
```
python3 uestc_login.py
python3 task.py
```

## TODO
make login and task module run daemon on server.
