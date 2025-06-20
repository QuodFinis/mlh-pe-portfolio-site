from flask import Flask, render_template

app = Flask(__name__)

nav_items = {
    'index': 'Home',
    'hobbies': 'Hobbies'
}

@app.context_processor
def inject_nav_items():
    return dict(nav_items=nav_items)

@app.route('/')
def index():
    return render_template(
        'index.html',
        title="My Portfolio",
        work_experience=[
            {
                'title': "Data Engineer – CVS Health",
                'dates': "Jan 2025 – Present",
                'bullets': [
                    "Decommissioned IBM DB2 on-prem DB, migrating 100M+ rows to SQL Server with optimized SSIS & C# packages.",
                    "Developed executive-facing Power BI dashboards enabling self-service access to key business insights.",
                    "Automated ETL with a C# web scraper, removing manual steps and improving data availability.",
                    "Created web app to prevent direct prod DB edits, replacing manual inserts/updates.",
                    "Optimized complex queries, reducing execution time by 50% for analytics reporting."
                ]
            },
            {
                'title': "Software Engineer Intern – CVS Health",
                'dates': "May 2024 – Aug 2024",
                'bullets': [
                    "Migrated on-prem Hadoop data to Google Cloud Platform; rebuilt egress pipelines using BigQuery.",
                    "Created performance-tuned egress framework, cutting transformation costs by 10% for large tables.",
                    "Automated builds and deployments using TeamCity and OctoDeploy, enhancing CI/CD.",
                    "Designed normalized database schemas for surveys in MSSQL with T-SQL."
                ]
            },
            {
                'title': "Software Engineer Intern – Metropolitan Transportation Authority",
                'dates': "Sept 2023 – Jan 2024",
                'bullets': [
                    "Built automated ETL pipelines with Python and Apache Airflow for hybrid data platforms.",
                    "Engineered ETL processes using Pandas & DuckDB to extract and clean SharePoint data.",
                    "Created real-time Power BI dashboards connected to Azure Data Lake, reducing ad-hoc reporting by 33%.",
                    "Maintained internal documentation using Sphinx and developed wiki resources."
                ]
            },
            {
                'title': "Software Engineer Intern – Air Force Research Lab",
                'dates': "June 2023 – Aug 2023",
                'bullets': [
                    "Researched and implemented genetic algorithms for network anomaly detection.",
                    "Built clustering algorithm with C++, openGA, and Boost to process millions of 3D points.",
                    "Reduced compute time by 15%+ through profiling and macro-based optimizations.",
                    "Used GitHub Actions to automate testing and streamline team collaboration."
                ]
            }
        ],
        education={
            'school': "The City College of New York (CCNY)",
            'degree': "Bachelor of Science, Computer Science"
        }
    )

@app.route('/hobbies')
def hobbies():
    return render_template(
        'hobbies.html',
        title="Hobbies",
        hobbies=[
            {'name': 'Hiking', 'image': 'img/hobby-hiking.jpg'},
            {'name': 'Swimming', 'image': 'img/hobby-swimming.jpg'},
            {'name': 'Reading', 'image': 'img/hobby-reading.jpg'},
            {'name': 'Games', 'image': 'img/hobby-gaming.jpg'},
        ]
    )
