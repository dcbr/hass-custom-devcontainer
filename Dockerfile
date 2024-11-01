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
        inotify-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node
RUN \
    source /usr/local/share/nvm/nvm.sh \
    && nvm install 22

EXPOSE 8123

VOLUME /workspace
RUN mkdir -p /config/www/workspace /config/custom_components

COPY src/ /usr/bin/
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
