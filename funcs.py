''' CLASS FUNCTIONS PY FILE '''

import googleapiclient.discovery 
import pandas as pd
import json
from dateutil import parser
import isodate 

#   data viz packages
import seaborn as sns
import matplotlib.pyplot as plt

class funcs:
    def getChannelStats(self, yt, channel_ids):      
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

    def getVideoIDs(self, yt, playlistID): 
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

    def getVideoDetails(self, yt, videoIDs):
        ''' retrieve details of videos given video IDs '''

        allVideoInfo = []

        for i in range(0,len(videoIDs), 50):
            request = yt.videos().list(
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