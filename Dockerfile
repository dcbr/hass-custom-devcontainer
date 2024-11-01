FROM mcr.microsoft.com/devcontainers/python:3.12

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Initialize dev environment (copied from https://github.com/home-assistant/core/blob/dev/Dockerfile.dev)
RUN \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        bluez \
        ffmpeg \
        libudev-dev \
        libavformat-dev \
        libavcodec-dev \
        libavdevice-dev \
        libavutil-dev \
        libgammu-dev \
        libswscale-dev \
        libswresample-dev \
        libavfilter-dev \
        libpcap-dev \
        libturbojpeg0 \
        libyaml-dev \
        libxml2 \
        git \
        cmake \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# Get go2rtc binary
RUN \
    curl -L https://github.com/AlexxIT/go2rtc/releases/download/v1.9.6/go2rtc_linux_amd64 --output /bin/go2rtc \
    && chmod +x /bin/go2rtc \
    && go2rtc --version

# Install Node
RUN \
    source /usr/local/share/nvm/nvm.sh \
    && nvm install 22

EXPOSE 8123

VOLUME /workspace
RUN mkdir /config

COPY container /usr/bin
COPY hassfest /usr/bin
COPY scripts/ /usr/src/scripts/

# Setup python virtual environment
RUN \
    pip3 install --upgrade wheel pip \
    && pip3 install uv
USER vscode
ENV VIRTUAL_ENV="/home/vscode/.local/ha-venv"
RUN uv venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt /tmp/requirements.txt
RUN uv pip install -r /tmp/requirements.txt

CMD sudo -E container
