import requests
#
class ProxySetting:

    ProxyHttpHost_DnB = {
                "158.151.208.51:8080"
                }

    useProxy = None
    test_url = "http://www.cnn.com/robots.txt"

    def Initialization():
        if ProxySetting.useProxy == None:
            try:
                resource = requests.get(ProxySetting.test_url)
                ProxySetting.useProxy = False
            except:
                ProxySetting.useProxy = True
            #
            # print("ProxySetting.useProxy={}".format(ProxySetting.useProxy))
        #
        return ProxySetting.useProxy


    @staticmethod
    def GetProxyHttpHost():
        ProxySetting.Initialization()
        if ProxySetting.useProxy:
            return ProxySetting.ProxyHttpHost_DnB
        else:
            return None


    @staticmethod
    def GetProxyHostDict():
        ProxySetting.Initialization()
        if ProxySetting.useProxy:
            return { "http": "http://" + ProxySetting.ProxyHttpHost_DnB }
        else:
            return None
