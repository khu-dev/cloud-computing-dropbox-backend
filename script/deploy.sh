pip freeze > requirements.txt
docker build . -t docker.pkg.github.com/khu-dev/cloud-computing-dropbox-backend/django
docker push docker.pkg.github.com/khu-dev/cloud-computing-dropbox-backend/django
ssh cloud-computing '
docker rmi docker.pkg.github.com/khu-dev/cloud-computing-dropbox-backend/django
docker pull docker.pkg.github.com/khu-dev/cloud-computing-dropbox-backend/django
docker rm -f django
docker run -d --name django -p 80:8000 docker.pkg.github.com/khu-dev/cloud-computing-dropbox-backend/django
docker ps
'