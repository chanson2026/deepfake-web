from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os 
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "CR_lab_06" 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #specify upload location
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #limit file size to 16 MB

#create iterable values table for allowed image
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg' 'gif']) 

def allowed_file(filename): #determine input validity, return new usable image url
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/pre_upload', methods=['POST','GET']) #for general site navigation
def not_home():
    if request.method == 'POST': #determine which selection was made
        if request.form['action'] == 'Upload Image':
            return redirect(url_for('home'))
        elif request.form['action'] == 'See Base Video':
            return redirect(url_for('video'))
        elif request.form['action'] == 'Choose Image to Manipulate':
            return redirect(url_for('choice'))
    else:
        return render_template('pre_index3.html')
    
@app.route('/choose_image', methods=['POST','GET']) #allow user to select an image
def choice():
    #long run plan: use variable for image filename, variable for video filename
    #use this through a hash table of string <K,V> pairs
    if request.method == 'POST': #execute one of the three selections
        if request.form['action'] == 'Select Image01':
            return redirect(url_for('first_video'))
        elif request.form['action'] == 'Select Image02':
            return redirect(url_for('second_video'))
        elif request.form['action'] == 'Select Image03':
            return redirect(url_for('video'))
        
    return render_template('image_choice.html')
    
@app.route('/video_content') #show embedded video
def video():
    return render_template('video_content.html')

@app.route('/video_content02')
def second_video():
    return render_template('video_content02.html')

@app.route('/video_content03')
def first_video():
    return render_template('video_content03.html')



@app.route('/') #home route currently, allows image upload (sub-route later)
def home():
    return render_template('index3.html')

@app.route('/', methods=['POST']) #post route for '/' to allow for image upload
def image_upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index3.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>') #defines route to display image upload
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/toolbar')
def toolbar_ex():
    # request actions could be:  
    # 'About', 'What is a Deepfake?'
    # 'How are Deepfakes Used'
    # 'Create Your Own Deepfake'
    # Social and Political Implications
    return render_template('toolbar_demo.html')


'''
@app.route('/about')
def about_page():
    return rendertemplate('about.html')

'''

if __name__ == "__main__":
    app.run(debug=True)