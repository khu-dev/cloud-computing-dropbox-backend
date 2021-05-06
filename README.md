# KHU 드롭박스 프로젝트

API Root url: http://api.drive.jinsu.me

> 편의상 `@umi0410(박진수 팀원)` 이 운영 중인 도메인 네임을 사용합니다.

https가 아닌 http임을 주의. (기존에는 AWS의 ACM이라는 인증서 서비스를 ALB와 함께 이용해 ALB단에서 SSL Termination이 이루어지게
하려했으나 AWS Educate에서 ACM도 이용이 불가능해서... 편의상 HTTP 서버를 이용해야겠음. Let's encrypt나 certbot을 이용하면 가능은
하지만 관리가 너무 번거로워짐.)

## How to deploy

ElasticBeanstalk을 이용하면 편리하게 배포를 자동화할 수 있지만 AWS Educate를 이용하면서는 IAM User key 발급이 지원되지 않고,
교수님께서 설정하신 AWS Educate Classroom 설정으로는 ElasticBeanstalk을 사용할 수 없었습니다. 따라서 **직접 EC2에 SSH 접속을
해서 프로세스를 내리고 현재 master를 다운 받은 뒤 프로세스를 새로 올리는 방식으로 배포**합니다. 이 과정은 master branch에 push할 경우
자동으로 진행됩니다.

* 배포 시에는 `./requirements.txt` 를 바탕으로 pip dependency를 설치합니다. 따라서 꼭 새로운 패키지를 설치한 경우 꼭 아래 커맨드를 통해
  의존성을 반영해주세요.
  ```shell
  $ pip freeze > requirements.txt
  ```

## 로그 보는 방법

```shell
$ ./script/logs.sh
```

EC2 인스턴스에 접속해서 로그를 볼 수 있습니다. 편의상 스크립트를 짜놓았으니 이용 바랍니다.

* SSH 접속을 해서 로그를 보기 때문에 `@umi0410(박진수 팀원)`에게 SSH 접속 pem key를 전달 받으세요.

## 데이터베이스 테이블 관리 방법

* 로컬에서 개발할 때에는 개개인의 로컬의 `sqlite3`를 사용합니다.
* EC2 서버에서는 RDS를 이용합니다.
* 여러 명이 Concurrent하게 한 DB에 마이그레이션을 하면 오류가 발생할 수 있습니다. migraiton 파일이 crash날 수도 있고, 테이블 정의가 꼬일 수 있습니다.
  따라서 그러한 충돌과 오류를 막기 위해 간단한 개발 단계이므로 **RDS의 테이블 정의를 수정하는 경우 RDS의 테이블을 모두 지운 뒤 초기 migration을 진행합니다. 이 코드는 `./script/migrate.sh` 에 정의되어있습니다.**
  