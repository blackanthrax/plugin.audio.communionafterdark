import sys
import xbmc
import xbmcgui
import xbmcplugin
import feedparser

from urlparse import parse_qsl

ADDON_ID="plugin.audio.communionafterdark"
MEDIA_URL='special://home/addons/{0}/resources/media'.format(ADDON_ID)
RSS_URI = "http://communionafterdark.com/rss.xml"

_url = sys.argv[0]
_handle = int(sys.argv[1])

xbmcplugin.setContent(_handle, 'audio')

def get_sets_from_rss():
	xbmc.log("CAD Plugin:: GET FEEDS")
	feed = feedparser.parse(RSS_URI)
	return feed["items"]

def get_sets():
	sets = []
	for (i, columns) in enumerate(get_sets_from_rss()):
		link = columns.get("guid")
		title = columns.get("title")
		date = columns.get("published_parsed")
		sets.append((title, link, date))
	return sets

def list_sets():
	sets = get_sets()
	listing = []



	for (title, link, date) in sets:
		list_item = xbmcgui.ListItem(label=title, title=date.strftime("%Y-%m-%d"))
		list_item.setProperty('IsPlayable', 'true')
		list_item.setProperty('fanart_image', MEDIA_URL + "/fanart.jpg")

		url = '{0}?action=play&set={1}'.format(_url, link)

		is_folder = False

		listing.append((url, list_item, is_folder))

	xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
	xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_TITLE)
	xbmcplugin.endOfDirectory(_handle)

def play_set(path):
	xbmc.log("CAD Plugin:: PLAY " + path)
	play_item = xbmcgui.ListItem(path=path)
	xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

def router(paramstring):
	xbmc.log("CAD Plugin:: ROUTER")
	params = dict(parse_qsl(paramstring))
	xbmc.log("CAD Plugin:: " + paramstring)
	if params:
		if params['action'] == 'listing':
			list_sets()
		elif params['action'] == 'play':
			play_set(params['set'])
	else:
		list_sets()

if __name__ == '__main__':
	xbmc.log("CAD Plugin:: MAIN THREAD")
	router(sys.argv[2][1:])