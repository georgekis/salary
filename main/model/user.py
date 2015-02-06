# coding: utf-8

from __future__ import absolute_import

from datetime import date
import hashlib

from flask.ext.restful import fields
from google.appengine.ext import ndb

import model
import util
import config


class User(model.Base):
  name = ndb.StringProperty(required=True)
  username = ndb.StringProperty(required=True)
  email = ndb.StringProperty(default='')
  auth_ids = ndb.StringProperty(repeated=True)
  active = ndb.BooleanProperty(default=True)
  admin = ndb.BooleanProperty(default=False)
  permissions = ndb.StringProperty(repeated=True)
  verified = ndb.BooleanProperty(default=False)
  token = ndb.StringProperty(default='')
  birthdate = ndb.DateProperty()
  job_title = ndb.StringProperty(default='')
  password_hash = ndb.StringProperty(default='')
  social_security_number = ndb.StringProperty(default='')

  def has_permission(self, perm):
    return self.admin or perm in self.permissions

  def avatar_url_size(self, size=None):
    return '//gravatar.com/avatar/%(hash)s?d=identicon&r=x%(size)s' % {
        'hash': hashlib.md5(
            (self.email or self.username).encode('utf-8')).hexdigest(),
        'size': '&s=%d' % size if size > 0 else '',
      }
  avatar_url = property(avatar_url_size)

<<<<<<< HEAD
  @ndb.ComputedProperty
  def age(self):
    if self.birthdate:
      bn = self.birthdate
      td = date.today()
      return td.year - bn.year - ((td.month, td.day) < (bn.month, bn.day))
    return None

  _PROPERTIES = model.Base._PROPERTIES.union({
      'active',
      'admin',
      'age',
      'auth_ids',
      'avatar_url',
      'email',
      'name',
      'permissions',
      'username',
      'verified',
    })

=======
>>>>>>> bfae23693b77e6d849f92f2a95ccd66972566def
  @classmethod
  def get_dbs(
      cls, admin=None, active=None, verified=None, permissions=None, **kwargs
    ):
    return super(User, cls).get_dbs(
        admin=admin or util.param('admin', bool),
        active=active or util.param('active', bool),
        verified=verified or util.param('verified', bool),
        permissions=permissions or util.param('permissions', list),
        **kwargs
      )

  @classmethod
  def is_username_available(cls, username, self_key=None):
    if self_key is None:
      return cls.get_by('username', username) is None
    user_keys, _ = util.get_keys(cls.query(), username=username, limit=2)
    return not user_keys or self_key in user_keys and not user_keys[1:]

  @classmethod
  def is_email_available(cls, email, self_key=None):
    if not config.CONFIG_DB.check_unique_email:
      return True
    user_keys, _ = util.get_keys(
        cls.query(), email=email, verified=True, limit=2,
      )
    return not user_keys or self_key in user_keys and not user_keys[1:]

<<<<<<< HEAD
  def get_pay_dbs(self, **kwargs):
    return model.Pay.get_dbs(
        ancestor=self.key,
        order=util.param('order') or '-date_for,name',
        **kwargs
      )
=======

USER_FIELDS = {
    'active': fields.Boolean,
    'admin': fields.Boolean,
    'auth_ids': fields.String,
    'avatar_url': fields.String,
    'email': fields.String,
    'name': fields.String,
    'permissions': fields.String,
    'username': fields.String,
    'verified': fields.Boolean,
  }

USER_FIELDS.update(model.BASE_FIELDS)
>>>>>>> bfae23693b77e6d849f92f2a95ccd66972566def
