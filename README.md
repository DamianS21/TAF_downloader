# INIT
This software is made to download TAFs for many airports from <https://www.ogimet.com/>. To speed up process and avoid query limit script uses proxies.

# Usage
## Downloading TAFs
### Range of dates
First prompt after launching the applicaiton asks user to insert date from which TAFs should be downloaded. Dates should be in NOTAM format (YYMMDDHHRR) and accepted by pressing enter.
Next prompt asks user to enter TO date. This script uses regexp to check correctness of date format.
### ICAO codes of airports
ICAO codes of airports should be separated by white space.
## Proxies
The sofware uses default proxies list if no proxie file (*proxies.txt*) was found.
To generate new proxies list use *get_proxies.py* script.

# Requierments
* Python 3
* requests
* bs4 (BeautifulSoup)
* datetime
* requests.exceptions
* pickle
* re
