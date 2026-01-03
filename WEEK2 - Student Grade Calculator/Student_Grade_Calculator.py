# ================================================
# Week 2 Project: Student Grade Calculator
# ================================================
# This program calculates grades and provides
# encouraging feedback for students

def get_marks(subject):
    """Get marks for a subject with error handling"""
    while True:
        try:
            marks = float(input(f"Enter marks for {subject} (0-100): "))
            if 0 <= marks <= 100:
                return marks
            else:
                print("Marks must be between 0 and 100!")
        except ValueError:
            print("Please enter a valid number!")

def calculate_grade(percentage):
    """Calculate grade based on percentage"""
    if percentage >= 90:
        return "A"
    elif percentage >= 75:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"

def get_message(grade):
    """Return encouraging message based on grade"""
    messages = {
        "A": "🌟 Outstanding! You're a star performer!",
        "B": "👏 Excellent work! Keep it up!",
        "C": "👍 Good job! You're doing well!",
        "D": "💪 You passed! Keep working hard!",
        "F": "📚 Don't give up! You can do better next time!"
    }
    return messages[grade]

def main():
    """Main program function"""
    print("=" * 50)
    print("STUDENT GRADE CALCULATOR")
    print("=" * 50)
    print()
    
    # Get student name
    student_name = input("Enter student name: ")
    print()
    
    # Define subjects
    subjects = ["Math", "Science", "English", "History", "Computer"]
    
    # Get marks for each subject
    marks_list = []
    for subject in subjects:
        marks = get_marks(subject)
        marks_list.append(marks)
    
    # Calculate total and percentage
    total_marks = sum(marks_list)
    max_marks = len(subjects) * 100
    percentage = (total_marks / max_marks) * 100
    
    # Calculate grade
    grade = calculate_grade(percentage)
    
    # Get encouraging message
    message = get_message(grade)
    
    # Display results
    print()
    print("=" * 50)
    print("GRADE REPORT")
    print("=" * 50)
    print(f"Student Name: {student_name}")
    print()
    print("Subject-wise Marks:")
    for i, subject in enumerate(subjects):
        print(f"{subject}: {marks_list[i]}")
    print()
    print(f"Total Marks: {total_marks}/{max_marks}")
    print(f"Percentage: {percentage:.2f}%")
    print(f"Grade: {grade}")
    print()
    print(message)
    print("=" * 50)

# Run the program
if __name__ == "__main__":
    main()
