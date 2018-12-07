FROM ffig/ffig-base
LABEL maintainer="FFIG <support@ffig.org>"


RUN add-apt-repository ppa:openjdk-r/ppa; \
add-apt-repository ppa:webupd8team/java; \
apt update; \
apt install -y openjdk-8-jdk libboost-python-dev; \
echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list; \
curl https://bazel.build/bazel-release.pub.gpg | apt-key add -; apt update ; apt install bazel -y; \
mkdir -p /opt; curl -s https://swift.org/builds/swift-4.1-release/ubuntu1610/swift-4.1-RELEASE/swift-4.1-RELEASE-ubuntu16.10.tar.gz | tar zxf - -C /opt;
ENV PATH=/opt/swift-4.1-RELEASE-ubuntu16.10/usr/bin:"$PATH"

COPY . /home/ffig
RUN find /home/ffig \( -name "*.py" -o -name "*.sh" \) -exec dos2unix -q {} \;
WORKDIR /home/ffig
