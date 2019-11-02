# Systemd 简单记录 [附]：uwsgi实例

> systemd 是一款与系统高耦合的管理软件

## 系统管理

### systemctl

```bash
# 关机
systemctl poweroff
# 重启
systemctl reboot
# 暂停系统
systemctl suspend
# 单用户状态（救援状态）
systemctl rescue
```

### systemd-analyze

```bash
# 查看服务启动耗时
systemd-analyze blame
# 查看系统启动耗时
systemd-analyze
# 显示指定服务的启动流
systemd-analyze critical-chain xxx.service
```

### localectl

```bash
# 查看本地设置
localectl
# 设置本地参数
localectl set-locale LANG=en_GB.utf8
```

### timedatectl

```bash
# 查看当前时区
timedatectl
# 显示可用时区列表
timedatectl list-timezones
# 设置时区
timedatectl set-timezone Asia/Shanghai
```

### hostnamectl

```bash
# 显示当前主机名
hostnamectl
# 设置主机名
hostnamectl set-hostname your-host-name
```

### loginctl

```bash
# 显示当前登录的用户列表
loginctl list-users
# 显示指定用户的信息
loginctl show-user username
```

## Unit

*系统中不同的资源统称为 **Unit***

### unit 分类

> 1. service ：系统服务
> 2. socket ：进程通信, 套接字单元
> 3. target ：多个unit构成的组
> 4. device ：硬件设备
> 5. swap ： swap文件
> 6. mount ：文件系统挂载点
> 7. automount ：自动挂载点
> 8. path ：路径
> 9. scope ：非systemd启动的外部进程
> 10. slice： 进程组
> 11. snapshot：systemd快照
> 12. timer ：定时器

### systemctl list-units

```bash
# 列出正在运行的 unit
systemctl list-units
# 列出所有的unit
systemctl list-units --all
# 根据类型列出unit，此命令列出类型为service的unit
systemctl list-units --type=service
# 列出加载失败的unit
systemctl list-units --failed
# 列出没有运行的unit
systemctl list-units --all --state=inactive
```

### systemctl status

```bash
# 显示系统状态
systemctl status
# 显示单个unit的状态
systemctl status xxx.service
```

### 查询状态

```bash
# 判断单个unit是否运行
systemctl is-active xxx.service
# 判断单个unit是否启动失败
systemctl is-failed xxx.service
# 判断单个unit是否建立的启动链接
systemctl is-enabled xxx.service
```

### unit 管理

```bash
# 启动一个服务
systemctl start xxx.service
# 停止一个服务
systemctl stop xxx.service
# 重启一个服务
systemctl restart xxx.service
# kill某个服务下的所有进程
systemctl kill xxx.service
# 重新加载服务文件
systemctl reload xxx.service
# 重新加载修改过的配置文件
systemctl daemon-reload
# 显示unit参数
systemctl show xxx.service
# 显示unit指定属性的值
systemctl show -p a xxx.service
# 设置unit指定属性的值
systemctl set-property xxx.service a=data
```

> 当配置文件修改后，需要重新加载配置文件并重新启动，方可生效
>
> ```bash
> systemctl daemon-reload
> systemctl restart xxx.service
> ```
>
>

### 查看依赖

```bash
# 添加 --all 参数是为了展开依赖中的target，不添加则显示结果中不展开target
systemctl list-dependencies --all xxx.service
```

## unit 配置文件

配置文件的默认目录： `/etc/systemd/system`

配置文件的实际目录：`/usr/lib/systemd/system`

> `/etc/systemd/system` 文件夹下大多是符号链接指向 `/usr/lib/systemd/system`

基本命令

```bash
# 在上述两个文件建立符号链接
systemctl enable xxx.service
# 取消链接
systemctl disable xxx.service
```

### systemctl list-unit-files

```bash
# 列出所有的配置文件
systemctl list-unit-files
# 输出置顶类型的配置文件
systemctl list-unit-files --type=service
```

> 输出结果中 STATE 有四中状态
>
> 1. enable: 已建立启动链接
> 2. disable: 未建立启动链接
> 3. static: 只能作为其他配置文件的依赖（没有[install]部分）
> 4. masked: 被禁止建立启动链接

### 配置文件区块

