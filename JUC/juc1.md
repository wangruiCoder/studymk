# Java 多线程高并发编程笔记
---
作者:kyrie。***学习记录，如有转发请注明地址。***

## 第一章 线程与进程
### 1.1 什么是进程
进程是应用程序的执行实例，例如QQ.exe等

### 1.2 什么是线程
线程是程序运行的最小单元，一个进程的所有任务都在线程中执行

### 1.3 线程的几种状态
- New 新建 `new Thread()`
- Runable 就绪状态 `调用start()后`
- Running 运行状态 `获得了CPU的时间片，并运行run()方法中的程序段`
- Block 阻塞状态 
> sleep 和 yield都可以打断程序执行
> sleep 程序休眠一段时间
> yield 程序退出一下到就绪状态 - (一般不用)
> join 只能在自己的方法里面调用别人，不可以自己调用自己，join的意思是阻塞自己让另外一个线程执行完成自己再开始执行
> notifyAll()
- destory 销毁状态 `线程正常执行完毕或者被打断后手动终止`
> stop方法(不建议使用，已经被废弃，stop的调用会引起程序运行状态的不一致)
 
> ***getState 可以清楚的看到线程的状态情况***

### 1.4 多线程
- 优点
> 能适当提高程序的执行效率
> 能适当提高资源的利用率（CPU，内存）

- 缺点
> 开启线程需要占用一定的内存空间（默认情况下，每一个线程都占 512 KB）
> 如果开启大量的线程，会占用大量的内存空间，降低程序的性能
> 线程越多，CPU 在调用线程上的开销就越大
> 程序设计更加复杂，比如线程间的通信、多线程的数据共享
 
## 第二章 synchronize
可重入锁，重量级锁，保证了原子性，可见性，但是不能保证指令会重排序
可重入体现在如下几个方面
- 同一个对象的 synchronize 方法可以调用 synchronize 方法
- 执行过程异常时，会自动中断释放锁

>最初jdk设计时默认直接就是重量级锁，后来经过改造synchronize增加了锁升级的过程（无锁，偏向锁，自旋锁，重量级锁）
### 2.1 synchronize（object）
> <font color="red">不能锁定String常量、Integer、Long及一些基本数据类型</font>
### 2.2 线程同步
1. 锁的是一个对象而不是一串代码段
2. 如果synchronize加在静态方法上锁定的即是`Class`，如果加在非静态代码块上锁定的是`this`
3. 锁升级（无锁，偏向锁，自旋锁，重量级锁）
> ***偏向锁***（无锁状态，只是在锁定对象上markword（`对象的64位地址的前两位用于标记锁类型`）进行标记，此时只有一个线程使用）
> ***自旋锁***（无锁状态，两个线程争抢一个锁，另外一个线程自旋等待，Hospot中默认自旋`10`次，锁升级为重量级锁）
> ***重量级锁***（向操作系统`OS`申请的锁,锁一旦升级将无法降级）

> 注意：**自旋锁-适用于执行时间较短且线程数较少的情况下，因为其会向jvm堆申请空间，如果执行时间长且线程特别多，容易造成jvm压力过大。反之执行时间长线程数多适合使用重量级锁**

### 2.3 synchronize 锁在如下情况时会怎么运行?
- 多个线程调用同一个对象中的synchronize方法和非synchronize方法
> 静态synchronize方法不会阻止非静态synchronize方法运行

- 多个线程调用同一个对象中的不同synchronize方法（都是静态或者非静态）
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
> 实现方式
> - 可见性使用了CPU的`MESI`缓存一致性协议
> - 重排序（CPU层面为了提升指令的执行效率，编译器complir 会将java的代码最后执行的指令进行重新排序）底层使用读写屏障来实现防止重排序，4种屏障，读写，写写，读读，写读。

### 第四章 CAS （compare and swap 1.8版本，1.8之后改为了 compare and set）
无锁优化 （自旋锁 乐观锁）
> CAS的原子类都在`java.util.concurrent.atomic`包下，包括`AtomicInteger`等
CAS的操作过程为：每次在设置新的值之前都会获取一遍上一次的值，以及期望值，如果在设置新值之前上一次的值被改变则会重新获取一次

