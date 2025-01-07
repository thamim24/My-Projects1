// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    const resumeContent = document.getElementById('resume-content');
    const resumeScore = document.getElementById('resume-score');
    const improvementSuggestions = document.getElementById('improvement-suggestions');

    if (resumeContent) {
        resumeContent.addEventListener('input', debounce(updateResumeScore, 1000));
    }

    function updateResumeScore() {
        const resumeText = resumeContent.innerText;
        fetch('/api/resume_score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ resume: resumeText }),
        })
        .then(response => response.json())
        .then(data => {
            resumeScore.textContent = data.score;
            improvementSuggestions.innerHTML = '';
            data.suggestions.forEach(suggestion => {
                const li = document.createElement('li');
                li.textContent = suggestion;
                improvementSuggestions.appendChild(li);
            });
        })
        .catch(error => console.error('Error:', error));
    }

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
});