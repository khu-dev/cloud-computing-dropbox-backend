
ssh -i ~/.ssh/cloud-computing.pem -o StrictHostKeyChecking=no ubuntu@api.drive.jinsu.me  '
cd /home/ubuntu
cp dev.yaml cloud-computing-dropbox-backend/config/
cd cloud-computing-dropbox-backend
echo ### RDS 데이터베이스를 마이그레이션합니다. ###
echo ### 기존에 RDS에 존재하던 테이블들은 미리삭제해주세요!!! ###
rm */migrations/00*.py || echo 삭제할 migration file이 없습니다. 괜찮아요~
DROPBOX_ENVIRONMENT=dev python3 manage.py makemigrations
DROPBOX_ENVIRONMENT=dev python3 manage.py migrate
echo ### RDS 데이터베이스 마이그레이션을 완료했습니다. ###
'
