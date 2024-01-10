#   importing class functions
from funcs import funcs 

import googleapiclient.discovery 
import pandas as pd
import json
from dateutil import parser
import isodate 

#   data viz packages
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":

    ###     API_KEY
    api_key = 'AIzaSyDpm5DA0da_-QJysM8sy0nsXQbUVFPg8EA'
    nm_playlistID = 'UU1emV4A8liRs9p80CY8ElUQ'

    channel_ids = [
        'UC1emV4A8liRs9p80CY8ElUQ'    #     @freeCodeCamp
    ]

    api_service_name = "youtube"
    api_version = "v3"

    #   creating class object to use encapsulated functions
    f = funcs()

    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    #   compile channel IDs for data extraction
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=",".join(channel_ids)
    )
    response = request.execute()
    chans = json.dumps(response, indent = 4)       #    beautifying data by compiling the info in json
    print(chans)
    print()

    #   table of stats
    chanStats = f.getChannelStats(youtube, channel_ids)
    print (chanStats)
    print()

    #   playlist items
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId="UU1emV4A8liRs9p80CY8ElUQ"
    )
    response = request.execute()
    pls = json.dumps(response, indent = 4)
    print (pls)
    print()

    #   video IDs
    vidIDs = f.getVideoIDs(youtube, nm_playlistID)
    print(vidIDs)
    print()

    #   video info
    vinfo = f.getVideoDetails(youtube, vidIDs)

    print(vinfo.isnull().any())
    numericCols = ['viewCount', 'likeCount', 'favouriteCount', 'commentCount']
    vinfo[numericCols] = vinfo[numericCols].apply(pd.to_numeric, errors = 'coerce', axis = 1)
    
    vinfo['publishedAt'] = vinfo['publishedAt'].apply(lambda x: parser.parse(x))    #   published date
    vinfo['pushblishDayName'] = vinfo['publishedAt'].apply(lambda x: x.strftime('%A'))   

    vinfo['durationSecs'] = vinfo['duration'].apply(lambda x: isodate.parse_duration(x))
    vinfo['durationSecs'] = vinfo['durationSecs'].astype('timedelta64[s]')
    print(vinfo[['durationSecs','duration']])
    print()

    vinfo['tagCount'] = vinfo['tags'].apply(lambda x: 0 if x is None else len(x))   #   apply tags counts

    print(vinfo)
    print()

    #   VISUALIZING: BEST PERFORMING VIDEOS
    ax = sns.barplot(x='title', y='viewCount', data=vinfo.sort_values('viewCount', ascending=False)[0:9])
    plot = ax.set_xticklabels(ax.get_xticklabels(), rotation=90)    #   allows for us to see the titles
    #plt.show()

    #   VISUALIZING: VIEW DISTRIBUTION PER VIDEO
    sns.violinplot(vinfo['viewCount'])
    plt.show()

    #   VISUALIZING: VIEWS V. LIKES AND COMMENTS
    fig, ax = plt.subplots(1,2)
    sns.scatterplot(data=vinfo, x='commentCount', y='viewCount', ax = ax[0])
    sns.scatterplot(data=vinfo, x='likeCount', y='viewCount', ax = ax[1])
    plt.show()  #   both insinuate positive correlations

    #   VISUALIZING: AVG VIDEO DURATION
    sns.histplot(data=vinfo, x='durationSecs', bins=30)
    plt.show()

    '''
    #    UNDER CONSTRUCTION
    #    VISUALIZING: UPLOAD SCHEDULE
    day = pd.DataFrame(vinfo['pushblishDayName'].value_counts())
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = day.reindex(weekdays)
    ax = day.reset_index().plot.bar(x='index', y='pushblishDayName', rot=0)
    '''
    


    


