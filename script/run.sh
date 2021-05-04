docker rmi docker.pkg.github.com/khu-dev/cloud-computing-dropbox-backend/django || echo Skip - 기존 이미지 삭제 과정
docker pull docker.pkg.github.com/khu-dev/cloud-computing-dropbox-backend/django
docker rm -f django || echo Skip - 기존 django 컨테이너 삭제
docker run -it --name django -p 8000:8000 docker.pkg.github.com/khu-dev/cloud-computing-dropbox-backend/django