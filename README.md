# loha-backend

## Docker 사용법 


### 0. Ubuntu 설치 (필자는 18.04 LTS 버젼을 사용함)

VM ware, Virtual Box를 이용하여도 되고 

AWS에서 계정을 만들어 EC2 Ubuntu 18.04 Free tier로 설치하여도 된다. 

[우분투 세팅](https://blog.lael.be/post/7264) 

위 링크는 그냥 공부 용도로 참고하면 되고 docker를 실행하기 위해서는 (5-1) 시스템 시간 설정)까지만 참고해도 될 것 같다. 

### 1. Docker 설치 

[초보를 위한 docker 설명1](https://subicura.com/2017/01/19/docker-guide-for-beginners-1.html)

[초보를 위한 docker 설명2](https://subicura.com/2017/01/19/docker-guide-for-beginners-2.html)

[초보를 위한 docker 설명3](https://subicura.com/2017/02/10/docker-guide-for-beginners-create-image-and-deploy.html)

위 사이트를 참고하여 작성했다. 정리하자면 다음 명령어를 ubuntu에서 실행시면 된다. 

(사용자가 root가 아닌 기본 사용자 ubuntu를 기준으로 작성했다.)

```
#(도커를 설치하는 명령어)
curl -fsSL https://get.docker.com/ | sudo sh 

# 현재 접속중인 사용자에게 권한주기 
# docker 명령어는 원래 root 권한으로 실행해야 되는데 현재 사용자에서 사용 가능하게 한다.
sudo usermod -aG docker $USER 
```

다음을 실행해 Docker가 설치되었는지 확인해 보자 

```
docker -v
```

정상적으로 설치되었으면 다음과 같이 출력된다.

```
Docker version 19.03.13, build {적당한 id}
```

### 2. Docker-composer 설치

[docker compose](https://docs.docker.com/compose/install/)

위 사이트를 참고하여 작성했다. 정리하면 다음 명령어만 실행하면 된다.

```
#compose 설치 
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

#권한설정
sudo chmod +x /usr/local/bin/docker-compose

#환경변수 설정 
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

다음을 실행해 Docker가 설치되었는지 확인해 보자 

```
docker-compose -v
```

정상적으로 설치되었으면 다음과 같이 출력된다.

```
docker-compose version 1.27.4, build {적당한 숫자}
```

### 3. Git 설치 

AWS를 사용한다면 이미 깔려 있을 것이니 통과해도 된다.

만약 설치가 안 되어 있다면 다음을 참고하여 설치하면 된다.

[git 설치](https://coding-factory.tistory.com/502)

git 설치 확인 

```
git --version
```

다음이 뜰 것이다.

```
git version 2.17.1
```

### 4. 현재 github를 git clone 

```
git clone https://github.com/AhnByungkyu/loha-backend.git
```