CAS可能存在ABA问题
如果是基本数据类型时，ABA问题可以忽略。如果是引用类型时，ABA问题可能引起程序运行错误的问题发生，解决的方案就是给引用对象增加version版本号，在CAS校验时除了校验引用，还需要校验版本号。
> CAS操作底层都是使用了`Unsafe`类的`compare and set`操作，`Unsafe`底层直接操作都是CPU的原语操作，使用读写屏障（防止指令重排序）保证了CAS的原子性问题

#### 4.1 性能比较
在高并发情况下，使用synchronize、atomic、longAdder时，性能差距越来越明显
``` text
1000并发，每个线程进行10000次累加的结果：
sync count: 10000000--time: 512
atomic count: 10000000--time: 163
LongAdder count: 10000000--time: 73
```
> - synchronize 在高并发情况下，由于锁资源争抢较多，所以很快升级为重量级锁(OS 操作系统锁)
> - atomic 类采用CAS操作，不会向系统申请锁，都是自旋等待。
> - LongAdder 采用CAS操作，但是其底层采用 ***分段锁***，所以性能会更好
> 不能一概而论sync性能就最差，性能问题应该结合实际的业务执行情况，或者压测结果来定论。现在版本的jdk对sync的优化已经性能很高了

### 第五章 ReentrantLock
可重入锁，独占锁。他具备跟synch一样的功能，但是释放锁需要手动释放，比synchronize更加灵活。
> 默认情况下`ReentrantLock`是一个非公平锁，
``` java
//非公平锁
ReentrantLock lock = new ReentrantLock();
//公平锁
ReentrantLock lock = new ReentrantLock(true);
```
#### 5.1 使用注意
使用try catch 包裹，finally 中释放锁,防止使用过程中导致的锁不释放的死锁情况发生。如下
``` java
    try {
        //获得锁
        lock.lock();
    } finally {
        //释放锁
        lock.unlock();
    }
```

#### 5.2 特性
- ReentrantLock 也是互斥锁，如果为同一把锁，多个线程会等待前面线程释放锁后执行
- 有同一把ReentrantLock锁的两个方法嵌套调用时锁可重入锁，例如A=>B
- ReentrantLock tryLock(1000) 试着获取锁，如果获取不到执行下面方法，这个是synchronize没有的
``` java
//试着获取锁获取规定时间内获取锁
if (lock.tryLock() || lock.tryLock(10, TimeUnit.SECONDS){
```

### 第六章 CountDownLatch 递减计数器
递减计数器。一般用于多个任务共同执行完毕后再执行其他任务时使用。
> countDownLatch.await();是阻塞运行，需要等countDownLatch的值为0后才可以执行下面的程序

### 第七章 CyclicBarrier 循环栅栏
CyclicBarrier 循环栅栏 设定一个数量范围，当线程数未达到数量时，所有线程都在等待，当达到数量时统一放行
例如好多朋友去约饭，餐厅要求人员全部到期了才可以进去占座吃饭
> 实际场景：一个操作可能需要同时操作数据库，操作文件，操作redis，但是之间又不互相依赖时，可以使用CyclicBarrier

### 第八章 Phaser 阶段执行
协调多个执行阶段，为每个程序阶段重用Phaser实例。每个阶段可以有不同数量的线程等待前进到另一个阶段

### 第九章 ReadWriteLock 读写锁
读-共享锁
写-排他锁
> 适用于少量线程写入，多个线程读取的场景。因为读锁共享，所以读取效率特别快，但是读必须加锁，防止脏读。

