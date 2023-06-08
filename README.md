# CMS setup
### Database
1. Import _anarkist.sql_ to a local MySQL DB named anarkist
2. Create a user named _anarkist_ with all privilidges in the DB
3. Update DB_CONFIG in hidden.py if needed

### Virtual Python env
1. Make sure Python3.9 is installed
2. Create venv: _python3.9 -m venv venv_
3. Activate venv: _source venv/bin/activate_
4. Install dependencies: _pip3.9 install -r requirements.txt_
5. Run app: _python3.9 app.py_

### Tailwind
1. _cd static/css/tailwind_
2. _npm install_
3. _npx tailwindcss -i tailwind.css -o ../app.css --watch_