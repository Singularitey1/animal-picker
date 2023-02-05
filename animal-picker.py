from deepface import DeepFace
from icrawler.builtin import GoogleImageCrawler
import os
import shutil
import wikipedia
import random

# emotion detection
face_analysis = DeepFace.analyze(img_path = "guy3.webp", enforce_detection=False)
dominantEmotion = face_analysis[0]["dominant_emotion"]
face_analysis[0]["emotion"].pop(dominantEmotion)
secondEmotion = max(face_analysis[0]["emotion"])

# sets favorite animal and search query
print(dominantEmotion + " and " + secondEmotion)
favorite_animal = "can"
query = favorite_animal + " " + dominantEmotion + " and " + secondEmotion + " animal"

# finds images using google image crawler
if os.path.exists("images"):
    shutil.rmtree("images")
image_crawler = GoogleImageCrawler(storage = {"root_dir": r'images'})
image_crawler.crawl(keyword = query, max_num = 3)

# keeps one random image
randInt = random.randint(1,3)
for file in os.listdir("images"):
    if file != "00000" + str(randInt) + ".jpg":
        os.remove("images/" + file)
    else:
        os.rename("images/" + file, "images/animalImage.jpg")

# function to search wikipedia for the inputted favorite animal
def searchWikipedia():
    search = wikipedia.search(favorite_animal, results = 1)
    if not search:
        search = wikipedia.suggest(favorite_animal)
        if search == None:
            return ["You may have spelled your favorite animal wrong.", "No link found."]
        try:
            result = wikipedia.summary(search, auto_suggest=False)
            link = wikipedia.page(search, auto_suggest=False).url
        except:
            return ["Wikipedia not found. Try to be specific.", "No link found."]
    else:
        try:
            result = wikipedia.summary(search[0], auto_suggest=False)
            link = wikipedia.page(search[0], auto_suggest=False).url
        except:
            return ["Wikipedia not found. Try to be specific.", "No link found."]
    return [result, link]

# prints the wikipedia summary and link of the favorite animal
print(searchWikipedia()[0])
print(searchWikipedia()[1])
