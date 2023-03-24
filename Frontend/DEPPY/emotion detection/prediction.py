#--------------------------------------------------------------------------------------------------------------------------------------------------------
# The cv2 module 
#   is a package for computer vision tasks. It is a wrapper around the OpenCV library, which is written in C++ and provides a large number of functions 
#   for image processing and computer vision tasks.

# numpy module 
#   is a numerical computing library for Python. It provides functions for working with large, multi-dimensional arrays and matrices of numerical data.

# load_model function 
#   from the keras.models module can be used to load a trained Keras model from a file. Keras is a high-level neural network library that runs 
#   on top of other lower-level libraries such as TensorFlow.

# Flask class 
#    from the flask module is a web microframework for Python. It provides a lightweight way to build web applications and APIs.

# render_template function 
#   from the flask module is used to render HTML templates.

# Response class 
#   from the flask module is used to create an HTTP response that can be returned by a Flask application
#--------------------------------------------------------------------------------------------------------------------------------------------------------
import cv2
import numpy as np
from keras.models import load_model
from flask import Flask, render_template, Response

# Load the cascade classifier for detecting faces
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load the trained model 
model = load_model('fer2013_100epochs.h5')

# define the Labels_dict with emotions 
labels_dict = {0:'Angry', 1:'Disgust', 2:'Fear', 3:'Happy', 4:'Neutral', 5:'Sad', 6:'Surprise'}

# Set up the video capture (0-machine web cam, 1- external web cam)
video = cv2.VideoCapture(0)

# For a recorded vedio input
#video_path = "./video/3.mp4"
#video = cv2.VideoCapture(video_path)

def gen_frames():
     # Initialize variables to store the emotion count
    emotion_count = {'Happy': 0, 'Sad': 0, 'Angry': 0, 'Fear': 0, 'Surprise': 0, 'Neutral': 0, 'Disgust': 0 }
    total_frames = 0
    
    happiness_percent = 0
    sadness_percent = 0
    anger_percent = 0
    fear_percent = 0
    surprise_percent = 0
    neutral_percent = 0
    disgust_percent = 0

    while video.isOpened():

        # Read frame from video capture
        success, frame = video.read()              

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Iterate over each face
        for (x, y, w, h) in faces:

            total_frames += 1

            #image pre-processing and normalization (match with the trained model)
            sub_face_image = gray[y:y+h, x:x+w]
            resized = cv2.resize(sub_face_image,(48,48))
            normalize = resized/255.0
            reshaped = np.reshape(normalize,(1,48,48,1))

            #prediction
            result = model.predict(reshaped)
            label = np.argmax(result, axis=1)[0]

            #draw the rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, labels_dict[label], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1)

            # Extract the label and probability of the highest predicted emotion
            top_emotion = labels_dict[label]

            # Increment the count for the emotion
            emotion_count[top_emotion] += 1

            # Calculate the percentage of each emotion
            happiness_percent = emotion_count['Happy'] / total_frames * 100
            sadness_percent = emotion_count['Sad'] / total_frames * 100
            anger_percent = emotion_count['Angry'] / total_frames * 100
            fear_percent = emotion_count['Fear'] / total_frames * 100
            surprise_percent = emotion_count['Surprise'] / total_frames * 100
            neutral_percent = emotion_count['Neutral'] / total_frames * 100
            disgust_percent = emotion_count['Disgust'] / total_frames * 100

            cv2.putText(frame, f'Happiness: {happiness_percent:.2f}%'   , (5, 15),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 0)
            cv2.putText(frame, f'Neutral: {neutral_percent:.2f}%'       , (5, 35),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 0)
            cv2.putText(frame, f'Sadness: {sadness_percent:.2f}%'       , (5, 55),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 0)
            cv2.putText(frame, f'Fear: {fear_percent:.2f}%'             , (5, 75),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 0)
            cv2.putText(frame, f'Surprise: {surprise_percent:.2f}%'     , (5, 95),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 0)
            cv2.putText(frame, f'Disgust: {disgust_percent:.2f}%'       , (5, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 0)
            cv2.putText(frame, f'Anger: {anger_percent:.2f}%'           , (5, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 0)


        if not success:
            break
        else:
            # encode an image frame in JPEG format, and then returning the resulting bytes as a generator.
            _, jpeg = cv2.imencode('.jpg', frame)

            # Yield the frame to the web browser
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

        
        # Save the final probability report to a file
        report_filename = 'emotion_report.txt'
        with open(report_filename, 'w') as report_file:
            report_file.write('Probability Report:\n')
            report_file.write('===================\n')
            report_file.write(f'Neutral: {neutral_percent:.2f}%\n')
            report_file.write(f'Sadness: {sadness_percent:.2f}%\n')
            
            report_file.write('- - - - - - - - - - \n')
            report_file.write(f'Surprise: {surprise_percent:.2f}%\n')
            report_file.write(f'Disgust: {disgust_percent:.2f}%\n')
            report_file.write(f'Happiness: {happiness_percent:.2f}%\n')
            report_file.write(f'Anger: {anger_percent:.2f}%\n')
            report_file.write(f'Fear: {fear_percent:.2f}%\n')
            report_file.write('\n\n')
            
            depressed_percent = sadness_percent+ neutral_percent/2 
            non_depressed_percent = happiness_percent + surprise_percent/2 + neutral_percent/2 + disgust_percent/2 + anger_percent/2 + fear_percent/2
           
            report_file.write(f'Depression prob% : {depressed_percent:.2f}%\n')
            report_file.write(f'Non-Depression prob%: {non_depressed_percent:.2f}%\n')
                    
            report_file.write('\nPREDICTION: ')
            report_file.write( "Depression detected" if depressed_percent>non_depressed_percent else "No depression detected") 
            

#Initialize the Flask app
app = Flask(__name__)

#Define app route for default page of the web-app :
@app.route('/')
def index():
    return render_template('index.html')

#Define app route for the Video feed:
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

#starting the flask server
if __name__ == "__main__":
    app.run()