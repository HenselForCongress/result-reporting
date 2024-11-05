# don/views/results.py
import os
import csv
import requests
from flask import Blueprint, render_template
from collections import defaultdict
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

results_blueprint = Blueprint('results', __name__)

# Environment variable for CSV debugging
CSV_DEBUG = os.getenv("CSV_DEBUG", "false").lower() == "true"
RESULTS_URL = "https://enr.elections.virginia.gov/cdn/results/Virginia/export-2024NovemberGeneral.json"

# Variables to store the latest data and last updated time
latest_data = None
last_updated = None
update_interval = 10



def fetch_data():
    global latest_data, last_updated
    response = requests.get(RESULTS_URL)
    if response.status_code == 200:
        latest_data = response.json()
        est = pytz.timezone("America/New_York")
        last_updated = datetime.now().astimezone(est).strftime('%I:%M %p')  # Format as "8:00 PM"


# Initialize a background scheduler to update data every `update_interval` seconds
scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_data, trigger="interval", seconds=update_interval)
scheduler.start()


@results_blueprint.route('/')
def index():
    if latest_data is None:
        fetch_data()  # Initial fetch if not already fetched

    # Prepare data structures for rendering
    candidates = set()
    county_data = defaultdict(lambda: defaultdict(dict))
    candidate_totals = defaultdict(int)

    for county in latest_data.get("localResults", []):
        county_name = county["name"]
        for race in county.get("ballotItems", []):
            if race["name"] == "Member, House of Representatives (8th District)":
                for candidate in race.get("ballotOptions", []):
                    candidate_name = candidate["name"]
                    candidates.add(candidate_name)
                    for precinct in candidate.get("precinctResults", []):
                        precinct_name = precinct["name"]
                        vote_count = precinct.get("voteCount", 0)
                        county_data[county_name][precinct_name][candidate_name] = vote_count
                        candidate_totals[candidate_name] += vote_count

    candidate_list = sorted(candidates)

    # Save to CSV if CSV_DEBUG is enabled
    if CSV_DEBUG:
        save_to_csv(latest_data, candidate_list, county_data)

    return render_template(
        'index.html',
        candidates=candidate_list,
        county_data=county_data,
        candidate_totals=candidate_totals,
        last_updated=last_updated,
        update_interval=update_interval  # Pass interval to the template
    )

# Function to save results to CSV for debugging
def save_to_csv(data, candidate_list, county_data):
    with open('RESULTS.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        header = ["County", "Precinct"] + candidate_list
        csv_writer.writerow(header)
        for county, precincts in county_data.items():
            for precinct, results in precincts.items():
                row = [county, precinct] + [results.get(candidate, 0) for candidate in candidate_list]
                csv_writer.writerow(row)


@results_blueprint.route('/voting-methods')
def voting_methods():
    # Get the election data
    response = requests.get(RESULTS_URL)
    data = response.json()

    # Prepare data structures
    candidates = set()
    voting_method_data = defaultdict(lambda: defaultdict(int))  # Voting method -> Candidate -> Vote count

    # Iterate over counties and collect results by voting method
    for county in data.get("localResults", []):
        for race in county.get("ballotItems", []):
            if race["name"] == "Member, House of Representatives (8th District)":
                for candidate in race.get("ballotOptions", []):
                    candidate_name = candidate["name"]
                    candidates.add(candidate_name)

                    for method_group in candidate.get("groupResults", []):
                        method_name = method_group["groupName"]
                        vote_count = method_group.get("voteCount", 0)

                        # Sum votes by voting method
                        voting_method_data[method_name][candidate_name] += vote_count

    candidate_list = sorted(candidates)

    return render_template(
        'voting_methods.html',
        candidates=candidate_list,
        voting_method_data=voting_method_data
    )