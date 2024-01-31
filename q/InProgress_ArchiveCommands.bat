python -m venv venv
.venv\Scripts\activate

pip freeze > "requirements.txt"
pip uninstall -r "requirements.txt"
pip uninstall -r "requirements.txt" -y

pip install -r "requirements.txt"

pip install django-enumchoicefield
