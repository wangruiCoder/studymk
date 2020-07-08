# Redis 学习笔记
---
## 基础知识
- 磁盘：
    1. 寻址：ms级
    2. 带宽：G/M/s
- 内存：
    1. 寻址：ns
    2. 带宽：很大
- 索引与数据的关系：
![](1.png)

## redis和memcache的区别
- redis提供了丰富的数据类型，同时也提供了数据类型对应的相关操作api
- redis是基于小量结果进行计算可以提升I/O
- memecache 把数据全部存在内存之中，断电后会挂掉，数据不能超过内存大小，但是redis可以实现磁盘持久化
- redis的使用场景会更多。

## redis 与客户端与操作系统的关系
redis 与操作系统之间实现的是epoll模型，多路复用
![关系图](2.png)




## 冷知识
- 只有windows才会有AIO，linux没有。
- 数据库引擎统计列表网站
https://db-engines.com/en

- linux查看帮助手册命令
man 命令