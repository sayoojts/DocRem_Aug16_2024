from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Scheduler
from flaskblog.scheduler.forms import UpdateRecordForm, DeleteRecordForm, SchedulerForm

scheduler = Blueprint('scheduler', __name__)

@scheduler.route("/remainder", methods=['GET', 'POST'])
def remainder():
    records = Scheduler.query.all()

    # Create form instances
    update_form = UpdateRecordForm()
    delete_form = DeleteRecordForm()

    if update_form.validate_on_submit():
        # Handle record update
        record = Scheduler.query.get(update_form.id.data)
        if record:
            record.document_name = update_form.document_name.data
            record.expiry_date = update_form.expiry_date.data
            db.session.commit()
            flash('Record updated successfully', 'success')
        else:
            flash('Record not found', 'danger')
        return redirect(url_for('scheduler.remainder'))

    if delete_form.validate_on_submit():
        # Handle record deletion
        record = Scheduler.query.get(delete_form.id.data)
        if record:
            db.session.delete(record)
            db.session.commit()
            flash('Record deleted successfully', 'success')
        else:
            flash('Record not found', 'danger')
        return redirect(url_for('scheduler.remainder'))

    return render_template('remainder.html', title='Document Remainder', records=records, update_form=update_form, delete_form=delete_form)

@scheduler.route('/update_record/<int:id>', methods=['POST'])
@login_required
def update_record(id):
    record = Scheduler.query.get_or_404(id)

    # Ensure the record belongs to the current user
    if record.user_id != current_user.id:
        flash('You do not have permission to update this record.', 'danger')
        return redirect(url_for('scheduler.remainder'))

    # Populate the form with data from the request
    form = UpdateRecordForm()

    if form.validate_on_submit():
        record.document_name = form.document_name.data
        record.expiry_date = form.expiry_date.data

        db.session.commit()
        flash('Your record has been updated!', 'success')
    else:
        flash('Error updating the record. Please check your inputs.', 'danger')

    return redirect(url_for('scheduler.remainder'))



@scheduler.route("/remainder/new", methods=['GET', 'POST'])
@login_required
def add_record():
    form = SchedulerForm()
    if form.validate_on_submit():
        remainder = Scheduler(
            document_name=form.document_name.data,
            expiry_date=form.expiry_date.data,
            user_id=current_user.id
        )
        # Add the new record to the database
        db.session.add(remainder)
        db.session.commit()
        flash('New record added successfully!', 'success')
        return redirect(url_for('scheduler.remainder'))

    # If form does not validate, render the form again with errors
    return render_template('add_document.html', form=form)



@scheduler.route('/delete_record/<int:id>', methods=['POST'])
@login_required
def delete_record(id):
    record = Scheduler.query.get_or_404(id)

    # Ensure the record belongs to the current user
    if record.user_id != current_user.id:
        flash('You do not have permission to delete this record.', 'danger')
        return redirect(url_for('scheduler.remainder'))

    db.session.delete(record)
    db.session.commit()
    flash('Your record has been deleted!', 'success')

    # Clear the session cache to ensure fresh data is loaded
    db.session.expire_all()

    return redirect(url_for('scheduler.remainder'))