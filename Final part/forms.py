# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, validators
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired
 
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()], render_kw={"placeholder":"Please Enter Your Email"})
    password = PasswordField('Password', validators=[InputRequired()], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")
 
class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder":"Please Enter Email"})
    first_name = StringField('First Name', validators=[DataRequired()], render_kw={"placeholder":"First Name"})
    last_name = StringField('Last Name', validators=[DataRequired()], render_kw={"placeholder":"Last Name"})
    contact_no = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=10)], render_kw={"placeholder":"Contact Number"})
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password should be at least 6 characters long')
    ], render_kw={"placeholder":"Password"})
 
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ], render_kw={"placeholder":"Re-Enter the Password"})
 
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[DataRequired()])
    submit = SubmitField("Register")

class AddJobForm(FlaskForm):
    job_id = StringField('Job ID', validators=[DataRequired()], render_kw={"placeholder":"Enter Job ID"})
    company_name = StringField('Company Name', validators=[DataRequired()], render_kw={"placeholder":"Name of Company"})
    role = StringField('Position', validators=[DataRequired()], render_kw={"placeholder":"Enter Job Title"})
    location = StringField('Location', validators=[DataRequired()], render_kw={"placeholder":"Job Location"})
    URL = StringField('Job Website', validators=[DataRequired()], render_kw={"placeholder":"Job Application URL"})
    #job_source = StringField('Job Source', validators=[DataRequired()], render_kw={"placeholder":"Where did you hear about the job?"})
    
    job_source = SelectField(
        'Job Source',
        choices=[('LinkedIn', 'LinkedIn'), ('Indeed', 'Indeed'), ('Handshake', 'Handshake'), ('Career page', 'Career page'), ('Other', 'other')],
        default = 'LinkedIn',
        validators=[DataRequired()]
    )

    # Corrected: Use SelectField for choices, not StringField
    referral = SelectField(
        'Referral',
        choices=[('yes', 'Yes'), ('no', 'No')],
        default = 'no',
        validators=[DataRequired()]
    )
 
    application_id = StringField('Application ID', validators=[DataRequired()], render_kw={"placeholder":"Enter Application ID"})
    status = SelectField(
        'Application Status',
        choices=[('applied', 'Applied'), ('interview', 'Interview'), ('pending', 'Pending'), ('offer', 'Offer'), ('rejected', 'Rejected')],
        validators=[DataRequired()]
    )
    application_date = DateField('Application Date', format='%Y-%m-%d', validators=[DataRequired()])
    
    submit = SubmitField("Add Job Application")