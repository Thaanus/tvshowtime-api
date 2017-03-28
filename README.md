# TVShowTime - API

PythonTvstAPI is a Pythonic API wrapper over the [TVShowTime](tvshowtime.com) REST API. It is a thin wrapper around all of the methods present in the current TVShowTime API specification.

Read the latest [TVShowTime API docs](https://api.tvshowtime.com/doc).

## Install


## How to Use
	# Load API wrapper from library
	from tvst import Tvst
	
	# Create API object.
	tvst = Tvst(CLIENT_ID, CLIENT_SECRET, USER_AGENT)

	# Authenticate without a token
	tvst.authenticate_user()

	# Authenticate with a token	
	tvst.authenticate_user(token='YOUR_TOKEN')
	
All of the API methods have docstrings attached which mirror the official documentation, as the API currently is a rather thin wrapper over top of the TVShowTime API. Users are advised to consult the source code or look at the TVShowTime API documentation for further info. Examples are also provided in the Examples directory of the repository.

## Examples

### Export your progress
	from tvst import Tvst
	import json
	
	tvst = Tvst(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
	tvst.authenticate_user(token='TOKEN')
	
	shows = []
	for i in range(100):
	    try:
	        lib = tvst.library(limit=100, page=i)
	        if lib['shows']:
	            [shows.append(show) for show in lib['shows']]
	            continue
	    except:
	        pass
	    
	    break
	 
	 with open('export.json', 'w') as outfile:
    	json.dump(shows, outfile)
	
	
### Archive ended show with all episode watched
	from tvst import Tvst
	tvst = Tvst(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
	tvst.authenticate_user(token='TOKEN')
	shows = tvst.library(limit=10000)['shows']
	
	for show in shows:
		if (show['aired_episodes'] == show['seen_episodes'] 
			and show['status'] == 'Ended'):
			tvst_to.archive(show['id'])