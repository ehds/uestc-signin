FROM ubuntu

ENV UESTC_HOME=/opt/uestc_signin
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo '$TZ' > /etc/timezone
RUN apt update
RUN apt -y install firefox
RUN apt -y install python3 python3-pip
RUN apt -y install git curl unzip
RUN apt -y install libgl1-mesa-glx
RUN curl -fSL https://github.com/ehds/uestc-signin/archive/master.zip -o uestc_signin.zip
RUN unzip uestc_signin.zip
RUN mv uestc_check ${UESTC_HOME}
RUN rm -rf uestc_signin.zip
RUN mkdir -p /etc/uestck_signin
COPY config_template.json /etc/uestc_signin/config.json
RUN cd ${UESTC_HOME} && bash install.sh

WORKDIR ${UESTC_HOME}
ENTRYPOINT ["python3","main.py"]
CMD ["/etc/uestc_check/config.json"]
