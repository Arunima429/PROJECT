import random

from flask import Flask, render_template,request,redirect,session
from DBConnection import Db

app = Flask(__name__)
app.secret_key="abc"

@app.route('/AB')
def hello_world():
    return 'Hello World!'


@app.route('/',methods=['post','get'])
def login():
    if request.method=='POST':
        uname=request.form['textfield2']
        passwrd=request.form['textfield']
        print(uname,passwrd)
        db=Db()
        res=db.selectOne("select * from login where username='"+uname+"' and password='"+passwrd+"'")
        print(res)
        if res is not None:
            if res['usertype']=="admin":
                return redirect('/home')
            elif res['usertype']=="police_station":
                session['lid']=res['login_id']
                return redirect('/police_home')
            elif res['usertype']=="user":
                session['lid'] = res['login_id']
                return redirect('/user_home')
            else:
                return '''<script>alert("Invalid");window.location="/"</script>'''
        else:
            return '''<script>alert("Invalid User");window.location="/"</script>'''
    else:
        return render_template("index.html")



@app.route('/home')
def home():
    return render_template("Admin/home.html")



@app.route('/policereg',methods=['post','get'])
def policereg():
    if request.method=='POST':
        pname=request.form['textfield']
        post=request.form['textfield2']
        pin= request.form['textfield3']
        phone = request.form['textfield4']
        Email= request.form['textfield5']
        passwrd=random.randint(0000,9999)
        db=Db()
        res=db.insert("insert into login VALUES ('','"+Email+"','"+str(passwrd)+"','police_station')")
        db.insert("insert into police_station VALUES ('"+str(res)+"','"+pname+"','"+post+"','"+pin+"','"+Email+"','"+phone+"')")
        return '<script>alert("DONE");window.location="/home"</script>'
    else:
        return render_template("Admin/policeRegistrationform.html")

@app.route('/police_view')
def police_view():
    db = Db()
    w = db.select("select * from police_station")
    return render_template("Admin/police_station_view.html",data=w)

@app.route('/police_update/<b>',methods=['post','get'])
def police_update(b):
    if request.method=='POST':
        pname = request.form['textfield']
        post = request.form['textfield2']
        pin = request.form['textfield3']
        phone = request.form['textfield4']
        Email = request.form['textfield5']
        db=Db()
        db.update("update police_station set station_name='"+pname+"',post='"+post+"',pincode='"+pin+"',phone_no='"+phone+"',email='"+Email+"' where police_id='"+b+"'")
        return '<script>alert("DONE");window.location="/police_view"</script>'

    else:
        db=Db()
        p=db.selectOne("select * from police_station WHERE police_id='"+b+"'")
        return render_template("Admin/policestationupdate.html",res=p)

@app.route('/police_delete/<p>')
def police_delete(p):
    db=Db()
    db.delete("delete from police_station WHERE police_id='"+p+"'")
    return '<script>alert("Deleted");window.location="/police_view"</script>'


@app.route('/crimlst')
def crimlst():
    db = Db()
    c = db.select("select * from criminal_list")
    return render_template("Admin/Criminallstview.html", res=c)





@app.route('/workerlst')
def workerlst():
    db = Db()
    w = db.select("select * from worker")
    return render_template("Admin/workerview.html",data=w)


@app.route('/compview')
def compview():
    db = Db()
    s = db.select("select * from complaint,user where complaint.user_id=user.user_id and reply='pending' ")

    return render_template("Admin/complaintview.html",res=s)

@app.route('/reply/<cid>')
def reply(cid):
    db=Db()
    r=db.selectOne("select * from complaint WHERE cmp_id='"+cid+"'")
    return render_template("Admin/reply.html",data=r)
@app.route('/reply_action/<cid>',methods=['post'])
def reply_action(cid):
    reply=request.form['textarea']
    db=Db()
    db.update("update complaint set reply='"+reply+"', r_date=curdate() where cmp_id='"+cid+"'")
    return redirect('/compview')


