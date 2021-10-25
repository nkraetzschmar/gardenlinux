FROM debian:buster

RUN apt-get update
RUN apt-get install -y bc fakeroot build-essential devscripts quilt stgit \
	unzip git kernel-wedge bison flex cpio dh-python dh-exec libelf-dev libssl-dev
RUN git config --global user.email "you@example.com"
RUN git config --global user.name "Your Name"
