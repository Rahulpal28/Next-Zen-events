import os, sqlite3, hashlib, secrets
from datetime import datetime
from flask import Flask, request, redirect, url_for, session, flash, render_template_string, g
app=Flask(__name__); app.secret_key=os.environ.get('SECRET_KEY','change-this-secret')
DB=os.environ.get('DATABASE_PATH',os.path.join(os.path.dirname(__file__),'nextzen.db'))
def db():
    if 'db' not in g: g.db=sqlite3.connect(DB); g.db.row_factory=sqlite3.Row
    return g.db
@app.teardown_appcontext
def close_db(e=None):
    c=g.pop('db',None)
    if c: c.close()
def ph(p,s=None):
    s=s or secrets.token_hex(16); return s+'$'+hashlib.pbkdf2_hmac('sha256',p.encode(),s.encode(),120000).hex()
def verify(p,v):
    try: s,d=v.split('$',1); return secrets.compare_digest(ph(p,s).split('$',1)[1],d)
    except: return False
def init():
    c=sqlite3.connect(DB); c.executescript('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,name TEXT,email TEXT UNIQUE,password TEXT,role TEXT DEFAULT 'user'); CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,title TEXT,category TEXT,city TEXT,event_date TEXT,budget INTEGER,description TEXT,organizer TEXT); CREATE TABLE IF NOT EXISTS vendors(id INTEGER PRIMARY KEY,name TEXT,category TEXT,city TEXT,price INTEGER,rating REAL,phone TEXT,description TEXT); CREATE TABLE IF NOT EXISTS bookings(id INTEGER PRIMARY KEY,user_id INTEGER,vendor_id INTEGER,event_type TEXT,event_date TEXT,city TEXT,budget INTEGER,notes TEXT,status TEXT DEFAULT 'Pending');''')
    if not c.execute("SELECT id FROM users WHERE email='admin@nextzen.local'").fetchone(): c.execute('INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)',('NextZen Admin','admin@nextzen.local',ph('ChangeMe123!'),'admin'))
    if not c.execute('SELECT id FROM vendors LIMIT 1').fetchone(): c.executemany('INSERT INTO vendors(name,category,city,price,rating,phone,description) VALUES(?,?,?,?,?,?,?)',[('Shubh Tent House','Tent & Venue','Bhopal',12000,4.7,'9876543210','Tents, seating and event lighting.'),('Rhythm Beats DJ','DJ & Sound','Bhopal',7000,4.5,'9876543211','DJ, sound system and stage audio.'),('Madhur Caterers','Catering','Bhopal',250,4.8,'9876543212','Catering packages, priced per plate.'),('Creative Decor Studio','Decoration','Indore',10000,4.6,'9876543213','Floral, balloon and themed decoration.'),('LensCraft Media','Photography','Indore',8000,4.4,'9876543214','Event photography, reels and video.'),('Royal Celebration Planners','Event Planner','Chhindwara',15000,4.9,'9876543215','Event coordination and vendor management.')])
    if not c.execute('SELECT id FROM events LIMIT 1').fetchone(): c.executemany('INSERT INTO events(title,category,city,event_date,budget,description,organizer) VALUES(?,?,?,?,?,?,?)',[('Campus Innovation Meetup','College','Bhopal','2026-11-15',25000,'Student demos, networking and technology talks.','NextZen Community'),('Community Celebration','Cultural','Chhindwara','2026-11-22',50000,'A local cultural gathering with performances.','Community Organizers'),('Startup Connect 2026','Networking','Indore','2026-12-05',75000,'Meet founders and build connections.','NextZen Community')])
    c.commit(); c.close()
