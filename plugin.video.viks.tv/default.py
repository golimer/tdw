# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, os, urllib, sys, urllib2

PLUGIN_NAME   = 'plugin.video.viks.tv'
handle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.viks.tv')
__settings__ = xbmcaddon.Addon(id='plugin.video.viks.tv')

siteUrl = 'viks.tv'
httpSiteUrl = 'http://' + siteUrl

Pdir = addon.getAddonInfo('path')
icon = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'icon.png'))
xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

def getURL(url,Referer = 'http://viks.tv/'):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		#sn=http[s:]
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L



def inputbox(t):
	skbd = xbmc.Keyboard(t, 'Название:')
	skbd.doModal()
	if skbd.isConfirmed():
		SearchStr = skbd.getText()
		return SearchStr
	else:
		return t



def play(url, cover):
		http=getURL(url)
		ss='//m3u8'
		es='//m3u8 names'
		tmp=mfindal(http,ss,es)[0]
		
		ss="]='"
		es="';"
		purl=mfindal(tmp,ss,es)[0][len(ss):]
		#print purl
		item = xbmcgui.ListItem(path=purl, thumbnailImage=cover, iconImage=cover)
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
		#xbmc.Player().play(purl)

def get_cepg(id):
	import time
	url='http://schedule.tivix.net/channels/viks/program/'+id+'/today/'
	udd = int(time.strftime('%Y%m%d'))
	#if 1==1:
	try:
		E=__settings__.getSetting(id)
		EPG=eval(E)
		udata = int(EPG[0]['start_at'][:11].replace('-',''))
		cdata = int(time.strftime('%Y%m%d'))
		#print str(udata)+" - "+str(cdata)
		if cdata>udata:
			E=getURL(url)
			__settings__.setSetting(id,E)
			print 'обновлена устаревшая программа: '+id
	except:
		try:
			E=getURL(url)
			__settings__.setSetting(id,E)
			print 'обновлена отсутствующая программа: '+id
		except:
			E='[{"name":"", "start_at": "'+time.strftime('%Y-%m-%d')+' --:--:--"}]'
			__settings__.setSetting(id,E)
			print 'неудалось загрузить программу: '+id

	try:
		#E=getURL(url)
		L=eval(E)
		#L=EPG[id]
		itm=''
		n=0
		for i in L:
			n+=1
			h=int(time.strftime('%H'))
			m=int(time.strftime('%M'))
			name=eval("u'"+i['name']+"'")
			stm =i['start_at'][11:-3]
			try:
				h2 = int(L[n]['start_at'][11:13])
				m2 = int(L[n]['start_at'][14:15])
			except:
				h2=h
				m2=m
			t1=h*60+m
			t2=h2*60+m2
			if t2>=t1: itm+= stm+' '+name+'\n'
		return itm
	except:
		return ''

def add_item (name, mode="", path = Pdir, ind="0", cover=None, funart=None):
	#print name
	#print path
	if __settings__.getSetting("fanart")=='true':funart=cover
	else: funart=icon
	if __settings__.getSetting("icons")!='true':cover=icon

	#if cover==None:	listitem = xbmcgui.ListItem("[B]"+name+"[/B]")
	#else:			
	listitem = xbmcgui.ListItem("[B]"+name+"[/B]", iconImage=cover)
	
	
	listitem.setProperty('fanart_image', funart)
	uri = sys.argv[0] + '?mode='+mode
	uri += '&url='  + urllib.quote_plus(path.encode('utf-8'))
	uri += '&name='  + urllib.quote_plus(xt(name))
	uri += '&ind='  + urllib.quote_plus(ind)
	if cover!=None:uri += '&cover='  + urllib.quote_plus(cover)
	if funart!=None and funart!="":uri += '&funart='  + urllib.quote_plus(funart)
	
	
	
	if mode=="play":
		if __settings__.getSetting("epgon")=='true':dict={"plot":get_cepg(ind)}
		else: dict={}
		try:listitem.setInfo(type = "Video", infoLabels = dict)
		except: pass

		fld=False
		listitem.setProperty('IsPlayable', 'true')
		listitem.addContextMenuItems([
			('[COLOR FF55FF55][B]+ Добавить в группу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=add&name='+name+'")'),
			('[COLOR FFFF5555][B]- Удалить из группы[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=rem&name='+name+'")'),
			('[COLOR FFFFFF55][B]v Группа [/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=select_gr")'),
			('[COLOR FFFFFF55][B]* Обновить каналы[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=update")'),])
		
	else: 
		fld=True
		listitem.addContextMenuItems([
			('[COLOR FF55FF55][B]+ Создать группу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=addgr")'),
			('[COLOR FFFF5555][B]- Удалить группу[/B][/COLOR]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=remgr")'),])
	
	#listitem.addContextMenuItems([
	#	('[B]+ Создать группу[/B]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=addgr")'),
	#	('[B]- Удалить группу[/B]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=remgr")'),
	#	('[B]+ Добавить в группу[/B]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=add&name='+name+'")'),
	#	('[B]- Удалить из группы[/B]', 'Container.Update("plugin://plugin.video.viks.tv/?mode=rem&name='+name+'")'),])
	xbmcplugin.addDirectoryItem(handle, uri, listitem, fld)

