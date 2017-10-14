# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from openerp import api
import pytz
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class sale_order(models.Model):
    _inherit = 'sale.order'


    def convert_strdate_toserver(self,date,format="%Y-%m-%d %H:%M:%S"):
        #print 'type(date): ',type(date)
        if isinstance(date, basestring):
            #print '111'
            date = datetime.strptime(date, format)
        
        #user_tz = self.env.user.tz or pytz.utc
        user_tz = pytz.timezone(self.env.user.tz) or pytz.utc
        
        #print 'user_tz: ',user_tz
        date = user_tz.localize(date)
        #commitment_date = datetime(commitment_date, user_tz)

        #CONVERT TO UTC
        date = date.astimezone(pytz.utc)
        #print 'date!!!: ',date
        return date


    def convert_tz(self, date, format="%Y-%m-%d %H:%M:%S"):
        """
        converts date to user's timezone
        """
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        display_date_result = datetime.strftime(pytz.utc.localize(datetime.strptime(date,
        DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),format) 
        return display_date_result


    def add_business_days(self,origin_date, add_days):
        '''
        Función que añade días hábiles a una fecha.
        '''
        while add_days > 0:
            origin_date += timedelta(days=1)
            weekday = origin_date.weekday()
            if weekday >= 5: # sunday = 6
                continue
            add_days -= 1
        return origin_date



    @api.model
    def create(self,vals):
        #print 'create'
        date_now = datetime.now()
        #print 'type(date_now): ',type(date_now)
        #print 'date_now: ',date_now

        date_now = datetime.strptime(self.convert_tz(date_now.strftime('%Y-%m-%d %H:%M:%S')),'%Y-%m-%d %H:%M:%S')
        date_standard = date_now.replace(hour=13, minute=0)
        #date_standard = date_now.replace(hour=23, minute=0)
        #date_standard = self.convert_tz(date_now.strftime('%Y-%m-%d %H:%M:%S'))
        #date_standard = date_now.replace(hour=13, minute=0)
        #date_standard = self.convert_strdate_toserver(date_standard)
        #print 'date_standard: ',date_standard

        #user_tz = pytz.timezone(self.env.user.tz)
        #print 'user_tz: ',user_tz
        #date_now = user_tz.localize(date_now)
        #print 'date_now2: ',date_now

        if date_now < date_standard:
            #BEFORE 13:00 HRS
            date = self.add_business_days(date_now,2)
            
        else:
            #AFTER 13:00 HRS
            date = self.add_business_days(date_now,3)
        #print 'date: ',date
        date = self.convert_strdate_toserver(date.strftime('%Y-%m-%d %H:%M:%S'))
        #print 'date: ',date
        vals['commitment_date'] = date
        return super(sale_order,self).create(vals)


    commitment_date = fields.Datetime('Commitment date')