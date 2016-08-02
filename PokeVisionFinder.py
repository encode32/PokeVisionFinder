import os
from sys import argv
import urllib2
import traceback
import argparse
from time import sleep,time
import json
from pokemons import pokemonlist
import httplib
import re
import requests

__author__ = 'encode'

_cities = []

_pokemons = []

_pokemonslisted = []

_session =requests.Session()
_sessionid = ""

_scriptpath = os.path.dirname(os.path.realpath(__file__))
#PokeSniper2 Configuration
ps_use = True
ps_path = _scriptpath+"\Sniper\PokeSniper2.exe"
ps_dir = _scriptpath+"\Sniper"

#ErrorLogger
def _logError(error):
    os.chdir(_scriptpath)
    with open("errors.log", "a+") as f:
        f.write(error + "\n")
        f.close()

#JsonData
def _jsondata(url):
    try:
        _rawdata = urllib2.urlopen(url)
        return json.load(_rawdata)
    except urllib2.HTTPError, e:
        if _verbose == 1:
            print '[ERROR] HTTPError'
        elif _verbose == 2:
            print '[ERROR] HTTPError = ' + str(e)
        _logError(str(e))
        return _jsondata(url)
    except urllib2.URLError, e:
        if _verbose == 1:
            print '[ERROR] URLError'
        elif _verbose == 2:
            print '[ERROR] URLError = ' + str(e)
        _logError(str(e))
        return _jsondata(url)
    except httplib.HTTPException, e:
        if _verbose == 1:
            print '[ERROR] HTTPException'
        elif _verbose == 2:
            print '[ERROR] HTTPException = ' + str(e)
        _logError(str(e))
        return _jsondata(url)
    except ValueError, e:
        if _verbose == 1:
            print '[ERROR] ValueError'
        elif _verbose == 2:
            print '[ERROR] ValueError = ' + str(e)
        _logError(str(e))
        return _jsondata(url)
    except Exception:
        if _verbose == 1:
            print '[ERROR] generic exception: '
        elif _verbose == 2:
            print '[ERROR] generic exception: ' + traceback.format_exc()
        _logError(traceback.format_exc())
        return _jsondata(url)

#JsonData Custom Headers
def _jsondatach(url):
    try:
        _headers = { 'User-Agent' : 'Mozilla/5.0' }
        _req = urllib2.Request(url, None,_headers)
        _rawdata = urllib2.urlopen(_req)
        return json.load(_rawdata)
    except urllib2.HTTPError, e:
        if _verbose == 1:
            print '[ERROR] HTTPError'
        elif _verbose == 2:
            print '[ERROR] HTTPError = ' + str(e)
        _logError(str(e))
        return _jsondata(url)
    except urllib2.URLError, e:
        if _verbose == 1:
            print '[ERROR] URLError'
        elif _verbose == 2:
            print '[ERROR] URLError = ' + str(e)
        _logError(str(e))
        return _jsondata(url)
    except httplib.HTTPException, e:
        if _verbose == 1:
            print '[ERROR] HTTPException'
        elif _verbose == 2:
            print '[ERROR] HTTPException = ' + str(e)
        _logError(str(e))
        return _jsondata(url)
    except ValueError, e:
        if _verbose == 1:
            print '[ERROR] ValueError'
        elif _verbose == 2:
            print '[ERROR] ValueError = ' + str(e)
        _logError(str(e))
        return _jsondata(url)
    except Exception:
        if _verbose == 1:
            print '[ERROR] generic exception: '
        elif _verbose == 2:
            print '[ERROR] generic exception: ' + traceback.format_exc()
        _logError(traceback.format_exc())
        return _jsondata(url)

def _jsondatachTrack(url):
    try:
        global sessionid
        if sessionid == "":
            return _jsondatachTrack(url)
        else:
            _rawdata = _session.get(url+sessionid, stream=True)
            return _rawdata.json()
    except urllib2.HTTPError, e:
        if _verbose == 1:
            print '[ERROR] HTTPError'
        elif _verbose == 2:
            print '[ERROR] HTTPError = ' + str(e)
        _logError(str(e))
        return _jsondata(url)
    except urllib2.URLError, e:
        if _verbose == 1:
            print '[ERROR] URLError'
        elif _verbose == 2:
            print '[ERROR] URLError = ' + str(e)
        _logError(str(e))
        return _jsondata(url)
    except httplib.HTTPException, e:
        if _verbose == 1:
            print '[ERROR] HTTPException'
        elif _verbose == 2:
            print '[ERROR] HTTPException = ' + str(e)
        _logError(str(e))
        return _jsondata(url)
    except ValueError, e:
        if _verbose == 1:
            print '[ERROR] ValueError'
        elif _verbose == 2:
            print '[ERROR] ValueError = ' + str(e)
        _logError(str(e))
        return _jsondata(url)
    except Exception:
        if _verbose == 1:
            print '[ERROR] generic exception: '
        elif _verbose == 2:
            print '[ERROR] generic exception: ' + traceback.format_exc()
        _logError(traceback.format_exc())
        return _jsondata(url)

#Find TrackMon Session
def _findSessionIdTrack():
    global sessionid
    print "[INFO] Finding SessionId for TrackMon"
    rw = re.compile('var sessionId \= \'(.*?)\'\;')
    r = _session.get("http://www.trackemon.com/")
    for line in r.iter_lines():
        if "sessionId" in line:
            suc = rw.search(line)
            if suc:
                sessionid = suc.group(1)
                print "[INFO] SessionId for TrackMon Found"
            else:
                _findSessionIdTrack()

