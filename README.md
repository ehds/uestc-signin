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
docker build -t uestc_signin:latest .

```

## Usage
Please sync time zone first
### Linux
set username and passwd at uestc.conf
```
user = '2018220xxxx'
password = 'xxx'

```

If you want to know if today's task has done, set the mail config section. You can get these settings from your email server provider, for example [mail.qq.com](https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=14&&no=1000898)

```
enable = true
pop_host = pop.qq.com
smtp_host = smtp.qq.com
port = 25
username = 
# passwd or token
password = 

# notification receivers
receivers = 
```



run the task
```
python3 main.py uestc.conf
```

### Docker

```
docker run -d --name uestc_signin -v path/to/uestc.conf:/etc/uestc_signin/uestc.conf uestc_signin
```

## TODO
1. support multiple users
2. fix log format
3. improve captcha recognition accuracy
