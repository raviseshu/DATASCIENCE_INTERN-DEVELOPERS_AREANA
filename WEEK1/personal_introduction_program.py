# ================================================
# Week 1 Project: Personal Introduction Program
# ================================================
# This program asks for user information and 
# displays a friendly welcome message

print("=" * 50)
print("PERSONAL INTRODUCTION PROGRAM")
print("=" * 50)
print()

# Getting user information
name = input("Please enter your name: ")
age = input("Please enter your age: ")
hobby = input("What is your favorite hobby? ")

# Converting age to integer for calculations
age_number = int(age)

# Creating a personalized welcome message
print()
print("=" * 50)
print("WELCOME!")
print("=" * 50)
print()
print(f"Hello, {name}!")
print(f"It's great to meet you!")
print(f"I see you are {age} years old.")
print(f"That means in 5 years, you'll be {age_number + 5} years old!")
print(f"I also learned that you love {hobby}.")
print(f"Keep enjoying {hobby} and learning Python!")
print()
print("=" * 50)
print("Thank you for using this program!")
print("=" * 50)
