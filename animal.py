# importing Flask and other modules
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from deepface import DeepFace
from icrawler.builtin import GoogleImageCrawler
import shutil
import wikipedia
import random

# Flask constructor
app = Flask(__name__)  

#Image contsructor using Jinja Static images
#img = os.path.join('static', 'Image')

#Confugres upload folder ?
upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder

#images_folder = os.path.join('images')
#app.config['UPLOAD2'] = images_folder

#upload_folder2 = os.path.join('images')
#app.config['UPLOAD_FOLDER'] = images
#Temporary method to contain AI/ML algos


# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def submit_data():
    if request.method == "POST":
                
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        
        img = os.path.join(app.config['UPLOAD'], filename) #Full file path
        
        favAnimal = request.form.get("aName") #name of favorite animal
        
                # emotion detection
        face_analysis = DeepFace.analyze(img_path = img, enforce_detection=False)
        dominantEmotion = face_analysis[0]["dominant_emotion"]
        face_analysis[0]["emotion"].pop(dominantEmotion)
        secondEmotion = max(face_analysis[0]["emotion"])

        # sets favorite animal and search query
        print(dominantEmotion + " and " + secondEmotion)
        favorite_animal = "dog"
        query = favorite_animal + " " + dominantEmotion + " and " + secondEmotion + " animal"

        # finds images using google image crawler
        if os.path.exists("images"):
            shutil.rmtree("images")
        filter = dict(type="photo")
        image_crawler = GoogleImageCrawler(storage = {"root_dir": r'images'})
        image_crawler.crawl(keyword = query, filters = filter, max_num = 3)

        # keeps one random image
        randInt = random.randint(1,3)
        for file in os.listdir("images"):
            if file != "00000" + str(randInt) + ".jpg":
                os.remove("images/" + file)
            else:
                os.rename("images/" + file, "images/animalImage.jpg")
        
        """file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD2'], 'animalImage.jpg'))
        img2 = os.path.join(app.config['UPLOAD2'], 'animalImage.jpg') #Full file path

        #foundImagePath = os.path.join("images", "animalImage.jpg")
        print(img)"""
        #PEOPLE_FOLDER = os.path.join('images')

        #app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
        #img2 = os.path.join(app.config['UPLOAD_FOLDER'], 'animalImage.jpg')
        
        return render_template('index.html', description = favAnimal, foundImage="http://127.0.0.1:5000/images/animalImage.jpg")

    """# getting input with name = fname in HTML form
       
       filepath = os.path.join(img, 'Smile.jpg')
       # getting input with name = lname in HTML form
       return  render_template("index.html", foundImage = filepath, description = newAnimal) #, description = "", foundImage = "")"""
    return render_template("index.html")
 
#Default Home Page
@app.route('/')
def home(): 
    return render_template("index.html")

if __name__=='__main__':
   app.run()