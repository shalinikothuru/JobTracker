from forms import LoginForm, SignupForm, AddJobForm
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask import request
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

DATABASE = 'jobs.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE User_id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(int(user['User_id']), user['Email'], user['Password'])
    return None

class User(UserMixin):
    def __init__(self, user_id, email, password):
        self.id = user_id
        self.email = email
        self.password = password

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE Email = ?', (email,)).fetchone()
        conn.close()
        if user and bcrypt.check_password_hash(user['Password'], password):
            user_obj = User(int(user['User_id']), user['Email'], user['Password'])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        contact_no = form.contact_no.data
        password = form.password.data
        gender = form.gender.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO Users (Email, First_Name, Last_Name, Contact_No, Password, Gender) VALUES (?, ?, ?, ?, ?, ?)',
                        (email, first_name, last_name, contact_no, hashed_password, gender))
            conn.commit()
            # Fetch the new user back to get the ID
            user = conn.execute('SELECT * FROM Users WHERE Email = ?', (email,)).fetchone()
        finally:
            conn.close()

        if user:
            user_obj = User(user['User_id'], user['Email'], user['Password'])
            login_user(user_obj)  # Log the user in
            return redirect(url_for('dashboard'))  # Redirect to the dashboard

    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    # Assume the User model has an attribute `first_name` that you retrieve and send to the template.
    # You need to adjust this according to how you retrieve user details from the database.
    user_id = current_user.get_id()  # current_user from Flask-Login
    conn = get_db_connection()
    user = conn.execute('SELECT First_Name FROM Users WHERE User_id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        user_first_name = user['First_Name']
    else:
        user_first_name = 'User'  # Default name if not found
    return render_template('dashboard.html', first_name=user_first_name)

@app.route("/add_job", methods=["GET", "POST"])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        user_id = current_user.get_id()
        job_id = form.job_id.data
        company_name = form.company_name.data
        role = form.role.data
        location = form.location.data
        url = form.URL.data
        job_source = form.job_source.data
        referral = form.referral.data
        application_id = form.application_id.data
        status = form.status.data
        application_date = form.application_date.data
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO Jobs (user_id, job_id, company_name, role, location, URL, job_source, referral, application_id, status, application_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (user_id, job_id, company_name, role, location, url, job_source, referral, application_id, status, application_date))
            conn.commit()
        finally:
            conn.close()
        return redirect(url_for("dashboard"))
    return render_template("add_job.html", form=form)

@app.route('/view_applications')
@login_required
def view_applications():
    user_id = current_user.get_id()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Jobs WHERE User_id = ?', (user_id,))
    job_apps = cursor.fetchall()
    conn.close()
    return render_template('view_applications.html', job_apps=job_apps)

@app.route('/update_job', methods=['POST'])
@login_required
def update_job():
    job_id = request.form.get('job_id')
    new_status = request.form.get('status')
    user_id = current_user.get_id()
    if job_id and new_status:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE Jobs SET Status = ? WHERE Job_id = ? AND User_id = ?', (new_status, job_id, user_id))
        conn.commit()
        conn.close()
        flash('Job status updated successfully.')
    else:
        flash('Error updating job status.')

    return redirect(url_for('view_applications'))

@app.route('/stats')
@login_required
def stats():
    user_id = current_user.get_id()  # Get the current user's ID
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch data for pie chart
    cursor.execute('''SELECT Status, COUNT(*) AS count FROM Jobs 
                      WHERE User_id = ? GROUP BY Status''', (user_id,))
    status_results = cursor.fetchall()
    status_labels = [x['Status'] for x in status_results]
    status_values = [x['count'] for x in status_results]

    # Fetch data for bar chart
    cursor.execute('''SELECT Job_source, COUNT(*) AS num_of_applications 
                      FROM Jobs WHERE User_id = ? AND Job_source IS NOT NULL 
                      GROUP BY Job_source''', (user_id,))
    job_source_results = cursor.fetchall()
    job_source_labels = [x['Job_source'] for x in job_source_results]
    job_source_values = [x['num_of_applications'] for x in job_source_results]

    # referral
    cursor.execute('''SELECT Referral, COUNT(*) AS num_of_applications 
                      FROM Jobs WHERE User_id = ? AND Referral IN ('YES', 'NO') 
                      GROUP BY Referral''', (user_id,))
    referral_results = cursor.fetchall()
    # Initialize data array for both possible referrals
    referral_data = [0, 0]  # Index 0 for YES, Index 1 for NO
    for result in referral_results:
        if result['Referral'] == 'YES':
            referral_data[0] = result['num_of_applications']
        else:
            referral_data[1] = result['num_of_applications']


    conn.close()

    return render_template('stats.html', 
                           status_labels=status_labels, 
                           status_values=status_values, 
                           job_source_labels=job_source_labels, 
                           job_source_values=job_source_values,
                           referral_data=referral_data)


@app.route('/interview_prep')
@login_required
def interview_prep():
    return render_template('interview_prep.html')

@app.route('/resume_tips')
@login_required
def resume_tips():
    return render_template('resume_tips.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)