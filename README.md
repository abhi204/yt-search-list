# yt-search-list
Fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube.

#### Installation:
- make sure you have pipenv installed on your pc. See [Installation](https://pypi.org/project/pipenv)
- Open the project directory in terminal and enable the virtual environment for current directory using command:
    ```sh
    $ pipenv shell
    ```
- Once you are in the virtual environment, install dependencies using command:
    ```sh
    $ pipenv install
    ```

#### Working:
This project needs to run 2 processes in order to work correctly. 
  1. Process for running the server
  2. Process for fetching data from Youtube API and adding it to the database

So, open the project directory in 2 terminals.
- In the first terminal, run the following command (to fetch data using Youtube API):
    ```sh
    $ pipenv shell
    $ python manage.py update_list
    ```
    (You should see a list of timestamps being printed)
- In the second terminal, run the following command (to run API server):
    ```sh
    $ pipenv shell
    $ python manage.py runserver
    ```

Now, Open the browser and use this API endpoint: http://localhost:8000/api/videos
This API endpoint returns latest videos sorted in reverse chronological order of their publishing date-time from YouTube for search key 'MUSIC'
(You should see a filter button available at top-right corner for filtering the video list)
