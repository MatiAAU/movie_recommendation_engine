import pandas
from ast import literal_eval
import wx
import gui
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the data from the csv files with the use of pandas
movies = pandas.read_csv('tmdb_5000_movies.csv')
credits = pandas.read_csv('tmdb_5000_credits.csv')

# Add 'cast' and 'crew' columns to the movies data frame
movies['cast'] = credits['cast']
movies['crew'] = credits['crew']

# Create a list of features(most important keywords) we are going to use to make recommendations
features = ['keywords', 'cast', 'crew', 'genres']

# Parsing is the process of analyzing text made of a sequence of tokens to determine its grammatical
# structure with respect to a given (more or less) formal grammar. ...
# This data structure can then be used by a compiler, interpreter or translator to create an executable
# program or library.

# Parse the stringifies features into their corresponding python objects
for feature in features:
    movies[feature] = movies[feature].apply(literal_eval)


# In this function, we are extracting the director's name from the crew feature
def get_director(d):
    for x in d:
        if x['job'] == 'Director':
            return x['name']


# Here we apply the get_director() function to the 'director' column in movies
movies['director'] = movies['crew'].apply(get_director)


# The isinstance() function checks if the object (first argument)
# is an instance or subclass of classinfo class (second argument).

# In this function, we create a list of the top 3 elements
# or if there are less than 3 elements we return entire list
def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names


# We need to define the list of our features one more time to apply the get_list() function
features = ['keywords', 'cast', 'genres']

for feature in features:
    movies[feature] = movies[feature].apply(get_list)


# In this function, we convert every string to lower case and get rid of spaces.
# This is done in order to avoid the vectorizer confusing, for example, the same first names of directors

def clean(x):
    if isinstance(x, list):
        return [str.lower(i.replace('', '')) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(' ', ''))
        else:
            return ''

features = ['keywords', 'cast', 'director', 'genres']

for feature in features:
    movies[feature] = movies[feature].apply(clean)


# We can now build the merge_features() function. This function will return a string
# containing all of the metadata about the movies that we need to create recommendations.

def merge_features(x):
    return ' '.join(x['keywords']) + ' ' \
           + ' '.join(x['cast']) + ' ' \
           + x['director'] + ' ' \
           + ' '.join(x['genres'])

movies['combined_features'] = movies.apply(merge_features, axis=1)

# After creating the 'combined_features' column, we can inject its strings into a CountVectorizer() object
# to get the count_matrix and cosine_similarity.

# Here we create new CountVectorizer() object from sklearn
cv = CountVectorizer(stop_words='english')

# Now we insert all the movie metadata we are using into the CountVectorizer() object
count_matrix = cv.fit_transform(movies['combined_features'])

# Finally, we count the cosine similarity to obtain the 'similarity score'(distance) between movies
cos_sim = cosine_similarity(count_matrix, count_matrix)

# We need to reset the index of our dataframe so that later we can get the index of a movie
# based on the provided title
movies = movies.reset_index()
idx = pandas.Series(movies.index, index=movies['title'].str.lower())

# In the recommend_movies() function, we take the film title together with the cosine_similarity score
# to return the ten most meaningful recommendations for the provided movie title by the user

def recommend_movies(title, cos_sim1=cos_sim):

    title = title.lower()

    # First, we get the index of the movie for the inserted title
    movie_index = idx[title]

    # Then we compute the cosine similarity scores of all movies in the dataset to the one provided by the user
    similarity_scores = list(enumerate(cos_sim1[movie_index]))

    # The movies are then sorted based on their similarity ratings.
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Next, we obtain the similarity scores of the 10 most related movies
    similarity_scores = similarity_scores[1:11]

    # Here we acquire the indices of those most similar movies
    recommended_movies = [i[0] for i in similarity_scores]

    # Finally, we convert the dataframe to be a list for later use
    # and return the titles of the 10 recommended movies
    recommendations = movies['title'].iloc[recommended_movies].values.tolist()
    return recommendations

# GRAPHICAL USER INTERFACE

if __name__ == '__main__':
    app = wx.App()
    frame = gui.MyFrame()
    app.MainLoop()
