from flask import Flask, request, render_template
import os
import matplotlib.pyplot as plt
import functions as fn
import audio_features
import soundfile
import io
from werkzeug.utils import secure_filename
app = Flask(__name__)
UPLOAD_FOLDER = "./"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
@app.route("/",methods=['GET','POST'])
def index():

    if(request.method=='GET'):
        # features_list=audio_features.feature_extraction_array('./my-rec.wav')
        try:
            prediction=fn.apply_model('./my-rec.wav')
            img, fig = fn.plot_melspectrogram('./my-rec.wav')
            fig.colorbar(img, format="%+2.f")
            spectro = plt.savefig('./static/spectro.png')
            result_1 = fn.Names_return(prediction)
        except:

            result_1=["please record", "a longer file"]
        
        spectro = True
        return render_template('index.html',voice_prediction= result_1[0],speech_prediction=result_1[1],spectro=spectro)
    else:
        if 'data' in request.files:
            url = "http://127.0.0.1:5000/"
            file = request.files['data']
            
            # Write the data to a file.
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            
            # Jump back to the beginning of the file.
            file.seek(0)
            
            # Read the audio data again.
            data, samplerate = soundfile.read(file)
            soundfile.write('my-rec.wav', data, samplerate)
            # fn.iter += 1
            #print(fn.iter)
            # with open("my-rec.wav", 'rb') as fp:
            #     audio = fp.read()
            # result = request.post(url, data=audio)
            # features_list=result.text

            # voice_prediction=""
            # speech_prediction=""
    # print(result_1[0])
            return render_template('index.html')



if __name__ == '__main__':        

    app.run(debug=True)