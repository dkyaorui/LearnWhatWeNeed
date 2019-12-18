# Go for循环中使用协程

再写测试代码时发现在for循环中使用遍历变量时，发现一个变量在多个协程中使用，与预期不符，下面时一次模拟。

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var wg sync.WaitGroup
    for item := 0; item < 10; item++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            fmt.Println(item)
        }()
    }
    wg.Wait()
}
```

> 2
> 10
> 10
> 10
> 10
> 10
> 10
> 10
> 10
> 10

发现结果并不像预期那样打印0-9，而是大量重复的值。

## 原因分析

`go `命令开启的协程并不受for循环影响，可能循环已经结束了协程还没开始执行，而像上面的代码协程中使用的是变量的地址，当协程使用值时取到的是那一时刻变量的值，而非是开启协程的那次循环中的值。所以在向协程开启的匿名函数中传递类似的值时，需要传递稳定变量，代码如下：

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var wg sync.WaitGroup
    for item := 0; item < 10; item++ {
        wg.Add(1)
        go func(i int) {
            defer wg.Done()
            fmt.Println(i)
        }(item)
    }
    wg.Wait()
}
```

> 0
> 9
> 3
> 4
> 6
> 7
> 8
> 2
> 5
> 1