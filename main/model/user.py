# coding: utf-8

from __future__ import absolute_import

import hashlib

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
  password_hash = ndb.StringProperty(default='')

  def has_permission(self, perm):
    return self.admin or perm in self.permissions

  def avatar_url_size(self, size=None):
    return '//gravatar.com/avatar/%(hash)s?d=identicon&r=x%(size)s' % {
        'hash': hashlib.md5(self.email or self.username).hexdigest(),
        'size': '&s=%d' % size if size > 0 else '',
      }
  avatar_url = property(avatar_url_size)

  _PROPERTIES = model.Base._PROPERTIES.union({
      'active',
      'admin',
      'auth_ids',
      'avatar_url',
      'email',
      'name',
      'permissions',
      'username',
      'verified',
    })

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

  def get_pay_dbs(self, **kwargs):
    return model.Pay.get_dbs(
        ancestor=self.key,
        order=util.param('order') or '-date_for' or 'name',
        **kwargs
      )