#Pokemon Name
def _pokename(id):
    return pokemonlist[int(id)-1]

#PokeSplit
def _pokesplit(pokemons):
    global _pokemons
    _pokemons = pokemons.split(",")

#POkePrinter
def _printer(name,lat,lng,exp):
    _time = time()
    _remain = float(exp)-time()
    _minutes = int(_remain / 60)
    _seconds = int(_remain % 60)
    _expire = str(_minutes) + " Minutes, " + str(_seconds) + " Seconds"
    print "-------------------------------------------------"
    print "Pokemon: " + name
    print "Coordinates: " + str(lat) + "," + str(lng)
    print "Expires in: " + _expire
    print "-------------------------------------------------"
    if _logging:
        _logPokemon(name, str(lat), str(lng), _expire)

#Logger
def _logPokemon(name, lat, lng, expire):
    os.chdir(_scriptpath)
    with open("pokemons.log", "a+") as f:
        f.write("[" + name + "] [" + lat + "," + lng + "] [" + expire + "]\n")
        f.close()

#CoordsLoader
def _populateCities():
    os.chdir(_scriptpath)
    with open("coords.txt", "a+") as f:
        _data = f.readlines()
        for line in _data:
            _citydata = line.split(":")
            _cities.append([_citydata[0],_citydata[1],_citydata[2]])
        f.close()

#Finder
def _finderTrackemon(city):
    print "[INFO] Looking pokemons in: " + city[0]
    _latitudesw = float(city[1]) - (0.05 * _zoomFactor)
    _longitudesw = float(city[2]) - (0.05 * _zoomFactor)
    _latitudene = float(city[1]) + (0.05 * _zoomFactor)
    _longitudene = float(city[2]) + (0.05 * _zoomFactor)

    _scanurl = "http://www.trackemon.com/fetch?location="+str(city[1])+","+str(city[2])+"&sessionId="
    _scanurljsondata = _jsondatachTrack(_scanurl)

    for pokename in _pokemons:
        try:
            for pokemon in _scanurljsondata['pokemon']:
                _id = pokemon['pokedexTypeId']
                _name = _pokename(_id)
                if pokename.lower() in _name.lower():
                    _lat = pokemon['latitude']
                    _lng = pokemon['longitude']
                    _exp = pokemon['expirationTime']
                    _id = pokemon['id']
                    if _id not in _pokemonslisted:
                        _pokemonslisted.append(_id)
                        _printer(_name, _lat, _lng, _exp)
                        if ps_use: _pokeSniper(_name, str(_lat), str(_lng))
                    else:
                        print "[INFO] Pokemon already listed found."
        except KeyError, e:
            if _verbose == 1:
                print '[ERROR] KeyError'
            elif _verbose == 2:
                import traceback
                print '[ERROR] KeyError= ' + str(e)
            _logError(str(e))
        except IndexError, e:
            if _verbose == 1:
                print '[ERROR] IndexError'
            elif _verbose == 2:
                print '[ERROR] IndexError= ' + str(e)
            _logError(str(e))

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
            if _verbose == 1:
                print '[ERROR] KeyError'
            elif _verbose == 2:
                import traceback
                print '[ERROR] KeyError= ' + str(e)
            _logError(str(e))
        except IndexError, e:
            if _verbose == 1:
                print '[ERROR] IndexError'
            elif _verbose == 2:
                print '[ERROR] IndexError= ' + str(e)
            _logError(str(e))

#Sniper
def _pokeSniper(name, lat, lng):
    os.chdir(ps_dir)
    os.system(ps_path+" "+name+" "+lat+" "+lng)

#Loop
def _loop():
    for city in _cities:
        if "Skip" in _useMode or "All" in _useMode:
            _finderSkipLagged(city)
        elif "Track" in _useMode or "All" in _useMode:
            _finderTrackemon(city)

#Init
_parser = argparse.ArgumentParser(description='PokeVisionFinder v0.1.3 - encode')
_parser.add_argument('-m','--mode', help='Mode of work', choices=["Skip", "Track","All"], default="All")
_parser.add_argument('-l', '--loop', help='Run infinite', action='store_true', default=False)
_parser.add_argument('-L','--logging', help='Log pokemons found', action='store_true', default=False)
_parser.add_argument('-c','--catchfile', help='Use catch file', action='store_true', default=False)
_parser.add_argument('-p','--pokemons', help='List of pokemons', default="Pikachu")
_parser.add_argument('-f','--factor', help='ZoomFactor', type=int, required=True, default=1)
_parser.add_argument('-v','--verbose', help='Verbose mode', type=int, choices=[0, 1, 2], default=0)
_args = _parser.parse_args()

_useMode = _args.mode

_logging = _args.logging

_zoomFactor = _args.factor

_catchfile = _args.catchfile

_nonstop = _args.loop

_verbose = _args.verbose

_inputpoke = ""

if _catchfile:
    _inputpoke = [line.strip() for line in open("catch.txt", 'r')]
    _pokemons = _inputpoke
else:
    _inputpoke = _args.pokemons
    _pokesplit(_inputpoke)

if "Track" in _useMode or "All" in _useMode:
    _findSessionIdTrack()
_populateCities()

if _nonstop:
    while 1:
        _loop()
else:
    _loop()