CSS="""*{box-sizing:border-box}body{margin:0;background:#f7f8fc;color:#172033;font:15px Arial,sans-serif}a{text-decoration:none;color:inherit}.nav{background:white;border-bottom:1px solid #e7e9f2;padding:18px 5%;display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}.brand{font-size:23px;font-weight:800}.brand span{color:#6558e8}.links{display:flex;gap:16px;align-items:center;flex-wrap:wrap}.wrap{max-width:1120px;margin:auto;padding:28px 20px 55px}.hero{padding:44px;border-radius:25px;color:white;background:linear-gradient(120deg,#201d4d,#6558e8 70%,#9486ff);display:flex;justify-content:space-between;gap:25px;align-items:center}.hero h1{font-size:clamp(34px,5vw,55px);margin:12px 0}.hero p{line-height:1.7;color:#e9e6ff;max-width:600px}.art{font-size:90px}.btn{border:0;display:inline-block;background:#6558e8;color:white;border-radius:10px;padding:12px 16px;font-weight:bold;cursor:pointer}.light{background:#f0efff;color:#5548cf}.search{display:flex;gap:10px;padding:14px;background:white;border-radius:16px;margin:20px 0;flex-wrap:wrap}.search input,.search select{flex:1;min-width:130px}.search input,input,select,textarea{font:inherit;border:1px solid #dfe2ed;padding:12px;border-radius:9px;background:white}.head{margin:32px 0 16px}.head h2{margin:5px 0;font-size:27px}.muted{color:#667085}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.card,.formbox{background:white;border:1px solid #e7e9f2;border-radius:17px;padding:20px}.emoji{height:72px;border-radius:13px;background:linear-gradient(135deg,#f0efff,#ffeaf2);display:grid;place-items:center;font-size:36px;margin-bottom:15px}.tag{background:#f0efff;color:#5548cf;border-radius:20px;padding:5px 9px;font-size:12px;font-weight:bold}.card h3{margin:12px 0 6px}.card p{color:#667085;line-height:1.55}.meta{font-size:13px;color:#596174;display:flex;gap:12px;flex-wrap:wrap;margin:14px 0}.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.formbox{max-width:650px;margin:20px auto;padding:26px}.field{margin:14px 0}.field label{display:block;font-weight:bold;font-size:13px;margin-bottom:7px}.field input,.field select,.field textarea{width:100%}.field textarea{min-height:90px}.notice{background:#eafaf0;color:#126b3a;padding:12px;border-radius:10px;margin-bottom:12px}.error{background:#fff0f0;color:#9f2525}.tablewrap{overflow:auto;background:white;border:1px solid #e7e9f2;border-radius:15px}table{width:100%;border-collapse:collapse;min-width:620px}td,th{padding:13px;text-align:left;border-bottom:1px solid #e7e9f2}th{background:#fafaff}.footer{text-align:center;color:#667085;padding:25px}.empty{padding:40px;background:white;border-radius:15px;text-align:center}.small{font-size:12px;color:#667085}@media(max-width:760px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.hero{padding:27px}.art{display:none}}@media(max-width:540px){.grid{grid-template-columns:1fr}.wrap{padding:18px 13px 40px}.hero{padding:23px}.nav{padding:16px}.formbox{padding:19px}}"""
BASE='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{{title}} · NextZen Events</title><style>'''+CSS+'''</style></head><body><nav class="nav"><a class="brand" href="/">Next<span>Zen</span> Events</a><div class="links"><a href="/">Discover</a><a href="/vendors">Vendors</a>{% if session.get('user_id') %}<a href="/my-bookings">My requests</a>{% if session.get('role')=='admin' %}<a href="/admin">Admin</a>{% endif %}<span>Hi, {{session.get('name')}}</span><a class="btn light" href="/logout">Log out</a>{% else %}<a href="/login">Log in</a><a class="btn" href="/register">Get started</a>{% endif %}</div></nav><main class="wrap">{% with msgs=get_flashed_messages(with_categories=true) %}{% for cat,msg in msgs %}<div class="notice {{'error' if cat=='error' else ''}}">{{msg}}</div>{% endfor %}{% endwith %}{{content|safe}}</main><footer class="footer">© {{year}} NextZen Events · Plan better. Celebrate together.</footer></body></html>'''
def page(content,title='Discover'): return render_template_string(BASE,content=content,title=title,year=datetime.now().year)
@app.route('/')
def home():
    q=request.args.get('q','').strip(); city=request.args.get('city','').strip(); cat=request.args.get('category','').strip(); sql='SELECT * FROM events WHERE 1=1'; a=[]
    if q: sql+=' AND (title LIKE ? OR description LIKE ?)'; a += [f'%{q}%',f'%{q}%']
    if city: sql+=' AND city LIKE ?'; a.append(f'%{city}%')
    if cat: sql+=' AND category=?'; a.append(cat)
    es=db().execute(sql+' ORDER BY event_date',a).fetchall(); cats=[r['category'] for r in db().execute('SELECT DISTINCT category FROM events').fetchall()]; opts=''.join(f'<option>{x}</option>' for x in cats)
    cards=''.join(f'<article class="card"><div class="emoji">🎟️</div><span class="tag">{e["category"]}</span><h3>{e["title"]}</h3><p>{e["description"]}</p><div class="meta">📍 {e["city"]}　 📅 {e["event_date"]}</div><div class="row"><b>₹{e["budget"]:,} budget</b><a class="btn light" href="/events/{e["id"]}">View event</a></div></article>' for e in es) or '<div class="empty">No events match your filters yet.</div>'
    return page(f'<section class="hero"><div><small>YOUR EVENT, YOUR WAY</small><h1>Big moments.<br>Beautifully planned.</h1><p>Discover events and find vendors for weddings, birthdays, college fests and community celebrations—all in one place.</p><a class="btn" style="background:white;color:#5548cf" href="/vendors">Explore vendors ↗</a>　<a class="btn" href="/events/new">List an event</a></div><div class="art">🎉✨</div></section><form class="search"><input name="q" placeholder="Search events" value="{q}"><input name="city" placeholder="City e.g. Bhopal" value="{city}"><select name="category"><option value="">All categories</option>{opts}</select><button class="btn">Search</button></form><div class="head"><h2>Upcoming events</h2><span class="muted">{len(es)} listed</span></div><div class="grid">{cards}</div>')
