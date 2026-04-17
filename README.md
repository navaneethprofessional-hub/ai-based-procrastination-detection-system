# AI-Based Procrastination Detection System

## Overview:
This project is an AI-powered productivity monitoring system that tracks user activity in real-time, classifies it into **focus** or **distraction**, and provides detailed insights through an interactive dashboard.
The system enables users to analyze their behavior patterns on both daily and weekly levels, helping them improve productivity and reduce distractions through data-driven insights.


## Key Features:
- Real-time activity tracking using active window detection  
- Automatic classification into focus and distraction using Machine Learning  
- Intelligent categorization of activities (e.g., YT Music, YT Movie, VS Code, PDF)  
- Daily and Weekly productivity analysis  
- Interactive dashboard with zoomable and dynamic charts  
- Time-based and day-based trend analysis  
- Separate insights for daily and weekly behavior  
- Focus streak tracking with weekly streak day identification  
- Personalized recommendations based on usage patterns  
- Lightweight system running locally  


## Tech Stack:
- **Python** – Core programming language  
- **Streamlit** – Interactive dashboard and UI  
- **SQLite** – Local database for storing activity logs  
- **Scikit-learn** – Machine learning model for classification  
- **Pandas** – Data manipulation and analysis  
- **Plotly** – Interactive charts and visualizations  
- **PyGetWindow** – Active window tracking  


## Project Structure:
procrastination_ai_system/
│
├── pycache/
├── .gitignore
├── activity.db
│
├── tracker.py
├── database.py
├── view_db.py
│
├── model.py
├── test_model.py
├── utils.py
│
├── analyzer.py
├── dashboard.py
│
├── training_data.csv
├── model.pkl
├── vectorizer.pkl
│
└── README.md


## System Workflow:

### 1. Tracking Phase:
- `tracker.py` continuously monitors the active window every 5 seconds  
- Cleans and categorizes application names  
- Stores activity data in the database  

### 2. Data Storage:
- SQLite database (`activity.db`) is used  
- Stores:
  - Application name  
  - Timestamp  

### 3. Classification:
- Activities are classified into:
  - Focus  
  - Distraction  

- Uses:
  - Machine Learning model (Naive Bayes)  
  - Rule-based enhancements  

### 4. Analysis:
- `analyzer.py` performs CLI-based analysis  

- Supports:
  - Daily analysis  
  - Weekly analysis  

- Computes:
  - Focus time  
  - Distraction time  
  - Productivity score  
  - Focus streak  
  - Behavioral insights  

### 5. Visualization:
- `dashboard.py` provides an interactive dashboard  

- Features:
  - Daily and Weekly toggle  
  - Dynamic charts using Plotly  
  - Real-time filtering  

---

## Dashboard Features:

### Daily View:
- Hour-wise activity trend  
- Focus vs Distraction pie chart  
- Application-based bar chart  
- Time-based insights  
- Maximum focus streak  

### Weekly View:
- Day-wise productivity trend  
- Weekly bar chart (Focus vs Distraction per day)  
- Weekly insights and behavior analysis  
- Maximum focus streak with day  
- Peak distraction day  


## Insights Provided"

### Daily Insights:
- Most used application  
- Most distracting application  
- Focus percentage  
- Distraction percentage  
- Behavior (Focused/Distracted)  
- Productivity level  
- Peak distraction hour  
- Maximum focus streak  
- Total sessions  
- Recommendation  

### Weekly Insights:
- Most used application  
- Most distracting application  
- Focus percentage  
- Distraction percentage  
- Weekly behavior  
- Weekly productivity  
- Peak distraction day  
- Maximum focus streak with day  
- Total sessions  
- Recommendation  


## Installation:

### 1. Clone Repository:
git clone https://github.com/navaneethprofessional-hub/ai-based-procrastination-detection-system.git
cd ai-based-procrastination-detection-system

### 2. Install Dependencies:
pip install -r requirements.txt

### 3. Run Tracker:
python tracker.py

### 4. Run Dashboard:
streamlit run dashboard.py


## Usage:
- Start the tracker to collect activity data  
- Use your system normally  
- Open the dashboard  
- Switch between Daily and Weekly views  
- Analyze insights to improve productivity  


## Example Categories:
- YT Music  
- YT Movie  
- YT Gaming  
- YT Python  
- VS Code  
- PDF  
- Notepad  


## Limitations:
- Works best on Windows systems  
- Depends on window title accuracy  
- ML model accuracy depends on training data  
- Does not track mobile activity  


## Future Enhancements:
- Real-time alerts  
- Focus goal tracking  
- Export reports (PDF/CSV)  
- Advanced ML models  
- Mobile support  
- Cloud integration  


## Author:
Navaneeth S  


## License:
This project is intended for educational and research purposes only.