#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig
from resources.lib.player import cPlayer
from resources.lib.packer import cPacker
import re, urllib, urllib2

 
SITE_IDENTIFIER = 'streamcomplet'
SITE_NAME = 'Streamcomplet.com'
SITE_DESC = 'Streaming Gratuit de 4891 Films Complets en VF'
 
URL_MAIN = 'http://streamcomplet.com/'

MOVIE_NEWS = (URL_MAIN, 'showMovies')

MOVIE_GENRES = (True, 'showGenre')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'Recherche Films', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautés', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)
    
            
    oGui.setEndOfDirectory()

def showMoviesSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = URL_MAIN + '?s='+sSearchText  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
            
                 
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action',URL_MAIN + 'film/action/'] )
    liste.append( ['Thriller',URL_MAIN + 'film/thriller/'] )
    liste.append( ['Drame',URL_MAIN + 'film/drame/'] )
    liste.append( ['Comedie',URL_MAIN + 'film/comedie/'] )        
    liste.append( ['Animation',URL_MAIN + 'film/animation/'] )
    liste.append( ['Policier',URL_MAIN + 'film/policier/'] )
    liste.append( ['Fiction',URL_MAIN + 'film/fiction/'] )  
    liste.append( ['Horreur',URL_MAIN + 'film/horreur/'] )
    liste.append( ['Historique',URL_MAIN + 'film/historique/'] ) 
    liste.append( ['Guerre',URL_MAIN + 'film/guerre/'] )
    liste.append( ['Aventure',URL_MAIN + 'film/aventure/'] ) 
    liste.append( ['Musique',URL_MAIN + 'film/musique/'] ) 
    liste.append( ['Romance',URL_MAIN + 'film/romance/'] )                             
               
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()  

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<div class="moviefilm"><a href=".+?"><img src="([^<]+)" alt=".+?" height=".+?" width=".+?" /></a><div class="movief"><a href="([^<]+)">([^<]+)</a></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[2]
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))     
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)
            
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<span class=\'current\'>.+?</span><a class="page larger" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl = aResult[1][0]
        return sUrl

    return False
    
    
def showHosters():

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()

    sPattern = 'src="(http:\/\/media\.vimple\.me.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        
        sUrl2 = aResult[1][0]

        oRequestHandler = cRequestHandler(sUrl2)
        oRequestHandler.addHeaderEntry('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
        oRequestHandler.addHeaderEntry('Referer',sUrl)
        sHtmlContent = oRequestHandler.request()
        
        sPattern = '<source.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            cGui().showInfo('Info', 'Chargement film' , 5) 
            web_url = 'http://media.vimple.me/playerk.swf/' + aResult[1][0]
            
            sHosterUrl = web_url

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle(sMovieTitle)
            oGuiElement.setMediaUrl(sHosterUrl)
            oGuiElement.setThumbnail(sThumbnail)

            oPlayer = cPlayer()
            oPlayer.clearPlayList()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()

        else:
            oGui = cGui()
            sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
            aResult = oParser.parse(sHtmlContent,sPattern)
            if (aResult[0] == True):
                sHtmlContent = cPacker().unpack(aResult[1][0])
                code = re.search('var code="([^"]+)"',sHtmlContent)
                if code:
                   sHosterUrl  = 'https://openload.co/embed/' + code.group(1)
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if (oHoster != False):
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
                     
            oGui.setEndOfDirectory()     
