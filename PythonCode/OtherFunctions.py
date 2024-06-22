from Libraries import *

# Other functions

def select_excel_file():
    # Create a Tkinter root window (it will be hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open the file dialog to select an Excel file
    file_path = filedialog.askopenfilename(
        title="Select an Excel file",
        filetypes=(("Excel files", "*.xlsx;*.xls"), ("All files", "*.*"))
    )

    # Check if a file was selected
    if file_path:
        # Check the file extension
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension in ['.xlsx', '.xls']:
            try:
                # Attempt to read the file with pandas to ensure it's a valid Excel file
                pd.read_excel(file_path)
                return file_path
            except Exception as e:
                print(f"\tThe selected file is not a valid Excel file: {e}")
                return None
        else:
            print("\tThe selected file is not an Excel file.")
            return None
    else:
        print("\tNo file selected")
        return None
    
def menuOptions():
    # Create a Tkinter root window (it will be hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Define menu options
    options = {
        1: "Start program",
        2: "End program"
    }
    
    # Create the menu message
    menu_message =  "-------------------------------------------\n"
    menu_message += "\tTimeTabling program"
    menu_message += "\n-------------------------------------------\n"
    menu_message += "\n-------------------------------------------\n"
    menu_message += "\t\tMenu"
    for key, value in options.items():
        menu_message += f"\n{key} - {value}"
    menu_message += "\n-------------------------------------------\n"

    # Display the dialog to choose an option
    while True:
        try:
            option = simpledialog.askinteger("Menu", menu_message)
            if option in options:
                break
            else:
                print("Invalid option. Please choose a valid option from the menu.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    return option

def MinutesAvailableBetween2Times(time_start, time_final):
    hours_start, minutes_start = map(int, time_start.split(':'))
    hours_final, minutes_final = map(int, time_final.split(':'))

    return (hours_final * 60 + minutes_final) - (hours_start * 60 + minutes_start)

def day_to_number(day):
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return days_of_week.index(day)

def getStartPossiblePeriod(assignment):

    period_scheduled = {}

    # Select a period id at random
    id_period = random.choice(range(0,len(assignment.periods)))
    available_times = assignment.periods[id_period].available

    # Select the days that happens the activity
    days = []
    for index_time in available_times:
        time = available_times[index_time]
        days.append(time['day'])
    days = list(set(days))

    
    days = random.sample(days, k=int(assignment.qnt_week))

    # Select slots for each day that satisfy the 2 previous conditions 
    for i, day in enumerate(days, start=1):
        list_available_dailyperiod = []
        for index_time in available_times:
            time = available_times[index_time]
            if time['day'] == day:
                list_available_dailyperiod.append(index_time)

        # Select random a period available in that day
        period_scheduled[i] = available_times[random.choice(list_available_dailyperiod)]
    
    # Arange the period schedule in the week days sequence
    period_scheduled_order = dict(sorted(period_scheduled.items(), key=lambda item: day_to_number(item[1]['day'])))

    i = 0
    for index in period_scheduled_order:
        i += 1
        period_scheduled[i] = period_scheduled_order[index]

    return period_scheduled

def getWeekDistribution(assignments):
    # Define the days of the week
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    day_index_map = {day: idx for idx, day in enumerate(days_of_week)}
    
    # Initialize assignments count per day
    assignments_a_day = [0] * 7
    
    # Count assignments for each day
    for assignment in assignments:
        time_scheduled = assignment.period_scheduled
        for index in time_scheduled:
            day_assignment = time_scheduled[index]['day']
            if day_assignment in day_index_map:
                assignments_a_day[day_index_map[day_assignment]] += 1
                
    return assignments_a_day
