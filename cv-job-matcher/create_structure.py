import os

structure = [
    "cv-job-matcher/app.py",
    "cv-job-matcher/utils.py",
    "cv-job-matcher/requirements.txt",
    "cv-job-matcher/static/css/style.css",
    "cv-job-matcher/static/js/script.js",
    "cv-job-matcher/templates/index.html",
    "cv-job-matcher/data/"
]

for path in structure:
    if path.endswith('/'):
        os.makedirs(path, exist_ok=True)
    else:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            pass

print("Directory structure created successfully.")