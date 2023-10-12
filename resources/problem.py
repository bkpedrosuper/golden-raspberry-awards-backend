from flask import jsonify, make_response
from flask_restx import Resource
from models.producer_movie import ProducerMovieModel
from models.movie import MovieModel
from models.producer import ProducerModel

from api import api
from db import db

problem_ns = api.namespace(name='Problem', description='Problem Solving Path', path='/problem')

def create_dict_response(producer: str, previous: int, following: int):
    return {
        "producer": producer,
        "interval": following - previous,
        "previousWin": previous,
        "followingWin": following,
    }

def get_max_from_query(partial_result, current_max, max_interval, producer) -> (list, int):
    # Calculate the maximum and minimum years
    max_year = partial_result.order_by(MovieModel.year.desc()).first()[0].year
    min_year = partial_result.order_by(MovieModel.year.asc()).first()[0].year
    subtraction = max_year - min_year

    if subtraction > max_interval:
        max_interval = subtraction
        current_max = [create_dict_response(producer.name, previous=min_year, following=max_year)]
    elif subtraction == max_interval:
        current_max.append(create_dict_response(producer.name, previous=min_year, following=max_year))
    
    return current_max, max_interval

def get_min_from_query(partial_result, current_min, min_interval, producer)  -> (list, int):
    # Find the min difference between two wins
    min_query = partial_result.order_by(MovieModel.year.asc())

    for i in range(1, min_query.count()):
        following_min = min_query[i][0].year
        previous_min = min_query[i - 1][0].year
        subtraction = abs(previous_min - following_min)

        if subtraction < min_interval:
            min_interval = subtraction
            current_min = [create_dict_response(producer.name, previous=previous_min, following=following_min)]
        elif subtraction == min_interval:
            current_min.append(create_dict_response(producer.name, previous=previous_min, following=following_min))
    
    return current_min, min_interval

class Problem(Resource):
    def get(self):
        # Join movies and producers via the producer_movie table and filter for winner movies
        query = db.session.query(MovieModel, ProducerModel) \
        .join(ProducerMovieModel, MovieModel.id == ProducerMovieModel.movie_id) \
        .join(ProducerModel, ProducerModel.id == ProducerMovieModel.producer_id) \
        .filter(MovieModel.winner == 1) \
        
        # Set variables
        mins = []
        maxs = []
        min_interval = float('inf')
        max_interval = float('-inf')
        
        # Get producers
        producers = ProducerModel.query.all()
        
        # Get the max and min for each producer
        for producer in producers:
            pid = producer.id

            # Get winners for producer
            partial_result = query.filter(ProducerModel.id == pid) \
            
            # Only checks if the producer has 2 or more wins
            if partial_result.count() < 2:
                continue
            
            # Update the list of maxs and mins
            maxs, max_interval = get_max_from_query(partial_result, maxs, max_interval, producer)
            mins, min_interval = get_min_from_query(partial_result, mins, min_interval, producer)

        # Return the message in JSON
        return make_response(
            jsonify(
                {
                    "min": mins,
                    "max": maxs,
                }
            ), 200
        )