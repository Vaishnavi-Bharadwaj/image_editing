#pip install flask opencv-python
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
import os
import cv2
#the following two lines are got from the flask documentation of how to upload a file to the flask
UPLOAD_FOLDER = 'uploads' #the folder that you are using where the img has to be uploaded 
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'} #the extensions you want to allow

app = Flask(__name__) #define an app

app.secret_key='super secret key' #a secret key has to be defined to run the flashed messages that is included in the index.html

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #this is got from the flask documentation of how to upload a file to the flask
#app.config is used to store configuration settings and options for your Flask application- configures various aspects of your app such as database connections, file upload locations and more


#this is got from the flask documentation of how to upload a file to the flask
#checks if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename,operation):
    print(f"the operation is {operation} and filename is {filename}")
    img=cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcess=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #converting to grayscale 
            cv2.imwrite(f"static/{filename}",imgProcess) #putting the img to static folder after converting
            return filename #this is done so that the filename can be used in the processImage function that is called in the edit function
    pass

@app.route("/") #user gets the message when the home page of the website is accessed
def home():
    return render_template("index.html") #to render a template from the templates folder

@app.route("/about") #user gets the message whatever is displayed in the about page 
def about():
    return render_template("about.html")

@app.route("/edit",methods=["GET","POST"]) #user gets the message("POST request is here") after clicking the submit button  
def edit():
    if request.method=="POST":
        operation=request.form.get("operation") #get the operation that has to be performed
        #this code is got from the flask documentation of uploading a file to the flask
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error" #instead of redirecting to request.url, return error message
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "Error! No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('download_file', name=filename))
            processImage(filename,operation) #call the processImage here 
            flash(f"Processed image available <a href='/static/{filename}' target='_blank'>here</a>") #to display this message to the user on the screen which is styled with the use of flashed category messages in index.html and target='_blank' is used to display the grayscale image on a new tab when the anchor tag here is clicked 
            return render_template("index.html") #use this instead of the above line
        
    return render_template("index.html")

app.run(debug=True) #to start the server