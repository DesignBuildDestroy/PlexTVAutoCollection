# Design Build Destroy 2021
# Plex TV Auto Collection
# - Adds TV shows to collections based on the Network name they belong to
# - Attempt to recreate TV stations, like sorting through Netflix originals, Hulu, CBS All access as 
#   like using their individual apps to break down large collections or see whats new on those services.

import time
import os.path
import urllib.request, json 
from plexapi.server import PlexServer

base_url = 'YOUR PLEX URL HERE'
token = 'YOUR PLEX TOKEN HERE'
plex = PlexServer(base_url, token)
tmdb_key = 'YOUR TMDB KEY HERE'

def ProcessTVnetworks(collection ='', network_id = ''):
    # Load the fist page to get the total page number of results so we can loop through each page's list
    base = "https://api.themoviedb.org/3/discover/tv?api_key=" + tmdb_key + "&with_networks=" + network_id + "&page=1"
    with urllib.request.urlopen(base) as url:
        data = json.loads(url.read().decode())
    
    total_pages = data['total_pages']
    
    # Loop through each page to process the show list and add to the collection if show is found in Plex
    for i in range(1,int(total_pages)+1):
        base = "https://api.themoviedb.org/3/discover/tv?api_key=" + tmdb_key + "&with_networks=" + network_id + "&page=" + str(i)
        try:
            with urllib.request.urlopen(base) as url:
                data = json.loads(url.read().decode())
            
            for results in data['results']:        
                # Grab the show name and the Guid value to compare to Plex to verify we got the right show
                title = results['name']
                guidID = "tmdb://" + str(results['id'])
                guidIDval = str(results['id'])
            
                print(title + "   ", end='')
                
                movies = plex.library.section('TV Shows')
                collected = movies.search(collection=collection, title=title)
                
                if collected:
                    # Show is already in the collection, skip
                    print("Already in " + collection)
                else:
                    # Show not in the connection loop through possible GUID locations for matching
                    # Plex may store the TMDB Guid in different places depending on the scanner used
                    # So we'll check in multiple spots, GUID is used to make sure we are matching 100%
                    # to the correct show as Plex sees it, using title only will result in mismatches
                    matched_guid = False
                    for item in plex.library.search(title, libtype="show"):
                        # Check the scanner guid value for match for the found title
                        if ("themoviedb" in item.guid) and (guidIDval in item.guid):
                            item.addCollection(collection)
                            print('Scanner Guid Matched')
                            matched_guid = True
                            break
                        else:
                            # If we got here no scanner guid matches so loop through alt guids instead for match
                            for guid in item.guids:
                                if guidID in guid.id:
                                    item.addCollection(collection)
                                    print('Guid Matched')
                                    matched_guid = True
                                    break
                    if matched_guid:
                        # We found a match already reset flag
                        matched_guid = False
                    else:
                        # If we got here show either doesn't exist or no Guid's matched
                        print('NOT FOUND')
                    
        except Exception as e:
            print("***** HOLD *****")
            print(e)
            time.sleep(30)
        finally:
            pass
        
#END processTVnetworks                            





#MAIN
def main():
    # Read custom network list with network ID's from TMDB
    # in CSV format each line as follows: COLLECTION NAME,TMDBID
    #  where collection name is what you want this networks collection to be titled in Plex (new or existing)
    #  and TMDBID being the actual TMDB network ID
    #  create multiple row entries with the same collection name and different TMDB ID's to lump networks together
    
    if (os.path.isfile("networks.csv") == True):
        text_file = open("networks.csv", "r")
        networks = text_file.readlines()
        text_file.close()
    
    for lines in networks:
        lines = lines.rstrip()      # clean /n from eol
        lines = lines.split(",")    # split collection name and TMDB ID
        ProcessTVnetworks(lines[0], lines[1])   # Get data from TMDB and build TV collections

    #END MAIN
    
if __name__ == "__main__":
    main()
#END
