# Python GIL 全局锁

## 概述

先看下官方对GIL作出的解释


> In CPython, the global interpreter lock, or GIL, is a mutex that prevents multiple native threads from executing Python bytecodes at once. This lock is necessary mainly because CPython’s memory management is not thread-safe. (However, since the GIL exists, other features have grown to depend on the guarantees that it enforces.)

简单来说，GIL就是一把全局排它锁，它保证了在同一时间内，只会有一个线程运行，也就是说Python的多线程并不是真正意义上的多线程，某种情况下效率可能会比不使用多线程低，下面会进行说明。

Python 支持多线程，但使用多线程时不可避免的问题就是保证数据完整性和状态同步，加锁是解决这一问题最简单的手段，于是 GIL 这把大锁就挂在了 Python 的头上，社区里的开发者，依赖这个 GIL 开发了大量的库，当开发者发现 GIL 十分影响效率时，整个社区的库已经相当依赖 GIL，移除GIL 变成了相当困难的事情。

## 原理

CPython 中线程是系统中真实的线程，没有任何区别，只在于 Cpython 含有 GIL 锁，一般默认 Python 的解释器为 Cpython。

Python 多线程的运行方式（图取自**David Beazley**的个人网站）

![](https://www.brianlv.com/image/gil-threads.png)

```Python
lock = threading.Lock()

def run_thread(n):
    # 获取锁:
    lock.acquire()
    try:
      #process
      pass
    finally:
      # 释放锁:
      lock.release()
```

但在 Python 的线程中，主线程在运行一定数量的指令到阀值后会释放锁后，进行一次线程调度，但 release 和 acquire 之间的间隔相当的小，这会造成在没有I/O操作的情况下，很有可能重新获取锁，而其他被唤醒的线程，只能等待，空耗资源，直到再次进入调度状态，幸运点会在唤醒时获取到锁，如此反复造成一个恶性循环，在 Python2 中这种情况很明显，Python 官方也对这方面不断的优化，在Python3 中情况稍好些，这也是为什么说 Python 的多线程并不是真正意义上的线程（表达或许不准确）。

## I/O 密集型和CPU密集型

*I/O 密集型：*程序中存在大量的 I/O 操作

*CPU 密集型：*程序中存在大量的需要长时间运算的操作

在官方文档中有这么一段表达：

```
Save the thread state in a local variable.
Release the global interpreter lock.
... Do some blocking I/O operation ...
Reacquire the global interpreter lock.
Restore the thread state from the local variable.
```

> **Note**: Calling system I/O functions is the most common use case for releasing the GIL, but it can also be useful before calling long-running computations which don’t need access to Python objects, such as compression or cryptographic functions operating over memory buffers. For example, the standard [`zlib`](https://docs.python.org/3/library/zlib.html#module-zlib) and [`hashlib`](https://docs.python.org/3/library/hashlib.html#module-hashlib) modules release the GIL when compressing or hashing data.

> 注意，调用系统I/O函数是释放GIL的最常见用例，同样在调用不需要访问Python对象的长时间运行的计算(如在内存缓冲区上操作的压缩或加密函数)之前，它也很有用。例如，标准的zlib和hashlib模块在压缩或散列数据时释放GIL。

显然，Python 多线程对I/O密集型的程序的友好度还是很不错的，可以获得较好的性能，但对于CPU密集型的程序并不是很友好了。

## 关于避免GIL对程序效率的影响

* 使用 multiprocessing

  这是 Python 中多进程的模块，但这并没有从根本上绕开 GIL 锁，每个进程中还是只允许同时运行一个线程，

* 使用非 CPython 解释器的版本

  比如 Jython， PyPy 等，但这些解释器版本的 Python，可能无法使用社区中现有的大量的库。

  

在功能和性能上，大多数人的选择还会是功能。



*另附一张龟叔对 GIL 的看法截图*

![](http://ww1.sinaimg.cn/large/d0055ab3ly1g1mdm2qdt1j20y20q07fp.jpg)