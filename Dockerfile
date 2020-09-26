FROM ubuntu

ENV UESTC_HOME=/opt/uestc_check

RUN apt update
RUN apt -y install firefox
RUN apt -y install python3 python3-pip
RUN apt -y install git curl unzip
RUN apt -y install libgl1-mesa-glx
RUN curl -fSL https://gitee.com/dshe/uestc_check/repository/archive/master.zip -o uestc_check.zip
RUN unzip uestc_check.zip
RUN mv uestc_check ${UESTC_HOME}
RUN rm -rf uestc_check.zip
RUN mkdir -p /etc/uestck_check
COPY config_template.json /etc/uestc_check/config.json

RUN cd ${UESTC_HOME} && bash install.sh

WORKDIR ${UESTC_HOME}
ENTRYPOINT ["python3","task.py"]
CMD ["/etc/uestc_check/config.json"]
