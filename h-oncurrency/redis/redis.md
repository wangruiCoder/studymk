# Redis 学习笔记
---
## 一 基础知识
- 磁盘：
    1. 寻址：ms级
    2. 带宽：G/M/s
- 内存：
    1. 寻址：ns
    2. 带宽：很大
- 索引与数据的关系：
![](1.png)

## 二 redis和memcache的区别
- redis提供了丰富的数据类型，同时也提供了数据类型对应的相关操作api
- redis是基于小量结果进行计算可以提升I/O
- memecache 把数据全部存在内存之中，断电后会挂掉，数据不能超过内存大小，但是redis可以实现磁盘持久化
- redis的使用场景会更多。

## 三 redis 与客户端与操作系统的关系
redis 与操作系统之间实现的是epoll模型，多路复用
![关系图](2.png)

## 四 epoll 
redis使用的是epoll 多路复用来实现的高吞吐量。
epoll与select的区别就是epoll有一个共享空间，但是select则是每次遍历用户态和内核态查找select绑定了谁。

## 五 redis基础知识
- redis是二进制安全的，汉字都转化为了2进制，一个汉字占用3字节
- redis单线程单进程（使用的是epoll多路复用），因为redis的数据如果全存放在内存中的话，内存的读取效率一般延迟都是ns级别，如果是多线程的话会牵扯到上下文切换，从而影响了读写效率。
- 目前redis单机可支持秒级 10万+请求，官方给出的数据是1.5M次 15万次
### 5.1 redis默认库
- redis默认提供了16个库，从0-15，每个库与每个库之间的数据是隔离的

### 5.2 常用命令
- select dbno 选择数据库
- flushall 删除整库（线上切勿使用）


### 5.2 String 常用命令
- set key 1232 nx (nx如果存在的则不设置，可以用于分布式锁)
- set key 1232 xx (xx 如果不存在则不设置，存在再设置)
- mset 设置多个key和value
- mget 获取多个key的value
- strlen 获取字符串长度
- append 从左侧拼接
- SETRANGE 设置从左侧开始的第几位开始替换字符（setrange key 4 "hello redis"）
- type 查看数据类型
- incr 自增
- decr 自减
- incrby 增加指定值
- decrby 减少指定值
### 5.3 bitmap
位数据结构和命令操作
![](3.png)
位操作相对于数据库来说极大的减少了数据存储空间，同时位操作的计算速度也很快
- setbit key offer value 设置key位置和值
- bitcount key start end 统计从起始位置到结束位置的bit的数量，统计数量的原理是bitmap链上对应的位值为1的。
- bitcount key -2 -1 从末尾统计倒数第1 和第2个数据


> 同一个用户365内，多少天登录过。
setbit sean 1 1 
setbit sean 2 1
setbit sean 4 1
bitcount sean 0 -1 (0头 -1尾)
![](4.png)

> 一段时间的活跃用户统计
setbit 20200701 1 1
setbit 20200701 2 1
setbit 20200702 1 1
bittop or resultkey 20200701 20200702
bitcount resultkey 0 -1 (0头 -1尾)
![](5.png)


## 冷知识
- 只有windows才会有AIO，linux没有。
- 数据库引擎统计列表网站
https://db-engines.com/en

- linux查看帮助手册命令
man 命令