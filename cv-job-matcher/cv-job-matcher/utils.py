# utils.py
from jinja2 import Template

def generate_cover_letter(name, job_title, company, skills):
    """Generate a cover letter based on user and job details."""
    template_str = """
Dear Hiring Manager,

I am excited to apply for the {{ job_title }} position at {{ company }}. With my experience in {{ skills }}, I am confident in my ability to contribute to your team.

[Add more personalized details here based on your CV and the job description.]

Thank you for considering my application.

Sincerely,
{{ name }}
    """
    template = Template(template_str)
    return template.render(name=name, job_title=job_title, company=company, skills=skills)