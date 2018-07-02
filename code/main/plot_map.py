import numpy as np
import pandas as pd
import datetime as dt
import geocoder
import textwrap
from flask import request
import plotly.offline as py
import plotly.graph_objs as go
from pull_from_db import get_all_food_trucks


def getPlotInfo(trucklist):
    '''
    Get food truck info that will be displayed on map
    args: list of food truck objects
    returns: pandas dataframe
    '''

    truck_df = pd.DataFrame({
        'id': [t.objectid for t in trucklist],
        'name': [t.applicant for t in trucklist],
        'lat': [t.latitude for t in trucklist],
        'lng': [t.longitude for t in trucklist],
        'foods': [t.fooditems for t in trucklist],
        'hours': [t.dayshours for t in trucklist],
        'website': [t.website for t in trucklist],
        'twitter': [t.twitter for t in trucklist],
        'yelp': [t.yelp for t in trucklist],
        'schedule': [t.schedule_dict for t in trucklist],
        'loc_desc': [t.location_desc for t in trucklist],
        'loc': [t.location for t in trucklist],
        'pop': [t.past_week_twitter_favs for t in trucklist],
        'sponsor': [t.is_sponsor for t in trucklist]
    })

    def hoverText(x):
        tmp = '<br>'.join(textwrap.wrap(x[0], 20, break_long_words=False))
        name = "<span style='font-size:20px; font-weight:bold'>" +\
            tmp + ":</span><br>"

        if x[1] is not None:
            hours = ''
            for k in ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                      'Friday', 'Saturday', 'Sunday']:
                if k in x[1]:
                    hours = hours + k[:3] +\
                     ': ' + x[1][k][0] + '-' + x[1][k][1] + '<br>'
            hour = "<br><span style='font-weight:bold'>Hours:</span><br>"\
                + hours
        else:
            hour = ''

        if x[2] == []:
            foods = 'Oops! Not Available'
        else:
            foods = ', '.join(x[2])
            tmp = textwrap.wrap(foods, 30, break_long_words=False)
            foods = '<br>'.join(tmp)
        food = "<br><span style='font-weight:bold'>Foods:</span><br>" +\
            foods + "<br>"

        if x[3] == x[3]:
            tmp = '<br>'.join(textwrap.wrap(x[3], 30, break_long_words=True))
            website = "<br><span style='font-weight:bold'>Website:</span><br>"\
                + "<a href='" + x[3] + "'>" + tmp + "</a><br>"
        else:
            website = ''

        if x[4] == x[4]:
            tmp = '<br>'.join(textwrap.wrap(x[4], 30, break_long_words=True))
            yelp = "<br><span style='font-weight:bold'>Yelp:</span><br>" +\
                "<a href='" + x[4] + "'>" + tmp + "</a><br>"
        else:
            yelp = ''

        if x[5] == x[5]:
            tid = x[5].split('/')[-1]
            twitter = "<br><span style='font-weight:bold'>Twitter:</span><br>"\
                + "<a href='" + x[5] + "'>" + tid + "</a><br>"
        else:
            twitter = ''

        if x[6] is not None:
            addr = '<br>'.join(textwrap.wrap(
                x[6], 30, break_long_words=True)) + '<br>'
        else:
            addr = ''

        return name + addr + hour + food + website + yelp + twitter

    truck_df['text'] = truck_df[['name', 'schedule', 'foods',
                                 'website', 'yelp', 'twitter', 'loc']].apply(
            hoverText, axis=1)

    return truck_df


