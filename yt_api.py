import googleapiclient.discovery 
import pandas as pd
import json
from dateutil import parser
import isodate 

#   data viz packages
import seaborn as sns
import matplotlib.pyplot as plt


def getChannelStats(yt, channel_ids):      
    ''' retrieve channel stats '''

    allData = []

    request = yt.channels().list(
        part = "snippet,contentDetails,statistics",
        id=','.join(channel_ids)
    )

    response = request.execute()

    #   loop thru items
    for item in response['items']:
        data = {
            'channelName': item['snippet']['title'],
            'subscribers': item['statistics']['subscriberCount'],
            'views': item['statistics']['viewCount'],
            'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
        }
        
        
        allData.append(data)
    #   RV = table of stats
    return (pd.DataFrame(allData))

def getVideoIDs(yt, playlistID): 
    ''' retrieve IDs of up to 50 videos '''

    videoIDs = []

    request = yt.playlistItems().list(
        part="snippet,contentDetails",
        playlistId = playlistID,
        maxResults = 50     #   yt api only retrieves most recent 50 uploads from selected user
    )
    response = request.execute()

    for item in response['items']:
        videoIDs.append(item['contentDetails']['videoId'])

    return videoIDs

def getVideoDetails(yt, videoIDs):
    ''' retrieve details of videos given video IDs '''

    allVideoInfo = []

    for i in range(0,len(videoIDs), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(videoIDs[i:i+50])
        )
        response = request.execute()
        
        for video in response['items']:
            statsToKeep = {
                'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
                'contentDetails': ['duration', 'definition', 'caption']
            }
            videoInfo = {}
            videoInfo['video_id'] = video['id']

            for key in statsToKeep.keys():
                for v in statsToKeep[key]:
                    try:
                        videoInfo[v] = video[key][v]
                    except:
                        videoInfo[v] = None

            allVideoInfo.append(videoInfo)
        
    return pd.DataFrame(allVideoInfo)      #    visualizing info as a table

if __name__ == "__main__":

    api_key = 'AIzaSyDpm5DA0da_-QJysM8sy0nsXQbUVFPg8EA'
    nm_playlistID = 'UUuTQDPUE12sy7g1xf1LAdTA'

    channel_ids = [
        'UCuTQDPUE12sy7g1xf1LAdTA'    
    ]

    api_service_name = "youtube"
    api_version = "v3"


    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    #   
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=",".join(channel_ids)
    )
    response = request.execute()
    chans = json.dumps(response, indent = 4)       #    compiling the info in json to make it pretty
    print(chans)
    print()

    #   table of stats
    chanStats = getChannelStats(youtube, channel_ids)
    print (chanStats)
    print()

    #   playlist items
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId="UUuTQDPUE12sy7g1xf1LAdTA"
    )
    response = request.execute()
    pls = json.dumps(response, indent = 4)
    print (pls)
    print()

    #   video IDs
    vidIDs = getVideoIDs(youtube, nm_playlistID)
    print(vidIDs)
    print()

    #   video info
    vinfo = getVideoDetails(youtube, vidIDs)

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
    


    