@app.route('/events/new',methods=['GET','POST'])
def new_event():
    if not session.get('user_id'): flash('Please log in to list an event.'); return redirect('/login')
    if request.method=='POST':
        f=[request.form.get(k,'').strip() for k in ['title','category','city','event_date','budget','description']]
        try: budget=max(0,int(f[4]))
        except: budget=0
        if not all([f[0],f[1],f[2],f[3],f[5]]): flash('Please complete required fields.','error')
        else: db().execute('INSERT INTO events(title,category,city,event_date,budget,description,organizer) VALUES(?,?,?,?,?,?,?)',(f[0],f[1],f[2],f[3],budget,f[5],session['name'])); db().commit(); flash('Your event has been listed.'); return redirect('/')
    return page('''<div class="formbox"><h2>List an event</h2><form method="post"><div class="field"><label>Event name</label><input name="title" required></div><div class="row"><div class="field"><label>Category</label><select name="category"><option>Wedding</option><option>Birthday</option><option>College</option><option>Cultural</option><option>Networking</option><option>Workshop</option><option>Other</option></select></div><div class="field"><label>City</label><input name="city" required></div></div><div class="row"><div class="field"><label>Date</label><input type="date" name="event_date" required></div><div class="field"><label>Budget (₹)</label><input type="number" name="budget" value="0" min="0"></div></div><div class="field"><label>Description</label><textarea name="description" required></textarea></div><button class="btn">Publish event</button></form></div>''','List event')
@app.route('/events/<int:eid>')
def event_detail(eid):
    e=db().execute('SELECT * FROM events WHERE id=?',(eid,)).fetchone()
    if not e: return page('<div class="empty">Event not found. <a href="/">Go home</a></div>'),404
    return page(f'<div class="card"><div class="emoji">🎊</div><span class="tag">{e["category"]}</span><h1>{e["title"]}</h1><p>{e["description"]}</p><div class="meta">📍 {e["city"]}　 📅 {e["event_date"]}　 Organizer: {e["organizer"]}</div><p><b>Estimated budget: ₹{e["budget"]:,}</b></p><a class="btn" href="/vendors?city={e["city"]}">Find vendors in {e["city"]}</a></div>',e['title'])
