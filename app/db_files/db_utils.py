import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import os
from app.models.movie import MovieModel
from app.models.producer import ProducerModel
from app.models.producer_movie import ProducerMovieModel
from flask import Flask
import sys
import re
from decouple import config

import logging
logging.basicConfig(level=logging.DEBUG)  # Set log level to DEBUG


def insert_movies_from_df(df: pd.DataFrame, db: SQLAlchemy):
    movies = []
    for _, row in df.iterrows():
        winner = 1 if row.winner == 'yes' else 0

        movies.append(
            MovieModel(
                title = row.title,
                year = row.year,
                winner= winner,
                )
        )
    [db.session.add(movie) for movie in movies]
    db.session.commit()


def insert_producers_from_df(df: pd.DataFrame, db: SQLAlchemy):
    all_producers = []
    for _, row in df.iterrows():
        # Get a list of producer_movies spliting them by ' and ' and ','
        producer_movies_list: list[str] = re.split(r' and |,', row.producers)

        # FIX THIS
        if "" in producer_movies_list:
            producer_movies_list.remove("")

        all_producers.extend(producer_movies_list)
    
    for producer_name in all_producers:
        try:
            producer = ProducerModel(name=producer_name)
            db.session.add(producer)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def insert_producers_movie_from_df(df: pd.DataFrame, db: SQLAlchemy):
    for _, row in df.iterrows():
        
        # Get the movie from row
        try:
            existing_movie = MovieModel.query.filter_by(title=row.title).first()
        except NoResultFound:
            print(f'Could not find movie {row.title}')
            sys.exit(0)

        # Get a list of producer_movies spliting them by ' and ' and ','
        producer_movies_list: list[str] = re.split(r' and |,', row.producers)

        # FIX THIS
        if "" in producer_movies_list:
            producer_movies_list.remove("")

        # Create a producer_movie for every relation
        for producer_name in producer_movies_list:
            existing_producer = ProducerModel.query.filter_by(name=producer_name.strip()).first()

            try:
                producer_movie = ProducerMovieModel(movie_id=existing_movie.id, producer_id=existing_producer.id)
                db.session.add(producer_movie)
            except IntegrityError:
                db.session.rollback()  
            except Exception as e:
                print(f'Error: {str(e)}')
    db.session.commit()


def populate_db(db: SQLAlchemy, app: Flask, test=False):
    app.logger.info(f'Populating Database...')
    with app.app_context():
        db.drop_all() # DELETE ALL DATA FROM DATABASE
        db.create_all() # CREATE ALL TABLES
        database_path = config('DB_PATH')
        if test:
            database_path = config('DB_TEST_PATH')
        
        database_df = pd.read_csv(f'{os.getcwd()}/{database_path}', sep=';') # read csv


        insert_movies_from_df(database_df, db)
        insert_producers_from_df(database_df, db)
        insert_producers_movie_from_df(database_df, db)