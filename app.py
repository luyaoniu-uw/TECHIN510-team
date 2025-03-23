import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import uuid  # Import UUID for generating unique keys

# Set page configuration
st.set_page_config(
    page_title="TECHIN 510 Project Ideas",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'reveal_topics' not in st.session_state:
    st.session_state.reveal_topics = False
if 'admin_password' not in st.session_state:
    st.session_state.admin_password = "admin123"  # Default password, change this!
if 'bidding_enabled' not in st.session_state:
    st.session_state.bidding_enabled = False
if 'confirm_bid' not in st.session_state:
    st.session_state.confirm_bid = False
if 'bid_data' not in st.session_state:
    st.session_state.bid_data = None
if 'reveal_bid_stats' not in st.session_state:
    st.session_state.reveal_bid_stats = False
if 'reveal_top_bidders' not in st.session_state:
    st.session_state.reveal_top_bidders = False
if 'current_section' not in st.session_state:
    st.session_state.current_section = "Section A"

# Available class sections
SECTIONS = ["Section A", "Section B"]

# File paths with section-specific files
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Function to get section-specific file paths
def get_section_files(section):
    section_suffix = section.replace(" ", "_").lower()
    return {
        'submissions': os.path.join(DATA_DIR, f"submissions_{section_suffix}.json"),
        'bids': os.path.join(DATA_DIR, f"bids_{section_suffix}.json")
    }

# Function to load existing submissions for current section
def load_submissions():
    section_files = get_section_files(st.session_state.current_section)
    submissions_file = section_files['submissions']
    
    try:
        if os.path.exists(submissions_file):
            # Check if file is empty
            if os.path.getsize(submissions_file) == 0:
                # File exists but is empty, return empty list
                return []
                
            with open(submissions_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    # Invalid JSON, create a new file with empty list
                    with open(submissions_file, 'w') as f:
                        json.dump([], f)
                    return []
        else:
            # Create the file with an empty list
            with open(submissions_file, 'w') as f:
                json.dump([], f)
            return []
    except Exception as e:
        st.error(f"Error loading submissions: {str(e)}")
        return []

# Function to save submissions for current section
def save_submission(name, netid, topic, description):
    section_files = get_section_files(st.session_state.current_section)
    submissions_file = section_files['submissions']
    
    try:
        submissions = load_submissions()
        
        # Check if this netid already submitted
        for submission in submissions:
            if submission['netid'] == netid:
                st.error(f"A submission with NetID {netid} already exists!")
                return False
        
        # Add new submission
        submission = {
            'name': name,
            'netid': netid,
            'topic': topic,
            'description': description,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'section': st.session_state.current_section
        }
        
        submissions.append(submission)
        
        # Save to file
        with open(submissions_file, 'w') as f:
            json.dump(submissions, f, indent=4)
        
        return True
    except Exception as e:
        st.error(f"Error saving submission: {str(e)}")
        return False

# Function to load existing bids for current section
def load_bids():
    section_files = get_section_files(st.session_state.current_section)
    bids_file = section_files['bids']
    
    try:
        if os.path.exists(bids_file):
            # Check if file is empty
            if os.path.getsize(bids_file) == 0:
                # File exists but is empty, return empty list
                return []
                
            with open(bids_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    # Invalid JSON, create a new file with empty list
                    with open(bids_file, 'w') as f:
                        json.dump([], f)
                    return []
        else:
            # Create the file with an empty list
            with open(bids_file, 'w') as f:
                json.dump([], f)
            return []
    except Exception as e:
        st.error(f"Error loading bids: {str(e)}")
        return []

# Function to save a bid for current section
def save_bid(netid, name, bids):
    section_files = get_section_files(st.session_state.current_section)
    bids_file = section_files['bids']
    
    try:
        all_bids = load_bids()
        
        # Check if this netid already bid
        for i, bid in enumerate(all_bids):
            if bid['netid'] == netid:
                # Update existing bid
                all_bids[i] = {
                    'netid': netid,
                    'name': name,
                    'bids': bids,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'section': st.session_state.current_section
                }
                break
        else:
            # Add new bid
            all_bids.append({
                'netid': netid,
                'name': name,
                'bids': bids,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'section': st.session_state.current_section
            })
        
        # Save to file
        with open(bids_file, 'w') as f:
            json.dump(all_bids, f, indent=4)
        
        return True
    except Exception as e:
        st.error(f"Error saving bid: {str(e)}")
        return False

# Function to toggle reveal topics state
def toggle_reveal():
    st.session_state.reveal_topics = not st.session_state.reveal_topics

# Function to toggle bidding state
def toggle_bidding():
    st.session_state.bidding_enabled = not st.session_state.bidding_enabled

# Function to toggle bid stats visibility
def toggle_bid_stats():
    st.session_state.reveal_bid_stats = not st.session_state.reveal_bid_stats

# Function to toggle top bidders visibility
def toggle_top_bidders():
    st.session_state.reveal_top_bidders = not st.session_state.reveal_top_bidders

# Function to authenticate admin
def authenticate(password):
    if password == st.session_state.admin_password:
        st.session_state.authenticated = True
        return True
    else:
        st.error("Incorrect password!")
        return False

# Function to change admin password
def change_password(current, new):
    if current == st.session_state.admin_password:
        st.session_state.admin_password = new
        st.success("Password changed successfully!")
        return True
    else:
        st.error("Current password is incorrect!")
        return False

# Function to delete a bid
def delete_bid(netid):
    section_files = get_section_files(st.session_state.current_section)
    bids_file = section_files['bids']
    
    try:
        all_bids = load_bids()
        
        # Find and remove the bid with the given netid
        for i, bid in enumerate(all_bids):
            if bid['netid'] == netid:
                del all_bids[i]
                break
        
        # Save the updated bids
        with open(bids_file, 'w') as f:
            json.dump(all_bids, f, indent=4)
        
        return True
    except Exception as e:
        st.error(f"Error deleting bid: {str(e)}")
        return False

# Function to handle bid submission
def handle_bid_submission():
    if st.session_state.bid_data:
        bid_data = st.session_state.bid_data
        if save_bid(bid_data['netid'], bid_data['name'], bid_data['bids']):
            st.session_state.bid_data = None
            st.session_state.confirm_bid = False
            return True
    return False

# Function to clear all submissions for current section
def clear_submissions():
    section_files = get_section_files(st.session_state.current_section)
    submissions_file = section_files['submissions']
    
    try:
        # Create empty submissions file
        with open(submissions_file, 'w') as f:
            json.dump([], f)
        return True
    except Exception as e:
        st.error(f"Error clearing submissions: {str(e)}")
        return False

# Function to clear all bids for current section
def clear_bids():
    section_files = get_section_files(st.session_state.current_section)
    bids_file = section_files['bids']
    
    try:
        # Create empty bids file
        with open(bids_file, 'w') as f:
            json.dump([], f)
        return True
    except Exception as e:
        st.error(f"Error clearing bids: {str(e)}")
        return False

# Main app layout
def main():
    st.title("UW Project Topic Submission")
    
    # Sidebar for admin login and user identification
    with st.sidebar:
        # Section selector (always visible)
        st.header("Class Section")
        selected_section = st.selectbox(
            "Select your class section:",
            options=SECTIONS,
            index=SECTIONS.index(st.session_state.current_section)
        )
        
        # Update current section if changed
        if selected_section != st.session_state.current_section:
            st.session_state.current_section = selected_section
            # Clear user identification when switching sections
            if 'user_name' in st.session_state:
                del st.session_state.user_name
            if 'user_netid' in st.session_state:
                del st.session_state.user_netid
            st.experimental_rerun()
        
        st.info(f"Currently viewing: {st.session_state.current_section}")
        
        st.header("Admin Panel")
        if not st.session_state.authenticated:
            with st.form("login_form"):
                password = st.text_input("Admin Password", type="password")
                submit_button = st.form_submit_button("Login")
                if submit_button:
                    authenticate(password)
        else:
            st.success("Authenticated as Admin")
            
            # Admin controls
            if st.button("Toggle Topic Visibility", key="toggle"):
                toggle_reveal()
            
            if st.button("Toggle Bidding", key="toggle_bid"):
                toggle_bidding()
            
            if st.button("Toggle Bid Statistics Visibility", key="toggle_stats"):
                toggle_bid_stats()
            
            if st.button("Toggle Top Bidders Visibility", key="toggle_top"):
                toggle_top_bidders()
            
            # Data management section
            st.subheader("Data Management")
            
            # Use expanders for clear data operations to avoid session state issues
            with st.expander(f"Clear All Submissions ({st.session_state.current_section})"):
                st.warning(f"⚠️ This will delete ALL submissions for {st.session_state.current_section}. This action cannot be undone!")
                if st.button("Clear All Submissions", key="clear_submissions_btn"):
                    if clear_submissions():
                        st.success(f"All submissions for {st.session_state.current_section} have been cleared!")
                        st.rerun()
            
            with st.expander(f"Clear All Bids ({st.session_state.current_section})"):
                st.warning(f"⚠️ This will delete ALL bids for {st.session_state.current_section}. This action cannot be undone!")
                if st.button("Clear All Bids", key="clear_bids_btn"):
                    if clear_bids():
                        st.success(f"All bids for {st.session_state.current_section} have been cleared!")
                        st.rerun()
            
            # Download data
            submissions = load_submissions()
            if submissions:
                df = pd.DataFrame(submissions)
                csv = df.to_csv(index=False)
                st.download_button(
                    label=f"Download {st.session_state.current_section} Submissions (CSV)",
                    data=csv,
                    file_name=f"project_submissions_{st.session_state.current_section.lower().replace(' ', '_')}.csv",
                    mime="text/csv"
                )
            
            # Download bids
            bids = load_bids()
            if bids:
                # Convert bids to a flat dataframe
                bid_rows = []
                for bid in bids:
                    for project_bid in bid['bids']:
                        bid_rows.append({
                            'netid': bid['netid'],
                            'name': bid['name'],
                            'project_id': project_bid['project_id'],
                            'project_title': project_bid['project_title'],
                            'points': project_bid['points'],
                            'timestamp': bid['timestamp'],
                            'section': st.session_state.current_section
                        })
                
                if bid_rows:
                    bid_df = pd.DataFrame(bid_rows)
                    bid_csv = bid_df.to_csv(index=False)
                    st.download_button(
                        label=f"Download {st.session_state.current_section} Bids (CSV)",
                        data=bid_csv,
                        file_name=f"project_bids_{st.session_state.current_section.lower().replace(' ', '_')}.csv",
                        mime="text/csv"
                    )
            
            # Change password
            with st.expander("Change Admin Password"):
                with st.form("change_password_form"):
                    current_pwd = st.text_input("Current Password", type="password")
                    new_pwd = st.text_input("New Password", type="password")
                    confirm_pwd = st.text_input("Confirm New Password", type="password")
                    
                    if st.form_submit_button("Change Password"):
                        if new_pwd != confirm_pwd:
                            st.error("New passwords don't match!")
                        else:
                            change_password(current_pwd, new_pwd)
        
        # User identification for bidding
        if st.session_state.reveal_topics and st.session_state.bidding_enabled:
            st.header("Identify Yourself for Bidding")
            with st.form("user_id_form"):
                user_name = st.text_input("Your Name")
                user_netid = st.text_input("Your UW NetID")
                submit_id = st.form_submit_button("Identify")
                
                if submit_id:
                    if not user_name or not user_netid:
                        st.error("Please enter your name and NetID")
                    else:
                        # Verify that the name and NetID match a submission
                        submissions = load_submissions()
                        valid_user = False
                        
                        for submission in submissions:
                            if submission['netid'].lower() == user_netid.lower() and submission['name'].lower() == user_name.lower():
                                valid_user = True
                                # Use the exact name and netid from the submission to ensure consistency
                                st.session_state.user_name = submission['name']
                                st.session_state.user_netid = submission['netid']
                                st.success(f"Identified as {submission['name']} ({submission['netid']}) in {st.session_state.current_section}")
                                break
                        
                        if not valid_user:
                            st.error(f"Your name and NetID don't match any project submission in {st.session_state.current_section}. Please use the same name and NetID you used when submitting your project topic.")
    
    # Main content
    try:
        submissions = load_submissions()
        
        # Display all topics if reveal is enabled
        if st.session_state.reveal_topics:
            st.header("All Project Topics")
            st.info("The instructor has revealed all project topics!")
            
            # Show notification about top bidders feature if enabled
            if st.session_state.reveal_top_bidders:
                st.success("Top bidders visibility is enabled! Project owners can now see the top 3 bidders for their projects.")
                
                # Add debugging information
                with st.expander("Troubleshooting Top Bidders Visibility"):
                    st.write("If you can't see the top bidders for your project, check the following:")
                    
                    # Check if user is identified
                    if 'user_netid' in st.session_state:
                        st.write(f"✅ You are identified as: {st.session_state.user_name} ({st.session_state.user_netid})")
                        
                        # Check if user has a project
                        user_has_project = False
                        user_project_id = None
                        user_project_title = None
                        for i, submission in enumerate(submissions):
                            if submission['netid'] == st.session_state.user_netid:
                                user_has_project = True
                                user_project_id = f"Project {i+1}"
                                user_project_title = submission['topic']
                                break
                        
                        if user_has_project:
                            st.write(f"✅ You have submitted a project: {user_project_id}: {user_project_title}")
                            
                            # Check if there are bids on the user's project
                            bids = load_bids()
                            project_bids = []
                            
                            if bids:
                                for bid in bids:
                                    for project_bid in bid['bids']:
                                        # More flexible matching to handle potential format differences
                                        bid_project_id = project_bid['project_id'].strip()
                                        current_project_id = user_project_id.strip()
                                        
                                        # Try different matching approaches
                                        exact_match = bid_project_id == current_project_id
                                        contains_match = bid_project_id in current_project_id or current_project_id in bid_project_id
                                        
                                        if exact_match or contains_match:
                                            project_bids.append({
                                                'Student': bid['name'],
                                                'NetID': bid['netid'],
                                                'Points': project_bid['points']
                                            })
                                    
                                    if project_bids:
                                        st.write(f"✅ There are {len(project_bids)} bids on your project")
                                        st.write("You should see the top bidders section below.")
                                        
                                        # Display top bidders directly here for better visibility
                                        st.subheader("👑 Top Bidders for Your Project")
                                        
                                        # Sort by points in descending order and take top 3
                                        top_bidders = sorted(project_bids, key=lambda x: x['Points'], reverse=True)[:3]
                                        
                                        # Create a DataFrame for display
                                        top_df = pd.DataFrame(top_bidders)
                                        st.dataframe(top_df)
                                        
                                        # Show a bar chart of top bidders
                                        if len(top_bidders) > 0:
                                            chart_data = pd.DataFrame({
                                                'Student': [f"{b['Student']} ({b['NetID']})" for b in top_bidders],
                                                'Points': [b['Points'] for b in top_bidders]
                                            })
                                            
                                            # Create Plotly bar chart with rotated x-axis labels
                                            fig = px.bar(
                                                chart_data, 
                                                x='Student', 
                                                y='Points',
                                                title='Top Bidders for Your Project'
                                            )
                                            
                                            # Customize the layout
                                            fig.update_layout(
                                                xaxis=dict(
                                                    tickangle=45,
                                                    tickmode='array',
                                                    tickvals=list(range(len(chart_data))),
                                                    ticktext=chart_data['Student']
                                                ),
                                                margin=dict(b=100)  # Add bottom margin for rotated labels
                                            )
                                            
                                            # Generate a unique key using UUID
                                            unique_key = f"top_bidders_chart_{uuid.uuid4()}"
                                            
                                            # Display the Plotly chart with the unique key
                                            st.plotly_chart(fig, use_container_width=True, key=unique_key)
                                        else:
                                            st.write("❌ There are no bids on your project yet")
                                        st.write("Once other students bid on your project, you'll see the top bidders section.")
                                    else:
                                        st.write("❌ There are no bids in the system yet")
                                else:
                                    st.write("❌ You haven't submitted a project")
                                    st.write("Only project owners can see the top bidders for their projects.")
                            else:
                                st.write("❌ You are not identified")
                                st.write("Please identify yourself in the sidebar to see top bidders for your project.")
                        
                        if 'user_netid' in st.session_state:
                            # Find if the current user has submitted a project
                            user_has_project = False
                            for submission in submissions:
                                if submission['netid'] == st.session_state.user_netid:
                                    user_has_project = True
                                    break
                            
                            if user_has_project:
                                st.info("Look for the 'Top Bidders for Your Project' section above.")
                            else:
                                st.warning("You haven't submitted a project, so you won't see any top bidders information.")
                        else:
                            st.warning("Please identify yourself in the sidebar to see top bidders for your project.")
            
            if not submissions:
                st.warning("No submissions yet.")
            else:
                # Display projects
                for i, submission in enumerate(submissions):
                    project_id = f"Project {i+1}"
                    project_title = submission['topic']
                    
                    with st.expander(f"{project_id}: {project_title} (by {submission['name']})"):
                        st.write(f"**Description:** {submission['description']}")
                        st.write(f"**Submitted by:** {submission['name']} ({submission['netid']})")
                        st.write(f"**Submitted on:** {submission['timestamp']}")
                        
                        # Show top bidders for this project if enabled and if the current user is the project owner
                        if st.session_state.reveal_top_bidders and 'user_netid' in st.session_state:
                            # Check if current user is the project owner
                            is_owner = submission['netid'] == st.session_state.user_netid
                            
                            if is_owner:
                                st.markdown("---")
                                st.markdown("### 👑 Top Bidders for Your Project (Expander View)")
                                st.write("For better visibility, the top bidders are also shown at the top of the page.")
                                
                                # Display top bidders in the expander view too
                                bids = load_bids()
                                if bids:
                                    # Collect all bids for this project
                                    project_bids = []
                                    for bid in bids:
                                        for project_bid in bid['bids']:
                                            # More flexible matching to handle potential format differences
                                            bid_project_id = project_bid['project_id'].strip()
                                            current_project_id = project_id.strip()
                                            
                                            # Try different matching approaches
                                            exact_match = bid_project_id == current_project_id
                                            contains_match = bid_project_id in current_project_id or current_project_id in bid_project_id
                                            
                                            if exact_match or contains_match:
                                                project_bids.append({
                                                    'Student': bid['name'],
                                                    'NetID': bid['netid'],
                                                    'Points': project_bid['points']
                                                })
                                    
                                    if project_bids:
                                        # Sort by points in descending order and take top 3
                                        top_bidders = sorted(project_bids, key=lambda x: x['Points'], reverse=True)[:3]
                                        
                                        # Create a DataFrame for display
                                        top_df = pd.DataFrame(top_bidders)
                                        st.dataframe(top_df)
                                        
                                        # Show a bar chart of top bidders
                                        if len(top_bidders) > 0:
                                            chart_data = pd.DataFrame({
                                                'Student': [f"{b['Student']} ({b['NetID']})" for b in top_bidders],
                                                'Points': [b['Points'] for b in top_bidders]
                                            })
                                            
                                            # Create Plotly bar chart with rotated x-axis labels
                                            fig = px.bar(
                                                chart_data, 
                                                x='Student', 
                                                y='Points',
                                                title='Top Bidders for Your Project'
                                            )
                                            
                                            # Customize the layout
                                            fig.update_layout(
                                                xaxis=dict(
                                                    tickangle=45,
                                                    tickmode='array',
                                                    tickvals=list(range(len(chart_data))),
                                                    ticktext=chart_data['Student']
                                                ),
                                                margin=dict(b=100)  # Add bottom margin for rotated labels
                                            )
                                            
                                            # Generate a unique key using UUID for the expander chart
                                            expander_key = f"expander_chart_{uuid.uuid4()}"
                                            
                                            # Display the Plotly chart with the unique key
                                            st.plotly_chart(fig, use_container_width=True, key=expander_key)
                                    else:
                                        st.info("No bids have been placed on your project yet.")
                
                # Bidding section
                if st.session_state.bidding_enabled:
                    st.header("Project Bidding")
                    st.info("You have a budget of 100 points to allocate across up to 3 projects.")
                    
                    # Show overall bid statistics if enabled
                    if st.session_state.reveal_bid_stats:
                        bids = load_bids()
                        if bids:
                            # Create a more detailed view of bids
                            bid_details = []
                            for bid in bids:
                                for project_bid in bid['bids']:
                                    bid_details.append({
                                        'Project': project_bid['project_title'],
                                        'Points': project_bid['points']
                                    })
                            
                            if bid_details:
                                st.subheader("Project Popularity Overview")
                                
                                # Create DataFrames for different statistics
                                bid_df = pd.DataFrame(bid_details)
                                
                                # Total points per project
                                points_per_project = bid_df.groupby('Project')['Points'].sum().reset_index()
                                points_per_project = points_per_project.sort_values('Points', ascending=False)
                                
                                # Number of bids per project
                                bids_per_project = bid_df.groupby('Project').size().reset_index(name='Number of Bids')
                                
                                # Average points per bid
                                avg_points = bid_df.groupby('Project')['Points'].mean().reset_index()
                                avg_points = avg_points.rename(columns={'Points': 'Average Points per Bid'})
                                avg_points['Average Points per Bid'] = avg_points['Average Points per Bid'].round(1)
                                
                                # Merge statistics
                                project_stats = points_per_project.merge(bids_per_project, on='Project')
                                project_stats = project_stats.merge(avg_points, on='Project')
                                project_stats = project_stats.sort_values('Points', ascending=False)
                                
                                # Display comprehensive statistics table
                                st.write("**Project Popularity Statistics:**")
                                st.dataframe(project_stats)
                                
                                # Create two columns for charts
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write("**Total Points by Project:**")
                                    # Create Plotly bar chart with rotated x-axis labels
                                    fig1 = px.bar(
                                        points_per_project, 
                                        x='Project', 
                                        y='Points',
                                        title='Total Points by Project'
                                    )
                                    
                                    # Customize the layout
                                    fig1.update_layout(
                                        xaxis=dict(
                                            tickangle=45,
                                            tickmode='array',
                                            tickvals=list(range(len(points_per_project))),
                                            ticktext=points_per_project['Project']
                                        ),
                                        margin=dict(b=100)  # Add bottom margin for rotated labels
                                    )
                                    
                                    # Display the Plotly chart
                                    st.plotly_chart(fig1, use_container_width=True, key=f"public_points_chart_{uuid.uuid4()}")
                                
                                with col2:
                                    st.write("**Number of Bids by Project:**")
                                    # Create Plotly bar chart with rotated x-axis labels
                                    fig2 = px.bar(
                                        bids_per_project, 
                                        x='Project', 
                                        y='Number of Bids',
                                        title='Number of Bids by Project'
                                    )
                                    
                                    # Customize the layout
                                    fig2.update_layout(
                                        xaxis=dict(
                                            tickangle=45,
                                            tickmode='array',
                                            tickvals=list(range(len(bids_per_project))),
                                            ticktext=bids_per_project['Project']
                                        ),
                                        margin=dict(b=100)  # Add bottom margin for rotated labels
                                    )
                                    
                                    # Display the Plotly chart
                                    st.plotly_chart(fig2, use_container_width=True, key=f"public_bids_chart_{uuid.uuid4()}")
                    
                    # Check if we need to handle a bid confirmation
                    if st.session_state.confirm_bid and st.session_state.bid_data:
                        bid_data = st.session_state.bid_data
                        st.warning(f"You've only allocated {bid_data['total_points']}/100 points. Are you sure you want to continue?")
                        
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if st.button("Confirm Bid"):
                                if handle_bid_submission():
                                    st.success("Your bids have been submitted successfully!")
                                    st.rerun()
                        with col2:
                            if st.button("Cancel"):
                                st.session_state.confirm_bid = False
                                st.session_state.bid_data = None
                                st.info("Bid cancelled. Please adjust your points allocation.")
                                st.rerun()
                    
                    # Only show the bidding form if we're not in confirmation mode
                    elif 'user_netid' in st.session_state and 'user_name' in st.session_state:
                        # Get existing bids for this user
                        existing_bids = []
                        for bid in load_bids():
                            if bid['netid'] == st.session_state.user_netid:
                                existing_bids = bid['bids']
                                break
                        
                        # Filter out the user's own project
                        available_projects = []
                        own_project = None
                        
                        for j, sub in enumerate(submissions):
                            if sub['netid'] == st.session_state.user_netid:
                                own_project = f"Project {j+1}: {sub['topic']}"
                            else:
                                available_projects.append((j, sub))
                        
                        if own_project:
                            st.info(f"Your own project ({own_project}) is excluded from the bidding options.")
                        
                        if not available_projects:
                            st.warning("There are no other projects available to bid on yet.")
                        else:
                            with st.form("bidding_form"):
                                st.write(f"**Bidding as:** {st.session_state.user_name} ({st.session_state.user_netid})")
                                
                                # Create bid inputs for up to 3 projects
                                bids = []
                                total_points = 0
                                
                                # Create columns for project selection and point allocation
                                for i in range(3):
                                    col1, col2 = st.columns([3, 1])
                                    
                                    with col1:
                                        # Default to existing selection if available
                                        default_index = 0
                                        if i < len(existing_bids):
                                            for j, (idx, sub) in enumerate(available_projects):
                                                if f"Project {idx+1}" == existing_bids[i]['project_id']:
                                                    default_index = j
                                                    break
                                        
                                        project_options = [f"Project {idx+1}: {sub['topic']}" for idx, sub in available_projects]
                                        project_options.insert(0, "Select a project")
                                        selected_project = st.selectbox(
                                            f"Project #{i+1}",
                                            options=project_options,
                                            index=default_index if i < len(existing_bids) else 0,
                                            key=f"project_{i}"
                                        )
                                    
                                    with col2:
                                        # Default to existing points if available
                                        default_points = 0
                                        if i < len(existing_bids):
                                            default_points = existing_bids[i]['points']
                                        
                                        points = st.number_input(
                                            "Points",
                                            min_value=0,
                                            max_value=100,
                                            value=default_points,
                                            step=5,
                                            key=f"points_{i}"
                                        )
                                    
                                    if selected_project != "Select a project":
                                        project_id = selected_project.split(":")[0].strip()
                                        project_title = selected_project[selected_project.index(":")+1:].strip()
                                        bids.append({
                                            "project_id": project_id,
                                            "project_title": project_title,
                                            "points": points
                                        })
                                        total_points += points
                                
                                # Display total points
                                st.write(f"**Total points allocated:** {total_points}/100")
                                
                                # Submit button
                                submit_bids = st.form_submit_button("Submit Bids")
                            
                            # Show visualization of user's current bids (outside the form)
                            existing_bids = []
                            for bid in load_bids():
                                if bid['netid'] == st.session_state.user_netid:
                                    existing_bids = bid['bids']
                                    break
                            
                            if existing_bids:
                                st.subheader("Your Current Bid Distribution")
                                
                                # Get all available projects (excluding the user's own)
                                all_projects = []
                                for j, sub in enumerate(submissions):
                                    if sub['netid'] != st.session_state.user_netid:
                                        all_projects.append(f"Project {j+1}: {sub['topic']}")
                                
                                # Create a dictionary mapping project titles to points
                                bid_dict = {bid['project_title']: bid['points'] for bid in existing_bids}
                                
                                # Create a DataFrame with all projects, filling in zeros for projects without bids
                                bid_data = []
                                for project in all_projects:
                                    # Extract just the project title part after the colon
                                    project_title = project[project.index(':')+1:].strip()
                                    # Find if this project has a bid
                                    points = 0
                                    for bid in existing_bids:
                                        if project_title in bid['project_title']:
                                            points = bid['points']
                                            break
                                    
                                    bid_data.append({
                                        'Project': project,
                                        'Points': points
                                    })
                                
                                # Create DataFrame and sort by points (descending)
                                bid_df = pd.DataFrame(bid_data)
                                bid_df = bid_df.sort_values('Points', ascending=False)
                                
                                # Create a Plotly bar chart with rotated x-axis labels
                                fig = px.bar(
                                    bid_df, 
                                    x='Project', 
                                    y='Points',
                                    title='Your Bid Distribution'
                                )
                                
                                # Customize the layout to rotate x-axis labels
                                fig.update_layout(
                                    xaxis=dict(
                                        tickangle=45,
                                        tickmode='array',
                                        tickvals=list(range(len(bid_df))),
                                        ticktext=bid_df['Project']
                                    ),
                                    margin=dict(b=100)  # Add bottom margin for rotated labels
                                )
                                
                                # Display the Plotly chart
                                st.plotly_chart(fig, use_container_width=True, key="user_bid_distribution")
                                
                                # Show a table view as well
                                st.write("**Your Current Bids:**")
                                # Only show projects with non-zero bids in the table
                                bid_table = bid_df[bid_df['Points'] > 0]
                                if not bid_table.empty:
                                    st.dataframe(bid_table)
                                else:
                                    st.info("You haven't placed any bids yet.")
                                
                                # Calculate and show remaining points
                                total_allocated = sum(bid['points'] for bid in existing_bids)
                                st.write(f"**Total points allocated:** {total_allocated}/100")
                                st.write(f"**Remaining points:** {100 - total_allocated}")
                            
                            # Handle form submission
                            if submit_bids:
                                if not bids:
                                    st.error("Please select at least one project to bid on.")
                                else:
                                    # Check for duplicate project selections
                                    selected_project_ids = [bid['project_id'] for bid in bids]
                                    if len(selected_project_ids) != len(set(selected_project_ids)):
                                        st.error("You've selected the same project multiple times. Please select each project only once.")
                                    elif total_points > 100:
                                        st.error("You've allocated more than 100 points! Please reduce your bids.")
                                    elif total_points == 0:
                                        st.error("Please allocate at least some points before submitting.")
                                    elif total_points < 100:
                                        # Store the bid data and set confirm flag
                                        st.session_state.bid_data = {
                                            'netid': st.session_state.user_netid,
                                            'name': st.session_state.user_name,
                                            'bids': bids,
                                            'total_points': total_points
                                        }
                                        st.session_state.confirm_bid = True
                                        st.rerun()
                                    else:
                                        # Save the bid directly if exactly 100 points
                                        if save_bid(st.session_state.user_netid, st.session_state.user_name, bids):
                                            st.success("Your bids have been submitted successfully!")
                    else:
                        st.warning("Please identify yourself in the sidebar to place bids.")
        
        # Otherwise show submission form
        else:
            st.header("Submit Your Project Topic")
            
            with st.form("submission_form"):
                name = st.text_input("Your Name")
                netid = st.text_input("UW NetID")
                topic = st.text_input("Project Topic")
                description = st.text_area("Project Description", height=150)
                
                submitted = st.form_submit_button("Submit")
                
                if submitted:
                    if not name or not netid or not topic or not description:
                        st.error("Please fill out all fields!")
                    else:
                        if save_submission(name, netid, topic, description):
                            st.success("Your project topic has been submitted successfully!")
        
        # Admin view of all submissions and bids
        if st.session_state.authenticated:
            st.header("Admin View: All Submissions")
            
            if not submissions:
                st.warning("No submissions yet.")
            else:
                df = pd.DataFrame(submissions)
                st.dataframe(df)
            
            st.header("Admin View: All Bids")
            bids = load_bids()
            
            if not bids:
                st.warning("No bids yet.")
            else:
                # Create a more detailed view of bids
                bid_details = []
                for bid in bids:
                    for project_bid in bid['bids']:
                        bid_details.append({
                            'Student': f"{bid['name']} ({bid['netid']})",
                            'Project': project_bid['project_title'],
                            'Points': project_bid['points'],
                            'Timestamp': bid['timestamp']
                        })
                
                if bid_details:
                    # Create tabs for different views
                    tab1, tab2, tab3 = st.tabs(["All Bids", "Project Summary", "Student Summary"])
                    
                    with tab1:
                        st.subheader("All Individual Bids")
                        bid_df = pd.DataFrame(bid_details)
                        st.dataframe(bid_df)
                    
                    with tab2:
                        st.subheader("Project Bid Summary")
                        
                        # Create DataFrames for different statistics
                        bid_df = pd.DataFrame(bid_details)
                        
                        # Total points per project
                        points_per_project = bid_df.groupby('Project')['Points'].sum().reset_index()
                        points_per_project = points_per_project.sort_values('Points', ascending=False)
                        
                        # Number of bids per project
                        bids_per_project = bid_df.groupby('Project').size().reset_index(name='Number of Bids')
                        
                        # Average points per bid
                        avg_points = bid_df.groupby('Project')['Points'].mean().reset_index()
                        avg_points = avg_points.rename(columns={'Points': 'Average Points per Bid'})
                        avg_points['Average Points per Bid'] = avg_points['Average Points per Bid'].round(1)
                        
                        # Merge statistics
                        project_stats = points_per_project.merge(bids_per_project, on='Project')
                        project_stats = project_stats.merge(avg_points, on='Project')
                        project_stats = project_stats.sort_values('Points', ascending=False)
                        
                        # Display comprehensive statistics table
                        st.dataframe(project_stats)
                        
                        # Create two columns for charts
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Total Points by Project:**")
                            # Create Plotly bar chart with rotated x-axis labels
                            fig1 = px.bar(
                                points_per_project, 
                                x='Project', 
                                y='Points',
                                title='Total Points by Project'
                            )
                            
                            # Customize the layout
                            fig1.update_layout(
                                xaxis=dict(
                                    tickangle=45,
                                    tickmode='array',
                                    tickvals=list(range(len(points_per_project))),
                                    ticktext=points_per_project['Project']
                                ),
                                margin=dict(b=100)  # Add bottom margin for rotated labels
                            )
                            
                            # Display the Plotly chart
                            st.plotly_chart(fig1, use_container_width=True, key=f"admin_points_chart_{uuid.uuid4()}")
                        
                        with col2:
                            st.write("**Number of Bids by Project:**")
                            # Create Plotly bar chart with rotated x-axis labels
                            fig2 = px.bar(
                                bids_per_project, 
                                x='Project', 
                                y='Number of Bids',
                                title='Number of Bids by Project'
                            )
                            
                            # Customize the layout
                            fig2.update_layout(
                                xaxis=dict(
                                    tickangle=45,
                                    tickmode='array',
                                    tickvals=list(range(len(bids_per_project))),
                                    ticktext=bids_per_project['Project']
                                ),
                                margin=dict(b=100)  # Add bottom margin for rotated labels
                            )
                            
                            # Display the Plotly chart
                            st.plotly_chart(fig2, use_container_width=True, key=f"admin_bids_chart_{uuid.uuid4()}")
                    
                    with tab3:
                        st.subheader("Student Bid Summary")
                        
                        # Get unique students
                        students = bid_df['Student'].unique()
                        
                        # Create a summary of each student's bids
                        student_summaries = []
                        
                        for student in students:
                            student_bids = bid_df[bid_df['Student'] == student]
                            total_points = student_bids['Points'].sum()
                            num_projects = len(student_bids)
                            
                            student_summaries.append({
                                'Student': student,
                                'Total Points': total_points,
                                'Projects Bid On': num_projects,
                                'Average Points per Project': round(total_points / num_projects, 1) if num_projects > 0 else 0
                            })
                        
                        student_summary_df = pd.DataFrame(student_summaries)
                        st.dataframe(student_summary_df)
                    
                    # Add option to reset a student's bid
                    st.subheader("Reset Student Bid")
                    
                    # Create a list of students with bids
                    student_options = [f"{bid['name']} ({bid['netid']})" for bid in bids]
                    
                    if student_options:
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            selected_student = st.selectbox(
                                "Select a student",
                                options=student_options
                            )
                        
                        with col2:
                            if st.button("Reset Bid"):
                                # Extract netid from the selected student
                                netid = selected_student.split("(")[1].split(")")[0]
                                if delete_bid(netid):
                                    st.success(f"Successfully reset bid for {selected_student}")
                                    st.rerun()
                    else:
                        st.info("No student bids to reset.")
                else:
                    st.warning("No bid details available.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please try refreshing the page or contact the administrator.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please try refreshing the page or contact the administrator.") 