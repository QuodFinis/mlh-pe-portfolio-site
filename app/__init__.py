import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
app = Flask(__name__)

# Navigation items
nav_items = {
    'index': 'Home',
    'hobbies_page': 'Hobbies'
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
