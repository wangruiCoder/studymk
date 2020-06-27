# Kafka 概念
***

## 第一章理论概念详解

### 1.1 事务
- producer事务
> 需要引入一个全局唯一的TransactionID，并将Producer获得的PID和TransactionID绑定，这样当Producer重启后就可以通过正在进行的TransactionID获取原来的PID。
为了管理Transaction，kafka引入了一个新的组件Transaction Coordinator。Producer就是通过Transaction Coordinator交互获得TransactionID对应的任务状态。Transaction Coordinator还负责将事务写入Kafka的一个内部Topic(_topic_)，这样即使整个服务重启，由于事务状态得到保存，进行中的事务状态可以得到恢复，从而继续进行。

>> 如果会话ID Pid发生了变化事务就需要重新进行，原来的将不可用

### 1.2 ISR
in-sync replicasct (ISR)同步副本，意思是和leader保持同步的follower集合

### 1.3 分区同步策略

### 1.4 日志（数据）文件

### 1.5 高效读写
- 顺序写磁盘
> 顺序写能到 600M/s 一直追加到文件末端
- 零拷贝（zero-copy）




## 第二章 具体使用

### 2.1 生产者

### 2.2 消费者
- 分配策略
> RoundRobin （轮训，按照消费者组划分）

> Range (按照主题划分，默认规则)

> 消费者数量发生变化时，会触发分配策略

- 消费者与partions的关系
> 消费者数量 <= partions 的数量，保证没有消费者处于闲置状态

### 2.3 消费者组

### 2.3 过滤器

### 2.4 

### 2.5




## 第三章 使用场景

### 3.1 常用命令
> 启动命令：`./kafka-server-start.sh -daemon ../config/server.properties`

### 3.2 场景验证
#### 1、 分布式部署时同属于一个consumer group 的消费者会重复消费吗？
> 不会重复消费，同属于一个consumer group的消费者不会重复消费消息
#### 2、分布式部署时不属于一个consumer group 的消费者订阅同一个topic时会重复消费吗？
> 会重复消费，两个组的消费者会互补干扰各自消费


## 第四章 spring boot 中操作kafka
### 4.1 kafkaTemplate 生产真


### 4.2 KafkaListener 消费
- 手动提交offset
application.yml 配置文件增加
`spring.kafka.consumer.enable-auto-commit: false`
`spring.kafka.listener.ack-mode: manual`

``` java
    //核心代码
    @KafkaListener(topics = "stu_kafka")
    public void printMessage(ConsumerRecord<Integer,String> consumerRecord, Acknowledgment ack){
        System.out.println(consumerRecord.value()+"--"+consumerRecord.offset()+"--"+consumerRecord.partition());
        //手动提交
        ack.acknowledge();
    }
```

> <b>RECORD</b> -- 每处理一条commit一次
<b>BATCH(默认)</b> -- 每次poll的时候批量提交一次，频率取决于每次poll的调用频率
<b>TIME</b> -- 每次间隔ackTime的时间去commit
<b>COUNT</b> -- 累积达到ackCount次的ack去commit
<b>COUNT_TIME</b> -- ackTime或ackCount哪个条件先满足，就commit
<b>MANUAL</b> -- Listener负责ack，但是背后也是批量上去
<b>MANUAL_IMMEDIATE</b> -- Listener负责ack，每调用一次，就立即commit

<b>除开MANUAL和MANUAL_IMMEDIATE，其他模式都是由spring根据约定的条件控制提交，我们在代码中调用consumer.commitAsync()是不起作用的。</b>

