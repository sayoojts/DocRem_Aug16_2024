from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, DateField
from wtforms.validators import DataRequired

class SchedulerForm(FlaskForm):
    document_name = StringField('Document Name', validators=[DataRequired()])
    expiry_date = DateField('Expiry Date', validators=[DataRequired()])
    submit = SubmitField('Add Record')

class AddRecordForm(FlaskForm):
    document_name = StringField('Document Name', validators=[DataRequired()])
    expiry_date = StringField('Expiry Date', validators=[DataRequired()])
    submit = SubmitField('Add')

class UpdateRecordForm(FlaskForm):
    id = HiddenField('ID')
    document_name = StringField('Document Name', validators=[DataRequired()])
    expiry_date = StringField('Expiry Date', validators=[DataRequired()])
    submit = SubmitField('Update')

class DeleteRecordForm(FlaskForm):
    id = HiddenField('ID')
    submit = SubmitField('Delete')

