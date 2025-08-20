import os
import time

import requests
from flask import Flask, render_template, request, redirect, url_for, Response
from dotenv import load_dotenv
from datetime import datetime
from peewee import *
from playhouse.shortcuts import model_to_dict
from prometheus_client import generate_latest, CollectorRegistry, Gauge
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)


if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = (
        MySQLDatabase(
            os.getenv("MYSQL_DATABASE"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            host=os.getenv("MYSQL_HOST"),
            port=3306)
        )

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])


# Navigation items
nav_items = {
    'index': 'Home',
    'hobbies_page': 'Hobbies',
    'timeline': 'Timeline'
}

@app.context_processor
def inject_nav_items():
    return dict(nav_items=nav_items)

# Static data
about_me = [
    "Hello! I'm a passionate developer with a love for technology and innovation. I enjoy solving complex problems and creating elegant solutions. When I'm not coding, you might find me off the beaten path, trekking through forests and swimming in lakes.",
    "My journey in software development began years ago, and since then, I've worked on various projects that have helped me grow both professionally and personally. I'm always eager to learn new skills and take on challenging opportunities."
]

work_experience = [
    {
        "title": "Data Engineer – CVS Health",
        "date_range": "Jan 2025 – Present",
        "description": [
            "Decommissioned IBM DB2 on-prem DB, migrating 100M+ rows to SQL Server with optimized SSIS & C# packages.",
            "Developed executive-facing Power BI dashboards enabling self-service access to key business insights.",
            "Automated ETL with a C# web scraper, removing manual steps and improving data availability.",
            "Created web app to prevent direct prod DB edits, replacing manual inserts/updates.",
            "Optimized complex queries, reducing execution time by 50% for analytics reporting."
        ]
    },
    {
        "title": "Software Engineer Intern – CVS Health",
        "date_range": "May 2024 – Aug 2024",
        "description": [
            "Migrated on-prem Hadoop data to Google Cloud Platform; rebuilt egress pipelines using BigQuery.",
            "Created performance-tuned egress framework, cutting transformation costs by 10% for large tables.",
            "Automated builds and deployments using TeamCity and OctoDeploy, enhancing CI/CD.",
            "Designed normalized database schemas for surveys in MSSQL with T-SQL."
        ]
    },
    {
        "title": "Software Engineer Intern – Metropolitan Transportation Authority",
        "date_range": "Sept 2023 – Jan 2024",
        "description": [
            "Built automated ETL pipelines with Python and Apache Airflow for hybrid data platforms.",
            "Engineered ETL processes using Pandas & DuckDB to extract and clean SharePoint data.",
            "Created real-time Power BI dashboards connected to Azure Data Lake, reducing ad-hoc reporting by 33%.",
            "Maintained internal documentation using Sphinx and developed wiki resources."
        ]
    },
    {
        "title": "Software Engineer Intern – Air Force Research Lab",
        "date_range": "June 2023 – Aug 2023",
        "description": [
            "Researched and implemented genetic algorithms for network anomaly detection.",
            "Built clustering algorithm with C++, openGA, and Boost to process millions of 3D points.",
            "Reduced compute time by 15%+ through profiling and macro-based optimizations.",
            "Used GitHub Actions to automate testing and streamline team collaboration."
        ]
    }
]

education = {
    "institution": "The City College of New York (CCNY)",
    "degree": "Bachelor of Science, Computer Science"
}

hobbies = [
    {
        "name": "Hiking",
        "image": "hobby-hiking.jpg",
        "description": "Exploring nature trails and mountains for adventure and relaxation."
    },
    {
        "name": "Swimming",
        "image": "hobby-swimming.jpg",
        "description": "Staying active and refreshed with regular swimming sessions."
    },
    {
        "name": "Reading",
        "image": "hobby-reading.jpg",
        "description": "Diving into books to discover new worlds and ideas."
    },
    {
        "name": "Gaming",
        "image": "hobby-gaming.jpg",
        "description": "Enjoying immersive video games and strategic challenges."
    }
]

name = "Mahmud Hasan"


@app.route('/')
def index():
    return render_template(
        'index.html',
        title=name,
        url=os.getenv("URL"),
        nav_items=nav_items,
        about_me=about_me,
        work_experience=work_experience,
        education=education,
        hobbies=hobbies,
        year=datetime.now().year
    )

@app.route('/hobbies')
def hobbies_page():
    return render_template(
        'hobbies.html',
        title="My Hobbies",
        nav_items=nav_items,
        hobbies=hobbies,
        year=datetime.now().year
    )


@app.route('/timeline')
def timeline():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())

    # Get error message from URL parameter
    error_message = request.args.get('error')

    return render_template(
        'timeline.html',
        title="Timeline",
        nav_items=nav_items,
        year=datetime.now().year,
        posts=posts,
        error_message=error_message
    )


@app.route('/submit_timeline_post', methods=['POST'])
def submit_timeline_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if not name or not email or not content:
        return redirect(url_for('timeline', error='Please fill in all fields'))

    TimelinePost.create(name=name, email=email, content=content)
    return redirect(url_for('timeline'))


@app.route('/api/timeline_post', methods=['POST'])
def post_timeline_post():
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    # Validate inputs
    if not name or not name.strip():
        return {"error": "Invalid Name"}, 400
    if not content or not content.strip():
        return {"error": "Invalid Content"}, 400
    if not email or '@' not in email:
        return {"error": "Invalid Email"}, 400

    # Create and save post if validation passes
    post = TimelinePost(name=name, email=email, content=content)
    post.save()

    return {"id": post.id, "message": "Resource created successfully."}, 201

@app.route('/api/timeline_post', methods=['GET'])
def get_all_timeline_post():
    # all posts
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:post_id>', methods=['GET'])
def get_timeline_post(post_id):
    """Get a specific timeline post by ID"""
    try:
        post = TimelinePost.get_by_id(post_id)
        return model_to_dict(post)
    except TimelinePost.DoesNotExist:
        return {"error": f"Post with id {post_id} not found."}, 404


@app.route("/metrics")
def metrics():
    registry = CollectorRegistry()

    # health gauges
    flask_up = Gauge("flask_up", "Flask app up", registry=registry)
    db_up = Gauge("mariadb_up", "MariaDB up", registry=registry)
    nginx_up = Gauge("nginx_up", "Nginx up", registry=registry)

    # latency gauges
    flask_latency = Gauge("flask_latency_ms", "Flask latency (ms)", registry=registry)
    db_latency = Gauge("mariadb_latency_ms", "MariaDB query latency (ms)", registry=registry)
    nginx_latency = Gauge("nginx_latency_ms", "Nginx latency (ms)", registry=registry)

    # --- Flask check (self request)
    start = time.time()
    try:
        r= requests.get("http://myportfolio:5000/", timeout=3)
        flask_up.set(1 if r.status_code == 200 else 0)
    except:
        flask_up.set(0)
    flask_latency.set((time.time() - start) * 1000)

    # --- MariaDB health check via Peewee connection
    try:
        start = time.time()
        with mydb.connection_context():
            mydb.execute_sql("SELECT 1;")
        db_up.set(1)
        db_latency.set((time.time() - start) * 1000)
    except Exception:
        db_up.set(0)
        db_latency.set(-1)

    # --- Nginx check
    try:
        start = time.time()
        r = requests.get("http://nginx")
        nginx_up.set(1 if r.status_code == 200 else 0)
        nginx_latency.set((time.time() - start) * 1000)
    except:
        nginx_up.set(0)
        nginx_latency.set(-1)

    return Response(generate_latest(registry), mimetype="text/plain")
