from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    try:
        mars = mongo.db.mars.find_one()
    except:
        return "mongo bork!"
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    try:
        mars = mongo.db.mars
    except:
        return "mongo bork!"
    try:
        mars_data = scraping.scrape_all()
    except:
        return "scraping bork!"
    try:
        mars.update_one({}, {"$set":mars_data}, upsert=True)
    except:
        return "mongo bork!"
    return redirect('/', code=302)


if __name__ == "__main__":
    app.run()







