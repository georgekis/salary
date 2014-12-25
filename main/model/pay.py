# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

import config
import model


class Pay(model.Base):
  user_key = ndb.KeyProperty(kind=model.User)
  name = ndb.StringProperty(required=True)
  date_for = ndb.DateProperty(required=True)
  date_paid = ndb.DateProperty(required=True)
  code = ndb.StringProperty(required=True)
  amount = ndb.FloatProperty(default=0.0)

  @ndb.ComputedProperty
  def amount_format(self):
    return u'%s %0.2f' % (config.CONFIG_DB.currency, self.amount)
