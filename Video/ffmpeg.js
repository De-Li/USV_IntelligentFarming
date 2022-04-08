//Main function:
//This script can maintain the streaming of ffmpeg.

var child_process_1 = require("child_process");
var _ffmpeg;
var videoStream = function () {
	if (_ffmpeg != null) return;
	console.log("start stream!");
	_ffmpeg = child_process_1.spawn('ffmpeg', ['-r','30','-video_size','640x480','-i', "/dev/video0", '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency', '-c:a', 'aac', '-ar', '44100', '-r','30', '-f', 'flv', 'rtmp://140.116.202.132:3033/live/UnderWaterVideoTainan']);
	_ffmpeg.stdout.setEncoding('utf8');
	_ffmpeg.stdout.on('data', function (data) { //觸發stdout的回呼函式
		//Here is where the output goes
		console.log('stdout: ' + data);
	});
	_ffmpeg.stderr.setEncoding('utf8');
	_ffmpeg.stderr.on('data', function (data) { //觸發stderr的回呼函式
		//Here is where the error output goes
		console.log('stderr: ' + data);
	});
	_ffmpeg.on('close', function (code) { //觸發close的回呼函式
		console.log('close:' + code);
		_ffmpeg = null;
	});
	_ffmpeg.on('exit', function (code) {  //觸發exit的回呼函式
		console.log('exit:' + code);
		_ffmpeg = null;
	});
	_ffmpeg.on('error', function (code) { //觸發error的回呼函式
		console.log('error:' + code);
		_ffmpeg = null;
	});
}
videoStream();
setInterval(videoStream, 300000); //每五分鐘檢查一次，若已斷線則重新串流。
