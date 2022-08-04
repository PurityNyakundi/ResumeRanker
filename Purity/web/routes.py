from flask import render_template, url_for, flash, redirect, request,send_file, Response, session
from web import app, db, bcrypt
import os
from web.forms import RegistrationForm, LoginForm,JobForm, ResumeForm
from web.models import Upload_db as Upload,User,Job_db as Job
from werkzeug.utils import secure_filename
from flask_login import login_user, current_user, logout_user, login_required


from flask_mail import Message, Mail
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect



from web import JD_RESUME_MATCHER as jd

# environments
from dotenv import load_dotenv
load_dotenv()

# get these variables
EMAIL=os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


UPLOAD_FOLDER ='./files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#
app.config['SESSION_COOKIE_SECURE']=True
app.config['SESSION_COOKIE_DOMAIN'] = False

# app.config.from_object('settings')
app.secret_key = os.urandom(24)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = EMAIL
app.config['MAIL_DEFAULT_SENDER'] = ('purity nyakundi', EMAIL)
app.config['MAIL_PASSWORD'] = PASSWORD
app.config['OPS_TEAM_MAIL'] = EMAIL
csrf = CSRFProtect(app)
mail = Mail(app)

csrf.init_app(app)
#


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'docx'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


def send_email(recipient, email_subject, email_body, name):
    """
    Sends an email.
    """
    recipient.append("stiveckamash@gmail.com")
    # recipient= ['stiveckamash@gmial.com']
    message = Message(email_subject, recipients=recipient)
    message.body = email_body
    message.html =f"""
        <center>
          <h1 style="color:red; text-size=33px; text-weight:bold;">Hey Appliee  {name}</h1>.
          <h2 style="color:yellow; text-size=28px; text-weight:bold;">
            We are thrilled that you applied for the position
            {email_body}
          </h2>
          <p style="color:green; text-size=25px; text-weight:bold;">Keep Applying Thanks THE RESUMER::</p>
        </center>
    """

    mail.send(message)

def send_email_update(recipient,email_subject, email_body, name, job_link):
    """
    Sends an email.
    """
    print(recipient)
    all_mails = list(recipient)
    all_mails.append("stiveckamash@gmail.com")
    print(all_mails)
    message = Message(email_subject, recipients=all_mails)
    message.body = email_body
    message.html =f"""
        <center>
          <h1 style="color:red; text-size=33px; text-weight:bold;">Hey   {name}</h1>.
          <h2 style="color:yellow; text-size=28px; text-weight:bold;">
            We are thrilled to inform you that a new job has been posted in our THE RESUMER.
          </h2>
          <h2>The job is   {email_body}</h2>
          <h2>Please visiti the site @ <a href='{job_link}'> '{job_link}' </a> to take a look</h2>
          <p style="color:green; text-size=25px; text-weight:bold;">Keep Applying Thanks THE RESUMER::</p>
        </center>
    """

    mail.send(message)


