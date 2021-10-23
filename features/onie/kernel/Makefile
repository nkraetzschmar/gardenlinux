SONIC_KERNEL_VERSION=202106

all:
	docker build . -t gardenlinux-onie-kernel-builder:latest
	docker run -it --rm -v $(shell pwd):/mnt gardenlinux-onie-kernel-builder:latest bash -c "cd /mnt && make kernel"

kernel:
	git clone https://github.com/Azure/sonic-linux-kernel /tmp/sonic-linux-kernel
	cd /tmp/sonic-linux-kernel && git checkout $(SONIC_KERNEL_VERSION) && make
	cp /tmp/sonic-linux-kernel/*.deb /mnt/