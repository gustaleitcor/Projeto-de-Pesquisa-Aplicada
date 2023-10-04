import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pprint
# from pytrends.request import TrendReq

movies = pd.read_csv("imdb_top_1000.csv")

names = movies["Series_Title"]
years = movies["Released_Year"]
imdb = movies["IMDB_Rating"]
metarating = movies["Meta_score"]
gross = movies["Gross"]


directors = []
for x in movies["Director"]:
    if x not in directors:
        directors.append(x)

MeanRatings = []
for x in directors:
    # DirectorX eh uma variavel temporaria usada apenas neste loop
    DirectorX = movies[movies["Director"] == x]
    MeanRatings.append(np.mean(DirectorX["IMDB_Rating"]))


# Initialize lists to store data
director_coefficients = []
all_bilheteriaOrdenada = []
all_imdb_ratings = []

# Iterate through directors
for x in directors:
    # Filter movies for the current director
    tempData = movies[movies["Director"] == x]

    # Remove rows with NaN values in the "Gross" column
    tempData = tempData.dropna(subset=["Gross"])

    # Convert "Gross" values to integers after removing commas
    bilheteriaOrdenada = [int(str(x).replace(',', ''))
                          for x in tempData["Gross"]]

    # Extract IMDB ratings
    imdb_ratings = tempData["IMDB_Rating"]

    # Check if there are enough data points to fit a linear regression model
    if len(bilheteriaOrdenada) > 1:
        # Plot the data points
        plt.plot(imdb_ratings, bilheteriaOrdenada, 'ro')

        # Fit a linear regression model
        coefficients = np.polyfit(
            np.log(bilheteriaOrdenada), np.log(imdb_ratings.to_list()), 1)

        for bilheteria in bilheteriaOrdenada:
            all_bilheteriaOrdenada.append(bilheteria)
        for rate in imdb_ratings.to_list():
            all_imdb_ratings.append(rate)

        # Append the coefficients to the list
        director_coefficients.append((x, coefficients))

all_coefficients = coefficients = np.polyfit(
    all_bilheteriaOrdenada, all_imdb_ratings, 1)
print(director_coefficients)


for director_coefficient in director_coefficients:
    def f(x):
        return director_coefficient[1][0]*np.log(x) + director_coefficient[1][1]

    if director_coefficient[1][0] > 10 or director_coefficient[1][1] > 10:
        continue

    # ax = plt.subplots()
    # ax.plot(x, f(x))
    # ax.set_xscale('log')

    x = np.linspace(0, 10**8)
    plt.plot(x, f(x), color='red')
    # plt.ylim(7, 10)


def f(x):
    return all_coefficients[0]*x + all_coefficients[1]


x = np.linspace(0, 10**8)
plt.plot(x, f(x), color='red')
plt.ylim(7, 10)

for x in director_coefficients:
    p = np.poly1d([x[1][0], x[1][1]])
    print(p)
