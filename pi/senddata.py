"""
Author: Humphrey Shotton
Filename: senddata.py
Version: 1.0 (2014-01-17)

Description:
Pi Car Park sensor server communication module.

Used to send update data about changed in the car parking spaces
to a central server.

"""
import requests
import random
import json
import data.settings as s

def post_request(vals, url):
    """
    Build a post request.

    Args:
        vals: Dictionary of (field, values) for the POST
            request.
        url: URL to send the data to.

    Returns:
        Dictionary of JSON response or error info.
    """
    # Build the request and send to server
    api_data = json.dumps(vals)
    headers = {'content-type': 'application/json'}

    try:
        requests.post(url, data=api_data, headers=headers)
    except:
        return {"error": "Error in connecting to server."}

def send_update(parkingspot_id, status_code, camera_id):
    """
    Sends the data of parking space status to the server
    using a HTTP POST request.

    Args:
        parkingspot_id: ID of the parkingspot
        status_code: Status of the car park.
        camera_id: ID of the camera the parkingspot belongs to

    Returns:
        Dictionary of elements from the JSON response.
    """
    # Create the post data
    vals = {
            "camera_id": camera_id,
            "electric_charge": random.choice([1, 0]),
            "is_available": status_code,
            "parkingspot_id": parkingspot_id}

    # create an array which will be used for the JSON dictionary
    parkingspots = []

    # append the post data to the array
    parkingspots.append(vals)

    #create the correct form in which the data will be sent to the server
    parkingspots_dict = {'parkingspot':parkingspots}

    # get URL from settings.py
    url = s.SERVER_URL

    # check URL
    print("URL IS:  " + url)

    return post_request(parkingspots_dict, url)


def register_area(area_id):
    """
    Sends the data to register a new parking space to the
    server using a HTTP POST request.

    Args:
        area_id: The area id to register.

    Returns:
        Dictionary of elements from the JSON response.
    """
    # Create the post data
    vals = {
            "register_park_id" : s.PARK_ID,
            "register_pi_id" : s.PI_ID,
            "register_area_id" : area_id}

    return post_request(vals, s.SERVER_URL + "register.php")


def deregister_pi():
    """
    Deregisters all areas associated with this pi.
    
    Returns:
        Dictionary of elements from the JSON response.
    """
    # Create the post data
    vals = {"deregister_password" : s.SERVER_PASS,
            "deregister_pi_id" : s.PI_ID}

    return post_request(vals, s.SERVER_URL + "deregister.php")


if __name__ == "__main__":
    # Example for sending updates
    for i in range(0,5):
        j = send_update(i, 1)
        print j

def register_pi(pi_id):
    """
    Sends the data to register a new raspberry pi to the
    server using a HTTP POST request.

    Args:
        pi_id: The pi id to register.

    Returns:
        Dictionary of elements from the JSON response.
    """
    # Create the post data
    vals = {"register_pi_id": pi_id}

    return post_request(vals, s.SERVER_URL)
