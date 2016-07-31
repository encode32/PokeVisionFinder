import os
import urllib2
from time import sleep,time
import json
from pokemons import pokemonlist

__author__ = 'encode'

_delay = 1 #seconds

_pokeVision = False

_apikey = "" #Your Google Places APIKey

_cities = ["London",
           "NewYork",
           "Tokyo",
           "NewDelhi",
           "WashingtonDC",
           "Beijing",
           "Berlin",
           "Paris",
           "Moscow",
           "Mumbai",
           "Seoul",
           "Toronto",
           "Manchester",
           "Kolkata",
           "HongKong",
           "Shanghai",
           "RioDeJaneiro",
           "Kiev",
           "Manila",
           "Istanbul",
           "Madrid"
           ]

_pokemons = []

#Clear
def _clear():
    #windows
    os.system('cls')
    #linux
    #os.system('clear')

#Sleep
def _sleep():
    sleep(_delay)

#JsonData
def _jsondata(url):
    _rawdata = urllib2.urlopen(url)
    return json.load(_rawdata)

#JsonData Custom Headers
def _jsondatach(url):
    _headers = { 'User-Agent' : 'Mozilla/5.0' }
    _req = urllib2.Request(url, None,_headers)
    _rawdata = urllib2.urlopen(_req)
    return json.load(_rawdata)

#Pokemon Name
def _pokename(id):
    return pokemonlist[id-1]

def _pokesplit(pokemons):
    global _pokemons
    _pokemons = pokemons.split(",")

#POkePrinter
def _printer(name,lat,lng,exp):
    _time = time()
    _remain = exp-time()
    _minutes = int(_remain / 60)
    _seconds = int(_remain % 60)
    print "-------------------------------------------------"
    print "Pokemon: " + name
    print "Coordinates: " + str(lat) + "," + str(lng)
    print "Expires in: " + str(_minutes) + " Minutes, " + str(_seconds) + " Seconds."
    print "-------------------------------------------------"

#Finder
def _finderGo(city):
    print "[INFO] Looking pokemons in: " + city
    _googleacurl = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input="+\
               city+"&types=(cities)&key="+_apikey
    _googleacjsondata = _jsondata(_googleacurl)

    _cityreference = _googleacjsondata['predictions'][0]['reference']

    _googledurl = "https://maps.googleapis.com/maps/api/place/details/json?reference="+\
              _cityreference+"&sensor=true&key="+_apikey
    _googledjsondata = _jsondata(_googledurl)

    _latitude = _googledjsondata['result']['geometry']['location']['lat']
    _longitude = _googledjsondata['result']['geometry']['location']['lng']

    _latitudene = _googledjsondata['result']['geometry']['viewport']['northeast']['lat']
    _longitudene = _googledjsondata['result']['geometry']['viewport']['northeast']['lng']

    _latitudesw = _googledjsondata['result']['geometry']['viewport']['southwest']['lat']
    _longitudesw = _googledjsondata['result']['geometry']['viewport']['southwest']['lng']

    _statusWait = True

    _scanurl = "https://api-live-us1.pokemongo.id/maps?vt=-"+str(_latitudesw)+","+str(_longitudesw)+\
               ","+str(_latitudene)+","+str(_longitudene)+"&u="+str(time())
    _scanurljsondata = _jsondatach(_scanurl)

    for pokename in _pokemons:
        for pokemon in _scanurljsondata['pokemons']:
            _id = pokemon['pokemon_id']
            _name = _pokename(_id)
            if pokename.lower() in _name.lower():
                _lat = pokemon['latitude']
                _lng = pokemon['longitude']
                _exp = pokemon['expires']
                _printer(_name, _lat, _lng, _exp)

#Finder
def _finderPokeVision(city):
    print "[INFO] Looking pokemons in: " + city
    _googleacurl = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input="+\
               city+"&types=(cities)&key="+_apikey
    _googleacjsondata = _jsondata(_googleacurl)

    _cityreference = _googleacjsondata['predictions'][0]['reference']

    _googledurl = "https://maps.googleapis.com/maps/api/place/details/json?reference="+\
              _cityreference+"&sensor=true&key="+_apikey
    _googledjsondata = _jsondata(_googledurl)

    _latitude = _googledjsondata['result']['geometry']['location']['lat']
    _longitude = _googledjsondata['result']['geometry']['location']['lng']

    _latitudene = _googledjsondata['result']['geometry']['viewport']['northeast']['lat']
    _longitudene = _googledjsondata['result']['geometry']['viewport']['northeast']['lng']

    _latitudesw = _googledjsondata['result']['geometry']['viewport']['southwest']['lat']
    _longitudesw = _googledjsondata['result']['geometry']['viewport']['southwest']['lng']

    _coords = [[_latitude,_longitude],
        [_latitudene,_longitudene],
        [_latitudesw,_longitudesw]]
    for _coord in _coords:

        _statusWait = True

        _scanurl = "https://pokevision.com/map/scan/"+str(_coord[0])+"/"+str(_coord[1])
        _scanurljsondata = {}

        while _statusWait:
            _scanurljsondata = _jsondatach(_scanurl)
            _status = _scanurljsondata['status']
            _sleep()
            if 'success' in _status: _statusWait = False
        _jobid = _scanurljsondata['jobId']

        _jobStatus = True

        _dataurl = "https://pokevision.com/map/data/"+str(_coord[0])+"/"+str(_coord[1])+"/"+_jobid
        _dataurljsondata = {}

        while _jobStatus:
            _dataurljsondata = _jsondatach(_dataurl)
            _sleep()
            if 'jobStatus' not in _dataurljsondata: _jobStatus = False

        for pokename in _pokemons:
            for pokemon in _dataurljsondata['pokemon']:
                _id = pokemon['pokemonId']
                _name = _pokename(_id)
                if pokename.lower() in _name.lower():
                    _lat = pokemon['latitude']
                    _lng = pokemon['longitude']
                    _exp = pokemon['expiration_time']
                    _printer(_name, _lat, _lng, _exp)

#Loop
def _loop():
    for city in _cities:
        if _pokeVision:
            _finderPokeVision(city)
        else:
            _finderGo(city)

#Init
_inputpoke = raw_input("Pokemon: ")
_pokesplit(_inputpoke)
_loop()
