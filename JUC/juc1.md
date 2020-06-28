# Java 多线程高并发编程笔记
---

## 第二章 synchronize
可重入锁，重量级锁，保证了原子性，可见性，但是不能保证指令会重排序
可重入体现在如下几个方面
- 同一个对象的 synchronize 方法可以调用 synchronize 方法
- 执行过程异常时，会自动中断释放锁

>最初jdk设计时默认直接就是重量级锁，后来经过改造synchronize增加了锁升级的过程
### 2.1 synchronize（object）
> <font color="red">不能锁定String常量、Integer、Long及一些基本数据类型</font>
### 2.2 线程同步
1. 锁的是一个对象而不是一串代码段
2. 如果synchronize加在静态方法上锁定的即是`Class`，如果加在非静态代码块上锁定的是`this`
3. 锁升级（偏向锁，自旋锁，重量级锁）
> ***偏向锁***（无锁状态，只是在锁定对象上markword（`对象的64位地址的前两位用于标记锁类型`）进行标记，此时只有一个线程使用）
> ***自旋锁***（无锁状态，两个线程争抢一个锁，另外一个线程自旋等待，Hospot中默认自旋`10`次，锁升级为重量级锁）
> ***重量级锁***（向操作系统`OS`申请的锁,锁一旦升级将无法降级）

> 注意：**自旋锁-适用于执行时间较短且线程数较少的情况下，因为其会向jvm堆申请空间，如果执行时间长且线程特别多，容易造成jvm压力过大。反之执行时间长线程数多适合使用重量级锁**

### 2.3 synchronize 锁在如下情况时会怎么运行?
- 多个线程调用同一个对象中的synchronize方法和非synchronize方法
> synchronize方法不会阻止synchronize方法运行

- 多个线程调用同一个对象中的不同synchronize方法
- 多个线程调用同一个对象中的同一个synchronize方法
> synchronize会阻塞多个线程运行，此时锁生效

- 多个线程调用同一个对象中的同一个非synchronize方法
- 多个线程调用同一个对象中的不同非synchronize方法
- 多个线程调用同一个对象中的静态synchronize方法和非静态synchronize方法
*<font color='red'>静态方法锁定的是Class，非静态方法锁定的是this，属于不同的锁，所以不会产生锁争用</font>*
> 不会阻塞运行

### 2.4 锁优化
- 锁细化，将synchronize加到具体执行的代码段上，而不是加到方法上
> 如果一段程序中好多细化的锁，这是可以选择锁粗化，直接加到方法或者大代码段上
- 如果使用synchronize锁定对象时，应该使用`final`修饰的对象，防止对象在其他地方被更改导致锁失效
``` java
final Object object = new Object();
synchronize(object);
```

### 第三章 volatile
保证线程可见性，但是不能保证原子性
禁止指令重排序
- DCL（Double Check Lock）单例
> - 可见性使用了CPU的`MESI`缓冲一致性协议
> - 重排序（CPU层面为了提升指令的执行效率，编译器complir 会将java的代码最后执行的指令进行重新排序）底层使用读写屏障来实现防止重排序。

### 第四章 CAS （compare and swap 1.8版本，1.8之后改为了 compare and set）
无锁优化 （自旋锁 乐观锁）
> CAS的类都在`java.util.concurrent.atomic`包下，包括`AtomicInteger`等
CAS的操作过程为：每次在设置新的值之前都会获取一遍上一次的值，以及期望值，如果在设置新值之前上一次的值被改变则会重新获取一次

CAS可能存在ABA问题
如果是基本数据类型时，ABA问题可以忽略。如果是引用类型时，ABA问题可能引起程序运行错误的问题发生，解决的方案就是给引用对象增加version版本号，在CAS校验时除了校验引用，还需要校验版本号。
> CAS操作底层都是使用了`Unsafe`类的`compare and set`操作，`Unsafe`底层直接操作都是CPU的原语操作，使用读写屏障（防止指令重排序）保证了CAS的原子性问题