```bash
#  定义unit的元数据以及与其他unit之间的关系
[Unit]
Description：A free-form string 简短描述
Documentation：A space-separated list of URIs 文档地址
Requires：unit 当前 Unit 依赖的其他 Unit，如果它们没有运行，当前 Unit 会启动失败
Wants：unit 与当前 Unit 配合的其他 Unit，如果它们没有运行，当前 Unit 不会启动失败
BindsTo：unit 它指定的 Unit 如果退出，会导致当前 Unit 停止运行
Before：unit 如果该字段指定的 Unit 也要启动，那么必须在当前 Unit 之后启动
After：unit 如果该字段指定的 Unit 也要启动，那么必须在当前 Unit 之前启动
Conflicts：unit 这里指定的 Unit 不能与当前 Unit 同时运行
Condition...：unit 当前 Unit 运行必须满足的条件，否则不会运行
Assert...：unit 当前 Unit 运行必须满足的条件，否则会报启动失败
# 只有service类型的unit才会生效该区块
[Service]
Type：定义启动时的进程行为。它有以下几种值。
# Type共有一下几个参数
# forking：以 fork 方式从父进程创建子进程，创建后父进程会立即退出
# oneshot：一次性进程，Systemd 会等当前服务退出，再继续往下执行
# dbus：当前服务通过D-Bus启动
# notify：当前服务启动完毕，会通知Systemd，再继续往下执行
# idle：若有其他任务执行完毕，当前服务才会运行
# simple：默认值，执行ExecStart指定的命令，启动主进程
Type=simple
ExecStart：启动当前服务的命令
ExecStartPre：启动当前服务之前执行的命令
ExecStartPost：启动当前服务之后执行的命令
ExecReload：重启当前服务时执行的命令
ExecStop：停止当前服务时执行的命令
ExecStopPost：停止当其服务之后执行的命令
RestartSec：自动重启当前服务间隔的秒数
Restart：定义何种情况 Systemd 会自动重启当前服务,下附restart参数表格 
TimeoutSec：定义 Systemd 停止当前服务之前等待的秒数
Environment：指定环境变量
# 定义系统相关的设置
[Install]
Alias：当前 Unit 可用于启动的别名
Also：当前 Unit 激活（enable）时，会被同时激活的其他 Unit
WantedBy：它的值是一个或多个 Target，当前 Unit 激活时符号链接会放入/etc/systemd/system目录下面以 Target 名 + .wants后缀构成的子目录中
RequiredBy：同上，后缀为.requires
```

##### Restart 参数表格

| 退出原因(↓) \| Restart= (→) | `no` | `always` | `on-success` | `on-failure` | `on-abnormal` | `on-abort` | `on-watchdog` |
| --------------------------- | ---- | -------- | ------------ | ------------ | ------------- | ---------- | ------------- |
| 正常退出                    |      | X        | X            |              |               |            |               |
| 退出码不为"0"               |      | X        |              | X            |               |            |               |
| 进程被强制杀死              |      | X        |              | X            | X             | X          |               |
| systemd 操作超时            |      | X        |              | X            | X             |            |               |
| 看门狗超时                  |      | X        |              | X            | X             |            | X             |

## Target

target 是多个unit构成的组，当启动一个target的时候，target内部的所有unit会被启动

```bash
# 查看默认启动的target
systemctl get-default
# 设置默认启动的target
systemctl set-default xxx.target
# 启动一个target，关闭前一个不属于启动的target的进程
systemctl isolate xxx.target
```



## 日志管理

### journalctl

```bash
# 查看所有日志（默认情况下 ，只保存本次启动的日志）
journalctl

# 查看内核日志（不显示应用日志）
journalctl -k

# 查看系统本次启动的日志，默认与追加 -0 效果一直
journalctl -b

# 查看上一次启动的日志（需更改设置）
journalctl -b -1

# 查看指定时间的日志
journalctl --since="2012-10-30 18:17:16"
journalctl --since "20 min ago"
journalctl --since yesterday
journalctl --since "2015-01-10" --until "2015-01-11 03:00"
journalctl --since 09:00 --until "1 hour ago"

# 显示尾部指定行数的日志 默认显示10行
journalctl -n 20

# 实时滚动显示最新日志
journalctl -f

# 查看指定服务的日志
journalctl /usr/lib/systemd/systemd

# 查看指定进程的日志
journalctl _PID=1

# 查看某个路径的脚本的日志
journalctl /usr/bin/bash

# 查看指定用户的日志
journalctl _UID=33 --since today

# 查看某个 Unit 的日志
journalctl -u nginx.service
journalctl -u nginx.service --since today

# 实时滚动显示某个 Unit 的最新日志
journalctl -u nginx.service -f

# 合并显示多个 Unit 的日志
journalctl -u nginx.service -u php-fpm.service --since today

# 查看指定优先级（及其以上级别）的日志，共有8级
# 0: emerg
# 1: alert
# 2: crit
# 3: err
# 4: warning
# 5: notice
# 6: info
# 7: debug
journalctl -p err -b

# 日志默认分页输出，--no-pager 改为正常的标准输出
journalctl --no-pager

# 以 JSON 格式（多行）输出
journalctl -b -u nginx.serviceqq -o json-pretty

# 显示日志占据的硬盘空间
journalctl --disk-usage

# 指定日志文件占据的最大空间
journalctl --vacuum-size=1G

# 指定日志文件保存多久
journalctl --vacuum-time=1years
```

## 实例 [uwsgi]

> 上线部署django项目

```bash
[Unit]
Description=DjangoWebSite
# 或者其他数据库service eg:mongod.service
After=mysqld.service

[Service]
WorkingDirectory=/path/to/your/WebSite-root
ExecStart=/usr/bin/uwsgi --ini /path/to/uwsgi.ini
ExecStop=/usr/bin/uwsgi --stop /path/to/uwsgi.pid
ExecReload=/usr/bin/uwsgi --reload /path/to/uwsgi.pid
Restart=on-failure
RestartSec=20s

[Install]
# multi-user.target 是多用户的target，可起到类似开机启动的作用
WantedBy=multi-user.target


```