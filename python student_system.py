STUDENT_FILE = "students.txt"
COURSE_FILE = "courses.txt"
INSTRUCTOR_FILE = "instructors.txt"
ENROLLMENT_FILE = "enrollments.txt"
SCHEDULE_FILE = "schedules.txt"

def save_data(filename, data):
    with open(filename, 'w') as f:
        for item in data:
            f.write(f"{item}\n")

def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []

# Initialize files if they don't exist
for file in [STUDENT_FILE, COURSE_FILE, INSTRUCTOR_FILE, ENROLLMENT_FILE, SCHEDULE_FILE]:
    if not load_data(file):
        save_data(file, [])

def register_student():
    student_id = input("Enter student ID: ")
    name = input("Enter student name: ")
    students = load_data(STUDENT_FILE)
    students.append(f"{student_id},{name}")
    save_data(STUDENT_FILE, students)
    print("Student registered!")

def register_course():
    course_code = input("Enter course code: ")
    title = input("Enter course title: ")
    
    # Verify instructor exists
    instructor_id = input("Enter instructor ID: ")
    instructors = load_data(INSTRUCTOR_FILE)
    if not any(instructor_id in inst for inst in instructors):
        print("Error: Instructor not found!")
        return
    
    day = input("Enter day (e.g., Mon, Tue): ")
    time = input("Enter time (e.g., 9:00-11:00): ")
    
    courses = load_data(COURSE_FILE)
    courses.append(f"{course_code},{title},{instructor_id}")
    save_data(COURSE_FILE, courses)
    
    schedules = load_data(SCHEDULE_FILE)
    schedules.append(f"{course_code},{day},{time}")
    save_data(SCHEDULE_FILE, schedules)
    print("Course registered with schedule!")

def register_instructor():
    instructor_id = input("Enter instructor ID: ")
    name = input("Enter instructor name: ")
    instructors = load_data(INSTRUCTOR_FILE)
    instructors.append(f"{instructor_id},{name}")
    save_data(INSTRUCTOR_FILE, instructors)
    print("Instructor registered!")

def enroll_student():
    student_id = input("Enter student ID: ")
    course_code = input("Enter course code: ")
    
    # Check if student exists
    students = load_data(STUDENT_FILE)
    if not any(student_id in s for s in students):
        print("Error: Student not found!")
        return
    
    # Check if course exists
    courses = load_data(COURSE_FILE)
    if not any(course_code in c for c in courses):
        print("Error: Course not found!")
        return
    
    # Check if already enrolled
    enrollments = load_data(ENROLLMENT_FILE)
    if any(enroll.startswith(f"{student_id},{course_code}") for enroll in enrollments):
        print("Error: Student already enrolled in this course!")
        return
    
    enrollments.append(f"{student_id},{course_code}")
    save_data(ENROLLMENT_FILE, enrollments)
    print("Enrollment successful!")

def view_enrollments():
    print("\nAll Enrollments:")
    enrollments = load_data(ENROLLMENT_FILE)
    students = load_data(STUDENT_FILE)
    courses = load_data(COURSE_FILE)
    schedules = load_data(SCHEDULE_FILE)
    
    for enroll in enrollments:
        if not enroll.strip() or enroll.count(',') != 1:  # Skip empty lines
            continue
            
        try:
            student_id, course_code = enroll.split(',')
            
            # Find student name
            student_name = "Unknown"
            for s in students:
                if s.count(',') == 1 and s.startswith(student_id + ","):
                    student_name = s.split(',')[1]
                    break
            
            # Find course info 
            course_title = "Unknown"
            instructor_id = "N/A"
            for c in courses:
                if c.count(',') >= 2 and c.startswith(course_code + ","):
                    parts = c.split(',')
                    course_title = parts[1]
                    instructor_id = parts[2]
                    break
            
            # Find schedule
            schedule = "Not scheduled"
            for s in schedules:
                if s.count(',') == 2 and s.startswith(course_code + ","):
                    day, time = s.split(',')[1:]
                    schedule = f"{day} {time}"
                    break
            
            print(f"Student: {student_name} ({student_id})")
            print(f"Course: {course_title} ({course_code})")
            print(f"Instructor: {instructor_id}")
            print(f"Schedule: {schedule}\n")
            
        except Exception as e:
            print(f"Skipping malformed enrollment: {enroll}")
            continue

def view_schedules():
    print("\nAll Course Schedules:")
    courses = load_data(COURSE_FILE)
    schedules = load_data(SCHEDULE_FILE)
    
    for s in schedules:
        course_code, day, time = s.split(',')
        course_title = next((c.split(',')[1] for c in courses if c.startswith(course_code)), "Unknown")
        print(f"Course: {course_title} ({course_code})")
        print(f"Time: {day} {time}\n")

