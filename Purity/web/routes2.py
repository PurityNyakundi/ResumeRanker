#
# from fileinput import filename
# from turtle import title
# from unicodedata import name
# from urllib.robotparser import RequestRate
# from flask import render_template, url_for, flash, redirect, request,send_file, Response, session
# from web import app, db, bcrypt
# from io import BytesIO
# import os
# from web.forms import RegistrationForm, LoginForm,JobForm
# from web.models import Upload_db as Upload,User,Job_db as Job
#
# from flask_mail import Message
# from flask_bootstrap import Bootstrap
# from flask_wtf.csrf import CSRFProtect
# from flask_mail import Mail
#
# from werkzeug.utils import secure_filename
# from flask_login import login_user, current_user, logout_user, login_required
#
# from web import JD_RESUME_MATCHER as jd
#
# UPLOAD_FOLDER ='./files'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#
#
#
#
# # app.config.from_object('settings')
# app.secret_key = os.urandom(24)
# # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# # app.config['MAIL_PORT'] = 587
# # app.config['MAIL_USE_TLS'] = True
# # app.config['MAIL_USE_SSL'] = False
# # app.config['MAIL_USERNAME'] = ''
# # app.config['MAIL_DEFAULT_SENDER'] = ('purity nyakundi', '')
# # app.config['MAIL_PASSWORD'] = ""
# # app.config['OPS_TEAM_MAIL'] = ''
# csrf = CSRFProtect(app)
# # mail = Mail(app)
#
# csrf.init_app(app)
#
#
#
# # send email function
# def send_email(recipient, email_subject, email_body):
#     """
#       function: send email
#        :param : recipient - deliver the email to this recipient
#                 email_subject - subject of the email
#                 email_body - Body of the mail..
#
#     """
#     message = Message(email_subject, recipients=[recipient])
#     message.body = email_body
#     mail.send(message)
#
#
#
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'docx'])
#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
#
# @app.route("/")
# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created! You are now able to log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)
#
# @app.route("/home",methods=['GET', 'POST'])
# def home():
#     job_data = Job.query.all()
#     if len(job_data)>0:
#         job = job_data[0]
#         resume = Upload.query.all()
#         print(len(resume))
#         resume_files = [f"./web/files/{t.name}" for t in resume if os.path.isfile(f"./web/files/{t.name}")]
#
#         # print(resume_files, job.filename1, "\n\n\n\n")
#         if len(resume_files)>0:
#             result = jd.process_files(f"./web/files/{job.filename1}", resume_files)
#         else:
#             result =[]
#     else:
#         result =[]
#     form = JobForm()
#     if request.method == 'POST':
#        file = request.files['InputFile']
#        print(file)
#
#        filename = secure_filename(file.filename)
#
#        if file and allowed_file(file.filename):
#
#           basedir = os.path.abspath(os.path.dirname(__file__))
#           filename = filename.replace("_","_")
#           filename = filename.replace("-","_")
#           filename = filename.replace(" ","_")
#           file_path =os.path.join(basedir,app.config['UPLOAD_FOLDER'], filename)
#           file.save(file_path)#
#         #   file2 = open(file_path, "rb")
#         #   print(f"Hey word dubg   {file2.read()}")
#           print(f"Hey word dubg   {file.filename}")
#           job = Job(company=form.company.data, Jobtitle=form.Jobtitle.data, filename1 = filename,data=file.read())
#           db.session.add(job)
#           db.session.commit()
#           flash('You have succssfully added Job description', 'success')
#           return redirect(url_for('home'))
#     return render_template('home.html',title = 'Home',form = form, result=result)
#
#
# # @app.route("/account/<job_id>")
# # def account():
# #     return render_template('account.html', title='Account')
#
#
#
#
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('JD'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if form.email.data == 'guest@example.com' and form.password.data == 'guest':
#             flash('You have been logged in!', 'success')
#             # login_user(user, remember=form.remember.data)#
#             session["is_admin"] = True
#             return redirect(url_for('home'))
#
#         elif user and bcrypt.check_password_hash(user.password, form.password.data):
#             session["is_admin"] = False
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('JD'))
#
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('login.html', title='Login', form=form)
#
#
# @app.route("/logout")
# def logout():
#     session["is_admin"] = None
#     logout_user()
#     return redirect(url_for('login'))
#
#
#
#
# @app.route('/upload/<job_id>', methods=['POST','GET'])
# def Upload1(job_id):
#     user_detail = current_user
#     job_uploaded = Job.query.filter_by(id = job_id).first()
#     print("hello")
#     if request.method == "POST":
#         file = request.files['file']
#         filename = secure_filename(file.filename)
#         if file and allowed_file(file.filename):
#             basedir = os.path.abspath(os.path.dirname(__file__))
#             filename = filename.replace("-","_")
#             filename = filename.replace(" ","_")
#             file.save(os.path.join(basedir,app.config['UPLOAD_FOLDER'], filename))#
#             print(user_detail)
#             newFile = Upload(name=filename,data=file.read(), user=user_detail, job_db= job_uploaded)
#             db.session.add(newFile)
#             db.session.commit()
#
#             #get job description#
#             resume_path = filename
#             resume_files = [f"./web/files/{resume_path}" for t in [resume_path] if os.path.isfile(f"./web/files/{resume_path}")]
#             print(resume_files)
#             result = jd.process_files(f"./web/files/{job_uploaded.filename1}", resume_files)
#
#             score = float(result[0][1].split("%")[0])
#
#             if score >=50:
#                 msg = "Congrats at " + str(current_user.username) + " you can proceed to the next stage"
#             else:
#                 msg = "Sorry " + current_user.username + " cannot proceed to the next phase"
#
#             # try:
#             #     send_email("stiveckamash@gmail.com", "hi there are you there", f"<h1>sending form this wotlsnfhlk</h1>  {msg}")
#             # except Exception as e:
#             #     flash(f"An eeror as   {e}")
#                 # return f"Eroor  as  {e}"
#
#
#             # flash('File successfully uploaded ' + file.filename + ' to the database!','success')
#
#             return render_template('account.html', title='Account', msg=msg)
#         else:
#             flash('Invalid Uplaod only txt, pdf,docx')
#
#     return render_template('account.html', title='Account')
#
# @app.route("/JD")
# def JD():
#     jobs = Job.query.all()
#     return render_template('JD.html', jobs=jobs)
#
# import os
#
# @app.route('/download/<job_id>')
# def download(job_id):
#     job = Job.query.filter_by(id=job_id).first()
#     import os
#     # resume = Upload.query.all()
#     # t = jd.process_files(f"./web/files/{job.filename1}", [f"./web/files/{job.filename1}"])
#     # print(f"files\{job.filename1}")
#     # resume_files = [f"./web/files/{t.name}" for t in resume]
#     # t = jd.process_files(f"./web/files/{job.filename1}", resume_files)
#     return send_file(f"files\{job.filename1}")#,attachment_filename=job.filename1,as_attachment=True
#
# @app.route("/view/<job_id>")
# def view_page(job_id):
#     job = Job.query.filter_by(id=job_id).first()
#     resume = Upload.query.filter_by(job_db = job)
#     resume_files = [f"./web/files/{t.name}" for t in resume if os.path.isfile(f"./web/files/{t.name}")]
#     if len(resume_files)>0:
#         t = jd.process_files(f"./web/files/{job.filename1}", resume_files)
#     else:
#         t =[]
#     result = t
#     return render_template("index.html", result=result)
