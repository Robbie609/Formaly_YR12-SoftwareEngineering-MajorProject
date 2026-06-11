# FORMALY

Formaly is a desktop application developed as part of a Year 12 Software Design and Development project. It is designed to improve the planning and management of school formal events by providing a central system for organising tasks, budgets, venues, attendance, and reporting.

![Formaly Banner](assets/Formaly_Banner.png)

## 📌 Project Overview

School formal planning often involves many separate tools such as spreadsheets, emails, and paper based lists. This can lead to confusion, missing information, and poor organisation.

Formaly solves this problem by combining all planning tasks into one structured system. It allows users to access only the parts they need based on their role, helping improve organisation, efficiency, and communication.

## 🎯 Aim

The aim of Formaly is to design and develop a centralised system that:
- Improves organisation of formal event planning
- Reduces reliance on multiple disconnected tools
- Allows different users to access relevant information through role based permissions
- Stores and manages data securely using a database

## 👥 Stakeholders

- **Admin** - Oversees the entire formal from the name to the final report
- **Planner** - Responsible for organising tasks, venues and formal features.
- **Support Staff** - Assists with updating information and completing attendance
- **Attendee** - Views relevant event information since they are the ones attending the formal

## ✨ System Features

- 📋 **Task Management System**  
  Allows creation, assignment, and tracking of tasks

- 🏛️ **Venue Management System**  
  Stores and compares venue details for decision making

- 👥 **Attendance System**  
  Records and monitors attendance information

- 📊 **Report Generation System**  
  Produces summaries of planning progress and formal data


## 🧰 Technologies Used

- **Python** 
- **Tkinter** 
- **SQLite**

## 🏗️ System Design Overview

Formaly follows a modular structure where different parts of the system are separated into components such as:
- Database management
- User interface pages
- Utility functions
- Role based access control

This improves maintainability and makes it easier to update or expand the system in the future.

## 🔐 Security and Access Control

The system uses role based access control to ensure users can only access features relevant to their responsibilities. This helps protect data integrity and prevents unauthorised changes.


## 📁 Project Structure
```text
formaly/
│
├── database/        
├── pages/           
├── utils/           
├── assets/          # Images and resources
├── main.py          # Main program entry point
└── README.md
```

## 🚀 How to Run Formaly
**📌 System Requirements**

Before installing Formaly, ensure your system meets the following requirements:
```text
Windows 10 or Windows 11
Python 3.10 or later
Visual Studio Code (VS Code)
At least 100 MB of free storage
Internet connection (required for initial setup and downloads)
```

**📥 Required Downloads**
Before running the application, install the following dependencies:

Download Python from the official website:
https://www.python.org/downloads/

During installation:
- Tick Add Python to PATH
- Then select Install Now

Download VS Code here:
https://code.visualstudio.com/
Install using the default settings and complete the setup.

After opening VS Code:
Go to the Extensions tab
Search for Python
Install the extension published by Microsoft

**📂 Project Installation**
1. Go to the Formaly GitHub repository
2. Click Code → Download ZIP
3. Extract the ZIP file to a folder on your computer
4. Open Visual Studio Code
5. Select File → Open Folder
6. Open the extracted Formaly project folder

**▶️ Running Formaly**
Method 1 (Recommended)
- Open main.py in Visual Studio Code
- Click Run Python File (top-right corner)

Method 2 (Terminal)
- Open the VS Code terminal and run:
```text
python main.py
```
- The Formaly login screen should now appear.

**✅Verifying Installation**

The installation is successful if:

- The application launches without errors
- The login screen appears correctly
- Navigation between pages works properly
- Data can be added, edited, and retrieved successfully

**🎉 Installation Complete**
Formaly is now fully installed and ready to use.
Users can log in and begin managing school formal events through the system.

**ACCOUNTS:**
```text
ADMIN:
- Username: Calvin
- Password: EppingFormal26ADMIN

PLANNER:
- Username: Rowan
- Password: #1EBHSPlanner

SUPPORT:
- Username: Calvin
- Password: EBHSupport_1
```

## Conclusion
Formaly provides a practical solution to improve how school formal events are planned and managed.