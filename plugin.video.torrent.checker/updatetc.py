# -*- coding: utf-8 -*-
import os, sys, xbmcaddon, time, urllib, xbmc

PLUGIN_NAME   = 'Torrent Checker'
addon = xbmcaddon.Addon(id='plugin.video.torrent.checker')
__settings__ = xbmcaddon.Addon(id='plugin.video.torrent.checker')
handle=""
icon  = os.path.join( addon.getAddonInfo('path'), 'icon.png')
LstDir = addon.getAddonInfo('path')

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

def fs_enc(path):
    sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
    return path.decode('utf-8').encode(sys_enc)

def fs_dec(path):
    sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
    return path.decode(sys_enc).encode('utf-8')


try:
	import tthp
except:
	print "Error import t2http"


def t2h_list(url):
	L=tthp.list(url)
	return L

def file_list(name):
		LD=[]
		try:Directory= __settings__.getSetting("SaveDirectory")
		except: Directory=os.path.join(addon.getAddonInfo('path'), 'strm')
		if Directory=="":Directory=os.path.join(addon.getAddonInfo('path'), 'strm')
		try:path = os.path.join(ru(Directory), name)
		except:path = os.path.join(Directory, name)
		
		#if os.path.isdir(path)==1: return []#os.mkdir(path)
		try:
			ldir = os.listdir(path)
			return ldir
		except: return []

def save_strm(name, epd, url, ind):
		#print '-==-==-=-=--=-==-=-=-=-=--==-=--=-==--=-=-=-=-=-==-=-=-=-=-=--==-=-=-=-=-=-=-=-=-'
		
		if isinstance(name, unicode): name=name.encode('utf-8')
		if isinstance(epd, unicode): epd=epd.encode('utf-8')
		
		try:Directory= __settings__.getSetting("SaveDirectory")
		except: Directory=os.path.join(addon.getAddonInfo('path'), 'strm')
		if Directory=="":Directory=os.path.join(addon.getAddonInfo('path'), 'strm')
		
		SaveDirectory = os.path.join(Directory, name)
		
		if os.path.isdir(fs_enc(SaveDirectory))==0: os.mkdir(fs_enc(SaveDirectory))
		
		uri = construct_request({
			'url': url,
			'title': epd,
			'ind':ind,
			'mode': 'play'
		})
		
		fl = open(fs_enc(os.path.join(SaveDirectory, epd)), "w")
		fl.write(uri)
		fl.close()

def save_tvshow_nfo(name, info={}):
		#title=name.encode('utf-8')#info['title']#
		#cn=title.find(" (")
		#if cn>0: title=title[:cn]
		print repr(name)
		try:title=name.encode('utf-8')
		except:title=name
		
		try:Directory= __settings__.getSetting("SaveDirectory")
		except: Directory=os.path.join(addon.getAddonInfo('path'), 'strm')
		if Directory=="":Directory=os.path.join(addon.getAddonInfo('path'), 'strm')
		
		if isinstance(Directory, unicode): Directory=Directory.encode('utf-8')
			
		SaveDirectory = os.path.join(Directory, name)
		if os.path.isdir(fs_enc(SaveDirectory))==0: os.mkdir(fs_enc(SaveDirectory))
		
		try:year=info['year']
		except:year=0
		try:plot=info['plot']
		except:plot=''
		try:cover=info['cover']
		except:cover=''
		try:fanart=info['fanart']
		except:fanart=''

		nfo='<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'+chr(10)
		nfo='<tvshow>'+chr(10)
		
		nfo+="	<title>"+title+"</title>"+chr(10)
		nfo+="	<showtitle>"+title+"</showtitle>"+chr(10)
		nfo+="	<year>"+str(year)+"</year>"+chr(10)
		nfo+="	<season>-1</season>"+chr(10)
		nfo+="	<plot>"+plot+"</plot>"+chr(10)
		nfo+="	<fanart>"+fanart+"</fanart>"+chr(10)
		nfo+="	<thumb>"+cover+"</thumb>"+chr(10)
		nfo+="</tvshow>"+chr(10)
		
		fl = open(fs_enc(os.path.join(SaveDirectory, "tvshow.nfo")), "w")
		fl.write(nfo)
		fl.close()


def save_nfo(name, epd ,s , e, info={}):
		try: s=s.encode('utf-8')
		except: pass
		try: e=e.encode('utf-8')
		except: pass

		title="season "+s+" episode "+e
		#title=title.encode('utf-8')
		try: title=title.encode('utf-8')
		except: pass
		#name=ru(info['title'])
		cn=name.find(" (")
		if cn>0: name=name[:cn]
		
		try:plot=info['plot']
		except:plot=''
		try:cover=info['cover']
		except:cover=''
		try:fanart=info['fanart']
		except:fanart=''

		try:Directory= __settings__.getSetting("SaveDirectory")
		except: Directory=os.path.join(addon.getAddonInfo('path'), 'strm')
		if Directory=="":Directory=os.path.join(addon.getAddonInfo('path'), 'strm')
		SaveDirectory = os.path.join(Directory, name)
		if os.path.isdir(fs_enc(SaveDirectory))==0: os.mkdir(fs_enc(SaveDirectory))
		
		nfo="<episodedetails>"+chr(10)
		nfo+="	<title>"+title+"</title>"+chr(10)
		nfo+="	<season>"+str(s)+"</season>"+chr(10)
		nfo+="	<episode>"+str(e)+"</episode>"+chr(10)
		nfo+="	<plot>"+plot+"</plot>"+chr(10)
		nfo+="	<fanart>"+fanart+"</fanart>"+chr(10)
		nfo+="	<thumb>"+cover+"</thumb>"+chr(10)
		nfo+="</episodedetails>"+chr(10)
		
		fl = open(fs_enc(os.path.join(SaveDirectory, epd+".nfo")), "w")
		fl.write(nfo)
		fl.close()


