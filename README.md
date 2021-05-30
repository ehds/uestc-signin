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
docker pull ehds/uestc-signin:latest
```
or build by yourself
```
docker build -t ehds/uestc-signin:latest .
```

## Usage
Please sync time zone first
### Linux
set username and passwd at confs/uestc.conf, you can add multiple conf file for every users.
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
python3 main.py confs
```

### Docker

```
docker run -d --name ehds/uestc-signin -v path/to/conf_dir:/etc/uestc_signin/confs uestc-signin
```

## TODO
1. support multiple users
2. fix log format
3. improve captcha recognition accuracy