@app.route('/vendors')
def vendors():
    q=request.args.get('q','').strip(); city=request.args.get('city','').strip(); cat=request.args.get('category','').strip(); sql='SELECT * FROM vendors WHERE 1=1'; a=[]
    if q: sql+=' AND (name LIKE ? OR description LIKE ?)'; a += [f'%{q}%',f'%{q}%']
    if city: sql+=' AND city LIKE ?'; a.append(f'%{city}%')
    if cat: sql+=' AND category=?'; a.append(cat)
    vs=db().execute(sql+' ORDER BY rating DESC',a).fetchall(); cats=[r['category'] for r in db().execute('SELECT DISTINCT category FROM vendors').fetchall()]; opts=''.join(f'<option>{x}</option>' for x in cats); icons={'Tent & Venue':'⛺','DJ & Sound':'🎧','Catering':'🍽️','Decoration':'🌸','Photography':'📸','Event Planner':'🎯'}
    cards=''.join(f'<article class="card"><div class="emoji">{icons.get(v["category"],"✨")}</div><span class="tag">{v["category"]}</span><h3>{v["name"]}</h3><div class="meta">📍 {v["city"]}　 ⭐ {v["rating"]:.1f}</div><p>{v["description"]}</p><div class="row"><b>From ₹{v["price"]:,}</b><a class="btn" href="/vendors/{v["id"]}/book">Request booking</a></div><p class="small">Contact: {v["phone"]}</p></article>' for v in vs) or '<div class="empty">No vendors found.</div>'
    return page(f'<div class="head"><h2>Find your perfect vendor</h2><p class="muted">Compare services, starting prices and ratings.</p></div><form class="search"><input name="q" placeholder="Vendor or service" value="{q}"><input name="city" placeholder="City" value="{city}"><select name="category"><option value="">All services</option>{opts}</select><button class="btn">Filter</button></form><div class="grid">{cards}</div>','Vendors')
@app.route('/vendors/<int:vid>/book',methods=['GET','POST'])
def book(vid):
    v=db().execute('SELECT * FROM vendors WHERE id=?',(vid,)).fetchone()
    if not v: return page('<div class="empty">Vendor not found.</div>'),404
    if not session.get('user_id'): flash('Log in to send a booking request.'); return redirect('/login')
    if request.method=='POST':
        f=[request.form.get(k,'').strip() for k in ['event_type','event_date','city','budget','notes']]
        try: budget=max(0,int(f[3]))
        except: budget=0
        if not all(f[:3]): flash('Fill event type, date and city.','error')
        else: db().execute('INSERT INTO bookings(user_id,vendor_id,event_type,event_date,city,budget,notes) VALUES(?,?,?,?,?,?,?)',(session['user_id'],vid,f[0],f[1],f[2],budget,f[4])); db().commit(); flash('Booking request sent! Track it under My requests.'); return redirect('/my-bookings')
    return page(f'<div class="formbox"><h2>Request a booking</h2><p>{v["name"]} · {v["category"]} · From ₹{v["price"]:,}</p><form method="post"><div class="field"><label>Event type</label><select name="event_type"><option>Wedding</option><option>Birthday</option><option>Ring ceremony</option><option>Haldi / Mehendi</option><option>College event</option><option>Cultural event</option><option>Other</option></select></div><div class="row"><div class="field"><label>Event date</label><input type="date" name="event_date" required></div><div class="field"><label>City</label><input name="city" value="{v["city"]}" required></div></div><div class="field"><label>Budget (₹)</label><input type="number" name="budget" value="{v["price"]}" min="0"></div><div class="field"><label>Notes</label><textarea name="notes"></textarea></div><button class="btn">Send request</button></form></div>','Request booking')
