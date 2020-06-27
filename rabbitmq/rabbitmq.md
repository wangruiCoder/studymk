# Rabbitmq 概念
***
## 第一章 什么是rabbitmq，可以干什么。
RabbitMQ 即一个消息队列，主要是用来实现应用程序的异步和解耦，同时也能起到消息缓冲，消息分发的作用。

RabbitMQ是实现AMQP（高级消息队列协议）的消息中间件的一种，最初起源于金融系统，用于在分布式系统中存储转发消息，在易用性、扩展性、高可用性等方面表现不俗。RabbitMQ主要是为了实现系统之间的双向解耦而实现的。当生产者大量产生数据时，消费者无法快速消费，那么需要一个中间层。保存这个数据。

AMQP，即Advanced Message Queuing Protocol，高级消息队列协议，是应用层协议的一个开放标准，为面向消息的中间件设计。消息中间件主要用于组件之间的解耦，消息的发送者无需知道消息使用者的存在，反之亦然。AMQP的主要特征是面向消息、队列、路由（包括点对点和发布/订阅）、可靠性、安全。

RabbitMQ是一个开源的AMQP实现，服务器端用Erlang语言编写，支持多种客户端，如：Python、Ruby、.NET、Java、JMS、C、PHP、ActionScript、XMPP、STOMP等，支持AJAX。用于在分布式系统中存储转发消息，在易用性、扩展性、高可用性等方面表现不俗。


[***rabbitmq官网***](http://www.rabbitmq.com/ "点击前往")
***
### 1.1 rabbitmq 概念详解

通常我们谈到队列服务, 会有三个概念： 发消息者、队列、收消息者，RabbitMQ 在这个基本概念之上, 多做了一层抽象, 在发消息者和 队列之间, 加入了交换器 (`Exchange`). 这样发消息者和队列就没有直接联系, 转而变成发消息者把消息给交换器, 交换器根据调度策略再把消息再给队列。

![图例1](20171101095315707.png '关系图')

- 左侧 P 代表 生产者，也就是往 RabbitMQ 发消息的程序。
- 中间即是 RabbitMQ，其中包括了 交换机 和 队列。
- 右侧 C 代表 消费者，也就是往 RabbitMQ 拿消息的程序。

![服务图2](2.jpg '内部服务图')

其中比较重要的概念有 6 个，分别为：信道，虚拟主机，交换机，队列，和绑定，路由键。

+ 信道（`Channel`）
>消息推送使用的通道
+ 虚拟主机（`virtual host`）
>一个虚拟主机持有一组交换机、队列和绑定。为什么需要多个虚拟主机呢？很简单，RabbitMQ当中，用户只能在虚拟主机的粒度进行权限控制。 因此，如果需要禁止A组访问B组的交换机/队列/绑定，必须为A和B分别创建一个虚拟主机。每一个RabbitMQ服务器都有一个默认的虚拟主机“/”。
+ 交换机（`Exchange`）
>Exchange 用于转发、分配消息，但是它不会做存储 ，如果没有 Queue bind 到 Exchange 的话，它会直接丢弃掉 Producer 发送过来的消息。这里有一个比较重要的概念：***路由键(`RoutingKey`)*** 。消息到交换机的时候，交互机会转发到对应的队列中，那么究竟转发到哪个队列，就要根据该路由键。
+ 队列（`Queue`）
>队列常用于存储消息，是由交换机存入的信息。
+ 绑定（`Bind`）
>交换机需要和队列相绑定，用于把交换机的消息绑定到队列上。
+ 路由键（`RoutingKey`）
>用于把交换器的消息绑定到队列上。

### 1.2 `Exchange`4种类型
最新版本的RabbitMQ有四种交换机类型，分别是Direct exchange、Fanout exchange、Topic exchange、Headers exchange。

+ Direct Exchange
>将消息中的Routing key与该Exchange关联的所有Binding中的Routing key进行比较，如果相等，则发送到该Binding对应的Queue中。

+ Topic Exchange
>将消息中的Routing key与该Exchange关联的所有Binding中的Routing key进行对比，如果匹配上了，则发送到该Binding对应的Queue中。`匹配规则：* 匹配一个单词，# 匹配0个或多个字符。*，# 只能写在.号左右，且不能挨着字符，单词和单词之间需要用.隔开。`

+ Fanout Exchange
>直接将消息转发到所有binding的对应queue中，这种exchange在路由转发的时候，忽略Routing key，类似于广播的形式。

+ Headers Exchanges
>将消息中的headers与该Exchange相关联的所有Binging中的参数进行匹配，如果匹配上了，则发送到该Binding对应的Queue中。

## 第二章 rabbitmq 使用的基本知识
了解rabbitmq安装完后默认设置以及基本用法
### 1.1 默认连接端口
> + 默认的单机连接端口为：5672
> + 默认的控制台端口为：15672 （访问地址：localhost:15672）
> + 默认的集群连接端口为：25672
### 1.2 配置用户及其权限
> `rabbitmqctl add_user admin 123456`
> `rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"`
> `rabbitmqctl set_user_tags admin administrator`
### 1.3 常用命令
> 启动服务：`rabbitmq-server -detached`
> 查看状态：`rabbitmqctl status`
> 关闭服务：`rabbitmqctl stop`
> 列出角色：`rabbitmqctl list_users`
> 启动web ui界面：`rabbitmq-plugins enable rabbitmq_management`
> 查看启动的插件列表：`rabbitmq-plugins list`  //[E*显示启动]   [e*隐式启动]



## 第三章 验证过程

### 1.1 使用rabbitmq传输对象注意要点
>1. 传输的对象必须序列化`public class UserBo implements Serializable`
>2. 消费者在接受对象时客户端的对象的包路径必须跟消费端的对象的包路径保持一致,不然会报序列化异常
>3. 可能在实际应用中传输的对象无法保证包名路径都一致，建议在传输过程中使用`Json`工具类将生产者传输的对象转为json，然后消费者接受到Json后进行反序列化。

### 1.2 队列配置要点
客户端在配置队列时需要注意
