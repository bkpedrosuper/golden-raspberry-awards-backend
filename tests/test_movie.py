import json
import pandas as pd
import os
import pytest
from decouple import config

def test_create_movie(client):
    """
    Test creating a new movie
    """
    # Test creating a new movie
    new_movie_data = {
        "title": "The Shawshank Redemption",
        "year": 1994,
        "winner": 0,
    }
    response = client.post("/movies/", json=new_movie_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["title"] == "The Shawshank Redemption"
    assert data["year"] == 1994

def test_get_all_movies(client):
    """
    Test to check if the application is creating the same number of movies from movielist_test.csv
    """
    response = client.get('/movies/')
    assert response.status_code == 200

    test_path = config('DB_TEST_PATH')
    data = json.loads(response.data)
    df_data = pd.read_csv(f"{os.getcwd()}/{test_path}", sep=';')
    
    assert len(data) == df_data.shape[0]

def test_get_movie(client):
    """
    Test: the API is returning a single movie correctly
    """
    # Test getting the details of a specific movie
    response = client.get("/movies/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == 1
    assert data["title"] == "Can't Stop the Music"
    assert data["year"] == 1980

@pytest.mark.parametrize("winner_param", ["true", "false"])
def test_winning_movies(client, winner_param):
    response = client.get(f'/movies/?winner={winner_param}')

    assert response.status_code == 200
    data = json.loads(response.data)
    movies = data['data']

    expected_winner = 1 if winner_param == "true" else 0
    for movie in movies:
        assert movie['winner'] == expected_winner
