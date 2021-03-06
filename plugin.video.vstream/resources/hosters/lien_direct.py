from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import re,urllib2,xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Lien direct'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR] [COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'lien_direct'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        
    def gethost(self, sUrl):
        sPattern = 'https*:\/\/(.+?)\/.+?'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0][1]

        return ''   

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
        
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = self.__sUrl

        #Special pour mangacity
        if 'pixsil' in api_call:
            api_call = api_call.split('|')[0] + '|Referer=http://www.mangacity.org/jwplayer/player.swf'
            
        #Special pour hd-stream.in et film-streaming.co
        if 'm3u8' in api_call:
            base = re.sub(r'(playlist.m3u8.+)','',api_call)
            oRequest = cRequestHandler(api_call)
            sHtmlContent = oRequest.request()
            sPattern =  ',NAME="([^"]+)".+?(chunklist.+?.m3u8)'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                #initialisation des tableaux
                url=[]
                qua=[]
                api_call = ''
                #Replissage des tableaux
                for i in aResult[1]:
                    url.append(str(i[1]))
                    qua.append(str(i[0]))

                #Si une seule url
                if len(url) == 1:
                   api_call = base + url[0]
                #si plus de une
                elif len(url) > 1:
                    #Afichage du tableau
                    dialog2 = xbmcgui.Dialog()
                    ret = dialog2.select('Select Quality',qua)
                    if (ret > -1):
                        api_call = base + url[ret]
                        
                    else: 
                        return False, False

        if (api_call):
            return True, api_call
            
        return False, False
 
