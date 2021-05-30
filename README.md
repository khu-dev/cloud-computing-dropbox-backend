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

## How to configure

```yaml
databases:
  default:
    ENGINE: 'django.db.backends.sqlite3'
    NAME: '../../db.sqlite3'

aws:
  # AWS Educate 특성상 credential을 이용하는 IAM User를 사용할 수 없으므로
  # IAM Role, Instance profile을 이용합니다. 따라서 EC2에서는 credential을 설정할 필요 없습니다.
  # 로컬의 경우 $ aws configure를 통해 설정할 것.
  s3_enabled: false
  region: "us-east-1"
  bucket_name: "storage.drive.jinsu.me"
  default_acl: "public-read"
```

`./config/$DROPBOX_ENVIRONMENT.yaml` 파일에 설정을 기입해주세요.
`./config/default.yaml` 은 Github에 공개되는 file이므로 credential을 포함하지 않게 주의해주세요. default.yaml은 예시 파일 같은 느낌이고, 각자 새로운 `.yaml` 만들어 사용할 것을 권장합니다.

* e.g. local 환경에서 개발할 때
  * local 환경에서도 credential을 이용할 수 있으니 `./config/local.yaml` 을 정의할 것을 추천합니다.
    DB는 간단히 SQLite3를, storage는 S3가 아닌 File system을 사용할 것을 권장합니다.
  * `DROPBOX_ENVIRONMENT=local`로 설정하신 뒤 `./config/local.yaml` 에 설정을 기입하시면 됩니다.
* e.g. dev 환경에 배포할 때
  * EC2에 배포하는 경우이고 `/home/ubuntu/dev.yaml` 을 자동으로 `/home/ubuntu/cloud-computing-dropbox-backend/config/dev.yaml` 로 복사해 이용하게 됩니다.
  * DB는 RDS를, storage는 S3를 이용합니다.


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
* 개발 환경(RDS)에 배포할 때에는 아래 커맨드 이용
  ```shell
  $ ./script/migrate.sh
  ```
* 로컬 환경에 배포할 때에는 직접 `makemigrations`와 `migrate` 커맨드를 이용할 것.

## API Documentation

## 1) 사용자 관련

### 사용자 회원가입

dropbox 사용자 회원 가입 api 설명입니다.

#### Request

#### URL

```http
POST /users
Host: 
```

#### Parameter

| Parameter      | Description                                            |
| -------------- | ------------------------------------------------------ |
| username       | 사용자 ID                                              |
| email          | 사용자 이메일                                          |
| password       | 사용자 비밀번호                                        |
| check_password | 비밀번호 체크(password와 check_password가 동일해야 함) |
| first_name     | 이름                                                   |
| last_name      | 성                                                     |

#### Response

```json
{
    "username": "mynameis",
    "email": "mynameis@gmail.com",
    "first_name": "Penguin",
    "last_name": "Park"
}
```

### 토큰 발급

dropbox에 로그인한 사용자에게 토큰 발급 api

#### Request

#### URL

```http
POST /api/token
Host: 
```

#### Parameter

| Parameter | Description     |
| --------- | --------------- |
| username  | 사용자 ID       |
| password  | 사용자 비밀번호 |



#### Response

```json
{
    "refresh": "eydasdsadasdsadasdsadsadMDdmNGVjNzg3OTRlNzZkZDEwMzM3NTEiLCJABC.Tk8hBzQXNIABCf5iLiPUo-Y37eE7Tg9ABCRk",
    "access": "eydasdsadsadasdsadsadsadsaJ0eXAiOiJKV1QiLCABCiJIUzI1NiJ9eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoABCjk2ODQ1LCJqdGkiOiI0MzUyMjQ3MmRmZjI0NGE1OTI3MGVhMTk0ZTllOWZmZCIsInVzZXJfaWQiOjJ9.5ROeABCQiz8Ql8Tp9UF5ZDl6BbgTCaqoAtnGQKgo"
}
```

### 토큰 갱신

토큰 갱신 api

#### Request

#### URL

```http
POST /api/token/refresh
Host: 
```

#### Parameter

| Parameter | Description   |
| --------- | ------------- |
| refresh   | refresh token |


#### Response

```json
{
    "access": "eyJ0edddddddjoiYWNjABCXGkiOiIwN2FlZGRlNjUyNWI0ABC.Y9fWy_YIIF1PB_ru20MifMEGwA1OiiNkDABC"
}
```

### 토큰 검증

토큰 검증 api

#### Request

#### URL

```http
POST /api/token/verify
Host: 
```

#### Parameter

| Parameter | Description  |
| --------- | ------------ |
| token     | access token |


#### Response

```json
{
}
```

### 사용자 비밀번호 수정

dropbox 사용자 비밀번호 수정 api 설명입니다.

#### Request

#### URL

```http
PUT /users/password/<int:pk>
Host: 
```

#### Parameter

| Parameter      | Description                                            |
| -------------- | ------------------------------------------------------ |
| password       | 사용자 새로운 비밀번호                                   |
| password2      | 사용자 새로운 비밀번호 체크                               |
| old_password   | 사용자 이전 비밀번호                                     |

#### Response

```json
{
}
```

### 사용자 프로필 수정

dropbox 사용자 프로필 수정 api 설명입니다.

#### Request

#### URL

```http
PUT /users/password/<int:pk>
Host: 
```

#### Parameter

| Parameter      | Description                                            |
| -------------- | ------------------------------------------------------ |
| username       | 사용자 새로운 비밀번호                                   |
| first_name     | 사용자 이름                                             |
| last_name      | 사용자 성                                               |
| email          | 사용자 이메일                                           |

#### Response

```json
{
    "username": "mynameis",
    "email": "mynameis@gmail.com",
    "first_name": "Penguin",
    "last_name": "Park"
}
```

### 사용자 리스트 조회

dropbox 사용자 리스트 조회 api 설명입니다.

#### Request

#### URL

```http
GET /users/list/
Host: 
```

#### Response

```
[
    {
     "username": "mynameis",
    "email": "mynameis@gmail.com",
    "first_name": "Penguin",
    "last_name": "Park",
    "date_joined": "2021-05-29T09:00:23.504315Z"
    }
]
```
  
