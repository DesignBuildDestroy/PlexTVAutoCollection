

import time
import os.path
import urllib.request, json 
from plexapi.server import PlexServer

baseurl = 'YOUR PLEX SERVER URL ie http://1.1.1.1:32400' 
token = 'YOUR PLEX TOKEN HERE'
plex = PlexServer(baseurl, token)

tmdbKey = 'YOUR TMDB API KEY HERE'

def ProcessTVnetworks(collection ="", networkID = ""):
    # Load the fist page to get the total page number of results
    base = "https://api.themoviedb.org/3/discover/tv?api_key=" +tmdbKey + "&with_networks=" + networkID + "&page=1"
    with urllib.request.urlopen(base) as url:
        data = json.loads(url.read().decode())
    
    totalPages = data['total_pages']
    
    # Loop through each page to process the show list and add to the collection
    for i in range(1,int(totalPages)+1):
        base = "https://api.themoviedb.org/3/discover/tv?api_key" +tmdbKey + "&with_networks=" + networkID + "&page=" + str(i)
        try:
            with urllib.request.urlopen(base) as url:
                data = json.loads(url.read().decode())
            
            for results in data['results']:        
                title = results['name']
                guidID = "tmdb://" + str(results['id'])
                guidIDval = str(results['id'])
            
                print(title + "   ", end='')

                movies = plex.library.section('TV Shows')
                collected = movies.search(collection=collection, title=title)
                if collected:
                    #print(title + " Already in " + collection)
                    print("Already in " + collection)
                else:
                    for item in plex.library.search(title, libtype="show"):
                        # Check the scanner guid value for match for the found title
                        if ("themoviedb" in item.guid) and (guidIDval in item.guid):
                            item.addCollection(collection)
                            #print(title + " Scanner guid Matched")
                            print('Scanner guid Matched')
                            break
                        else:
                            # If we got here no scanner guid matches so loop through alt guids instead for match
                            for guid in item.guids:
                                if guidID in guid.id:
                                    item.addCollection(collection)
                                    #print(title + " Guid Matched")
                                    print('Guid Matched')
                                    break
                                else:
                                    # Here nothing matches or guids not present to verify the show
                                    # Log no match or something most likely show not in library
                                    a=1 #placeholder
                                    break
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
