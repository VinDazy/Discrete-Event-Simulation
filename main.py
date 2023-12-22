# Function to run the simulation based on user's choice
def run_simulation(choice):
    if choice == '1':
        import Resources.Deterministic
        Resources.Deterministic.run()
    elif choice == '2':
        import Resources.Exponential
        Resources.Exponential.run()
    elif choice == '3':
        import Resources.Hyper_Exponential
        Resources.Hyper_Exponential.run()
    elif choice == '4':
        import Resources.Coorelated_Exponential
        Resources.Coorelated_Exponential.run()
    else:
        print("Invalid choice. Please select a number from 1 to 4.")

# Prompt the user for their choice
print("Choose a workload model to run the simulation:")
print("1. Deterministic")
print("2. Exponential")
print("3. Hyper-Exponential")
print("4. Correlated-Exponential")

user_choice = input("Enter the number of your choice: ")

# Run simulation based on user's choice
run_simulation(user_choice)
