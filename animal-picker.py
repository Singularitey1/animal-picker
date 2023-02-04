from deepface import DeepFace
from icrawler.builtin import GoogleImageCrawler
import os
import shutil
import wikipedia

# emotion detection
face_analysis = DeepFace.analyze(img_path = "i4.jpg", enforce_detection=False)
dominantEmotion = face_analysis[0]["dominant_emotion"]
face_analysis[0]["emotion"].pop(dominantEmotion)
secondEmotion = max(face_analysis[0]["emotion"])

# sets favorite animal and search query
print(dominantEmotion + " and " + secondEmotion)
favorite_animal = "cat"
query = favorite_animal + " " + dominantEmotion + " and " + secondEmotion + " animal"

# finds image using google image crawler
if os.path.exists("images"):
    shutil.rmtree("images")
image_crawler = GoogleImageCrawler(storage = {"root_dir": r'images'})
filter = dict(type="photo")
image_crawler.crawl(keyword = query, filters=filter, max_num = 1)

# function to search wikipedia for the inputted favorite animal
def searchWikipedia():
    search = wikipedia.search(favorite_animal, results = 1)
    if not search:
        search = wikipedia.suggest(favorite_animal)
        if search == None:
            return "You may want to rewrite your favorite animal."
        result = wikipedia.summary(search + search[-1])
    else:
        result = wikipedia.summary(search[0] + search[0][-1])
    return result

# prints the wikipedia summary of the favorite animal
print(searchWikipedia())
