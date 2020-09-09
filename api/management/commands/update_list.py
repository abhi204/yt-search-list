import time, requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Video, API_Key

class Command(BaseCommand):
    help = 'Populates the Video table using Youtube API calls'

    request_url = 'https://www.googleapis.com/youtube/v3/search'
    search_key = 'Music' # Search term used for API calls
    key = 'AIzaSyCnID_19-EMZByGwKjEmGnDWZ1IbRcTJnY' # API key attached to the request

    def handle(self, *args, **kwargs):
        interval = 10 # Time to wait before next API Call

        # If NO video is currently in the database, start a new search
        # Else return the publish date of the oldest video in the database
        if Video.objects.all().count() == 0:
            published_before_datetime = None
        else:
            published_before_datetime = Video.objects.all().order_by('-publish_datetime').last().publish_datetime

        # published_before_datetime stores the date before which we need to search videos

        page_token = None # no page token available intially for searching
        search_params = {
            'part': 'snippet',
            'q': self.search_key,
            'type': 'video',
            'order': 'date',
            'maxResults': 60,
            'key': self.key
        }
        while True:
            page_token = self.populate_database(published_before_datetime, page_token, search_params)
            if page_token == None: # Api call failed OR no more pages available
                break
            time.sleep(interval)
        


    def populate_database(self, published_before_datetime, page_token, search_params):

        if page_token != None: # get next page results
            search_params['pageToken'] = page_token
        elif published_before_datetime != None: # Continue populating database from where we last left off
            search_params['publishedBefore'] = published_before_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
        else: # the database is currently empty. Start a search
            # Ensure that we get the updated videos list
            search_params['publishedAfter'] = (datetime.now()+timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

        response = requests.get(self.request_url, params=search_params)

        if str(response.status_code) == '200':
            response = response.json() # Convert json response to python dictionary
            next_page_token = response['nextPageToken']

            for item in response['items']:
                video_data = item['snippet']
                video = Video() # Video Model instance
                video.title = video_data['title']
                video.description = video_data['description']
                video.publish_datetime = video_data['publishedAt']
                video.thumbnail_url = video_data['thumbnails']['default']['url']
                video.save()
                print(video.publish_datetime)

            return next_page_token # needed for next API call
        else:
            print('failed to fetch data')
            print(response.json())

    def get_published_before_datetime(self):
        # If NO video is currently in the database, return current time
        # Else return the publish date of the oldest video in the database
        if Video.objects.all().count() == 0:
            return datetime.now()
        else:
            return Video.objects.all().order_by('-publish_datetime').last().publish_datetime
        
