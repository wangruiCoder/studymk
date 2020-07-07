# 线程池学习笔记
---
## 第一章线程池类关系
Executor->ExecutorService->AbstractExecutorService->ThreadPoolExecutor

ExecutorService 继承了Executor
AbstractExecutorService 实现了 ExecutorService
ThreadPoolExecutor 继承了AbstractExecutorService

## 第二章线程池相关类

### 2.1 Callable
`Callable`是一个可以带返回结果的线程类
与Runable比，Callable带有返回值。并且支持泛型。call方法还会抛出异常

### 2.2 FutureTask
获取未来任务的返回值，需要跟Callable配合使用
> FutureTask实现了RunnableFuture接口，RunnableFuture继承了Runnable, Future

### 2.3 CompletableFuture
管理多个线程的返回值
``` java
public class T3_ComplateFuture {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        //自定义实体类
        TestEntity testEntity = new TestEntity();
        CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> get1());
        CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> get2());

        future1.thenAccept(testEntity :: setName);
        future2.thenAccept(testEntity :: setAge);
        //allof 方法调用时不可以带泛型
        //join
        CompletableFuture.allOf(future1,future2).join();

        System.out.println(testEntity.toString());
    }
    private static String get1(){
        return "1";
    }
    private static String get2(){
        return "2";
    }

}
class TestEntity {
    String name ;
    String age;

    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public String getAge() {
        return age;
    }
    public void setAge(String age) {
        this.age = age;
    }
    @Override
    public String toString() {
        return "TestEntity{" +
                "name='" + name + '\'' +
                ", age='" + age + '\'' +
                '}';
    }
}
```

### 2.4 ThreadPoolExecutor
线程池，线程池中维护了两个队列，一个是等待任务队列，一个是任务执行队列

#### 1 核心线程数
`corePoolSize`线程池中同时工作的线程数

#### 2 最大核心线程数
`maximumPoolSize`队列满时可以支持最大的核心线程数

#### 3 空闲时间
`keepAliveTime` 线程池中空闲线程的存活时间

#### 4 空闲时间单位
`TimeUnit` 存活时间单位

#### 5 阻塞队列
BlockingQueue

> 使用`LinkedBlockingQueue `时`maximumPoolSize`不生效

#### 6 线程工厂
ThreadFactory
- 默认Executors.defaultThreadFactory()
- 自定义需要实现ThreadFactory接口

#### 7 拒绝策略
RejectedExecutionHandler

- ThreadPoolExecutor.AbortPolicy()
> 中止策略，并且抛出异常
- ThreadPoolExecutor.CallerRunsPolicy()
> 调用者运行策略，如果队列满了，无法加入的线程归调用者线程执行，例如main方法
- ThreadPoolExecutor.DiscardOldestPolicy()
> 丢弃掉老的任务
- ThreadPoolExecutor.DiscardPolicy()
> 直接丢弃不抛出异常
- 自定义拒绝策略，一般情况下会选择自定义拒绝策略

### 2.5 SingleThreadExecutor 单线程线程池 （属于ThreadPoolExecutor的快捷方式）
只有一个线程运行的线程池
- corePoolSize = 1
- maximumPoolSize = 1
- keepAliveTime = 0L 永不过期
- BlockingQueue = LinkedBlockingQueue 最大支持Integer的最大值
- 拒绝策略 AbortPolicy 拒绝并抛出异常
``` java
//源码片段
public static ExecutorService newSingleThreadExecutor() {
    return new FinalizableDelegatedExecutorService
    //注意下面的参数，使用的默认的线程工厂和拒绝策略
        (new ThreadPoolExecutor(1, 1,
            0L, TimeUnit.MILLISECONDS,
            new LinkedBlockingQueue<Runnable>()));
    }
```
> 用途：某一个异步任务执行时间特别长，但是执行过程中又不能被其他线程同时执行的任务。

### 2.6 CachedThreadPool 缓存线程池
- corePoolSize = 0
- maximumPoolSize = int最大值
- keepAliveTime = 60秒
- BlockingQueue = SynchronousQueue 同步队列
- 拒绝策略 AbortPolicy 拒绝并抛出异常
```java
//源码片段
public static ExecutorService newCachedThreadPool() {
    // 核心线程数为0 ，证明任务来到就会被立即执行
    return new ThreadPoolExecutor(0, Integer.MAX_VALUE,
            60L, TimeUnit.SECONDS,
            new SynchronousQueue<Runnable>());
```
> 用途：适用于短而快的频繁任务，这个线程池接到任务就会立即执行。

### 2.7 FixedThreadPool 固定大小线程池
- corePoolSize = 设置的固定值
- maximumPoolSize = corePoolSize
- keepAliveTime = 0L 永不过期
- BlockingQueue = LinkedBlockingQueue 最大支持Integer的最大值
- 拒绝策略 AbortPolicy 拒绝并抛出异常
``` java
//源码片段
public static ExecutorService newFixedThreadPool(int nThreads) {
    //固定大小体现在 corePoolSize = maximumPoolSize，并且核心线程永不过期
    return new ThreadPoolExecutor(nThreads, nThreads,
                0L, TimeUnit.MILLISECONDS,
                new LinkedBlockingQueue<Runnable>());
```
> 用途：适用于当前线程数能稳定的保证任务执行，不会有什么流量高峰的这种情况，整体趋势偏向于平稳。
### 2.8 ScheduledThreadPool 定时任务线程池
- corePoolSize = 设置的固定值
- maximumPoolSize = int最大值
- keepAliveTime = 0L 永不过期
- BlockingQueue = DelayedWorkQueue 可以按照时间顺序排序的队列
- 拒绝策略 AbortPolicy 拒绝并抛出异常
``` java
//源码片段
public ScheduledThreadPoolExecutor(int corePoolSize) {
    super(corePoolSize, Integer.MAX_VALUE, 0, NANOSECONDS,
            new DelayedWorkQueue());
}
```
> 用途：适用于定时任务。
一般情况下复制定时任务会选择使用：quartz和cron

### 2.2 ForkJoinPool
- 分解汇总的任务
- CPU密集型
- 用很少的线程可以执行很多的任务(子任务)，ThreadPoolExecutor无法做到