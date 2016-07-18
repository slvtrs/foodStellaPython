
from flask import Flask, request
from flask_restful import Resource, Api

import re
import math
import json
import string
import numpy as np
from sklearn.preprocessing import normalize
from difflib import SequenceMatcher
import nltk
import urlparse
from scipy import spatial
import csv
import itertools

#only in productin
import database_setup

ingredientsfile = open("recipe_ingredients.json", "r")

class Search(Resource):
    def get(self):
		search_array = []

		output_file = open("search_output.txt", "r")
		for line in output_file:
			x = int(line)
			search_array.append(x)
		output_file.close()

		return User.query.all()

class Recommend(Resource):
	def get(self):
		recipe = request.args.get('recipe')
		x = int(recipe)
		file = open("recommender_input.txt", "w")
		file.write(recipe)
		file.close()

		def cosine_similarity(arr1, arr2):
			return 1 - spatial.distance.cosine(arr1, arr2)

		file = open("recommender_dv.txt", "r")


		raw_description_vectors = []

		for line in file:
			newline = line.strip(' ').strip('\n').split(' ')
			#print newline
			raw_description_vectors.append(newline[:-1])

		#print raw_description_vectors
		description_vectors = []
		for line in raw_description_vectors:
			description_vectors.append(map(float, line))

		#output the recipe_id and recipe names of the most similar recipes
		file.close()
		cosine_distances = []

		for j,i in enumerate(description_vectors):
			cosine_distances.append(cosine_similarity(map(float, description_vectors[x-1]), map(float, i)))
			#print cosine_similarity(map(float, mass_fractions_matrix[0]), map(float, i))

		cosine_distances = np.asarray(cosine_distances)
		order = cosine_distances.argsort()

		recommended_array = []
		file = open("recommender_output.txt", "w")
		for i in order[-11:][::-1][1:]:
			file.write(str(i+1))
			file.write('\n')
			recommended_array.append((i+1))
			#print cosine_similarity(map(float, description_vectors[x-1]), map(float, description_vectors[i]))
		file.close()
		return recommended_array



app = Flask(__name__)
api = Api(app)

api.add_resource(Search, '/search')
api.add_resource(Recommend, '/recommend')



if __name__ == '__main__':
    app.run(debug=True)