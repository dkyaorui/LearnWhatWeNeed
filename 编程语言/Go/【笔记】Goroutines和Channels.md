# Goroutines和Channels

## Goroutines

**Goroutine**是Go并发执行的单元。类似于其他语言的线程。

创建一个新的**Goroutine**使用`go`语句。

```go
go function()
```



## Channels

Channels 是Go语言并发体之间的通信机制，每一个`channel`都有特定的数据类型。

创建一个`int`类型的`channel`:

```go
ch := make(chan int)
```

和Map类似，channel也对应make创建的底层数据结构的引用。channel的零值为`nil`。

两个类型相同的channel可以使用==比较，同时channel也可以和nil进行比较。

channel有发送和接收两个主要操作：

```go
ch <- p // 向channel中发送一个数据p
p = <- ch // 从channel中接收一个数据存储到p
```

关闭channel

```go
close(ch)
```

当一个channel关闭后，任何对其的操作都会产生panic。

对不带缓存的channel进行操作时，只有接收和发送方完成了一组操作时，才会继续执行代码，否则将发生阻塞，也就是说发送一个数据后需要等待数据被接收，接收数据时必须要有数据已经发送才可以继续执行代码。