---
title: macOS docker daemon 探索
date: 2022-02-13 16:02:20
updated: 2022-02-13 16:02:20
tags: [docker, macOS, container]
---

根据目前（2022/02）最新的 [Docker Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement)，Docker Desktop 只对小于 250 员工且年收入不到 1 千万美元的公司，个人用户，教育用途和非商业开源项目，提供免费使用。

对于 Mac 和 Windows 用户来说，如果不能使用 Docker Desktop，还是有非常多的可替代方案。比如 Podman, colima 甚至 docker-machine。而我个人在比较早期的时候，一直是通过 docker machine 的方式在 Mac 上使用 docker。后来发现 docker machine 不再维护，镜像不再更新。转向使用 Docker Desktop。现在公司因为不在 Docker Desktop 免费使用用户范围内。这里简单记录一下，自己在 Mac 上使用 docker 的方案。

简单分为三大块

- 虚拟机安装
- 共享文件
- 连通网络

<!-- more -->

## 虚拟机安装

在非 linux 系统上运行容器服务，本质上都是通过运行一个 linux 虚拟机来实现的。免费常用的虚拟机软件 [VirtualBox](https://www.virtualbox.org/) 可以很好的胜任这个工作。既然我们的目的是通过虚拟机来运行 dockerd 服务。这里选择一个小巧精简的系统 [Alpine Linux](https://alpinelinux.org/downloads/)，它的虚拟系统优化版本只有 54.5 MB。


VirtualBox 可以在官网下载安装包。除了安装 VirtualBox 本身，还需要安装它的扩展包，在后面的文件共享时依赖于此。同样可以从官网下载到。

还可以通过 brew 安装：
```bash
$ brew install virtualbox

$ brew install virtualbox-extension-pack
```

安装好 VirtualBox 后，新建虚拟机，选择创建一个命名为 "docker" 的 64-bit Linux 系统，1 GB 内存。20 GB 动态分配磁盘。创建好以后。在“Tools” - “Network” 中创建一张虚拟网卡。

在 docker 虚拟机的网络设置中，启用 “Adapter 2”，网络类型选择 “Host-only Adapter”，下面会自动选上我们前面创建好的虚拟网卡。这里稍微解释一下，默认 “Adapter 1” 是 NAT 网络，用来访问外网。这个 IP 在我们的电脑上访问不通。所以新增一个主机网络，用于在电脑上访问这台虚拟机。

再在存储中将我们下好的 Alpine 镜像分配到空的片盘中。就可以开始启动我们的虚拟机了。

虚拟机启动后，进入安装系统。使用 root 免密登录。输入 `setup-alpine` 开始安装系统。

```bash
$ setup-alpine

Select keyboard layout: [none] us

Select variant (or 'abort'): us

Enter system hostname (fully qualified from, e.g. 'foo.example.org') [localhost]: docker

Which one do you want to initialize? (or '?' or 'done') [eth0]
Ip address for eth0? (or 'dhcp', 'none', '?') [dhcp]
Which one do you want to initialize? (or '?' or 'done') [eth1]
Ip address for eth1? (or 'dhcp', 'none', '?') [dhcp]
Do you want to any manual network configuration? (y/n) [n]

New password: docker
Retype password: docker

Which timezone are you in? ('?' for list) [UTC] Asia
Which sub-timezone of 'Asiz' are you in? ('?' for list) Shanghai

HTTP/FTP proxy URL? (e.g. 'http://proxy:8080', or 'none') [none]
Which NTP client to run? ('busybox', 'openntpd', 'chrony' or 'none') [chrony]

Enter mirror number (1-62) or URL to add  (or r/f/e/done) [1] 31

Which SSH server? ('openssh', 'dropbear' or 'none') [openssh]

Which disk(s) would you like to use? (or '?' for help or 'none') [none] sda

How would you like to use it? ('sys', 'data', 'crypt', 'lvm' or '?' for help) [?] sys

WARNING: Erase the above disk(s) and continue? (y/n) [n] y

$ poweroff # 关机
```

安装完成，在存储设置中将安装镜像移除。重新启动 docker 虚拟机。使用 root 用户登录。现将我们电脑的 ssh 公钥添加到 `/root/.ssh/authorized_keys` 文件中。

```shell
$ mkdir .ssh
$ cd .ssh
$ wget -O authorized_keys https://github.com/eirture.keys
```

通过 ifconfg 查看 eth1 IP 地址，现在可以在电脑上通过 ssh 登录到虚拟机中了。

登录后，可以开始安装 docker。开启社区仓库地址。取消 `/etc/apk/repositories` 文件第三行的注释

```shell
$ cat /etc/apk/repositories

#/media/cdrom/apks
http://mirrors.sjtug.sjtu.edu.cn/alpine/v3.15/main
http://mirrors.sjtug.sjtu.edu.cn/alpine/v3.15/community  # 删除这一行开头的 #
#http://mirrors.sjtug.sjtu.edu.cn/alpine/edge/main
#http://mirrors.sjtug.sjtu.edu.cn/alpine/edge/community
#http://mirrors.sjtug.sjtu.edu.cn/alpine/edge/testing

$ apk update
$ apk add docker

$ rc-update add docker default  # 开启自动启动 docker 服务
```

在 mac 上可以配置 DOCKER_HOST，可以直接访问虚拟机中的 docker 服务。（需要先在 mac 上安装 docker 命令工具 `brew install docker`）

```shell
$ export DOCKER_HOST=ssh://root@192.168.56.103
$ docker version

```

## 文件共享

可以直接使用 VirtualBox 提供的文件共享功能。需要先在虚拟机中安装 VirtualBox 扩展驱动。

```shell
$ apk add virtualbox-guest-additions
```

在虚拟机配置的共享目录设置中把 /Users 目录配置为永久共享路径。挂载点设置为 Users。将挂载信息配置到虚拟机的 `/etc/fstab` 文件中。

```fstab
# 添加如下行
Users /Users vboxsf defaults 0 0
```

通过 mount 命令挂在并查看是否挂在成功。
```shell
$ mkdir /Users
$ mount -a

$ ls -l /Users
```

## 连通网络

我们可以通过虚拟机转发所有发往容器网络的包。安装好 docker 以后，默认 ipv4 的转发功能已经开启。

```shell
$ cat /proc/sys/net/ipv4/ip_forward
1
```

在虚拟机中配置 iptables 允许 eth1 发往 172.16.0.0/12 网段的包。

```shell
$ iptables -A FORWARD -i eth1 -d 172.16.0.0/12 -j ACCEPT
```

可以把这个规则配置添加到 dockerd 启动的配置文件中。dockerd 启动完成后，自动配置该规则。在 /etc/init.d/docker 文件中，增加以下内容：

```shell
start_post() {
	iptables -A FORWARD -i eth1 -d 172.16.0.0/12 -j ACCEPT
}
```

另外还需要在 mac 主机上添加一个路由规则，将发往 172.16/12 网段的包，发往 192.168.56.103 （虚拟机 eth1 IP）网关。

```
$ sudo route add -net 172.16/12 192.168.56.103
```

启动一个 nginx 服务验证，可以在 mac 上直接通过容器 ip 访问 nginx 服务了。

```
$ docker run --rm --name nginx -i -d nginx
$ docker inspect nginx -f '{{ .NetworkSettings.IPAddress }}'
172.17.0.2

$ curl 172.17.0.2
```

最后我自定义了两个命令别名，快速启动和关闭 docker 虚拟机。在启动的时候增加路由表信息，关闭时候删除路由表信息。

```shell
alias dds='VBoxManage list runningvms' # 查看正常运行的虚拟机
alias ddsr='VBoxManage startvm --type headless docker && echo "Waiting..." && sudo route add -net 172.16.0.0 -netmask 255.248.0.0 192.168.56.103' # 启动 docker 服务 (dockerd start)
alias ddso='ssh root@<your-docker-vm-ip> poweroff && && sudo route delete 172.16/13' # 停止 docker 服务 (dockerd stop)
```

## 结尾

到此，我们有了一个简单的替代 Docker Desktop 方案。当然直接使用 Podman 或 colima 也可以满足大多数使用场景。不过在网络上笔者往前探索了一步。而无论 Podman, colima 还是笔者的方案。都有存在一个问题。就是共享的文件，无法修改权限和 owner。而在某些场景下，通过 bind 目录的方式共享的目录，可能在容器内部，因为 owner 或权限无法修改也无法读写。Docker Desktop 使用自己的 gRPC fuse 方案避免了这个问题。

## 参考

- [Install Alpine on VirtualBox - Alpine Linux](https://wiki.alpinelinux.org/wiki/Install_Alpine_on_VirtualBox#Install_drivers_for_Virtual_Box)
- [networking - How can I use Linux as a Gateway? - Unix &amp; Linux Stack Exchange](https://unix.stackexchange.com/a/222065/379653)
- [mac os (freebsd)的路由规则学习 - 知乎](https://zhuanlan.zhihu.com/p/163103180)
- [File Sharing with Docker Desktop - Docker Blog](https://www.docker.com/blog/file-sharing-with-docker-desktop/)
