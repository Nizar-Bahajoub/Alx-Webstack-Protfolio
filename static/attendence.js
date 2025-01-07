var isActive = false;
function startPresence() {
    var video = document.getElementById('video_feed');
    if (!isActive) {
        startStream(video);
        isActive = true;
        document.getElementById('start_stop').innerText = 'Stop Presence Check';
    } else {
        stopStream(video);
        isActive = false;
        document.getElementById('start_stop').innerText = 'Start Presence Check';
    }
}

function startStream(videoElement) {
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                videoElement.srcObject = stream;
            })
            .catch(function (error) {
                console.log("Something went wrong with the webcam: ", error);
            });
    }
}

function stopStream(videoElement) {
    videoElement.style.display = "none";
    if (videoElement.srcObject) {
        var tracks = videoElement.getTracks();
        tracks.forEach(track => {
            track.stop();
        });
        videoElement.srcObject = null;
    }
}

/* var uniqueNames = new Set(); // Set to store unique names
function updateDetectedFaces(names) {
    var faceLabels = document.getElementById('face_labels');
    names.forEach(function(name) {
        // Add new names to the set
        if (!uniqueNames.has(name)) {
            uniqueNames.add(name);
            var label = document.createElement('div');
            label.textContent = name;
            faceLabels.appendChild(label);
        }
    });
}

// Event listener for receiving new frames
var eventSource = new EventSource("{{ url_for('video_feed') }}");
eventSource.onmessage = function(event) {
    var data = JSON.parse(event.data);
    updateDetectedFaces(data.detected_faces);
};

// Stop event listener when the window is closed or navigated away
window.onbeforeunload = function() {
    eventSource.close();
}; */