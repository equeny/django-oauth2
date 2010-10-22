#-*- coding: utf-8 -*-

class OAuth2Error(Exception):
    pass

class MissRedirectUri(OAuth2Error):
    pass