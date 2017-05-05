FROM ffig/ffig-base
MAINTAINER FFIG <support@ffig.org>

COPY . /home/ffig
RUN find /home/ffig \( -name "*.py" -o -name "*.sh" \) -exec dos2unix {} +
WORKDIR /home/ffig
