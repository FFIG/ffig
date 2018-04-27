FROM ffig/ffig-base
MAINTAINER FFIG <support@ffig.org>

RUN add-apt-repository ppa:openjdk-r/ppa; apt update; apt install -y openjdk-8-jdk
RUN mkdir -p /opt; curl -s https://swift.org/builds/swift-4.1-release/ubuntu1610/swift-4.1-RELEASE/swift-4.1-RELEASE-ubuntu16.10.tar.gz | tar zxvf - -C /opt
ENV PATH=/opt/swift-4.1-RELEASE-ubuntu16.10/usr/bin:"$PATH"

COPY . /home/ffig
RUN find /home/ffig \( -name "*.py" -o -name "*.sh" \) -exec dos2unix {} +
WORKDIR /home/ffig
