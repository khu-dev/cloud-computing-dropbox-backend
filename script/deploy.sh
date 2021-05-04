pip freeze > requirements.txt
docker build . -t ghcr.io/umi0410/cloud-computing:latest
docker push ghcr.io/umi0410/cloud-computing:latest
ssh cloud-computing '
docker rmi ghcr.io/umi0410/cloud-computing:latest
docker pull ghcr.io/umi0410/cloud-computing:latest
docker rm -f django
docker run -d --name django -p 80:8000 ghcr.io/umi0410/cloud-computing
'