@app.route('/notify',methods=['POST','GET'])
def notify():
    if request.method=='POST':
        notif=request.form['textarea']
        db=Db()
        db.insert("insert into notification VALUES ('',curdate(),'"+notif+"')")
        return '<script>alert("notification sent");window.location="/home"</script>'
    else:

        return render_template("Admin/notification.html")


@app.route('/feedback')
def feedback():
    db = Db()
    w = db.select("select * from feedback,user where feedback.user_id=user.user_id")

    return render_template("Admin/feedbackview.html", res=w)

# ////////////////////////////////////////////////////////////////

@app.route('/police_home')
def police_home():
    return render_template('PoliceStation/police_home.html')

@app.route('/policefeedback')
def policefeedback():
    db = Db()
    w = db.select("select * from feedback,user where feedback.user_id=user.user_id and police_id='"+str(session['lid'])+"'")

    return render_template('PoliceStation/feedbackview.html',res=w)


@app.route('/view_complaint')
def view_complaint():
    db = Db()
    s = db.select("select * from complaint,user where complaint.user_id=user.user_id and reply='pending'")

    return render_template("PoliceStation/complaintview.html",res=s)


@app.route('/view_notify')
def view_notify():
    db = Db()
    s = db.select("select * from notification")

    return render_template("PoliceStation/ViewNotify.html",res=s)

@app.route('/workerreg',methods=['post','get'])
def workerreg():
    if request.method=='POST':
        wname=request.form['textfield2']
        gender=request.form['RadioGroup1']
        dob= request.form['textfield3']
        phone = request.form['textfield4']
        place= request.form['textfield5']
        skills = request.form['textfield6']
     #   passwrd=random.randint(0000,9999)
        db=Db()
       # res=db.insert("insert into login VALUES ('','"+Email+"','"+str(passwrd)+"','police_station')")
        db.insert("insert into worker VALUES ('','"+wname+"','"+gender+"','"+phone+"','"+dob+"','"+place+"','"+skills+"')")
        return '<script>alert("DONE");window.location="/police_home"</script>'
    else:
        return render_template("PoliceStation/workerReg.html")

@app.route('/worker_view')
def worker_view():
    db = Db()
    w = db.select("select * from worker")
    return render_template("PoliceStation/workerView.html",res=w)



@app.route('/worker_update/<b>',methods=['post','get'])
def worker_update(b):
    if request.method=='POST':

        wname = request.form['textfield2']
        gender = request.form['RadioGroup1']
        dob = request.form['textfield3']
        phone = request.form['textfield4']
        place = request.form['textfield5']
        skills = request.form['textfield6']
        db=Db()
        db.update("update worker set w_name='"+wname+"',gender='"+gender+"',phone_no='"+phone+"',dob='"+dob+"',place='"+place+"',skills='"+skills+"' where w_id='"+b+"'")
        return '<script>alert("DONE");window.location="/worker_view"</script>'

    else:
        db=Db()
        p=db.selectOne("select * from worker WHERE w_id='"+b+"'")
        return render_template("PoliceStation/workerUpdate.html",res=p)

@app.route('/worker_delete/<p>')
def worker_delete(p):
    db=Db()
    db.delete("delete from worker WHERE w_id='"+p+"'")
    return '<script>alert("Deleted");window.location="/worker_view"</script>'


@app.route('/crimreg',methods=['post','get'])
def crimreg():
    if request.method=='POST':
        name=request.form['textfield5']
        gender=request.form['RadioGroup1']
        dob= request.form['textfield3']
        place= request.form['textfield2']
        crimetype = request.form['textfield']
        # stationdetails = request.form['textarea']
     #   passwrd=random.randint(0000,9999)
        db=Db()
       # res=db.insert("insert into login VALUES ('','"+Email+"','"+str(passwrd)+"','police_station')")
        db.insert("insert into criminal_list VALUES ('','"+name+"','"+crimetype+"','"+place+"','"+gender+"','"+dob+"','"+str(session['lid'])+"')")
        return '<script>alert("DONE");window.location="/police_home"</script>'
    else:
        return render_template("PoliceStation/CriminalReg.html")

