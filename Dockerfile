FROM ubuntu:24.04

RUN apt update && apt install apt-transport-https && \
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64 /" > /etc/apt/sources.list.d/nvidia.list && \
    touch /etc/apt/apt.conf.d/99verify-peer.conf && \
    echo 'Acquire { https::Verify-Peer "false"; }' | tee /etc/apt/apt.conf.d/99verify-peer.conf && \
    apt update --allow-insecure-repositories &&  \
    apt install -y --allow-unauthenticated libcudnn9-cuda-12 libcublas-12-9 python3 python3-pip python3-venv

WORKDIR /app

RUN python3 -m venv .venv &&  \
    pip3 install faster-whisper==1.2.1 --break-system-packages \
    # pip3 install -r requirements.txt --break-system-packages
