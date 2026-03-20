@echo off
python build.py
git add .
git commit -m "Automated blog post update"
git push origin main
echo Blog published successfully.