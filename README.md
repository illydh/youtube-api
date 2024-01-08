##  Preamble

##  Using the YouTube Data API

Before using the script, the user needs access to the YouTube Data API module with a unique key.

Here is the manual to the API: https://developers.google.com/youtube/v3/getting-started

##  Getting started

Here are the steps to access the API (first time):

1. Make sure you are logged in to a Google Account when starting. All Google accounts have access to the API.
1. From the manual, go to step 2 under 'Before you start' and click the link to 'Google Developers Console'.
1. In the top-left corner next to the Google Cloud button, click the projects button on it's right-side. Click 'NEW PROJECT'. Fill in the fields and click 'CREATE' to start a new project.
1. Select your project. Click 'Credentials', 'CREATE CREDENTIALS', and copy the key generated in the 'Your API key' field.
1. Paste your key into the ```api_key``` string variable of the ```__main__``` section of the main script.
1. Return to the 'APIs & Services' dashboard and click '+ ENABLE APIS AND SERVICES'. Search for 'youtube data api v3', and click the result then 'ENABLE' to activate the API.
1. Return to the API manual and click 'Python' under 'Quickstarts' in the left-side bar. Follow this manual to install necessary packages

##  Packages in-use

- googleapiclient
- pandas
- json
- dateutil
- isodate
- seaborn
- matplotlib

##  Inputting channel IDs

In the ```channel_ids``` array variable of ```__main__```, I have a pre-inputted channel ID ready to be tested.

To access the data of any other YouTube creator, replace the string within the array with your preferred creator. This is how find their ID:

1. From their channel, right-click any background space.
1. Click 'View Page Source'.
1. From the Page Source, CTRL+f (windows) or CMD+f (mac) and highlight 'channelid'.
1. Copy the corresponding value from this dictionary key. This is your channel ID!