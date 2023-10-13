import json

def test_problem(client):
    """
    Checks if the problem is being correctly solved by the API
    """
    response = client.get('/problem/')
    data = json.loads(response.data)
    
    expected_max = {
        "followingWin": 1994,
        "previousWin": 1985,
        "interval": 9,
        "producer": "Buzz Feitshans"
    }

    expected_min = {
        "followingWin": 1994,
        "previousWin": 1990,
        "interval": 4,
        "producer": "David Matalon"
    }

    assert data['max'][0]['followingWin'] == expected_max["followingWin"]
    assert data['max'][0]['previousWin'] == expected_max["previousWin"]
    assert data['max'][0]['interval'] == expected_max["interval"]
    assert data['max'][0]['producer'] == expected_max["producer"]

    assert data['min'][0]['followingWin'] == expected_min["followingWin"]
    assert data['min'][0]['previousWin'] == expected_min["previousWin"]
    assert data['min'][0]['interval'] == expected_min["interval"]
    assert data['min'][0]['producer'] == expected_min["producer"]