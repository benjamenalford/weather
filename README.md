# Weather

A few scripts to grab the predicted weather for the next year and then what the actual weather was.

The original use was for a scarf where the rows all represent a day of the year, the forcasted weather was used for planning how much yarn to get and sizing the scarf.

For the actual scarf, there is a script (get_weather.py) that I have running daily via Jenkins to pull the previous days weather.

- [Weather.ipynb](weather.ipynb) - Grabs the forecasted weather for the next year from some rando site. A day after I wrote the initial script they changed the page so I had to redo it. well I didn't have to but whatever, I did. ( the old version is in the git history )
- [Weather Update.ipynb](Weather%20Update.ipynb) - a dumping ground of me playing with the NWS weather app.
- [get_weather](scripts\get_weather.py) - script to grab the previous days weather,  can run as a cron job, jenkins,manually, task scheduler, or whatever.   auto gets the previous date, but you can set a date to find out what the weather for that date was


don't judge.
