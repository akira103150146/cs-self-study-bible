FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential gdb valgrind strace ltrace binutils file xxd git make \
      python3 python3-pip python3-venv ca-certificates \
 && rm -rf /var/lib/apt/lists/*
RUN pip3 install --break-system-packages --no-cache-dir \
      pytest numpy matplotlib pandas flask pillow
WORKDIR /work
