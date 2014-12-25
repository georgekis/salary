from flask.ext import wtf
import auth
import flask
import model
import wtforms
import util

from main import app


###############################################################################
# Create
###############################################################################
class PayUpdateForm(wtf.Form):
  name = wtforms.StringField('Name', [wtforms.validators.required()])
  date_for = wtforms.DateField('Date For', [wtforms.validators.required()])
  date_paid = wtforms.DateField('Date Paid', [wtforms.validators.required()])
  code = wtforms.StringField('Code', [wtforms.validators.required()])
  amount = wtforms.FloatField('Amount', [wtforms.validators.required()])


@app.route('/pay/create/', methods=['GET', 'POST'])
@auth.login_required
def pay_create():
  form = PayUpdateForm()
  if form.validate_on_submit():
    pay_db  = model.Pay(
        parent=auth.current_user_key(),
        name=form.name.data,
        code=form.code.data,
        date_for=form.date_for.data,
        date_paid=form.date_paid.data,
        amount=form.amount.data,
      )
    pay_db.put()
    flask.flash('New pay was successfully created!', category='success')
    return flask.redirect(flask.url_for('pay_list', order='date_for'))
  return flask.render_template(
      'pay/pay_update.html',
      html_class='pay-create',
      title='Create Pay',
      form=form,
    )


###############################################################################
# Update
###############################################################################
@app.route('/pay/<int:pay_id>/update/', methods=['GET', 'POST'])
@auth.login_required
def pay_update(pay_id):
  pay_db = model.Pay.get_by_id(pay_id, parent=auth.current_user_key())
  if not pay_db or pay_db.key.parent() != auth.current_user_key():
    flask.abort(404)
  form = PayUpdateForm(obj=pay_db)
  if form.validate_on_submit():
    form.populate_obj(pay_db)
    pay_db.put()
    return flask.redirect(flask.url_for('pay_list', order='-modified'))
  return flask.render_template(
      'pay/pay_update.html',
      html_class='pay-update',
      title=pay_db.name,
      form=form,
      pay_db=pay_db,
    )


###############################################################################
# List
###############################################################################
@app.route('/pay/')
@auth.login_required
def pay_list():
  pay_dbs, pay_cursor = model.Pay.get_dbs(ancestor=auth.current_user_key())

  return flask.render_template(
      'pay/pay_list.html',
      html_class='pay-list',
      title='Pay List',
      pay_dbs=pay_dbs,
      next_url=util.generate_next_url(pay_cursor),
    )
