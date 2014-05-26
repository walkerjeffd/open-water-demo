from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_required, current_user
from . import main
from .. import db, admin
from ..models import User, Location, Dataset, Project
from .forms import EditProfileForm, UploadDatasetForm
from .tools import s3_upload, s3_url
from flask.ext.admin.contrib.sqla import ModelView

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/datasets')
@login_required
def dataset_list():
    datasets = current_user.datasets.all()
    return render_template('dataset_list.html', datasets=datasets)

@main.route('/datasets/<int:id>')
@login_required
def dataset_detail(id):
    dataset = Dataset.query.get_or_404(id)
    # fileurl = csvfiles.url(dataset.filename)
    # filepath = csvfiles.path(dataset.filename)
    # import csv
    # with open(filepath, 'rb') as csvfile:
    #     reader = csv.reader(csvfile)
    #     rows = [row for row in reader]
    # return render_template('dataset_detail.html', dataset=dataset, fileurl=fileurl, headers=rows[0], rows=rows[1:100])
    return render_template('dataset_detail.html', dataset=dataset, headers=[], rows=[])

@main.route('/upload-dataset', methods=['GET', 'POST'])
@login_required
def upload_dataset():
    form = UploadDatasetForm(user=current_user)
    if form.validate_on_submit():
        try:
            source_filename, file_url = s3_upload(request.files['file'])
        except Exception:
            flash('Error uploading file, contact administrator.')
            return redirect(url_for('.upload_dataset'))
        dataset = Dataset(location_id=form.location.data,
                          project_id=form.project.data,
                          source_filename=source_filename,
                          file_url = file_url,
                          user_id=current_user.id)
        db.session.add(dataset)
        db.session.commit()
        flash('The dataset has been uploaded.')
        return redirect(url_for('.dataset_detail', id=dataset.id))
    return render_template('upload_dataset.html', form=form)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Location, db.session))
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Dataset, db.session))