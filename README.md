# 米游社每日任务工具
 **参照了 [@inky-s](https://github.com/inky-s) 的代码。** 

 **https://github.com/inky-s/myb_workflow** 

- 支持多用户批量操作
- 操作随机冷却时间
- 若操作失败，会自动重试一次
- 从配置文件中读取用户Cookies和程序设置
- 操作结果会写入日志文件
- 可以完成每日获取米游币和不同版区的经验任务

 **以下是使用方法：** 
1. 先设置好配置文件`config.ini`，包含：

    `uid`（米哈游通行证ID，与Cookies所需`stuid`是一样的）

    `stoken`（抓包获取，这个值似乎是不会变更的，不同设备上同一账号都一样）
    
    `module_id`(游戏板块ID，具体看`config.ini`里的注释）
    
    `t1` `t2`（操作冷却时间，具体看`config.ini`里的注释）

    `timeout`（服务器连接超时时间）

2. 运行`main.py`或运行[编译好的程序](https://github.com/FailDragon-Plus/auto_mys/releases)。

3. 可前往`./logs/mhytool.log`查看日志。



- Python新手，代码可能有点繁琐有点问题，这个东西主要还是写出来自用的。😂


 **效果演示：**
 ```
2021-10-09 20:57:32  INFO  程序启动。  
2021-10-09 20:57:32  INFO  用户 uid_1 - 279155555：开始任务。  
2021-10-09 20:57:33  INFO  原神 - 签到成功，获得 30 积分。  
2021-10-09 20:57:37  INFO  原神 - 帖子 10674490 —— 阅读成功。  
...  
2021-10-09 20:57:51  INFO  原神 - 帖子 10674490 —— 点赞成功。  
...  
2021-10-09 20:58:02  INFO  原神 - 帖子 10674224 —— 已经点赞过了。  
...  
2021-10-09 20:58:03  INFO  原神 - 帖子 10672953 —— 点赞成功。  
...  
2021-10-09 20:58:18  INFO  原神 - 帖子 10671976 —— 转发成功。  
2021-10-09 20:58:18  INFO  帖子相关操作结束。  
2021-10-09 20:58:18  INFO  用户 uid_1 - 279155555：任务结束。  
2021-10-09 20:58:20  INFO  用户 uid_2 - 248466666：开始任务。  
...
2021-10-09 20:59:04  INFO  用户 uid_2 - 248466666：任务结束。  
2021-10-09 20:59:08  INFO  用户 uid_3 - 299677777：开始任务。  
...
2021-10-09 20:59:58  INFO  用户 uid_3 - 299677777：任务结束。  
2021-10-09 20:59:58  INFO  所有用户均操作完毕。  
2021-10-09 20:59:58  INFO  程序结束。  
```