def get_canals(url):
	try:SG=__settings__.getSetting("Sel_gr")
	except:
		SG='Все каналы'
	if SG=='': 
		SG='Все каналы'
	http=getURL(url)
	#print http
	ss='<div class="all_tv">'
	es='an></a>'
	L=mfindal(http,ss,es)
	LL=[]
	CL=get_gr()
	for i in L:
		ss='http://viks.tv/'
		es='"> <img'
		url=mfindal(i,ss,es)[0]
		
		ss='<img src="'
		es='"><span>'
		img='http://viks.tv/'+mfindal(i,ss,es)[0][len(ss):]

		ss='<span>'
		es='</sp'
		title=mfindal(i,ss,es)[0][len(ss):]
		if SG=='Все каналы' or title in CL:
			LL.append({'url':url, 'img':img, 'title':title})
	return LL


def upd_canals_db():
	LL=[]
	for pg in range(1,5):
		url=httpSiteUrl+'/page/'+str(pg)
		http=getURL(url)
		
		ss='<div class="all_tv">'
		es='an></a>'
		L=mfindal(http,ss,es)
		
		CL=get_gr()
		for i in L:
			ss='http://viks.tv/'
			es='"> <img'
			url=mfindal(i,ss,es)[0]
		
			ss='<img src="'
			es='"><span>'
			img='http://viks.tv/'+mfindal(i,ss,es)[0][len(ss):]

			ss='<span>'
			es='</sp'
			title=mfindal(i,ss,es)[0][len(ss):]
			
			LL.append({'url':url, 'img':img, 'title':title})
			
	__settings__.setSetting("Channels",repr(LL))
	return LL

def upd_EPG():
	url='http://schedule.tivix.net/channels/viks/program/nearest/'
	EPG=getURL(url)
	__settings__.setSetting("EPG",EPG)
	return eval(EPG)

Ldf=[('Основные',['РТР Планета','5 Канал','НТВ','Пятница!','Че ТВ','Звезда','СТС','ТВЦ','Рен ТВ','ТВ3','Россия 1','Пятый','Первый канал','Домашний','Культура','Россия 24','ТНТ']),
	('Детские',['СоюзМультфильм','Nick Jr','Том и Джерри','Ginger','Nickelodeon','Cartoon Network','2х2','Disney','Карусель']),
	('Познавательные',['Discovery','Моя планета','Охотник и рыболов','Охота и рыбалка','Viasat Explorer','Viasat Nature','Animal Family','Живая планета','National Geographic','История','Viasat History','History','Animal Planet']),
	('Музыкальные',['RU TV','VH1 Europe','Муз ТВ']),
	('Новостные',['CNN','РБК','LifeNews','Россия 1','Первый канал','Россия 24']),
	('Спортивные',['МАТЧ! Арена','Спорт 1','Спорт 2','Футбол 2','Футбол 1','МАТЧ! Футбол 3','Бокс','Матч! Боец','Беларусь 24','КХЛ','Матч! Футбол 1','Матч! Наш футбол','Евроспорт','Евроспорт 2','Матч'])]

def select_gr():
	try:L=eval(__settings__.getSetting("Groups"))
	except:
		L=Ldf
		__settings__.setSetting("Groups",repr(L))
	
	Lg=['Все каналы',]
	for i in L:
		Lg.append(i[0])
		
	if Lg!=[]:
		sel = xbmcgui.Dialog()
		r = sel.select("Группа:", Lg)
	if r>=0:
		SG=Lg[r]
		__settings__.setSetting("Sel_gr",SG)
	xbmc.executebuiltin("Container.Refresh")
		#try:SG=__settings__.getSetting("Sel_gr")
		#except:SG=''
	
