
ssh -i ~/.ssh/cloud-computing.pem -o StrictHostKeyChecking=no ubuntu@api.drive.jinsu.me  '
cd /home/ubuntu/cloud-computing-dropbox-backend
echo ### RDS 데이터베이스를 마이그레이션합니다. ###
echo ### 기존에 RDS에 존재하던 테이블들은 미리삭제해주세요. ###
rm */migrations/00*.py
python3 manage.py makemigrations
python3 manage.py migrate
echo ### RDS 데이터베이스 마이그레이션을 완료했습니다. ###
'
