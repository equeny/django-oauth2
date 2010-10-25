#-*- coding: utf-8 -*-
import datetime

from piston.handler import BaseHandler

class DateHandler(BaseHandler):
    
    allowed_methods = ('GET', )
    
    def read(self, request):
        return datetime.datetime.utcnow()