# AI-Based Procrastination Detection System

## Overview:
This project is an AI-powered productivity monitoring system that tracks user activity in real-time, classifies it into **focus** or **distraction**, and provides meaningful insights through an interactive dashboard.

The system helps users understand their behavior patterns and improve productivity by identifying time spent on useful vs distracting activities.


## Key Features:
* Real-time activity tracking using active window detection
* Automatic classification into focus and distraction
* Smart categorization of YouTube content (e.g., YT Python, YT Food, YT Movie)
* Interactive dashboard with visual analytics
* Time-based productivity analysis
* Personal insights and recommendations
* Focus streak tracking
* Lightweight and runs locally


## Tech Stack"

* **Python** – Core programming language
* **Streamlit** – Dashboard and visualization
* **SQLite** – Local database for storing activity logs
* **Machine Learning (Scikit-learn)** – Text classification
* **Matplotlib & Pandas** – Data analysis and charts
* **PyGetWindow** – Active window tracking


## Project Structure:
procrastination_ai_system/
│
├── _pycache__/              # Python cache files
├── .gitignore               # Ignored files configuration
├── activity.db              # SQLite database (ignored in Git)
│
├── analyzer.py              # Analysis logic (processing insights)
├── dashboard.py             # Streamlit dashboard UI
├── database.py              # Database connection & operations
├── model.py                 # ML model loading and prediction
├── test_model.py            # Testing ML model
├── tracker.py               # Tracks user activity (core tracker)
├── utils.py                 # Helper functions
├── view_db.py               # View database records
│
├── training_data.csv        # Dataset used for training model
├── model.pkl                # Trained ML model (ignored)
├── vectorizer.pkl           # Text vectorizer (ignored)
│
└── README.md                # Project documentation


## How It Works:

1. **Tracking Phase**:
   * The `tracker.py` continuously monitors the active window every 5 seconds.
   * It cleans and categorizes the application name before storing it in the database.

2. **Storage**:
   * Data is stored in an SQLite database (`activity.db`).

3. **Classification**:
   * Activities are classified as **focus** or **distraction** using:

     * Keyword-based rules
     * Machine learning model (fallback)

4. **Visualization**:
   * The `dashboard.py` reads stored data and displays:

     * Focus vs Distraction pie chart
     * Time-based trends
     * Application usage bar chart
     * Personal insights


## Installation:

### 1. Clone the repository:
```bash
git clone https://github.com/navaneethprofessional-hub/ai-based-procrastination-detection-system.git
cd ai-based-procrastination-detection-system
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the tracker:
```bash
python tracker.py
```

### 4. Run the dashboard:
```bash
streamlit run dashboard.py
```

## Usage:
* Start the tracker to begin collecting activity data
* Use your system normally
* Open the dashboard to analyze your productivity
* Identify distraction patterns and improve focus


## Dashboard Insights:
The dashboard provides:
* Total focus time and distraction time
* Productivity score (%)
* Most used application
* Most distracting application
* Peak distraction time
* Maximum focus streak
* Time-based behavior analysis


## Example Categories:
The system intelligently categorizes activities such as:
* YT Python
* YT SQL
* YT Food
* YT Movie
* YT Music
* YT IPL
* VS Code
* PDF


## Limitations:
* Works best on Windows systems
* Depends on window title accuracy
* ML model accuracy depends on training data
* Cannot track mobile usage


## Future Enhancements:
* Real-time distraction alerts
* Mobile app integration
* Cloud-based data storage
* Advanced ML model (deep learning)
* Weekly/monthly reports
* Focus goal setting


## Author:
Navaneeth S


## License:
This project is for educational and research purposes.
