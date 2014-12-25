# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

import config
import model


class Pay(model.Base):
  name = ndb.StringProperty(default='')
  date_for = ndb.DateProperty(auto_now_add=True)
  date_paid = ndb.DateProperty(auto_now_add=True)
  code = ndb.StringProperty(default='')
  amount = ndb.FloatProperty(default=0.0)

  @ndb.ComputedProperty
  def amount_format(self):
    return u'%s %0.2f' % (config.CONFIG_DB.currency, self.amount)