### 第十章 Semaphore 信号量
Semaphore用于限制可以访问某些资源（物理或逻辑的）的线程数目，他维护了一个许可证集合，有多少资源需要限制就维护多少许可证集合
``` java
    /*
        * 设置信号量为1 ，则表示只有一个线程可以运行，设置为2表示可以有两个同时运行
        */
    Semaphore semaphore = new Semaphore(1);
    new Thread(() -> {
        try {
            //获取信号量 信号量值减1
            semaphore.acquire();
            System.out.println("t1 run");
            TimeUnit.SECONDS.sleep(1);
            System.out.println("t1 run2");
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            //释放信号量 信号量值加1，一定要在finally中关闭，类似于lock的unlock
            semaphore.release();
        }

    }).start();
```
> 用于买票或者同一个资源的访问数限制

### 第十一章 Exchanger 交换器
只用于两个工作线程之间交换数据，如果有一个线程没有进行数据交换则另外一个线程一直阻塞。
使用场景：例如游戏中两个人交换装备
``` java
new Thread(()->{
    String s = "T2";
    try {
        //交换数据到另外一个线程
        s = exchanger.exchange(s);
        System.out.println(Thread.currentThread().getName()+"--"+s);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
},"thread2").start();
```

### 第十二章 LockSupport
阻塞和唤醒线程使用，类似于wait和notify
 * （1）wait和notify都是Object中的方法,在调用这两个方法前必须先获得锁对象，但是park不需要获取某个对象的锁就可以锁住线程。
 * （2）notify只能随机选择一个线程唤醒，无法唤醒指定的线程，unpark却可以唤醒一个指定的线程。
 > 底层是使用Unsafe类实现的，跟CAS使用的是同一个类。
``` java
//示例
Thread t = new Thread(() -> {
    for (int i = 0; i < 10; i++) {
        System.out.println("TT"+i);
        if (i==5){
            //锁定
            LockSupport.park();
        }
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
});
t.start();
//解锁
LockSupport.unpark(t);
```

### 第十三章 AQS (AbstractQueuedSynchronizer)
`AbstractQueuedSynchronizer`是所有的java的锁的父类，其底层实现是基于CAS+volatile实现的，volatile体现在类的属性都是volatile修饰的，cas体现在获取锁和加入锁队列（双向链表CLH）都是基于cas的方式实现的。

锁等待队列锁定时只锁定最后一个节点，然后使用CAS操作来判断是否可以给最后一个节点增加尾节点。因为是个最后一个节点增加锁，所以效率比较高，一般情况下我们自己写代码都是会选择会给整个链表加锁

`AbstractQueuedSynchronizer`的核心是维护了一个原子的`state`和Node队列(双向链表)，其通过不同锁的实现的一个state值来控制锁的状态。`AbstractQueuedSynchronizer`他底层使用到了`模板方法设计模式`。所有子类都继承其实现自己的锁状态

#### 13.1 关于AQS的面试题
1. synchronize和ReentrantLock实现了AQS中的那些方法
> 需要看源码解释
> - tryAcquire 方法、unlock方法

### 第十四章 ThreadLocal 
是一个线程内部的存储类，可以在指定线程内存储数据，数据存储以后，只有指定线程可以得到存储数据。
实际上是ThreadLocal的静态内部类ThreadLocalMap为每个Thread都维护了一个数组table

``` java
ThreadLocal threadLocal = new ThreadLocal();
threadLocal.set(111);
//用完必须remove，防止内存泄漏
threadLocal.remove();
```

#### 14.1 使用场景
- 在spring的声明式事务中就会使用到ThreadLocal，例如同一个service方法中需要对数据库有N次操作，当第一次操作获取到数据库连接后会放入到ThreadLocal中，其他的几个操作会从ThreadLocal中直接获取数据库连接，保证是同一个连接支持数据库事务。

### 第十五 java的引用
四种引用类型
1. 强
`Object object = new Object()`
2. 软 `SoftReference`
当内存不够用时会将软引用GC掉，可以用于内存缓存。
3. 弱 `WeakReference`
只要遭到gc就会被回收,一般用于容器。
目前ThreadLocal中就有使用(可翻阅源码查看其ThreadLocal.Map底层继承了WeakReference)
4. 虚 
用于管理堆外内存的，例如netty中的DirectByteBuffer

### 面试题
