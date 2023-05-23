**Set up
1. python3 -m venv venv (creaing venv in venv-dir)
2. source venv/bin/activate
3. pip install -r requirements.txt (Install deps)
4. python3 app.py

**Tailwind
1. cd static/css/tailwind
2. npm install -d tailwindcss@latest postcss@latest autoprefixer@latest
3. npx tailwindcss -i tailwind.css -o ../app.css --watch