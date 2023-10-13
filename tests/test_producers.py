import json

def test_create_producer(client):
    """
    Test creating a new producer
    """

    new_producers_data = {
        "name": "bkpedrosuper"
    }
    response = client.post('/producers/', json=new_producers_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["name"] == "bkpedrosuper"

def test_get_producers(client):
    """
    Test to check if the application is creating the correct producers
    """
    response = client.get('/producers/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    producers_names = [producer.name for producer in data]
    expected_producers = ['Allan Carr', 'Buzz Feitshans', 'David Matalon']
    assert len(data) == 3
    assert expected_producers == producers_names

def test_get_producers(client):
    """
    Test to check if the API is correctly loading an specific producer
    """
    # Test getting the details of a specific producers
    response = client.get('/producers/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == 1
    assert data["name"] == "Allan Carr"