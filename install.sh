#azure sdk install 
pip install azure-identity
pip install azure-keyvault-secrets
pip install python-dotenv

#django install
pip install django
django-admin startproject ./Tool/
python manage.py migrate
#python3 manage.py migrate
django-admin startapp ./Tool/pipe

#비동기

wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
make test
redis-server # redis 실행
redis-cli ping # 정상 설치되었는지 확인