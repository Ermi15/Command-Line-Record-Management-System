# Student Management System
(Made by)
#Ermias Leulseged (UGR/1423/17)
#Semeon Teshome (UGR/0246/17)
#Bereket Ayana (UGR/1267/17)

## Description
Simple command-line software managing student records, courses, and instructors for enrollments, using text files as storage.

## Features
-  Register students, courses, and instructors
-  Enroll students in courses  
-  View all enrollments
-  Assign courses to instructors 
-  View and modify schedules 
-  Automatically save data to text files

## Usage
1. Run the program: python student_system.py
2. Select an option from the menu.
3. Upon selection, follow the instructions for the operations.

## Data Files
These text files are used in the system:
- students.txt - Stores student records (ID,Name)
- courses.txt - Stores course information (Code,Title)
- instructors.txt - Stores instructor details (ID,Name)  
- enrollments.txt - Stores enrollment records (StudentID,CourseCode)
- schedules.txt - Stores schedules for the instructors and students (CourseCode,date,time)

## Notes
- All files are stored in the same directory as the script.
- Files are automatically created if they don't already exist.
- Some basic validation is done to check enrollment of non-existent students or courses.
