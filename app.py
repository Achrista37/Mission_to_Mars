

#################################################
# Database Setup
#################################################
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars2

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_db = mongo.db.mars_db.find_one()

    # Return template and data
    return render_template("index.html", mars_db=mars_db)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape_all():
    # Run the scrape function
    mars_db = mongo.db.mars_db
    mars_data = scrape_mars2.scrape()
    print(mars_data)
    # Update the Mongo database using update and upsert=True
    mars_db.update_many({}, {"$set": mars_data}, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
