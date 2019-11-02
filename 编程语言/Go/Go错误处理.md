# Golang的错误处理

## 错误处理

#### Go标准包提供的错误处理

##### 错误类型

首先查看Go官方提供的error类型是一个接口类型

```go
// The error built-in interface type is the conventional interface for
// representing an error condition, with the nil value representing no error.
type error interface {
    Error() string
}
```

这个接口只包含一个`Error()`方法，所以只要我们实现这个方法即实现了一个错误。

```go
type timeOutError struct {
}

func (tError *timeOutError) Error() string{
    return "连接超时"
}
```

##### 动态创建错误

我们在同台创建错误时常用一个方法`errors.New()`，首先我们看一下这个方法的源码。

```go
// New returns an error that formats as the given text.
func New(text string) error {
    return &errorString{text}
}

// errorString is a trivial implementation of error.
type errorString struct {
    s string
}

func (e *errorString) Error() string {
    return e.s
}
```

这个方法通过传入的`text`创建不同的`errorString`，这个结构体实现了`Error()`方法，这样便可以动态的创建不同的错误类型。

以上就是Go内置的error核心。

#### 第三方提供的错误处理包

看过源码我们很清楚的知道内置的error类型包含的信息十分有限，所以我们在创建自己的错误类型的时候，可以添加我们想要的额外信息：如错误所在文件及其行数、时间、运行时系统栈的信息等。

例如：

```go
type myError struct {
    text string
    location string
    stack []uintptr
}
```

我们只需要实现获取我们想要信息的方法即可在错误发生时记录更多我们想要的信息并且代码更加易读可维护。

在开发中当然不能每次开发都重复造轮子，这里推荐一个错误处理包 `github.com/pkg/errors`。

##### `github.com/pkg/errors`

这个库使用起来非常方便。

- 生成一个新的错误

  ```go
  func New(message string) error
  ```

- 对已有的error做二次封装

  ```go
  //只附加新的信息
  func WithMessage(err error, message string) error
  
  //只附加调用堆栈信息
  func WithStack(err error) error
  
  //同时附加堆栈和信息
  func Wrap(err error, message string) error
  ```

这里附上errors的[文档地址](https://godoc.org/github.com/pkg/errors)。

## 识别各类网络错误

首先，还是看一下net包中error的错误源码。

```go
// An Error represents a network error.
type Error interface {
    error
    Timeout() bool   // Is the error a timeout?
    Temporary() bool // Is the error temporary?
}
```

`net.Error` 的具体类型被封装为`net.OpError`

```go
// OpError is the error type usually returned by functions in the net
// package. It describes the operation, network type, and address of
// an error.
type OpError struct {
    // Op is the operation which caused the error, such as
    // "read" or "write".
    Op string

    // Net is the network type on which this error occurred,
    // such as "tcp" or "udp6".
    Net string

    // For operations involving a remote network connection, like
    // Dial, Read, or Write, Source is the corresponding local
    // network address.
    Source Addr

    // Addr is the network address for which this error occurred.
    // For local operations, like Listen or SetDeadline, Addr is
    // the address of the local endpoint being manipulated.
    // For operations involving a remote network connection, like
    // Dial, Read, or Write, Addr is the remote address of that
    // connection.
    Addr Addr
    
    // Err is the error that occurred during the operation.
    Err error
}
```

以下是我们可能见到的错误类型：

- `net.ParseError`
- `net.AddrError`
- `net.UnknownNetworkError`
- `net.InvalidAddrError`
- `net.DNSConfigError`
- `net.DNSError`
- `net.PathError`
- `net.SyscallError`

> `net.SyscallError` 与具体的操作系统调用有关。

根据net包中的错误逻辑，我们就可以有针对的处理对应的网络错误了。

```go
import (
    "fmt"
    "net"
    "os"
    "syscall"
)

func checkNetError(err error) bool {
    // 判断是否为网络错误
    if netError, err := err.(net.Error); err {
        // 判断是否超时
        if netError.Timeout() {
            fmt.Printf("Timeout Error: %s", netError)
            return true
        } else {
            // 判断是否为正常错误
            if opError, err := netError.(*net.OpError); err {
                // 匹配错误类型
                switch expr := opError.Err.(type) {
                // DNS 错误
                case *net.DNSError:
                    fmt.Printf("DNSError: %s", netError)
                    return true
                // 系统调用错误
                case *os.SyscallError:
                    if errno, err := expr.Err.(syscall.Errno); err {
                        switch errno {
                        case syscall.ECONNREFUSED:
                            fmt.Printf("syscall.ECONNREFUSED Error: %s", netError)
                            return true
                        case syscall.ETIMEDOUT:
                            fmt.Printf("syscall.ETIMEDOUT Error: %s", netError)
                            return true
                        }
                    }
                }
            }

        }
    }
    return false
}
```

