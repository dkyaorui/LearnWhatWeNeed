# Linux 基础

## 系统启动流程

### 系统引导概述

1. 计算机硬件加载 BIOS（计算机中最接近硬件的软件）并检查硬件是否健康；
2. 引导系统，读取 MBR（默认第0柱面、第0磁道、第1个扇区）；
   1. 第一个扇区的大小为 512 Bytes，其中引导程序占 446 Byte，磁盘分区表 DPT 占 64 Byte，剩余 2 Byte 是 MBR 结束位；
3. Linux 大部分版本使用 Grub 作为系统引导，但 Grub 较大，一般由 MBR 指向 Grub 进行系统启动。
   1. Grub 根据配置文件加载 kernel 镜像，并运行内核加载后的第一个程序 `/sbin/init` ，这个程序会根据 `/etc/inittab` 来进行初始化的工作，更具文件中的配置来确定系统将要运行的 runlevel，默认值在 `id:3:initdefault` 中；
4. Linux 根据 `/etc/inittab` 中定义的系统初始化配置 `si::sysinit:/etc/rc.d/rc.sysinit` 执行 `/etc/rc.sysinit` 脚本；
   1. `/etc/rc.sysinit` 脚本将设置系统变量、网络配置、并启动 swap、设定 `/proc` 、加载用户自定义模块、内核设置等。
5. 根据读到的 runlevel 来确定启动的服务，如果值为 5，就会启动`/etc/rc5.d` 下的所有脚本；
6. 运行 `/etc/.local`；
7. 生成终端或者桌面。

### 系统运行级别

1. 级别

   1. 0 级：关机；
   2. 1 级：单用户模式（忘记系统密码时，可以通过这种方式进入维护模式，修改密码）；
   3. 2 级：多用户模式，但没有网络链接；
   4. 3 级：完全多用户模式，这是 Linux 最常见的运行模式；
   5. 4 级：保留未使用；
   6. 5 级：窗口模式，支持网络，支持多用户；
   7. 6 级：重启。 

2. 不同 runlevel 之间的区别

   ```
   [root@localhost~]#ll/etc/rc3.d/
   total288
   ............
   lrwxrwxrwx1rootroot15Oct7 20:52 K15httpd>../init.d/httpd
   lrwxrwxrwx1rootroot13Oct7 20:55 K20nfs>../init.d/nfs
   ............
   lrwxrwxrwx1rootroot18Oct7 20:50 S08iptables>../init.d/iptables
   lrwxrwxrwx1rootroot17Oct7 20:52 S10network>../init.d/network
   ............
   ```
   
   分别以 K 和 S 开头接两位数字再接文件名链接的是上层目录 `init.d` 中的脚本，K 代表 kill，S 代表 start，先执行 K，所有的 K 执行完后执行 S，K 和 S 中按后接的数字从小到大顺序执行。

### 获取帮助

1. 使用 `man package ` 命令可以获取相关的帮助
   1. Linux 下有九种man文件：
      1. 常见命令说明；
      2. 可调用的系统；
      3. 函数库；
      4. 设备文件；
      5. 文件格式；
      6. 游戏说明；
      7. 杂项；
      8. 系统管理员可用命令；
      9. 内核说明。
2. 使用 `info package` 获取帮助

## Linux 用户管理

### Linux 用户和用户组

#### UID 和 GID

1. Linux 通常采用32位的整数来区分用户而不是用户名，这个整数就是 UID，普通用户的 UID 通常从500开始。
   1. root 用户的 UID 为0；
   2. 通过 `id` 可以查看当前用户的 id
2. Linux 还有用户组的概念，用于管理拥有相同权限的用户，一个用户组相当于一个班级。
   1. 通过 `groups` 可以查看当前用户所在的所有组

3. `who` 命令可以查看当前系统的在线用户。

#### `/etc/passwd` 和 `/etc/shadow`

1. `/etc/passwd` 最早是用来保存用户密码，随着技术的发展，每个用户都需要读取这个文件，存在风险，所以有了 `/etc/shadow` , 将密码从 `/etc/passwd` 中剥离了出来，密码经过加密保存在 `/etc/shadow`。

### Linux 账号管理

Linux 用户分为 根用户，系统用户和普通用户

#### 新增和删除用户

1. 新增用户

   `useradd ` 命令用于新增用户：

    >   `	    useradd test` 会为 test 用户分配一个 UID，并创建目录 `/home/test`，> 然后复制 `/etc/skel` 到 `/home/test` 下，再创建用户组 test