def get_gr():
	try:SG=__settings__.getSetting("Sel_gr")
	except:
		SG=''
	if SG=='': 
		SG='Все каналы'
		__settings__.setSetting("Sel_gr",SG)
	try:L=eval(__settings__.getSetting("Groups"))
	except:L=[]
	CL=[]
	for i in L:
		if i[0]==SG: CL=i[1]
	return CL

def add(id):
	try:L=eval(__settings__.getSetting("Groups"))
	except:L=Ldf
	Lg=[]
	for i in L:
		Lg.append(i[0])
		
	if Lg!=[]:
		sel = xbmcgui.Dialog()
		r = sel.select("Группа:", Lg)
		COG=L[r][1].append(id)
		
	__settings__.setSetting("Groups",repr(L))

def rem(id):
	#try:SG=__settings__.getSetting("Sel_gr")
	#except:
	SG=''
	try:L=eval(__settings__.getSetting("Groups"))
	except:L=Ldf
	L2=[]
	if SG == "":
		for i in L:
			lj=[]
			for j in i[1]:
				if j!=id: 
					lj.append(j)
			L2.append([i[0],lj])
	else:
		for i in L:
			if i[0] == SG: 
				j=i[1].remove(id)
				L2.append([i[0],j])
			else:
				L2.append(i)
	__settings__.setSetting("Groups",repr(L2))
	xbmc.executebuiltin("Container.Refresh")

def add_gr():
	name=inputbox('')
	try:L=eval(__settings__.getSetting("Groups"))
	except:L=Ldf
	st=(name,[])
	if st not in L:L.append(st)
	__settings__.setSetting("Groups",repr(L))

def rem_gr():
	try:L=eval(__settings__.getSetting("Groups"))
	except:L=Ldf
	Lg=[]
	for i in L:
		Lg.append(i[0])
		
	if Lg!=[]:
		sel = xbmcgui.Dialog()
		r = sel.select("Группа:", Lg)
	if r>=0:
		name=Lg[r]
	
		L2=[]
		for i in L:
			if i[0]!=name: L2.append(i)
		__settings__.setSetting("Groups",repr(L2))


	

def root():
	try:
		SG=__settings__.getSetting("Sel_gr")
	except:
		SG=''
	if SG=='':
		SG='Все каналы'
		__settings__.setSetting("Sel_gr",SG)
	add_item ('[COLOR FF55FF55]Группа: '+SG+'[/COLOR]', 'select_gr')
	
	try:L=eval(__settings__.getSetting("Channels"))
	except:L=[]
	if L==[]: L=upd_canals_db()
		
	#try:EPG=eval(__settings__.getSetting("EPG"))
	#except:EPG={}
	#if EPG=={}: 
	#EPG=upd_EPG()

	#for pg in range(1,5):
		#curl=httpSiteUrl+'/page/'+str(pg)
		#L=get_canals(curl)
		#ind=0
	CL=get_gr()
	ttt=""
	for i in L:
			name  = i['title']
			url   = i['url']
			cover = i['img']
			id    = get_id(url)
			
			if SG=='Все каналы' or name in CL:
				#ttt+="'"+name+"',"
				#print ttt
				add_item (name, 'play', url, id, cover)
			#ind+=1
			
			
	xbmcplugin.endOfDirectory(handle)

def get_id(url):
			ss='viks.tv/'
			es='-'
			id=mfindal(url,ss,es)[0][len(ss):]
			return id


def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

params = get_params()

try:mode = urllib.unquote_plus(params["mode"])
except:mode =""
try:name = urllib.unquote_plus(params["name"])
except:name =""
try:url = urllib.unquote_plus(params["url"])
except:url =""
try:cover = urllib.unquote_plus(params["cover"])
except:cover =""
try:ind = urllib.unquote_plus(params["ind"])
except:ind ="0"


if mode==""         : root()
if mode=="add"      : add(name)
if mode=="rem"      : rem(name)
if mode=="addgr"    : add_gr()
if mode=="remgr"    : rem_gr()
if mode=="update"   : upd_canals_db()
if mode=="select_gr": select_gr()
if mode=="play"     : play(url, cover)
if mode=="rename"   : updatetc.rename_list(int(ind))
#xbmc.executebuiltin("Container.Refresh")