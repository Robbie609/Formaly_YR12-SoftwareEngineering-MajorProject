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

## 🚀 How to Run the Project
**Requirements**
- Python 3.10 or higher

**Steps**
1. Step 1

## Conclusion
Formaly provides a practical solution to improve how school formal events are planned and managed.