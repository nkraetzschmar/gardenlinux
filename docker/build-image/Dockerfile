ARG build_base_image=gardenlinux/slim
FROM	golang:latest as golang
COPY	garden-feat.go /go/src
RUN	go install golang.org/x/lint/golint@latest \
     && cd /go/src \
     && golint garden-feat.go \
     && go mod init garden-feat.go \
     && go mod tidy -go=1.16 \
     && go mod tidy -go=1.17 \
     && go build garden-feat.go

FROM debian:testing-slim AS aarch64-binutils
ENV DEBIANFRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates git build-essential texinfo flex bison zlib1g-dev
RUN git clone https://sourceware.org/git/binutils-gdb.git
WORKDIR /binutils-gdb
RUN ./configure --prefix=/opt/binutils --target=aarch64-linux-gnu --disable-werror --disable-gdb --disable-sim --with-system-zlib
RUN make prefix=/opt/binutils tooldir=/opt/binutils -j $(nproc)
RUN make prefix=/opt/binutils tooldir=/opt/binutils install

FROM debian:testing-slim AS aarch64-efi-stub
ENV DEBIANFRONTEND=noninteractive
RUN dpkg --add-architecture arm64
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates git build-essential crossbuild-essential-arm64 gnu-efi:arm64
WORKDIR efi_stub
RUN git clone https://github.com/systemd/systemd.git
RUN cp systemd/src/boot/efi/*.c systemd/src/boot/efi/*.h systemd/src/fundamental/*.c systemd/src/fundamental/*.h ./
COPY efi_stub/Makefile Makefile
RUN make

FROM 	$build_base_image
ARG	DEBIAN_FRONTEND=noninteractive

RUN	apt-get update \
     &&	apt-get install -y --no-install-recommends \
		debian-ports-archive-keyring \
		debootstrap \
		wget ca-certificates gettext-base \
		dosfstools mtools datefudge squashfs-tools e2fsprogs \
		fdisk mount cryptsetup gnupg xz-utils bsdextrautils \
		sbsigntool \
		libcap2-bin \
		python3 \
		python3-mako \
		qemu-user-static \
		qemu-utils \
		cpio \
	&& if [ "$(dpkg --print-architecture)" = "amd64" ]; then apt-get install -y --no-install-recommends syslinux syslinux-common isolinux xorriso; fi \
     &&	rm -rf /var/lib/apt/lists/*

ENV	PATH=${PATH}:/opt/gardenlinux/bin
#COPY	--from=gcr.io/kaniko-project/executor:latest /kaniko/executor /usr/local/bin/executor
COPY	--from=golang /go/src/garden-feat /usr/local/bin/garden-feat
RUN	echo "progress=bar:force:noscroll\nverbose=off" >> /etc/wgetrc

COPY --from=aarch64-binutils /opt/binutils /opt/binutils
COPY --from=aarch64-efi-stub /efi_stub/stub.efi /opt/efi_stub/linuxaa64.efi.stub

WORKDIR	/tmp
