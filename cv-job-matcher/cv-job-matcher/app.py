# app.py
from flask import Flask, request, jsonify, render_template
from PyPDF2 import PdfReader
import spacy
import sqlite3
from utils import generate_cover_letter

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def init_db():
    """Initialize the SQLite database with a jobs table and sample data."""
    conn = sqlite3.connect("data/job_listings.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs 
                 (id INTEGER PRIMARY KEY, title TEXT, company TEXT, skills TEXT)''')
    # Insert sample jobs if the table is empty
    c.execute("SELECT COUNT(*) FROM jobs")
    if c.fetchone()[0] == 0:
        sample_jobs = [
            (1, "Software Engineer", "TechCorp", "Python, Flask, SQL"),
            (2, "Data Analyst", "DataCo", "SQL, Python, Excel"),
            (3, "Web Developer", "WebDesign", "HTML, CSS, JavaScript")
        ]
        c.executemany("INSERT INTO jobs VALUES (?, ?, ?, ?)", sample_jobs)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/upload_cv', methods=['POST'])
def upload_cv():
    """Handle CV upload, extract skills, and match to jobs."""
    if 'cv' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['cv']
    try:
        reader = PdfReader(file)
        text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    except Exception as e:
        return jsonify({'error': f'Failed to read PDF: {str(e)}'}), 400

    # Extract skills using spaCy (basic entity extraction as placeholder)
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents]  # In a real app, refine this with a custom model

    # Fetch jobs from database
    conn = sqlite3.connect("data/job_listings.db")
    c = conn.cursor()
    c.execute("SELECT id, title, company, skills FROM jobs")
    jobs = [{'id': row[0], 'title': row[1], 'company': row[2], 'skills': row[3]} for row in c.fetchall()]
    conn.close()

    # Match jobs based on skill overlap
    matches = [job for job in jobs if any(skill.lower() in job['skills'].lower().split(', ') for skill in skills)]
    return jsonify({'job_matches': matches})

@app.route('/generate_cover_letter', methods=['POST'])
def generate_cover_letter_route():
    """Generate a cover letter for a selected job."""
    data = request.json
    job_id = data.get('job_id')

    conn = sqlite3.connect("data/job_listings.db")
    c = conn.cursor()
    c.execute("SELECT title, company, skills FROM jobs WHERE id = ?", (job_id,))
    job = c.fetchone()
    conn.close()

    if job:
        cover_letter = generate_cover_letter("User Name", job[0], job[1], job[2])
        return jsonify({'cover_letter': cover_letter})
    return jsonify({'error': 'Job not found'}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)