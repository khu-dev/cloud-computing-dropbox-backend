docker rmi ghcr.io/umi0410/cloud-computing:latest || echo Skip - 기존 이미지 삭제 과정
docker pull ghcr.io/umi0410/cloud-computing:latest
docker rm -f django || echo Skip - 기존 django 컨테이너 삭제
docker run -it --name django -p 80:8000 ghcr.io/umi0410/cloud-computing