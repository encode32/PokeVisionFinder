import os
from sys import argv
import urllib2
from time import sleep,time
import json
from pokemons import pokemonlist
import httplib

__author__ = 'encode'

_delay = 5 #seconds

_useMode = "Skip" #Skip,Go

_logging = True

_zoomFactor = 1 #1 = 0.05 = 13.85Km

_nonstop = False

_cities = []

_pokemons = []

_pokemonslisted = []

#PokeSniper2 Configuration
ps_use = True
ps_path = ""
ps_dir = ""

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
    try:
        _rawdata = urllib2.urlopen(url)
        return json.load(_rawdata)
    except urllib2.HTTPError, e:
        print '[ERROR] HTTPError = ' + str(e.code)
        return _jsondata(url)
    except urllib2.URLError, e:
        print '[ERROR] URLError = ' + str(e.reason)
        return _jsondata(url)
    except httplib.HTTPException, e:
        print '[ERROR] HTTPException'
        return _jsondata(url)
    except Exception:
        import traceback
        print '[ERROR] generic exception: ' + traceback.format_exc()
        return _jsondata(url)

#JsonData Custom Headers
def _jsondatach(url):
    try:
        _headers = { 'User-Agent' : 'Mozilla/5.0' }
        _req = urllib2.Request(url, None,_headers)
        _rawdata = urllib2.urlopen(_req)
        return json.load(_rawdata)
    except urllib2.HTTPError, e:
        print '[ERROR] HTTPError = ' + str(e.code)
        return _jsondatach(url)
    except urllib2.URLError, e:
        print '[ERROR] URLError = ' + str(e.reason)
        return _jsondatach(url)
    except httplib.HTTPException, e:
        print '[ERROR] HTTPException'
        return _jsondatach(url)
    except Exception:
        import traceback
        print '[ERROR] generic exception: ' + traceback.format_exc()
        return _jsondatach(url)

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
    _expire = str(_minutes) + " Minutes, " + str(_seconds) + " Seconds"
    print "-------------------------------------------------"
    print "Pokemon: " + name
    print "Coordinates: " + str(lat) + "," + str(lng)
    print "Expires in: " + _expire
    print "-------------------------------------------------"
    _logPokemon(name, str(lat), str(lng), _expire)

#Logger
def _logPokemon(name, lat, lng, expire):
    with open("pokemons.log", "a+") as f:
        f.write("[" + name + "] [" + lat + "," + lng + "] [" + expire + "]\n")
        f.close()

#CoordsLoader
def _populateCities():
    with open("coords.txt", "a+") as f:
        _data = f.readlines()
        for line in _data:
            _citydata = line.split(":")
            _cities.append([_citydata[0],_citydata[1],_citydata[2]])
        f.close()

#Finder
def _finderSkipLagged(city):
    print "[INFO] Looking pokemons in: " + city[0]
    _latitudesw = float(city[1]) - (0.05 * _zoomFactor)
    _longitudesw = float(city[2]) - (0.05 * _zoomFactor)
    _latitudene = float(city[1]) + (0.05 * _zoomFactor)
    _longitudene = float(city[2]) + (0.05 * _zoomFactor)

    _scanurl = "https://skiplagged.com/api/pokemon.php?bounds="+str(_latitudesw)+","+str(_longitudesw)+\
               ","+str(_latitudene)+","+str(_longitudene)
    _scanurljsondata = _jsondatach(_scanurl)

    for pokename in _pokemons:
        try:
            for pokemon in _scanurljsondata['pokemons']:
                _id = pokemon['pokemon_id']
                _name = _pokename(_id)
                if pokename.lower() in _name.lower():
                    _lat = pokemon['latitude']
                    _lng = pokemon['longitude']
                    _exp = pokemon['expires']
                    _combo = _name+str(_lat)+str(_lng)
                    if _combo not in _pokemonslisted:
                        _pokemonslisted.append(_combo)
                        _printer(_name, _lat, _lng, _exp)
                        if ps_use: _pokeSniper(_name, str(_lat), str(_lng))
                    else:
                        print "[INFO] Pokemon already listed found."
        except KeyError, e:
            print '[ERROR] KeyError = ' + str(e)
        except IndexError, e:
            print '[ERROR] IndexError = ' + str(e)

#Finder
def _finderGo(city):
    print "[INFO] Looking pokemons in: " + city
    _latitudesw = float(city[1]) - (0.05 * _zoomFactor)
    _longitudesw = float(city[1]) - (0.05 * _zoomFactor)
    _latitudene = float(city[2]) + (0.05 * _zoomFactor)
    _longitudene = float(city[2]) + (0.05 * _zoomFactor)

    _scanurl = "https://api-live-us1.pokemongo.id/maps?vt=-"+str(_latitudesw)+","+str(_longitudesw)+\
               ","+str(_latitudene)+","+str(_longitudene)+"&u="+str(time())
    _scanurljsondata = _jsondatach(_scanurl)

    for pokename in _pokemons:
        try:
            for pokemon in _scanurljsondata['pokemons']:
                _id = pokemon['pokemon_id']
                _name = _pokename(_id)
                if pokename.lower() in _name.lower():
                    _lat = pokemon['latitude']
                    _lng = pokemon['longitude']
                    _exp = pokemon['expires']
                    _printer(_name, _lat, _lng, _exp)
        except KeyError, e:
            print '[ERROR] KeyError = ' + str(e)
        except IndexError, e:
            print '[ERROR] IndexError = ' + str(e)

#Sniper
def _pokeSniper(name, lat, lng):
    os.chdir(ps_dir)
    os.system(ps_path+" "+name+" "+lat+" "+lng)

#Loop
def _loop():
    for city in _cities:
        _sleep()
        if "Skip" in _useMode:
            _finderSkipLagged(city)
        elif "Go" in _useMode:
            _finderGo(city)

#Init
_inputpoke = ""

_populateCities()
if len(argv) == 2:
    # If argv[1] is less than 10 (catch.txt) use file
    if len(argv[1]) < 10:
        _inputpoke = [line.strip() for line in open(argv[1], 'r')]
    # Else the user want to type in manually.
    else: _inputpoke = argv[1]
elif len(argv) == 5:
    if len(argv[1]) < 10:
        _inputpoke = [line.strip() for line in open(argv[1], 'r')]
    else:
        _inputpoke = argv[1]
        _pokesplit(_inputpoke)
    _nonstop = int(argv[2]) == 1
    _zoomFactor = float(argv[3])
    _logging = int(argv[4]) == 1
else:
    _inputpoke = raw_input("Pokemon: ")
    _pokesplit(_inputpoke)

if _nonstop:
    while 1:
        _loop()
        _sleep()
else:
    _loop()
