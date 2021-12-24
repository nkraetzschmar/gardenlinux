OBJS = bootspec-fundamental.o efivars-fundamental.o string-util-fundamental.o sha256.o assert.o devicetree.o disk.o graphics.o measure.o pe.o secure-boot.o util.o cpio.o initrd.o splash.o stub.o linux.o

.SUFFIXES:
.PHONY: all

all: stub.efi

stub.so: $(OBJS)

%.o: %.c
	aarch64-linux-gnu-gcc \
		-c $< \
		-o $@ \
		-fno-stack-protector \
		-fno-strict-aliasing \
		-fpic \
		-fwide-exec-charset=UCS2 \
		-nostdlib \
		-std=gnu99 \
		-ffreestanding \
		-fshort-wchar \
		-isystem /usr/include/efi \
		-isystem /usr/include/efi/aarch64 \
		-DSD_BOOT \
		-DGNU_EFI_USE_MS_ABI \
		-DGIT_VERSION='""' \
		-Wall \
		-Werror \

%.so:
	aarch64-linux-gnu-ld \
		-o $@ \
		-fuse-ld=bfd \
		-L /usr/lib/ \
		-T /usr/lib/elf_aarch64_efi.lds \
		-nostdlib \
		-znocombreloc \
		-Bsymbolic \
		-shared \
		-fwhole-program \
		--defsym=EFI_SUBSYSTEM=0xa \
		/usr/lib/crt0-efi-aarch64.o \
		$^ \
		-lefi \
		-lgnuefi

%.efi: %.so
	aarch64-linux-gnu-objcopy \
		-j '.bss*' \
		-j .data \
		-j .dynamic \
		-j .dynsym \
		-j .osrel \
		-j '.rel*' \
		-j .sbat \
		-j .sdata \
		-j .sdmagic \
		-j .text \
		-O binary \
		$< \
		$@
