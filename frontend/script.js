let audioUrl = null;

async function askQuestion() {
    const question = document.getElementById('questionInput').value;
    if (!question) return;
    
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('result').classList.add('hidden');
    
    try {
        const response = await fetch('http://127.0.0.1:8000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question })
        });
        
        const data = await response.json();
        
        document.getElementById('answerText').textContent = data.answer;
        audioUrl = data.audio_file;
        
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('result').classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('loading').classList.add('hidden');
        alert('Error getting answer. Make sure the backend is running.');
    }
}

function playAudio() {
    if (audioUrl) {
        const audio = new Audio(audioUrl);
        audio.play();
    }
}

document.getElementById('questionInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        askQuestion();
    }
});