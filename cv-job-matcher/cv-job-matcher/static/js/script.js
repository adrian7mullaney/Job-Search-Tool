// static/js/script.js
document.getElementById('upload-button').addEventListener('click', () => {
    const fileInput = document.getElementById('cv-file');
    const file = fileInput.files[0];
    if (!file) return alert('Please select a file');

    const formData = new FormData();
    formData.append('cv', file);
    fetch('/upload_cv', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) throw new Error(data.error);
        const jobList = document.getElementById('job-list');
        jobList.innerHTML = '';
        data.job_matches.forEach(job => {
            const li = document.createElement('li');
            li.textContent = `${job.title} at ${job.company}`;
            li.className = 'cursor-pointer hover:text-blue-500 transition duration-200';
            li.addEventListener('click', () => {
                fetch('/generate_cover_letter', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({job_id: job.id})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) throw new Error(data.error);
                    document.getElementById('cover-letter').textContent = data.cover_letter;
                    document.getElementById('modal').classList.remove('hidden');
                })
                .catch(error => alert('Error generating cover letter: ' + error));
            });
            jobList.appendChild(li);
        });
    })
    .catch(error => alert('Error uploading CV: ' + error));
});

document.querySelector('.close').addEventListener('click', () => {
    document.getElementById('modal').classList.add('hidden');
});

document.getElementById('copy-button').addEventListener('click', () => {
    const coverLetter = document.getElementById('cover-letter').textContent;
    navigator.clipboard.writeText(coverLetter).then(() => {
        alert('Cover letter copied to clipboard!');
    }).catch(error => alert('Failed to copy: ' + error));
});