def plotMap():
    '''
    Plot food truck info with markers and annotations on map
    '''
    with open('map_token', 'r') as f:
        mapbox_token = f.read()

    trucklist = get_all_food_trucks()
    truck_df = getPlotInfo(trucklist)

    def open_today(x):
        if x:
            return dt.datetime.now().strftime('%A') in x
        else:
            return False

    def open_now(x):
        if not x:
            return False
        now = dt.datetime.now()
        if now.strftime('%A') not in x:
            return False
        start = x[now.strftime('%A')][0]
        end = x[now.strftime('%A')][1]
        start_time = dt.time(int(start.split(':')[0]),
                             int(start.split(':')[1]), 0)
        end_time = dt.time(int(end.split(':')[0]),
                           int(end.split(':')[1]), 0)
        return (start_time <= now.time()) & (end_time >= now.time())

    def get_user_loc():
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip = request.environ['REMOTE_ADDR']
        else:
            ip = request.environ['HTTP_X_FORWARDED_FOR']
        g = geocoder.ip(ip).latlng
        return g[0], g[1]

    lat = 37.773972
    lon = -122.431297
    user_loc = False
    try:
        lat, lon = get_user_loc()
        user_loc = True
    except Exception:
        pass

    truck_df.loc[[0, 10, 30, 60, 100, 150, 210, 280, 360], 'sponsor'] = 1
    truck_today = truck_df[truck_df.schedule.apply(open_today)]
    truck_now = truck_df[truck_df.schedule.apply(open_now)]
    pop_idx = truck_today.sort_values('pop', ascending=False).index[:10]
    pop_msk = truck_today.index.isin(pop_idx)

    symbol_dict = {0: 'restaurant', 1: 'star'}

    data = go.Data([
        go.Scattermapbox(
            lat=truck_today[pop_msk]['lat'],
            lon=truck_today[pop_msk]['lng'],
            name=truck_today[pop_msk]['id'],
            mode='markers',
            marker=go.Marker(
                color='#fc9272',
                size=25,
                opacity=0.5
            ),
            hoverinfo='text',
            text=truck_today[pop_msk]['text'],
            textposition='top left',
            hoverlabel=dict(bgcolor='#ffffe5', bordercolor='#fec44f',
                            font=dict(family='Courier New', color='#cc4c02'))
        ),
        go.Scattermapbox(
            lat=truck_today[pop_msk]['lat'],
            lon=truck_today[pop_msk]['lng'],
            name=truck_today[pop_msk]['id'],
            mode='markers',
            marker=go.Marker(
                color='#fc9272',
                size=15,
                opacity=0.8
            ),
            hoverinfo='text',
            text=truck_today[pop_msk]['text'],
            textposition='top left',
            hoverlabel=dict(bgcolor='#ffffe5', bordercolor='#fec44f',
                            font=dict(family='Courier New', color='#cc4c02'))
        ),
        go.Scattermapbox(
            lat=truck_today['lat'],
            lon=truck_today['lng'],
            name=truck_today['id'],
            mode='markers',
            marker=go.Marker(
                symbol=truck_today['sponsor'].map(symbol_dict),
                size=10,
                opacity=0.6
            ),
            hoverinfo='text',
            text=truck_today['text'],
            textposition='top left',
            hoverlabel=dict(bgcolor='#ffffe5', bordercolor='#fec44f',
                            font=dict(family='Courier New', color='#cc4c02'))
        ),
        go.Scattermapbox(
            lat=truck_now['lat'],
            lon=truck_now['lng'],
            name=truck_now['id'],
            mode='markers',
            marker=go.Marker(
                symbol=truck_now['sponsor'].map(symbol_dict),
                size=15,
                opacity=1
            ),
            hoverinfo='text',
            text=truck_now['text'],
            textposition='top left',
            hoverlabel=dict(bgcolor='#ffffe5', bordercolor='#fec44f',
                            font=dict(family='Courier New', color='#cc4c02'))
        ),
        go.Scattermapbox(
            visible=user_loc,
            lat=[lat],
            lon=[lon],
            name='user',
            mode='markers',
            marker=go.Marker(
                color='rgb(255, 0, 0)',
                size=15,
                opacity=0.6
            ),
            hoverinfo='text',
            text='You are here',
            textposition='top left',
            hoverlabel=dict(bgcolor='#ffffe5', bordercolor='#fec44f',
                            font=dict(family='Courier New', color='#cc4c02'))
        )
    ])

    layout = go.Layout(
        autosize=True,
        height=600,
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=mapbox_token,
            bearing=0,
            center=dict(
                lat=lat,
                lon=lon
            ),
            pitch=0,
            zoom=14,
            style='outdoors'
        ),
    )

    fig = dict(data=data, layout=layout)
    py.plot(
        fig, auto_open=False, filename='mapPlot.html', show_link=False,
        config={'displayModeBar': False})
