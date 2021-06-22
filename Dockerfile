FROM ubuntu

ENV UESTC_HOME=/opt/uestc_signin
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo '$TZ' > /etc/timezone
RUN apt update
RUN apt -y install firefox
RUN apt -y install python3 python3-pip
RUN apt -y install git curl unzip pkg-config
# Dependent libs
RUN apt -y install libgl1-mesa-glx libcairo2-dev libjpeg-dev libgif-dev

RUN curl -fSL https://github.com/ehds/uestc-signin/archive/refs/heads/master.zip -o uestc-signin.zip
RUN unzip uestc-signin.zip
RUN mv uestc-signin-master ${UESTC_HOME}
RUN rm -rf uestc-signin.zip
RUN mkdir -p /etc/uestc-signin
RUN cd ${UESTC_HOME} && bash install.sh
WORKDIR ${UESTC_HOME}
CMD ["/usr/bin/bash"]
