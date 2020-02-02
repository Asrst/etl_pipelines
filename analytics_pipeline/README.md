# Analytics Pipeline
This repo contains the code for creating a simple data pipeline from fake log files.


# Usage
* Execute the three scripts mentioned below, in order.

* `generate_logs.py` - generates fake webserver logs.
* `store_logs.py` -- parses the logs and stores them in a SQLite database.
* `count_visitors.py` -- pulls from the database to count visitors to the site per day.

You should see output from `count_visitors.py`.


# Installation
To get this repo running:

1. Install Python 3.
2. Create a [virtual environment](https://docs.python.org/3/library/venv.html).
3. Clone this repo with `git clone REPO_URL`
4. Change directory using `cd analytics_pipeline`
5. Install the requirements with `pip install -r requirements.txt`



