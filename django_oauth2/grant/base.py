#-*- coding: utf-8 -*-

class IBackend(object):
    
    def validate_credentials(self, username, password):
        raise NotImplementedError
    
    def validate_assertion(self, assertion_type, assertion):
        raise NotImplementedError