def view_student_schedule():
    student_id = input("Enter student ID: ")
    
    students = load_data(STUDENT_FILE)
    if not any(student_id in s for s in students):
        print("Error: Student not found!")
        return
    
    enrollments = load_data(ENROLLMENT_FILE)
    courses = load_data(COURSE_FILE)
    schedules = load_data(SCHEDULE_FILE)
    
    print(f"\nSchedule for Student {student_id}:")
    found = False
    
    for enroll in enrollments:
        if enroll.startswith(student_id):
            found = True
            course_code = enroll.split(',')[1]
            
            # Get course info
            course_info = next((c for c in courses if c.startswith(course_code)), None)
            if course_info:
                course_title = course_info.split(',')[1]
                instructor_id = course_info.split(',')[2]
            else:
                course_title = "Unknown"
                instructor_id = "N/A"
            
            # Get schedule
            schedule = next((f"{s.split(',')[1]} {s.split(',')[2]}" for s in schedules if s.startswith(course_code)), "Not scheduled")
            
            print(f"- {course_title} ({course_code})")
            print(f"  Instructor: {instructor_id}")
            print(f"  Time: {schedule}\n")
    
    if not found:
        print("No enrollments found for this student.")

def assign_instructor_to_course():
    course_code = input("Enter course code: ")
    new_instructor = input("Enter new instructor ID: ")
    
    # Verify instructor exists
    instructors = load_data(INSTRUCTOR_FILE)
    if not any(new_instructor in inst for inst in instructors):
        print("Error: Instructor not found!")
        return
    
    courses = load_data(COURSE_FILE)
    updated = False
    
    for i, course in enumerate(courses):
        if course.startswith(course_code + ","):
            parts = course.split(',')
            parts[2] = new_instructor
            courses[i] = ','.join(parts)
            updated = True
            break
    
    if updated:
        save_data(COURSE_FILE, courses)
        print("Instructor updated successfully!")
    else:
        print("Error: Course not found!")

def update_schedule():
    course_code = input("Enter course code: ")
    
    # Verify course exists
    courses = load_data(COURSE_FILE)
    if not any(course_code in c for c in courses):
        print("Error: Course not found!")
        return
    
    new_day = input("Enter new day: ")
    new_time = input("Enter new time: ")
    
    schedules = load_data(SCHEDULE_FILE)
    updated = False
    
    for i, s in enumerate(schedules):
        if s.startswith(course_code + ","):
            schedules[i] = f"{course_code},{new_day},{new_time}"
            updated = True
            break
    
    if updated:
        save_data(SCHEDULE_FILE, schedules)
        print("Schedule updated successfully!")
    else:
        print("Error: Schedule not found for this course!")

def view_instructor_schedule():
    instructor_id = input("Enter instructor ID: ")
    
    instructors = load_data(INSTRUCTOR_FILE)
    if not any(instructor_id in inst for inst in instructors):
        print("Error: Instructor not found!")
        return
    
    courses = load_data(COURSE_FILE)
    schedules = load_data(SCHEDULE_FILE)
    
    print(f"\nTeaching Schedule for Instructor {instructor_id}:")
    found = False
    
    for course in courses:
        if course.endswith(instructor_id):
            found = True
            code, title, _ = course.split(',')
            
            # Find schedule
            schedule = next((f"{s.split(',')[1]} {s.split(',')[2]}" for s in schedules if s.startswith(code + ",")), "Not scheduled")
            
            print(f"- {title} ({code})")
            print(f"  Time: {schedule}\n")
    
    if not found:
        print("No courses assigned to this instructor.")

def main_menu():
    while True:
        print("\n=== ADMINISTRATION SYSTEM ===")
        print("1. Register Student")
        print("2. Register Course")
        print("3. Register Instructor")
        print("4. Enroll Student")
        print("5. View All Enrollments")
        print("6. View All Schedules")
        print("7. View Student Schedule")
        print("8. Assign/Change Instructor")
        print("9. Update Course Schedule")
        print("10. View Instructor Schedule")
        print("11. Exit")
        
        choice = input("Choose option (1-11): ")
        
        if choice == '1':
            register_student()
        elif choice == '2':
            register_course()
        elif choice == '3':
            register_instructor()
        elif choice == '4':
            enroll_student()
        elif choice == '5':
            view_enrollments()
        elif choice == '6':
            view_schedules()
        elif choice == '7':
            view_student_schedule()
        elif choice == '8':
            assign_instructor_to_course()
        elif choice == '9':
            update_schedule()
        elif choice == '10':
            view_instructor_schedule()
        elif choice == '11':
            print("Exiting system...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()