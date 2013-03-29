from xbmcswift2 import Plugin
from BeautifulSoup import BeautifulSoup as BS
import re
import urllib

BASE_URL = 'http://www.teamhww.nl/category/videos/'
VIDEO_URL = 'http://stream.hardwarewoensdag.tv/'

def get_video_link(page):
    print page
    src = urllib.urlopen(page).read()
    html = BS(src)
    video_url =  VIDEO_URL + re.search('\w+\.mp4',src).group();
    video_description = html.find('meta',{"property" : 'og:description'}).get('content')
    video_title = html.find('meta',{"property" : 'og:title'}).get('content')

    video_image = html.find('meta',{"property" : 'og:image'})
    try:
        video_image = video_image.get('content')
    except AttributeError:
        pass

    video = {
            'path': video_url,
            'label' : video_title,
            'info' : {'title' : video_title, 'year': 2013},
            'thumbnail' : video_image,
            'is_playable': True,
    }
    return video


plugin = Plugin()


@plugin.route('/')
def index():
    items = []
    src = urllib.urlopen(BASE_URL)
    html = BS(src)
    for video in html.findAll('article')[:15]:
        video_link = video.find('a').get('href')
        items.append(get_video_link(video_link))
    return items


if __name__ == '__main__':
    plugin.run()
