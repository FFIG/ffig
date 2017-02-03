FROM ubuntu:16.04
MAINTAINER Jonathan B Coe <jbcoe@me.com>

RUN apt-get -y update && apt-get install -y python-software-properties software-properties-common
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test
RUN apt-get -y update && apt-get install -y python-pip git cmake ninja-build ruby pypy python3 python3-pip clang libclang-3.8-dev libc++1 libc++-dev ruby-dev

RUN pip install --upgrade pip && pip install jinja2 nose
RUN pip3 install --upgrade pip && pip install nose
RUN gem install ffi

RUN apt-get autoremove -y
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN useradd c-api-user && mkdir -p /home/c-api-user && chown c-api-user /home/c-api-user
ENV HOME /home/c-api-user
ENV LD_LIBRARY_PATH /usr/lib/llvm-3.8/lib:$LD_LIBRARY_PATH

COPY . /home/c-api-user/demo
WORKDIR /home/c-api-user/demo/
