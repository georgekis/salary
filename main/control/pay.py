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


@app.route('/pay/<int:pay_id>/', methods=['GET', 'POST'])
@app.route('/pay/create/', methods=['GET', 'POST'])
@auth.login_required
def pay_update(pay_id=0):
  if pay_id:
    pay_db = model.Pay.get_by_id(pay_id, parent=auth.current_user_key())
  else:
    pay_db = model.Pay(parent=auth.current_user_key())
  if not pay_db:
    flask.abort(404)

  form = PayUpdateForm(obj=pay_db)
  if form.validate_on_submit():
    form.populate_obj(pay_db)
    pay_db.put()
    return flask.redirect(flask.url_for('pay_list'))
  return flask.render_template(
      'pay/pay_update.html',
      html_class='pay-update',
      title=pay_db.name or 'Create Pay',
      form=form,
      pay_db=pay_db,
    )


###############################################################################
# List
###############################################################################
@app.route('/pay/')
@auth.login_required
def pay_list():
  pay_dbs, pay_cursor = auth.current_user_db().get_pay_dbs()

  return flask.render_template(
      'pay/pay_list.html',
      html_class='pay-list',
      title='Pay List',
      pay_dbs=pay_dbs,
      next_url=util.generate_next_url(pay_cursor),
    )


###############################################################################
# Admin Pay List
###############################################################################
@app.route('/admin/pay/')
@auth.admin_required
def admin_pay_list():
  pay_dbs, pay_cursor = model.Pay.get_dbs()

  return flask.render_template(
      'admin/pay_list.html',
      html_class='admin-pay-list',
      title='Pay List',
      pay_dbs=pay_dbs,
      next_url=util.generate_next_url(pay_cursor),
    )
