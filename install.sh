#azure sdk install 
pip install azure-identity
pip install azure-keyvault-secrets
pip install python-dotenv

#django install
pip install django
django-admin startproject ./Tool/
python manage.py migrate
#python3 manage.py migrate
django-admin startapp ./Tool/pybo