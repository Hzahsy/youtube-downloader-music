document.getElementById('downloadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const url = document.getElementById('urlInput').value;
    const status = document.getElementById('status');

    status.textContent = 'Downloading...';
    status.style.color = 'yellow';

    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        });

        if (response.ok) {
            const result = await response.json();
            status.textContent = result.message;
            status.style.color = 'green';
        } else {
            const error = await response.json();
            status.textContent = error.error;
            status.style.color = 'red';
        }
    } catch (error) {
        status.textContent = 'Error: ' + error.message;
        status.style.color = 'red';
    }
});