@app.route('/my-bookings')
def my_bookings():
    if not session.get('user_id'): return redirect('/login')
    rs=db().execute('SELECT b.*,v.name vendor FROM bookings b JOIN vendors v ON b.vendor_id=v.id WHERE b.user_id=? ORDER BY b.id DESC',(session['user_id'],)).fetchall(); trs=''.join(f'<tr><td>{r["vendor"]}</td><td>{r["event_type"]}</td><td>{r["event_date"]}</td><td>{r["city"]}</td><td>₹{r["budget"]:,}</td><td><span class="tag">{r["status"]}</span></td></tr>' for r in rs) or '<tr><td colspan="6">No requests yet. Browse vendors to start.</td></tr>'
    return page(f'<h2>My booking requests</h2><div class="tablewrap"><table><tr><th>Vendor</th><th>Event</th><th>Date</th><th>City</th><th>Budget</th><th>Status</th></tr>{trs}</table></div>','My requests')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form.get('name','').strip(); email=request.form.get('email','').strip().lower(); p=request.form.get('password','')
        if not name or not email or len(p)<8: flash('Enter name, email and a password of at least 8 characters.','error')
        else:
            try: cur=db().execute('INSERT INTO users(name,email,password) VALUES(?,?,?)',(name,email,ph(p))); db().commit(); session.update(user_id=cur.lastrowid,name=name,role='user'); return redirect('/')
            except sqlite3.IntegrityError: flash('Email already registered. Please log in.','error')
    return page('''<div class="formbox"><h2>Create account</h2><form method="post"><div class="field"><label>Full name</label><input name="name" required></div><div class="field"><label>Email</label><input name="email" type="email" required></div><div class="field"><label>Password (8+ characters)</label><input name="password" type="password" minlength="8" required></div><button class="btn">Create account</button></form></div>''','Register')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        u=db().execute('SELECT * FROM users WHERE email=?',(request.form.get('email','').strip().lower(),)).fetchone()
        if u and verify(request.form.get('password',''),u['password']): session.update(user_id=u['id'],name=u['name'],role=u['role']); return redirect('/')
        flash('Email or password is incorrect.','error')
    return page('''<div class="formbox"><h2>Welcome back</h2><form method="post"><div class="field"><label>Email</label><input name="email" type="email" required></div><div class="field"><label>Password</label><input name="password" type="password" required></div><button class="btn">Log in</button></form><p class="small">New here? <a href="/register">Create an account</a></p></div>''','Login')
@app.route('/logout')
def logout(): session.clear(); return redirect('/')
@app.route('/admin',methods=['GET','POST'])
def admin():
    if session.get('role')!='admin': flash('Admin access required.','error'); return redirect('/login')
    if request.method=='POST':
        s=request.form.get('status'); bid=request.form.get('booking_id')
        if s in ['Pending','Contacted','Confirmed','Declined']: db().execute('UPDATE bookings SET status=? WHERE id=?',(s,bid)); db().commit(); flash('Booking status updated.')
    rs=db().execute('SELECT b.*,u.name customer,v.name vendor FROM bookings b JOIN users u ON b.user_id=u.id JOIN vendors v ON b.vendor_id=v.id ORDER BY b.id DESC').fetchall(); trs=''.join(f'<tr><td>{r["customer"]}</td><td>{r["vendor"]}</td><td>{r["event_type"]} / {r["event_date"]}</td><td><form method="post"><input type="hidden" name="booking_id" value="{r["id"]}"><select name="status">'+''.join(f'<option {"selected" if r["status"]==s else ""}>{s}</option>' for s in ['Pending','Contacted','Confirmed','Declined'])+'</select> <button class="btn">Save</button></form></td></tr>' for r in rs)
    return page(f'<h2>Admin dashboard</h2><p class="muted">Manage vendor booking requests and update status.</p><div class="tablewrap"><table><tr><th>Customer</th><th>Vendor</th><th>Event</th><th>Status</th></tr>{trs or "<tr><td colspan=4>No bookings yet.</td></tr>"}</table></div><p class="small">Demo admin: admin@nextzen.local / ChangeMe123! — change before public launch.</p>','Admin')
@app.route('/health')
def health(): return {'status':'ok','app':'NextZen Events'}
with app.app_context(): init()
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)),debug=False)
