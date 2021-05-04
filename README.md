# KHU 드롭박스 프로젝트

API Root url: http://api.drive.jinsu.me

> 편의상 `@umi0410(박진수 팀원)` 이 운영 중인 도메인 네임을 사용합니다.

## 유용한 script 파일들

개발하고 운영, 배포할 때 유용할 스크립트 파일들을 `script/` 경로에 정리해놨습니다.

* `./script/deploy.sh` - EC2 서버에 현재 local의 상태와 같은 서버를 배포합니다.

* `./script/logs.sh` - EC2 서버의 Django 로그를 보여줍니다.
  
* `./script/run.sh` - EC2 서버가 아닌 로컬에서 Django 컨테이너를 실행합니다. 프론트엔드 개발자가 사용하기 유용합니다.

## How to deploy

ElasticBeanstalk을 이용하면 편리하게 배포를 자동화할 수 있지만 AWS Educate를 이용하면서는 IAM User key 발급이 지원되지 않고,
교수님께서 설정하신 AWS Educate Classroom 설정으로는 ElasticBeanstalk을 사용할 수 없었습니다. 따라서 **직접 EC2에 SSH 접속을
해서 컨테이너를 지운 뒤 새로운 컨테이너를 띄우는 방식으로 배포**합니다.

필요한 항목은 다음과 같고 모두 `@umi0410(박진수 팀원)`에게서 제공받을 수 있습니다.

1. EC2 접속을 위한 `ssh pem key `
2. 원활한 ssh 명령어 수행을 위한 `ssh config`
3. Github package registry에 로그인하기 위한 `Github token`

```shell
$ docker login docker.pkg.github.com -u umi0410
```

전달 받은 .pem key과 config를 .ssh에 저장합니다. 이후 위의 커맨드를 통해 container registry에 인증합니다.

```shell
$ ./script/deploy.sh
```

앞서 설명한 설정이 완료되면 간단히 위의 커맨드로 EC2 서버에 현재 작업물을 배포할 수 있습니다.

## 로그 보는 방법

```shell
$ docker logs -f django
```

EC2 인스턴스에 접속해서 도커 컨테이너의 로그를 볼 수 있습니다.

## 로컬에서 Django 서버 실행하기 (프론트엔드 개발자님을 위함 ㅎㅎ)

```shell
$ ./script/run.sh
```

http://0.0.0.0:8000 에 django 서버를 띄웁니다. docker container를 실행하기 때문에 최신 이미지를 이용해
아무런 추가작업 없이 로컬에서 django 서버를 이용할 수 있습니다.
