import yaml
import requests
import json

## Declarations
authfile = "/Users/Jonny/Documents/genius_api_auth.txt"
base_url = "http://api.genius.com"
search_url = base_url + "/search"

# Prepare authorization
auth_info = open(authfile,'r')
auth_string = auth_info.read()
auth_dict = yaml.load(auth_string)
headers = {'Authorization' : 'Bearer {}'.format(auth_dict['access'])}

def _get(path, params=None, headers=None):

    url = '/'.join([base_url, path])
    if not headers:
        headers = {'Authorization': 'Bearer {}'.format(auth_dict['access'])}

    response = requests.get(url=url, params=params, headers=headers)

    return response.json()

def _search(term, params=None, headers=None):
    if params:
        search_param['q'] = term
    else:
        search_param = {'q':term}

    if not headers:
        headers = {'Authorization': 'Bearer {}'.format(auth_dict['access'])}

    request = requests.get(search_url,params=search_param,headers=headers)
    request_json = request.json()
    request_json = request_json['response']['hits']
    return request_json

def get_artist_id(artist_name):
    # Search for the artist, but since genius API only returns songs...
    search_results = _search(artist_name)
    # iterate through songs
    for i in range(len(search_results)):
        this_artist_name = search_results[i]['result']['primary_artist']['name']
        if artist_name == this_artist_name:
            artist_id = search_results[i]['result']['primary_artist']['id']
            break

    return artist_id

def get_artist_songs(artist_name):
    print "Getting songs for {}".format(artist_name)
    artist_id = get_artist_id(artist_name)
    current_page = 1
    next_page = True
    songs = []

    print "Got ID: {}".format(artist_id)

    while next_page:

        path = "artists/{}/songs/".format(artist_id)
        params = {'page': current_page}
        data = _get(path=path, params=params)

        page_songs = data['response']['songs']

        if page_songs:
            for asong in page_songs:
                if asong['primary_artist']['name'] == artist_name:
                    songs.append(asong)

            current_page += 1
        else:
            next_page = False

    return songs
