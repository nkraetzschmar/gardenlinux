Garden Linux ONIE image
=======================

Testing / Development VM
------------------------
It is a good idea to have a VM to test/develop the Garden Linux ONIE-compatible image with.
Compile a Garden Linux ONIE installer image and serve it via http as `onie-installer-x86_64.bin`:

    make onie

    sudo apt-get install -y nginx
    sudo cp .build/onie/*/amd64/*/onie-installer-x86_64.bin /var/www/html/onie-installer-x86_64.bin


Now you have to create the ONIE environment. Easiest way is to clone the ONIE repository and build ONIE using a docker container as described at https://github.com/opencomputeproject/onie/tree/2021.08/contrib/build-env.

    git clone https://github.com/opencomputeproject/onie
    cd onie
    git checkout 2021.08
    cd contrib/build-env
    docker build -t debian:onie-builder .
    cd ../../
    docker run -it --rm -v $(pwd):/tmp/onie -w /tmp/onie/build-config --name onie-builder debian:onie-builder make -j4 MACHINE=kvm_x86_64 all

You will find the ONIE images in the `build/images` directory.

To create a VM you need to install libvirt. And create a default libvirt network:

    sudo apt-get install qemu-system libvirt-clients libvirt-daemon-system virtinst
    
    cat <<EOF > default.xml
    <network>
        <name>default</name>
        <uuid>9a05da11-e96b-47f3-8253-a3a482e445f5</uuid>
        <forward mode='nat'/>
        <bridge name='virbr0' stp='on' delay='0'/>
        <mac address='52:54:00:0a:cd:21'/>
        <ip address='192.168.122.1' netmask='255.255.255.0'>
            <dhcp>
            <range start='192.168.122.2' end='192.168.122.254'/>
            </dhcp>
        </ip>
    </network>
    EOF

    sudo virsh --connect qemu:///session net-define --file default.xml

Then create the VM:
    
    sudo virt-install \
        -n gardenlinux-onie \
        --os-type=Linux \
        --os-variant=debian10 \
        --ram=4096 \
        --vcpus=2 \
        --disk path=$(pwd)/build/images/gardenlinux-onie-vm.img,bus=virtio,size=4 \
        --graphics none \
        --cdrom $(pwd)/build/images/*.iso \
        --network default

virt-install will create an empty VM disk image `gardenlinux-onie-dev.img` and start the VM. Be quick and select the `ONIE: Embed ONIE` option from the boot menu to install ONIE on the VM's disk.
After installation the VM will reboot into ONIE. It will start auto-discovery of a NOS installer image and pick it up from the nginx server configured above (`http://192.168.122.1/onie-installer-x86_64.bin`). ONIE will execute the gardenlinux-onie installer and then reboots into Garden Linux.


### Handy virsh commands:

* exit the console using the escape key Ctrl + ] (German Mac keyboard: Strg + Opt + 6)
* reconnect to the console using the virsh console command `sudo virsh --connect qemu:///session console gardenlinux-onie`
* stop the VM using the command `sudo virsh --connect qemu:///session destroy gardenlinux-onie`
* delete the VM using `sudo virsh --connect qemu:///session undefine gardenlinux-onie`.
