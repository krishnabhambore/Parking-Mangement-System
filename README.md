PARKING MANAGEMENT SYSTEM
Project README / Reference Document
Parking Management System
A web-based Parking Management System developed using Python, Flask, SQLite, HTML5, CSS3, and
JavaScript. The application helps manage vehicle parking, parking slots, vehicle entry and exit, parking duration,
parking charges, and parking records through a simple and user-friendly interface.
Features
• Vehicle Entry Management
• Vehicle Exit Management
• Parking Slot Management
• Vehicle Registration
• Parking Slot Availability Tracking
• Parking Time Calculation
• Parking Fee Calculation
• Vehicle Search
• Parking Record Management
• Active Parking Tracking
• Completed Parking Records
• Entry and Exit Time Tracking
• Parking History
• Dashboard / Summary
• Responsive Web Interface
• SQLite Database Storage
• Simple and Professional User Interface
Tech Stack
Frontend
• HTML5
• CSS3
• JavaScript
Backend
• Python
• Flask
Database
• SQLite
Project Structure
Parking-Management-System/
n
nnn app.py
nnn parking.db
nnn requirements.txt
nnn README.md
n
nnn static/
n nnn style.css
n nnn app.js
n
nnn templates/
n nnn index.html
n
nnn venv/
Database Tables
The system uses SQLite to store parking-related information.
Parking Table
Field Description
Parking ID Unique parking record identifier
Vehicle Number Vehicle registration number
Vehicle Type Type of vehicle
Slot Number Assigned parking slot
Entry Time Vehicle entry time
Exit Time Vehicle exit time
Parking Duration Total parking duration
Parking Fee Amount charged
Status Active / Completed
Application Workflow
User
↓
Open Parking Management System
↓
Enter Vehicle Details
↓
Check Parking Slot Availability
↓
Assign Parking Slot
↓
Record Vehicle Entry
↓
Vehicle Remains Parked
↓
Vehicle Exit Request
↓
Calculate Parking Duration
↓
Calculate Parking Fee
↓
Record Exit Time
↓
Release Parking Slot
↓
Update Parking Record
Main Steps
• Open the Parking Management System.
• Enter vehicle details.
• Check available parking slots.
• Assign an available parking slot.
• Record the vehicle entry time.
• Store the parking information in the database.
• When the vehicle leaves, record the exit time.
• Calculate the total parking duration.
• Calculate the parking fee.
• Release the occupied parking slot.
• Update the parking record.
• Display parking history and details.
User Interface
• Navigation / Header Section
• Parking Dashboard
• Vehicle Entry Form
• Vehicle Details
• Parking Slot Information
• Active Parking Records
• Vehicle Exit Section
• Parking Fee Display
• Parking History
• Search / Record Management
Installation
1. Clone or Download the Project
git clone https://github.com/krishnabhambore/Parking-Mangement-System
cd Parking-Mangement-System
2. Create Virtual Environment
python -m venv venv
3. Activate Virtual Environment — Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate
4. Install Dependencies
pip install -r requirements.txt
5. Run the Application
python app.py
6. Open the Application
http://127.0.0.1:5000/
Live Application
The Parking Management System is deployed online using PythonAnywhere.
Live Demo: https://krishnabg.pythonanywhere.com
Screenshots
Add actual project screenshots here:
Dashboard:
![Dashboard](screenshots/dashboard.png)
Vehicle Entry:
![Vehicle Entry](screenshots/vehicle-entry.png)
Parking Records:
![Parking Records](screenshots/parking-records.png)
Vehicle Exit:
![Vehicle Exit](screenshots/vehicle-exit.png)
Future Enhancements
• User Login and Authentication
• Admin and Staff Roles
• Multiple Parking Areas
• Real-Time Parking Slot Availability
• QR Code Based Vehicle Entry and Exit
• Online Payment Integration
• UPI Payment Integration
• Parking Reservation
• Automatic SMS Notifications
• Email Notifications
• PDF Parking Reports
• Advanced Dashboard Analytics
• Cloud Database Integration
• Mobile Application
• Vehicle Number Plate Recognition
Learning Outcomes
• Python Programming
• Flask Web Application Development
• SQLite Database Management
• HTML5
• CSS3
• JavaScript
• CRUD Operations
• Database Connectivity
• Web Application Design
• Backend Development
• Frontend Development
Author
Student Name: Krishna Ganesh Bhambore
USN: Your USN
Course: BCA
Project: Parking Management System
Technologies: Python | Flask | SQLite | HTML5 | CSS3 | JavaScript
GitHub
https://github.com/krishnabhambore/Parking-Mangement-System
Live Demo
https://krishnabg.pythonanywhere.com
License
