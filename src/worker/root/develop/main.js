canvas = document.getElementById("display");
canvasContext = canvas.getContext('2d');
canvas.width = 1366;
canvas.height = 768;

async function convertAudioFileToDataUrl(file) {
    reader = new FileReader();

    loadPromise = new Promise((resolve, reject) => {
        reader.onload = (event) => {
            resolve(event.target.result);
        };
    });

    reader.readAsDataURL(file);

    return loadPromise;
}

function render(spectrum) {
    barWidth = Math.round(canvas.width / spectrum.length);
    canvasContext.fillStyle = 'rgba(100, 210, 240, 0.9)';
    canvasContext.clearRect(0, 0, canvas.width, canvas.height);
    for (i = 0; i < spectrum.length; i++) {
        canvasContext.fillRect((barWidth + 1) * i, canvas.height, barWidth, -(spectrum[i] * (canvas.height)) / 255 + 10);
    }
}

fileInput = document.getElementById("file-input");

let audio = null,
    audioSource = null,
    intervalId = null;

fileInput.addEventListener('change', async (event) => {
    audioContext = new AudioContext();
    analyzerNode = audioContext.createAnalyser();

    if (audio) {
        audio.pause();
        audio.src = '';
    }
    if (audioSource) {
        audioSource.disconnect();
    }
    if (intervalId) {
        clearInterval(intervalId);
    }

    analyzerNode.fftSize = 2048;
    file = fileInput.files[0];

    if (file) {
        spectrumArray = new Uint8Array(analyzerNode.frequencyBinCount);

        audio = new Audio();
        audio.src = await convertAudioFileToDataUrl(file);
        audio.loop = true;

        audioSource = audioContext.createMediaElementSource(audio);
        audioSource.connect(analyzerNode);
        analyzerNode.connect(audioContext.destination);

        /*
        requestAnimationFrame(() => {
            analyzerNode.getByteFrequencyData(spectrumArray);
            render(spectrumArray);
            requestAnimationFrame(this);
        });
        */

        intervalId = setInterval((event) => {
            analyzerNode.getByteFrequencyData(spectrumArray);
            render(spectrumArray);
        }, 1/60);

        audio.play();
    }
});

link.addEventListener('keypress', (evt) => {
    if(evt.keyCode == 13) {
        audioContext = new AudioContext();
        analyzerNode = audioContext.createAnalyser();

        if (audio) {
            audio.pause();
            audio.src = '';
        }
        if (audioSource) {
            audioSource.disconnect();
        }
        if (intervalId) {
            clearInterval(intervalId);
        }

        analyzerNode.fftSize = 2048;
        spectrumArray = new Uint8Array(analyzerNode.frequencyBinCount);

        audio = new Audio();
        audio.src = link.value;
        audio.loop = true;

        audioSource = audioContext.createMediaElementSource(audio);
        audioSource.connect(analyzerNode);
        analyzerNode.connect(audioContext.destination);

        intervalId = setInterval((event) => {
            analyzerNode.getByteFrequencyData(spectrumArray);
            render(spectrumArray);
        }, 1/60);

        audio.play();
    }
});