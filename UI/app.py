from flask import Flask, flash, request, redirect, url_for, render_template
import pandas as pd
from imagescraper import ImageScraper

app = Flask(__name__)
app.config["Debug"] = True
imgscrape = ImageScraper()

matric_factorization_df = pd.read_csv("file2.csv")
knn_df = pd.read_csv("file1.csv")

def get_movie_name(address):
    return address.split("/")[-1].split(".")[0]

@app.route("/homepage", methods=["GET"])
def homepage():
    return render_template("index.html")

@app.route("/show_recommendation", methods=["POST"])
def show_recommendation():
    try:
        user_id = int(request.form["user_id"])
        if not 0 < user_id < 611:
            raise UserIDException(user_id)
        matrix_data = list(matric_factorization_df.iloc[user_id - 1])
        knn_data = list(knn_df.iloc[user_id - 1])
        matrix_send_data = []
        knn_send_data = []
        for x in matrix_data:
            print(x)
            # imgscrape.download_poster(x)
            # matrix_send_data.append("/posters/"+x)
            url = imgscrape.get_poster_url(x)
            matrix_send_data.append(url)
        
        for x in knn_data:
            print(x)
            # imgscrape.download_poster(x)
            # knn_send_data.append("/posters/"+x)
            url = imgscrape.get_poster_url(x)
            knn_send_data.append(url)

        return render_template(
            "portfolio-details.html",
            matrix_data=matrix_send_data,
            knn_data=knn_send_data,
        )

    except UserIDException as e:
        return f"Please enter a userid between 1 and 610, your userid was{str(e.value)}"


class UserIDException(Exception):
    def __init__(self, value):
        self.value = value

    # __str__ is to print() the value
    def __str__(self):
        return repr(self.value)

app.run()