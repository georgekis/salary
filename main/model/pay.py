# coding: utf-8

from __future__ import absolute_import

from google.appengine.ext import ndb

from api import fields
import config
import model
import util

class Pay(model.Base):
  name = ndb.StringProperty(default='')
  date_for = ndb.DateProperty(auto_now_add=True)
  date_paid = ndb.DateProperty(auto_now_add=True)
  code = ndb.StringProperty(default='')
  amount = ndb.FloatProperty(default=0.0)

  @ndb.ComputedProperty
  def amount_format(self):
    return u'%s %0.2f' % (config.CONFIG_DB.currency, self.amount)

  @ndb.ComputedProperty
  def is_positive(self):
    return self.amount >= 0

  @classmethod
  def get_dbs(cls, is_positive=None, **kwargs):
    return super(Pay, cls).get_dbs(
        is_positive=is_positive or util.param('is_positive', bool),
        **kwargs
      )


  FIELDS = {
    'amount': fields.Float,
    'amount_format': fields.String,
    'code': fields.String,
    'date_for': fields.DateTime,
    'date_paid': fields.DateTime,
    'is_positive': fields.Boolean,
    'name': fields.String,
  }

  FIELDS.update(model.Base.FIELDS)
