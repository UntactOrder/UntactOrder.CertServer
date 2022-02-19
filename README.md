# [EN]UntactOrder: Non-Contact Order<br/>[KO]언택트오더: 비대면 주문
UntactOrder Cert Server(언택트오더 시스템 인증서 서버) <python 3.10>

> [EN] This is a server for UntactOrder HTTPS Cert System.
>> The UntactOrder Project is an open-source project that began with the prototype of UntactOrder; 'Non-Contact Order', which was produced through the Design Thinking Process course in the second semester of 2021.
>>
>> The goal is to provide a free solution that allows non-face-to-face orders within the store in the form of deferred payment, which is still using face-to-face ordering.
>
>> You only need to host this certificate server if you want to implement a new UntactOrder system as a whole, and you won't have to modify CertServer other than that.
>
> [KO] 이 서버는 언택트오더 HTTPS 인증서 시스템을 위한 서버입니다.
>> 언택트오더 프로젝트는 2021년 2학기 어드벤처디자인 수업에서 Design Thinking 과정을 통해 제작되었던 ‘언택트오더; 비대면 주문’ 프로토타입에서 시작된 오픈소스 프로젝트입니다.
>>
>> 기존의 대면 주문 방식에서 벗어나 후불 결제 형태의 매장 내에서 비대면으로 주문 할 수 있는 솔루션을 무료로 제공하겠다는 목표를 가지고 있습니다.
>
>> 언택트오더 시스템 전체를 새로 구현하고자 할 때만 이 인증서 서버를 호스팅 할 필요가 있으며, 그 이외에는 CertServer를 수정하실 필요는 없을 것입니다.
>
> More Information about UntactOrder Project can be found at [UntactOrder Project Notion Page.](https://www.notion.so/cuws/e82c5c200ea642a98f36970e0b49b49b)


### [EN] Development Environment / [KO] 개발 환경
* IntelliJ IDEA Ultimate 2021.3 (or up)
* Python 3.10.2 (or up)
* [Oracle Cloud Free Tier; OCI] Canonical Ubuntu 20.04 LTS (Image Build: 2022.01.18-0)
* [OCI] VM.Standard.E2.1.Micro (1 core OCPU, 1 GB memory, 0.48 Gbps network bandwidth)

### [EN] Programming Language / [KO] 사용 언어
* Python 3

### [EN] Required Modules / [KO] 필요 모듈
* see requirements.txt

### [EN] License / [KO] 라이센스
* MIT License

# [EN] Usage Instruction / [KO] 사용법
## [EN] Disclaimer / [KO] 디스클레이머
* [EN] This software is provided "as is" without warranty of any kind.
* [EN] The author does not guarantee the stability/security//validity/etc of this software.
* [KO] 이 소프트웨어는 어떠한 종류의 보증도 없이 "있는 그대로" 제공됩니다.
* [KO] 저자는 이 소프트웨어의 안정성/보안/유효성/등을 보장하지 않습니다.

## [EN] Precautions / [KO] 유의사항
* [EN] It is recommended not to use CJK Letters(A.K.A. Jiantizi/Hiragana/Katakana/Hangul) in the project path.
* [EN] To prevent possible problems, it is recommended to name the project folder 'CertServer' except 'UntactOrder.'.
* [KO] 프로젝트 경로에 CJK 문자(중국 번체/히라가나/가타가나/한글)를 사용하지 않는 것을 권장합니다.
* [KO] 혹시 모르는 문제를 방지하기 위해 깃 레포 클론시에 프로젝트 폴더 이름을 'UntactOrder.'를 제외한 'CertServer'로 지정하는 것을 권장합니다.

## [EN] 0. Preparations / [KO] 0. 사전 작업
#### (1). [EN] Development environment setting is required (refer to the the development environment part at the top)
#### (1). [KO] 개발 환경 세팅 필요 (상단 개발 환경 설명된 부분 참고)
<pre>a. install Intellij IDEA and Python
b. prepare server resources | ref: https://www.wsgvet.com/cloud/5
c. install python3.10.2 (or up) | ref: https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux-system/
</pre>
#### (2). [EN] Update Python Main Version (linux only, Windows user just use python keyword)
#### (2). [KO] 파이썬3 호출 키워드로 호출되는 파이썬 버전 변경 (리눅스만, 윈도우 사용자는 python 키워드로 사용)
###### [Reference] https://codechacha.com/ko/change-python-version/
```sh
<-- Check the Python version list. -->
$ ls /usr/bin/ | grep python3
>> python3
>> python3
>> python3.10
>> python3.8
```
```sh
<-- Change the Python main version -->
$ sudo update-alternatives --install /usr/bin/python3 python /usr/bin/python3.10 1
>> update-alternatives: renaming python link from /usr/bin/python3.10 to /usr/bin/python3
```
#### (3). [EN] Create a new ssh keypair with passphrase and add key to server instance. (Optional)
#### (3). [KO] 오라클 서버 접속을 위한 비밀번호가 있는 ssh 키 페어 생성 후 서버에 등록. (선택적 적용)
###### [Reference] https://story.stevenlab.io/210
###### [Reference] https://my-t-space.tistory.com/31
~~~sh
<-- Check this on the client -->
$ ssh -i [key_file] [ubuntu_user_name]@[static_ip]
~~~
#### (4). [EN] Change the ssh port (Oracle Cloud settings should also be changed)
#### (4). [KO] ssh 포트 변경 (Oracle Cloud 설정도 바꿔야 함)
##### - Change ssh setting => Change iptables firewall setting => Change Oracle Cloud setting
###### [Reference] https://www.lesstif.com/lpt/ssh-22-20776114.html
###### [Reference] https://meyouus.tistory.com/135
~~~sh
<-- Open new ssh port and drop 22 port (If you don't set netfilter-personality, it's initialized upon reboot.) -->
$ sudo iptables -A INPUT -i eth0 -p tcp --dport 22 -j DROP
$ sudo iptables -I INPUT 5 -p tcp --dport [ssh_port_number] -j ACCEPT
$ sudo apt install iptables-persistent netfilter-persistent
$ netfilter-persistent save
$ netfilter-persistent start
~~~
~~~sh
<-- Check this on the server -->
$ sudo apt install net-tools
$ netstat -nap | grep [port_number]
~~~
~~~sh
<-- Check this on the client -->
$ ssh -i [key_file] [ubuntu_user_name]@[static_ip]
~~~
#### (5). [EN] Install nginx / [KO] nginx 설치
~~~sh
<-- Linux -->
$ sudp apt update -y
$ sudo apt install nginx
~~~
<pre>
<-- Windows -->
download stable version from http://nginx.org/en/download.html
</pre>
#### (6). [EN] git clone / [KO] 깃 클론
~~~sh
<-- Do this on your home directory. -->
$ git clone https://github.com/UntactOrder/UntactOrder.CertServer.git CertServer
$ cd CertServer
$ sudo chmod 775 run.sh
$ sudo chmod 775 start.sh
$ sudo chmod 775 stop.sh
~~~
#### (7). [EN] install required python packages/modules / [KO] 파이썬 패키지/모듈 설치
~~~sh
$ sudo apt remove python-pip python3-pip
$ sudo apt install python3.10-distutils python3.10-dev
$ sudo cp /usr/local/bin/pip3.10 /usr/local/bin/pip3
$ pip3 install -r ./requirements.txt
~~~
#### (8). [EN] set timezone / [KO] 타임존 변경
~~~sh
$ sudo timedatectl set-timezone Asia/Seoul
$ timedatectl
>>                Local time: Sat 2022-02-19 01:19:49 KST
>>            Universal time: Fri 2022-02-18 16:19:49 UTC
>>                  RTC time: Fri 2022-02-18 16:19:49
>>                 Time zone: Asia/Seoul (KST, +0900)
>> System clock synchronized: yes
>>               NTP service: active
>>           RTC in local TZ: no
~~~

### 1. Set CertServer
* ???
<pre>????</pre>

### 2. Set Nginx
systemctl status nginx.service

sudo systemctl restart nginx.service
sudo service nginx restart

