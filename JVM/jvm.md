# JVM 学习笔记
---
## 第一章 JVM 基础概念
### 1.1 Java 从编码到执行的过程
![执行过程](1593848011(1).png)

### 1.2 JVM
- Jvm是一种规范，是虚构出来的一台计算机。
- 从跨平台的语言到跨语言的平台
> scala 等语言都会编译成class文件运行在jvm之上
- jvm跟java无关，jvm只与class文件格式有关

### 1.3 Jvm 的实现
- Hotspot
- Jrockit
- J9-IBM
- Microsoft VM
- TaobaoVM
> Hotspot的深度定制版
- LiquidVM
- azul zing
> 最新垃圾回收的业界标杆，速度快，特别是垃圾回收

### 1.4 JVM JRE JDK 关系
![](1593848842(1).png)

## 第二章 Class File Format
使用Idea的 jClasslib 对照查看一个class file 结构理解

jvm总共有256条指令，其中只有8条指令是原子性的

## 第三章 Class Loading Linking Initializing （类加载和初始化）
jvm默认是懒加载，当需要使用的时候再去加载。
### 3.1 加载过程

- Loading
- Linking
    1. Verfication
    2. Preparation
    3. resolution
    > 静态变量初始化
- initializing
### 3.2 加载层次
自上而下进行实际查找和加载
自底向上检查该类是否已经加载parent方向
***4种类加载器及其负责的加载范围：***
1. Bootstrap
> 加载lib/rt.jar charset.jar等核心类
2. Extension
> 加载扩展jar包，jre/lib/ext/*.jar，或者由-Djava.ext.dirs指定扩展包路径
3. App
> 加载classpath指定的内容，也就是平时开发自己写的类由App加载
4. Custom ClassLoader
> 自定义类加载器

类加载过程
![](1593855960(1).png)
### 3.3 双亲委派
Jvm是按需动态加载采用双亲委派机制
先是从底向上Custom->App->Extension->Bootstrap检查一遍，再是从顶向下委派加载一遍Bootstrap->Extension->App->Custom
``` java
//源码体现
protected Class<?> loadClass(String name, boolean resolve)
    throws ClassNotFoundException {
    synchronized (getClassLoadingLock(name)) {
        // First, check if the class has already been loaded
        //第一步检查当前类加载器中是否已经加载过，如果没有去父类加载器里面找，这里直接体现了自底向上查找
        Class<?> c = findLoadedClass(name);
        if (c == null) {
            long t0 = System.nanoTime();
            try {
                if (parent != null) {
                    //去父类加载器里面找，注意loadClass，类似于递归查询
                    c = parent.loadClass(name, false);
                } else {
                    //父类加载器中没有找到就去Bootstrap里面找，如果经历了这么一圈后还没有找到开始走下面的c== null
                    c = findBootstrapClassOrNull(name);
                }
            } catch (ClassNotFoundException e) {
                // ClassNotFoundException thrown if class not found
                // from the non-null parent class loader
            }

            if (c == null) {
                // If still not found, then invoke findClass in order
                // to find the class.
                //委派加载开始，判定当前类归谁加载
                long t1 = System.nanoTime();
                //findClass体现了 *** 模板设计模式 ***，他的最原始方法直接回抛出异常，需要子类加载器实现后调用子类的具体实现
                c = findClass(name);

                // this is the defining class loader; record the stats
                sun.misc.PerfCounter.getParentDelegationTime().addTime(t1 - t0);
                sun.misc.PerfCounter.getFindClassTime().addElapsedTimeFrom(t1);
                sun.misc.PerfCounter.getFindClasses().increment();
            }
        }
        if (resolve) {
            resolveClass(c);
        }
        return c;
    }
}

```
为什么要使用双亲委派？
- 主要是类加载安全问题
- 次要是资源问题

### 3.4 混合模式
- 解释器
- JIT （Just-In-Time compiler）
- 混合模式
    1. 混合使用解释器+热点代码编译
    2. 热点代码检测
        - 多次被调用的方法（方法计数器）
        - 多次被调用的循环（循环计数器）
> -XX:compileThreshold=10000  默认的检查热点代码的循环次数
> Xmixed 默认是混合模式，开始解释执行，启动速度较快，对热点代码实行检测和编译
> -Xint 使用解释模式，启动很快执行稍慢
> -Xcomp 使用纯编译模式，执行很快，启动很慢。

### 3.5 Linking 类加载的第一个阶段，静态成员变量的加载过程
#### 3.5.1 Verfication
验证文件是否符合JVM规定
#### 3.5.2 Preparation
静态成员变量赋默认值
#### 3.5.3 resolution
将类、方法、属性等符合引用解析为直接引用。常量池中的各种符号引用解析为指针，偏移量等内存地址的直接引用


### 3.6 initializing 初始化
调用类初始化代码，例如构造函数等，给静态成员变量赋初始值

## 第四章 JMM java memory moudle （java的内存模型）
### 4.1 硬件数据一致性
- MESI intel的缓冲一致性协议

### 4.2 缓存行（面试会被问到）
读取内存中缓存的时候以cache line为基准向更高级的缓存块中读取，这么做主要是用于提升效率，目前line为 长度为64位。
大概的读取顺序是:
CPU寄存器->CPU L1缓存->CPU L2缓存->CPU L3缓存->机器内存->本地磁盘->远程磁盘。
> 从左向右读取的速度越来越低。并且缓存的空间也会越来越大，因为CPU中本身的寄存器中位置很有限只有4位。

#### 4.2.1 伪共享
位于同一缓存行的两个不同数据，被两个不同的CPU锁定，产生互相影响的伪共享问题。
> 解决伪共享问题：使用缓存行对齐能够提高效率。
```java
// Disruptor 的RingBuffer 源码，为了解决INITIAL_CURSOR_VALUE的缓存行问题，直接定义了7个long。
//人为的组成一个64位空间的缓存行，这样就可以保证同一缓存行中无其他字节数据。这么做虽然加快了速度，但是却多使用了一些内存空间。
public final class RingBuffer<E> extends RingBufferFields<E> implements Cursored, EventSequencer<E>, EventSink<E> {
    public static final long INITIAL_CURSOR_VALUE = -1L;
    protected long p1;
    protected long p2;
    protected long p3;
    protected long p4;
    protected long p5;
    protected long p6;
    protected long p7;
```
### 4.3 乱序问题
是因为CPU层面会指令重排序，所以会出现乱序问题，在java中为了解决乱序问题需要使用volatile（底层是通过Unsafe类实现，Unsafe类的底层是基于CPU的内存屏障来实现）。



