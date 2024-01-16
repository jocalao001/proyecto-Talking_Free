let recognition;

function toggleListening() {
    if (!recognition) {
        startListening();
    } else {
        stopListening();
    }
}

function startListening() {
    recognition = new webkitSpeechRecognition();
    recognition.lang = 'es-ES';
    recognition.continuous = true;

    recognition.onresult = function (event) {
        const result = event.results[event.results.length - 1][0].transcript;
        const currentTranscription = document.getElementById('transcription').innerText;
        document.getElementById('transcription').innerText = currentTranscription + ' ' + result;
    };

    recognition.onend = function () {
        // No detener el reconocimiento aquí, permitir que continúe
    };

    recognition.start();
}

function stopListening() {
    if (recognition) {
        recognition.stop();
        recognition = null;  // Limpiar la instancia después de detenerla
    }
}

document.addEventListener("DOMContentLoaded", function () {
    var el = document.getElementById('toggleButton');
    el?.addEventListener('mousedown', function () {
        startListening();
    });

    el?.addEventListener('mouseup', function () {
        // No detener el reconocimiento aquí para permitir la transcripción en tiempo real
    });
});

function clearTranscription() {
    // Esperar 100 milisegundos antes de limpiar la transcripción
    setTimeout(function () {
        document.getElementById('transcription').innerText = '';
    }, 100);
}