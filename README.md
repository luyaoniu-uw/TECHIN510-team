# UW Project Topic Submission App

A Streamlit web application for collecting and managing project topic submissions from students, with a bidding system for project selection.

## Features

- Students can submit their name, UW NetID, project topic, and description
- Admin authentication for instructors
- Admin can view all submissions in a table format
- Admin can download all submissions as a CSV file
- Admin can toggle visibility of all topics to students
- Prevents duplicate submissions from the same NetID
- Bidding system where students can allocate 100 points across up to 3 projects
- Admin can view and download bid data
- Visual summary of bids per project

## Setup and Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Usage

### For Students
1. Fill out the submission form with your name, UW NetID, project topic, and description
2. Click "Submit" to save your project topic
3. When the instructor enables topic visibility, you'll be able to see all submitted topics
4. When bidding is enabled, identify yourself in the sidebar and allocate your 100 points across up to 3 projects

### For Instructors (Admin)
1. Access the admin panel from the sidebar
2. Login with the default password: `admin123` (change this immediately!)
3. View all submissions in the admin view section
4. Download submissions as a CSV file
5. Toggle topic visibility to reveal all topics to students
6. Toggle bidding to enable the bidding system for students
7. View all bids in the admin view section, including a summary chart
8. Download bids as a CSV file
9. Change the admin password for security

## Bidding System

The bidding system allows students to:
- Allocate a budget of 100 points across up to 3 projects
- Update their bids at any time before the bidding period ends
- See a running total of points allocated

Instructors can:
- Enable/disable the bidding system
- View all bids in a table format
- See a summary chart of points allocated per project
- Download all bid data as a CSV file

## Data Storage

- All submissions are stored in a JSON file at `data/submissions.json`
- All bids are stored in a JSON file at `data/bids.json`
- These files are created automatically when the first submission/bid is made

## Security Note

The default admin password is `admin123`. It is highly recommended to change this password immediately after the first login for security purposes.

## Requirements

- Python 3.7+
- Streamlit 1.32.0+
- Pandas 2.1.1+ 