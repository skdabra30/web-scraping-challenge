from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scraper")

@app.route("/")
def home():

    mars_info = mongo.db.mars_info.find_one()

    return render_template("index.html", mars_dict=mars_info)

@app.route("/scrape")
def data_scrape():

    import scrape_mars

    mars_info = mongo.db.mars_info

    mars_data = scrape_mars.scrape()

    mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=False)