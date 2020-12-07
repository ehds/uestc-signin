# UESTC-Sign-In

## Installation

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
docker build -t uestc_check:latest .

```

## Usage
Please sync time zone first
### Linux
set username and passwd at config_template.json
```
user = '2018220xxxx'
passwd = 'xxx'

```
run the task
```
python3 main.py config.json
```

### Docker

```
docker run -d --name uestc_check -v path/to/config.json:/etc/uestc_check/config.json uestc_check
```

## TODO
1. support multiple users
2. fix log format
3. improve captcha recognition accuracy