@app.route('/crime_view')
def crime_view():
    db = Db()
    w = db.select("select * from criminal_list,police_station where criminal_list.station_id=police_station.police_id")
    return render_template("PoliceStation/crimeView.html",res=w)


@app.route('/crime_update/<b>',methods=['post','get'])
def crime_update(b):
    if request.method=='POST':
        name = request.form['textfield']
        gender = request.form['RadioGroup1']
        dob = request.form['textfield2']
        place = request.form['textfield3']
        crimetype = request.form['textfield4']
        db=Db()
        db.update("update criminal_list set name='"+name+"',gender='"+gender+"',dob='"+dob+"',place='"+place+"',crime_type='"+crimetype+"' where c_id='"+b+"'")
        return '<script>alert("DONE");window.location="/crime_view"</script>'

    else:
        db=Db()
        p=db.selectOne("select * from criminal_list WHERE c_id='"+b+"'")
        print(p)
        ge=p['gender']
        do=p['dob']
        print(ge,do)
        return render_template("PoliceStation/crimeupdate.html",res=p,gender=ge,Do=do)

@app.route('/criminal_delete/<p>')
def criminal_delete(p):
    db=Db()
    db.delete("delete from criminal_list WHERE c_id='"+p+"'")
    return '<script>alert("Deleted");window.location="/crime_view"</script>'



#/////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/userreg',methods=['post','get'])
def userreg():
    if request.method == 'POST':
        uname = request.form['textfield']
        place= request.form['textfield2']
        phoneno = request.form['textfield3']
        email = request.form['textfield4']
        passwrd= request.form['textfield5']
        db = Db()
        res=db.insert("insert into login VALUES ('','"+email+"','"+str(passwrd)+"','user')")
        db.insert("insert into user VALUES ('"+str(res)+"','" + uname + "','" + phoneno + "','" + place+ "','" + email+ "')")
        return '<script>alert("DONE");window.location="/user_home"</script>'
    else:
        return render_template("User/reg.html")


@app.route('/user_home')
def user_home():
    return render_template('User/user_home.html')


@app.route('/send_feedback',methods=['POST','GET'])
def send_feedback():
    if request.method=='POST':
        feedback=request.form['textfield']
        db=Db()
        db.insert("insert into feedback VALUES ('','"+str(session['lid'])+"',curdate(),'"+feedback+"')")
        return '<script>alert("notification sent");window.location="/user_home"</script>'
    else:

        return render_template("User/AddFeedback.html")


@app.route('/send_Complaint',methods=['POST','GET'])
def send_Complaint():
    if request.method=='POST':
        p=request.form['select']
        comp=request.form['textarea']
        db=Db()
        db.insert("insert into complaint VALUES ('','"+str(session['lid'])+"','"+comp+"',curdate(),'pending','pending','"+p+"')")
        return '<script>alert("Complaint sent");window.location="/user_home"</script>'
    else:
        db=Db()
        ss=db.select("select * from police_station")

        return render_template("User/addComplaint.html",data=ss)

@app.route('/view_reply')
def view_reply():
    db = Db()
    s = db.select("select reply,r_date from complaint where reply!='pending'")
    return render_template('User/replyview.html',res=s)

@app.route('/search_worker',methods=['post','get'])
def search_worker():
    db = Db()
    if request.method == 'POST':
        w = request.form['textfield']
        q=db.select("select * from worker where w_name LIKE '%"+w+"%'")
        return  render_template('User/searchWorker.html',res=q)
    else:
        q = db.select("select * from worker")
        return render_template('User/searchWorker.html',res=q)


if __name__ == '__main__':
    app.run(port=5000)