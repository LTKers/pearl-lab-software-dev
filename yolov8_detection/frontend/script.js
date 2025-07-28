const video = document.getElementById('webcam');
const processedImg = document.getElementById('processed');
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    console.error('Error accessing webcam:', err);
  });

async function sendFrame() {
  if (video.readyState < 2) { 
    return;
  }

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const base64img = canvas.toDataURL('image/jpeg');

  try {
    const response = await fetch('https://your-app.herokuapp.com/detect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: base64img })
    });

    const data = await response.json();

    processedImg.src = data.processed_image;

    console.log('Detections:', data.detections);

  } catch (error) {
    console.error('Error sending frame:', error);
  }
}

setInterval(sendFrame, 500);