def get_list():# получить список заданий
	try:
		H=__settings__.getSetting("History")
		if H=='': HL=[]
		else: HL=eval(H)
	except:
		HL=[]
		__settings__.setSetting("History", repr(HL))
	return HL

def add_list(c, manual=True):# --- добавить задание по (имя, url)
		HL=get_list()
		if c not in HL:
			name=c[0]
			if manual: t=inputbox(name)
			else: t=name
			for i in ['\\','/','*',':','|','"','>','<','?']:
				t=t.replace(i,"")
			if t<>"": name=t
			c[0]=name
			HL.append(c)
			__settings__.setSetting("History", repr(HL))

def rem_list(i):# --- удалить задание по индексу
		HL=get_list()
		HL.pop(i)
		__settings__.setSetting("History", repr(HL))
		#xbmc.executebuiltin("Container.Update()")

def rename_list(i):# --- переименовать задание по номеру задания
		HL=get_list()
		oldname=HL[i][0]
		newname=inputbox(HL[i][0])
		if oldname<>newname:
			HL[i][0]=newname
			__settings__.setSetting("History", repr(HL))
			try: rem(oldname)
			except: pass
			update()
		#xbmc.executebuiltin("Container.Update()")

def add_comment(i): # --- добавить комментарий
		HL=get_list()
		n=len(HL[i])
		if n==4:
			old=HL[i][3]
		elif n==3:
			old=""
			HL[i].append("")
		else: 
			old=""
			HL[i].append([])
			HL[i].append("")
		new=inputbox(old)
		if old<>new:
			HL[i][3]=new
			__settings__.setSetting("History", repr(HL))

def filtr_list(i, p):# --- добавить правило автопереименования эпизодов по номеру задания
		HL=get_list()
		if len(HL[i])<3: HL[i].append([p,])
		else:HL[i][2].append(p)
		__settings__.setSetting("History", repr(HL))

def get_filtr(i):# --- получить правила автопереименования эпизодов по номеру задания
		HL=get_list()
		if len(HL[i])<3: return []
		else: return HL[i][2]

def rem_filtr(i):# --- удалить правила автопереименования эпизодов по номеру задания
		HL=get_list()
		if len(HL[i])<3: HL[i].append([])
		else:HL[i][2]=[]
		__settings__.setSetting("History", repr(HL))
		#xbmc.executebuiltin("Container.Refrch()")

def rem(name):# --- удалить ранее сохраненные STRM по имени задания
		LD=[]
		
		if isinstance(name, unicode): name=name.encode('utf-8')
		
		try:Directory= __settings__.getSetting("SaveDirectory")
		except: Directory=os.path.join(addon.getAddonInfo('path'), 'strm')
		if Directory=="":Directory=os.path.join(addon.getAddonInfo('path'), 'strm')
		path = fs_enc(os.path.join(Directory, name))
		
		if os.path.isdir(path):
			lst=os.listdir(path)
			for i in lst:
				pf=os.path.join(path, i)
				print pf
				os.remove(pf)
			os.rmdir(path)

def inputbox(t):
	skbd = xbmc.Keyboard(t, 'Название:')
	skbd.doModal()
	if skbd.isConfirmed():
		SearchStr = skbd.getText()
		return SearchStr
	else:
		return t

def construct_request(params):
	return '%s?%s' % ('plugin://plugin.video.torrent.checker/', urllib.urlencode(params))

def update():
	print "----- Torrent Checker update start -----"
	L=get_list()
	for i in L:
		name  = i[0].decode('utf-8')
		url   = i[1]
		url2   = urllib.unquote_plus(i[1])
		if url2[:4]=='plug':
			xbmc.executebuiltin('RunPlugin("'+url2+'")')
			time.sleep(10)
		else:
			if len(i)>2: f = i[2]
			else: f=[]
			try:new_ep_lst = tthp.list(url)
			except:new_ep_lst =[]
			try:old_ep_lst = file_list(name)
			except:old_ep_lst = []
			for j in new_ep_lst:
				epd = j.name
				epd = epd.replace('\\'," ")+".strm"
				epd_f=""
				for k in f:
					opid=k[0]
					if opid=="t":epd_f+=k[1]
					else:epd_f+=epd[k[0]:k[1]+1]
				epd_f+=".strm"
				if f==[]:epd_f=epd
				ind = j.index
				if epd not in old_ep_lst: save_strm(name, epd_f, url, ind)
				#print old_ep_lst
	at=time.strftime('Обновлено: %d.%m.%Y - %H:%M')
	__settings__.setSetting("AT", at)
	xbmc.executebuiltin('UpdateLibrary("video", "", "false")')
	print "----- Torrent Checker update end -----"

def update_last():
	print "----- update start -----"
	L=get_list()
	i=L[-1]
	#for i in L:
	if True:
			name  = i[0].decode('utf-8')
			url   = i[1]
			if len(i)>2: f = i[2]
			else: f=[]
			new_ep_lst = tthp.list(url)
			try:old_ep_lst = file_list(name)
			except:old_ep_lst = []
			for j in new_ep_lst:
				epd = j.name
				epd = epd.replace('\\'," ")+".strm"
				epd_f=""
				for k in f:
					opid=k[0]
					if opid=="t":epd_f+=k[1]
					else:epd_f+=epd[k[0]:k[1]+1]
				epd_f+=".strm"
				if f==[]:epd_f=epd
				ind = j.index
				if epd not in old_ep_lst: save_strm(name, epd_f, url, ind)
				#print old_ep_lst
	print "----- update end -----"
