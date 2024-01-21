document.getElementById('start-recording').addEventListener('click', function() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            const audioChunks = [];

            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener('stop', () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('file', audioBlob, 'audio.wav');

                console.log("Sending audio data:", formData); // Debug before sending
                fetch('/transcribe', {
                    method: 'POST',
                    body: formData
                })
                // .then(response => response.json())
                .then(response => {
                    console.log("Response received:", response); // Debug after receiving response
                    // Check if the response is ok (status code 200-299)
                    if (!response.ok) {
                        throw new Error('Network response was not ok ' + response.statusText);
                    }
                    return response.json(); // This will fail if the response isn't JSON
                })
                .then(data => {
                    document.getElementById('status').textContent = data.transcript;
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('status').textContent = "Error: " + error.message;
                });
            });

            mediaRecorder.start();
            document.getElementById('status').textContent = "Recording started...";

            setTimeout(() => {
                mediaRecorder.stop();
                document.getElementById('status').textContent = "Recording stopped, processing...";
            }, 5000);
        })
        .catch(error => {
            console.error('Error accessing the microphone:', error);
            document.getElementById('status').textContent = "Error accessing the microphone: " + error.message;
        });
});
