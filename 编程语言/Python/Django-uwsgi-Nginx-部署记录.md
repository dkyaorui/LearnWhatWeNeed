# Django + uwsgi + Nginx 部署过程

### `Django` 设置

```python
# settings.py
...
DEBUG = False
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
...
```

部署web前先使用`collectstatic`命令收集静态文件至static文件夹

```python
python manage.py collectstatic
```



### 安装 `uwsgi`
```python
pip install uwsgi
```

> *!最好在root权限下安装*

###  编写 `uwsgi.ini` 文件 

```ini
socket=127.0.0.1:8001
chmod-socket = 666
# the base directory (full path)
chdir=/path/to/your/website_root_dir
# Django's wsgi file, app is your project's name
module=app.wsgi
master=true
# maximum number of worker processes
#processes = 2
#thread numbers startched in each worker process
# 最佳线程数 = [(线程等待时间+线程cup时间)/线程cup时间]×cpu数量
#threads = 
# 当服务器退出是自动删除 unix socket文件和pid文件
vacuum = true
# set the virtualen path if you use the virtualenv
virtualenv=/path/to/your/venv_root_dir
pidfile=uwsgi.pid
# gid 用户组id  uid 用户id
# logfile-chmod 日志文件权限
# master=true 指定启动主进程
# callable = xxx uwsgi加载的模块中哪个变量将被调用#
```

> 保存后 使用 `uwsgi uwsgi.ini` 测试是否正常运行`Django`项目 , 此时无法加载静态文件属于正常状态，我们通过`Nginx`寻找静态文件

### 配置 `Nginx` 

安装就不在这里赘述了，Google 和 百度 都可以找到详细的教程

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
	              '$status $body_bytes_sent "$http_referer" '
	              '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

    server {
	listen       80 default_server;
	listen       [::]:80 default_server;
	# set the server_name according to your own needs
	server_name  django_web_site;

	# Load configuration files for the default server block.
	include /etc/nginx/default.d/*.conf;

	location / {
	    root /path/to/your/website_root_dir
	    proxy_redirect off;
	    include uwsgi_params;
		# note: the uwsgi_pass is the port which the uwsgi listen
	    uwsgi_pass 127.0.0.1:8001;
	    uwsgi_param UWSGI_CHDIR /path/to/your/website_root_dir
		# app is your django project's name
	    uwsgi_param UWSGI_SCRIPT app.wsgi;
	    index index.html;
		# the limits of upload size
	    client_max_body_size    4m;	
       }
	location /static {
	    alias /path/to/your/website/static;
	}
       	
	location /media {
	    alias /path/to/your/website/media;
	} 
	error_page 404 /404.html;
	    location = /40x.html {
	}

	error_page 500 502 503 504 /50x.html;
	    location = /50x.html {
	}
    }

}
```

> 执行命令 `service nginx restart` , 在本地则访问 `localhost:80` 在服务器则直接访问 ip或者域名检查部署是否成功

关于保持项目运行　*可以使用 `systemd` 或者 `screen`软连接 保持django项目的运行*

