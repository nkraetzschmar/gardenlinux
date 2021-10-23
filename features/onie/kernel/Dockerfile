FROM debian:buster

RUN apt-get update
RUN apt-get install -y build-essential git wget stgit kernel-wedge quilt bison flex \
                u-boot-tools util-linux \
			    gperf device-tree-compiler python-all-dev xorriso \
				autoconf automake texinfo libtool libtool-bin \
				gawk libncurses5 libncurses5-dev bc \
				dosfstools mtools pkg-config help2man libexpat1 \
				libexpat1-dev fakeroot python3-sphinx rst2pdf \
				libefivar-dev libnss3-tools libnss3-dev libpopt-dev \
				libssl-dev sbsigntool uuid-runtime uuid-dev cpio \
				bsdmainutils dh-python
RUN git config --global user.email "you@example.com"
RUN git config --global user.name "Your Name"
