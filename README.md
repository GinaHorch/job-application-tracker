# Job Application Tracker 📋

A Job Application Tracker designed to help you organise and manage your job hunt effectively. This web application enables users to keep track of job applications, monitor deadlines, and follow up on opportunities, all in one convenient location.

Whether you want to use the deployed version or customise the code for your own needs, this tracker is flexible, user-friendly, and built with a robust tech stack.

## 🚀 Features

- **User Authentication:** Secure signup and login functionality.
- **Dashboard:** View all job applications with filter options by status, company, or due date.
- **Job Details Management:** Add, edit, view, and delete job applications.
- **Follow-Up Reminders:** Highlight applications with upcoming or overdue follow-up dates.
- **Responsive Design:** Optimised for both desktop and mobile devices.

## 🛠️ Tech Stack

### Backend
- **Flask:** Lightweight Python web framework.
- **Flask-SQLAlchemy:** ORM for database management.
- **Flask-WTF:** Form handling and validation.
- **Flask-Login:** User authentication and session management.
- **Flask-Migrate:** Database migrations.
- 
### Frontend
- **HTML5 and CSS3:** Semantic markup and custom styling.
- **Bootstrap:** Responsive and mobile-first design.
- **JavaScript:** Dynamic user interactions.

### Database
- **PostgreSQL:** Hosted on Heroku for production.
- **SQLite:** For local development.

### Deployment
**Heroku:** Cloud hosting for the live application.

### 🌐 Live Demo
Explore the deployed version of the Job Application Tracker here:
[Job Application Tracker - Live App](https://sis-job-app-tracker-e04920ceed08.herokuapp.com/)

### 🖥️ Local Setup
To run the project locally, follow these steps:

#### Prerequisites
- Python 3.10+
- PostgreSQL or SQLite
- Git
- Virtual environment (optional but recommended)

#### Installation
1. **Clone the Repository:**
    ```bash
    git clone https://github.com/GinaHorch/job-application-tracker.git
    cd job-application-tracker

2. **Set Up a Virtual Environment (optional):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate   

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Set Up the Database:**

- For SQLite (default):
    ```bash
    flask db upgrade
- For PostgreSQL, configure your DATABASE_URL in .env and run:
    ```bash
    flask db upgrade

5. **Run the Application:**
    ```bash
    flask run

6. **Access the Application:** Open your browser and go to http://127.0.0.1:5000.

### 🤝 Contributing
If you want to customise this project or improve it, feel free to fork the repository and submit a pull request. Contributions are always welcome!

### 📝 License
This project is licensed under the MIT License. You’re free to use, modify, and distribute it as needed.

### 💬 Feedback
If you have any feedback, suggestions, or questions, feel free to reach out by creating an issue in this repository.