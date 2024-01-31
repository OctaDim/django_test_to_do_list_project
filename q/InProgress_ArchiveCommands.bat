python -m venv venv
.venv\Scripts\activate

pip freeze > "requirements.txt"
pip uninstall -r "requirements.txt"
pip uninstall -r "requirements.txt" -y

pip install -r "requirements.txt"

pip install django-enumchoicefield

git checkout my_branch rem Go to the branch my_branch
git rebase master rem Rebasing all commits to the master
git checkout master rem Go to the branch master
git merge my_branch —ff rem (fast forward merge) To merge with my_branch WITHOUT merging commit
git merge my_branch —no-ff rem (no fast forward merge) To merge with my_branch WITH merging commit
