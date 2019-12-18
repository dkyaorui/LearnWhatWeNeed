# Go mod 报错：unkonw reversion

今天将开发环境切换到Linux后，使用`go mod download`下载依赖时，一个私有仓库的项目报出了**unkonw reversion**的错误。

- 第一个思路：版本不存在

  检查了私有仓库的版本号，发现对应版本存在，所以这个思路错误

- 第二个思路：git版本错误

  这个是在搜索错误时发现的，`go get`依赖git， 但没有具体的依据需要特定版本的git，切换到了2.7.4版本的git，发现依旧报错

- 第三个思路：怀疑权限问题

  检查了仓库权限，发现账号有权限，但在stackoverflows上发现了一个`go get`连接私有仓库时可能出现的错误情况，git在没有设置账号密码时要不断地输入，并且会报**unknow reversion**的错误，我在开发机使用的密钥连接仓库，再次Google一番相关设置，发现git默认使用的https去连接，而我使用密钥连接需要替换url地址，需要做如下设置：

  ```bash
  # ~/.gitconfig
  
  [url "git@your-personal-register-url"]
  	insteadOf = https://your-personal-register-url/
  ```

  再去尝试使用`go mod`下载依赖时，顺利下载所有依赖。

所以错误**unkonw reversion**具有一定的误导性，当遇见此错误时，应首先考虑是否是权限出现问题。