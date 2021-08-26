# Plex TV Network Auto Collection
Python script to automatically create Network based TV collections to recreate TV network lists in Plex Media Center

## Features
- Using TheMovieDB.org API to validate what network a TV show belongs to and add it to a Collection in Plex under that networks name
- Using Plex unofficial API, sorts through all TV shows in a given library checking against TMDB to add Collection
- Should be run as a scheduled task not more than once a day as it takes some time to roll through large libraries and prevents hammering TMDB api
- Wait and Retry added if TMDB api or Plex times out

## Work in progress..