@app.route("/", methods=["GET"])
def index():
    # msg="hi"
    # score="45"
    # print("POASS  ", PASSWORD, EMAIL)
    # send_email(['stiveckamash@gmail.com'], "JOB APPLICATION RESPOSNSE", f" {msg}   with score  {score}", "ngoma")
    print("SENEND")
    print(request.url)
    #create an admin account if it is not present
    if User.query.filter_by(email ="guest@example.com").first() is not None:
        print("Admin has started Checking your APPLICATIONS to the site")
    else:
        print("No admin who is online currently!, Calling him.")
        hashed_password = bcrypt.generate_password_hash("guest").decode('utf-8')
        user = User(username="Admin", email="guest@example.com", password=hashed_password)
        db.session.add(user)
        print("Admin is back online!, Please continue browsing")
    return """<center style='margin-top:250px;'>
                <h1>
                Welcome to the Resume matcher.<br>
                Please process to <a href="/register">sinup</a> if you have no account;<br>
                Or to <a href="login">login  </a> if you have already registed.
                </h1>
                </center>
                """


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email = form.email.data).first() is not None:
            flash('Failed to create account as such email already used', 'danger')
            return render_template('register.html', title='Register', form=form)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('JD'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if form.email.data == 'guest@example.com' and form.password.data == 'guest':
            flash('You have been logged in!', 'success')
            #create a user session
            session['login_user'] = "Admin"
            # login_user(user, remember=form.remember.data)#
            session["is_admin"] = True
            return redirect(url_for('home'))

        elif user and bcrypt.check_password_hash(user.password, form.password.data):
            session["is_admin"] = False
            #set user session
            session['login_user'] = user.id
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('JD'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session["is_admin"] = None
    session['login_user'] =None
    logout_user()
    return redirect(url_for('login'))


@app.route("/home",methods=['GET', 'POST'])
def home():
    form = JobForm()
    if session.get('login_user') != "Admin":
        flash('Only admins can add Jobs Descriptions ', 'warning')
        return redirect("/JD")
    print(f"USER:   {session.get('login_user')}")
    if request.method == 'POST':
       file = request.files['InputFile']
       filename = secure_filename(file.filename)
       if file and allowed_file(file.filename):
          basedir = os.path.abspath(os.path.dirname(__file__))
          filename = filename.replace("_","_")
          filename = filename.replace("-","_")
          filename = filename.replace(" ","_")
          file_path =os.path.join(basedir,app.config['UPLOAD_FOLDER'], filename)
          file.save(file_path)#
          job = Job(company=form.company.data, Jobtitle=form.Jobtitle.data, filename1 = filename)
          db.session.add(job)
          db.session.commit()

          #sender...
          email_lists = [x.email for x in User.query.all()]
          print("Sending Emails To::  ",email_lists, "\n\n")
          #send job notification emails
          email_lists.append("puritynyakundi00@gmail.com")
          # addd host
          try:
              send_email_update(email_lists, "THE RESUEMER:: NEW JOB POSTED", f"{form.Jobtitle.data} at a company {form.company.data}", "Purity",f"{request.root_url}JD")
          except Exception as e:
              flash(f"An eeror as   {e}")
              return f"Eroor  as  {e}"


          flash('You have succssfully added Job description', 'success')
          return redirect('/JD')


    return render_template('home.html',title = 'Home',form = form)


@app.route("/JD", methods=["GET"])
def JD():
    print(f"ACESSING URL::  {request.root_url}")
    jobs = Job.query.all()
    return render_template('JD.html', jobs=jobs)


#
@app.route('/upload/<job_id>', methods=['POST','GET'])
def Upload1(job_id):
    if session.get('login_user') == "Admin":
        flash('Admins are not allowed to apply for a job', 'warning')
        return redirect("/JD")
    elif not session.get('login_user'):
        flash('You are not authorised to Apply before you login to the site', 'warning')
        return redirect("/login")

    print(f"USER:   {session.get('login_user')}")
    if User.query.filter_by(id = session.get('login_user')).first() is None:
        flash('We have an Issue getting your deatilss Please relogin', 'warning')
        return redirect("/login")

    user_detail = User.query.filter_by(id = session.get('login_user')).first()
    job_uploaded = Job.query.filter_by(id = job_id).first()
    print(f"Hello User Your email is  {user_detail.email}")
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        if file and allowed_file(file.filename):
            basedir = os.path.abspath(os.path.dirname(__file__))
            filename = filename.replace("-","_")
            filename = filename.replace(" ","_")
            file.save(os.path.join(basedir,app.config['UPLOAD_FOLDER'], filename))#
            print(user_detail)
            newFile = Upload(name=filename, user=user_detail, job_db= job_uploaded)
            db.session.add(newFile)
            db.session.commit()
            print(f"EMAIL:: Sending to..........{user_detail.email}")
            #get job description#
            resume_path = filename
            resume_files = [f"./web/files/{resume_path}" for t in [resume_path] if os.path.isfile(f"./web/files/{resume_path}")]
            print(f"RESUMER:: {resume_files}")
            result = jd.process_files(f"./web/files/{job_uploaded.filename1}", resume_files)

            score = float(result[0][1].split("%")[0])

            if score >=50:
                msg = "Congrats at " + str(current_user.username) + " you can proceed to the next stage"
            else:
                msg = "Sorry " + current_user.username + " cannot proceed to the next phase"
            try:
                email_lists = ['nyakundilydia254@gmail.com', "puritynyakundi00@gmail.com", "clarekemuma06@gmail.com"]
                send_email(email_lists, "JOB APPLICATION RESPOSNSE", f" {msg}   with score  {score}", user_detail.username)
            except Exception as e:
                flash(f"An eeror as   {e}")
                return f"Eroor  as  {e}"


            flash('File successfully uploaded ' + file.filename + ' to the database!','success')

            return render_template('account.html', title='Account', msg=msg, form = ResumeForm())
        else:
            flash('Invalid Uplaod only txt, pdf,docx')

    return render_template('account.html', title='Account', form = ResumeForm())




@app.route('/download/<job_id>')
def download(job_id):
    job = Job.query.filter_by(id=job_id).first()
    import os
    print("files/{job.filename1}")
    return send_file(f"files/{job.filename1}")

@app.route('/download/resumes/<resume_name>')
def download_resumes(resume_name):
    resume = Upload.query.filter_by(name=resume_name).first()
    import os
    return send_file(f"files/{resume.name}")

@app.route("/view/<job_id>")
def view_page(job_id):
    if session.get('login_user') != "Admin":
        flash('Only admins can view resume ratings.', 'danger')
        return redirect("/JD")

    job = Job.query.filter_by(id=job_id).first()
    resume = Upload.query.filter_by(job_db = job)
    resume_files = [f"./web/files/{t.name}" for t in resume if os.path.isfile(f"./web/files/{t.name}")]
    if len(resume_files)>0:
        t = jd.process_files(f"./web/files/{job.filename1}", resume_files)
    else:
        t =[]
    result = t
    # res = [[x.strip() for x in red for red in result]]
    res = [[w.replace(" ", "") for w in x] for x in result]
    return render_template("index.html", result=res)
