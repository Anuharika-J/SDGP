//Creating variables

var gumStream; 						
var rec; 							
var input; 	
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext 
var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");

//add events to 3 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
	console.log("recordButton clicked");

    var constraints = { audio: true, video:false }

 	recordButton.disabled = true;
	stopButton.disabled = false;
	pauseButton.disabled = false

	
	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

		
		audioContext = new AudioContext();

		
		/*document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"*/
		
		gumStream = stream;
		
		input = audioContext.createMediaStreamSource(stream);

		rec = new Recorder(input,{numChannels:1})

		//start the recording process
		rec.record()

		console.log("Recording started");

	}).catch(function(err) {
	  	//enable the record button if getUserMedia() fails
    	recordButton.disabled = false;
    	stopButton.disabled = true;
    	pauseButton.disabled = true
	});
	
	scoreContainert.style.display = "block";
	
}

function pauseRecording(){
	console.log("pauseButton clicked rec.recording=",rec.recording );
	if (rec.recording){
		//pause
		rec.stop();
		pauseButton.innerHTML="Resume";
	}else{
		//resume
		rec.record()
		pauseButton.innerHTML="Pause";

	}
}

function stopRecording() {
	console.log("stopButton clicked");

	stopButton.disabled = true;
	recordButton.disabled = false;
	pauseButton.disabled = true;

	pauseButton.innerHTML="Pause";
	
	//tell the recorder to stop the recording
	rec.stop();

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();


	rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
	
	var url = URL.createObjectURL(blob);
	var au = document.createElement('audio');
	var li = document.createElement('li');
	var link = document.createElement('a');

	//name of .wav file 
	var filename ="input";

	au.controls = true;
	au.src = url;

	//save to disk link
	link.href = url;
	link.download = filename+".wav"; 
	link.innerHTML = "Save to disk";

	li.appendChild(au);
	
	li.appendChild(document.createTextNode(filename+".wav "))

	li.appendChild(link);
	
	//add the li item to the ol
	recordingsList.appendChild(li);
	scoreContainert.style.display = "none";
	scoreContainer.style.display = "block";
	
	
}