2. 修改密码

   `passwd` 在根用户下使用时可以接用户名，其他用户不能接任何参数。

3. 修改用户

   `usermod` 

4. 删除用户

   `userdel` 如果使用 `-r` 参数，将会删除该用户的所有文件

#### 新增和删除用户组

1. 新增用户组

   `groupadd` 命令用于新增用户组

2. 删除用户组

   `groupdel` 命令用于删除用户组 

#### 检查用户信息

1. 查看用户：`user`, `who`, `w`
2. 调查用户：`finger`

### 任务执行

#### 单一任务执行

`at now + n minutes` n 分钟后执行一次接下来指定的任务

> [root@localhost~]#at now + 30 minutes
>
> at>/sbin/shutdownhnow
>
> at><EOT>
>
> job 1 at 20121106 23:39
>
>  
>
> [root@localhost~]#at 00:00 2015-10-07
>
> at>/sbin/shutdown -h now
>
> at><EOT>
>
> job2at2012110700:00

使用 `atq` 可以查看当前使用 `at` 调度的任务

使用 `atrm` 可以删除任务

#### 周期性执行任务 

cron

## Linux 文件管理

### 文件和目录管理

#### Linux 常见目录

* `/bin`：常见用户指令；
* `/boot`：内核和启动文件；
* `/dev`：设备文件；
* `/etc`：系统和服务配置文件；
* `/home`：默认的系统用户家目录；
* `/mnt`：系统加载文件系统常用的挂载点；
* `/lib`：系统函数库目录；
* `/opt`：第三方软件安装目录；
* `/proc`：虚拟文件系统；
* `/root`：root 用户家目录；
* `/sbin`：存放系统管理命令；
* `/tmp`：临时文件的存放目录；
* `/usr`：存放与用户直接相关的文件和目录；
* `/media`：系统用来挂载光驱等临时文件系统的挂载点。

特殊目录  (.)  和 (..)

`pwd` 查看当前路径的绝对路径。

`ls` 查看当前目录下文件，可接参数 `-al` 查看隐藏文件和权限

#### 文件相关操作

创建文件：`touch`

删除文件：`rm`

移动或重命名文件：`mv`

查看文件：`cat`

查看文件头：`head`

查看文件尾：`tail`

文件格式转换（windows文件转unix文件）：`dos2unix`

查看文件大小：`du`

查看文件类型：`file`

#### 文件和目录权限

改变文件权限：`chmod`

> 我们定义r=4，w=2，x=1，如果权限是rwx，则数字表示为7，如果权限是rx，则数字表示为5。假设想设置一个文件的权限是：拥有者的权限是读、写、执行（rwx），拥有组的权限是读、执行（rx），其他人的权限是只读（r），那么可以使用命令`chmod 754 somefile`来设置。如果需要修改的不是一个文件而是一个目录，以及该目录下所有的文件、子目录、子目录下所有的文件和目录（即递归设置该目录下所有的文件和目录的权限），则需要使用R参数，也就是`chmod -R 754 somedir`

改变文件拥有者：`chown`

改变文件拥有组：`chgrp`

#### 查找文件

一般查找：`find`

数据库查找：`locate`

查找执行文件：`which`/`whereis`

#### 文件解压和压缩

*.gz：`gunzip`/`gzip`

*.tar.gz/\*.tgz：`tar -zxvf`/`tar -zcvf` *解压时 `-C` 指定解压目录*

### Linix 文件系统

#### 文件系统

Linux 采用文件系统+虚拟文件系统用于翻译物理磁盘中的0和1。

文件系统是操作系统用于区分磁盘或分区上相关文件的数据结构，是在磁盘上组织文件的方法。

#### 软链接和硬链接

硬链接：实际链接，指通过索引节点进行链接。

> 在 Linux 文件系统中，所有的文件都会有一个编号，称为 inode，多个文件名指向同一节点是被允许的，这种链接就是硬链接。只有在删除最后一个链接时，文件所占空间才会被释放。

硬链接的限制：

* 不允许给目录创建硬链接；
* 只能在同一文件系统中的文件之间才能创建硬链接。

软连接：符号链接，是一个包含了另一个文件路径名的文件，可以指向任意文件和目录，也可以跨文件系统。

> 删除软连接并不会删除源文件。

