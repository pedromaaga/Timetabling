from Libraries import *
from StoreDataFunctions import CreatSlots, Excelfile2Dataframe, CreateObjectAssignments, OtherConditions
from OptimizationFunctions import ParametersOptimizationProgram, runOptimizationProgram,PlotResults

# Interface functions

class TimetablingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timetabling Program")
        self.root.geometry("450x450")
        
        self.excel_file = None
        self.excel_name = tk.StringVar()
        self.excel_assig = tk.StringVar()
        self.process_done = tk.StringVar()
        self.assignment_day = tk.StringVar()
        self.assignment_start = tk.StringVar()
        self.assignment_end = tk.StringVar()

        self.timetabling = None
        self.assignments = None
        self.max_iterations = None
        self.tabu_list_size = None
        self.num_runs = None
        self.other_conditions = None

        self.dropdown_var = StringVar(self.root)
        self.dropdown_var.trace_add("write", lambda *args: self.getResults())
        self.dropdown_var.set("")  # default value

        self.button_excelfile = None
        self.button_run = None
        
        self.setupInitial()

    def setupInitial(self):
        # Add a title label
        self.root.grid_columnconfigure(0, weight=1, minsize=100)
        self.root.grid_columnconfigure(1, weight=1, minsize=100)
        self.root.grid_columnconfigure(2, weight=1, minsize=100)
        self.root.grid_columnconfigure(3, weight=1, minsize=100)

        label = tk.Label(self.root, text="Timetabling Program", font=("Helvetica", 20, "bold"))
        label.grid(row=0, columnspan=4, pady=10)
        
        label = tk.Label(self.root, text="Choose an Excel file", font=("Helvetica", 13, "bold"))
        label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Add labels to display file properties
        label = tk.Label(self.root, text="Name:", font=("Helvetica", 8))
        label.grid(row=2, column=0, columnspan=2, padx=10, sticky="e")
        label = tk.Label(self.root, text="Quantity of assignments:", font=("Helvetica", 8))
        label.grid(row=3, column=0, columnspan=2, padx=10, sticky="e")

        label = tk.Label(self.root, textvariable=self.excel_name, font=("Helvetica", 8))
        label.grid(row=2, column=2, padx=10)
        label = tk.Label(self.root, textvariable=self.excel_assig, font=("Helvetica", 8))
        label.grid(row=3, column=2, padx=10)

        # Add buttons
        self.button_excelfile = tk.Button(self.root, text="Select", command=self.clickButtonExcel, font=("Helvetica", 10), width=10)
        self.button_excelfile.grid(row=1, column=2, columnspan=2, padx=15, pady=5)

        self.button_run = tk.Button(self.root, text="Run", command=self.clickButtonRun, state="disabled", font=("Helvetica", 10), width=10)
        self.button_run.grid(row=4, columnspan=4, pady=10)
        
        # Process section
        section_label = tk.Label(self.root, text="Process", font=("Helvetica", 13, "bold"))
        section_label.grid(row=5, column=0, columnspan=2, pady=5, padx=10)
        label_process = tk.Label(self.root, textvariable=self.process_done, font=("Helvetica", 11))
        label_process.grid(row=5, column=2, columnspan=2, pady=5, padx=10)

        # Results section
        results_label = tk.Label(self.root, text="Results", font=("Helvetica", 13, "bold"))
        results_label.grid(row=6, column=0, columnspan=2, pady=5, padx=10)

        # Add dropdown list

        options = [""]
        self.dropdown_menu = OptionMenu(self.root, self.dropdown_var, *options)
        self.dropdown_menu.config(width=20)
        self.dropdown_menu.grid(row=6, column=2,columnspan=2, padx=5, pady=5)

        label = tk.Label(self.root, text="Day", font=("Helvetica", 8))
        label.grid(row=7, column=0, columnspan=2, padx=10)
        label = tk.Label(self.root, text="Start time", font=("Helvetica", 8))
        label.grid(row=7, column=2, padx=10)
        label = tk.Label(self.root, text="End time", font=("Helvetica", 8))
        label.grid(row=7, column=3, padx=10)

    def getExcelFile(self):
        return self.excel_file

    def getTimetabling(self):
        return self.timetabling

    def clickButtonExcel(self):
        self.excel_file = self.selectExcelFile()

        if self.excel_file:
            self.readData()
            self.excel_name.set(os.path.basename(self.excel_file))
            self.excel_assig.set(str(len(self.assignments)))
            self.button_run.config(state="normal")
        else:
            self.excel_name.set("")
            self.excel_assig.set("")
            self.button_run.config(state="disabled")

    def clickButtonRun(self):
        ## Optimization program
        print("\n-> Running the optimization program  (...)")
        self.timetabling = runOptimizationProgram(self, self.assignments, self.max_iterations, self.tabu_list_size, self.num_runs, self.other_conditions)
        self.changeDropdownOptions()

    def selectExcelFile(self):
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
                    print("\tExcel file selected!")
                    print(f"\tName: {os.path.basename(file_path)}")
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

    def readData(self):
        # Parameters of the optimization program
        print("\n-> Reading the data  (...)")
        wake_time, sleep_time, delta_time, self.tabu_list_size, self.max_iterations, self.num_runs = ParametersOptimizationProgram(self.excel_file)
        self.other_conditions = OtherConditions(self.excel_file)

        # Create time slots
        all_slots = CreatSlots(wake_time, sleep_time, delta_time)

        # Read assignments from excel file
        df_assignments = Excelfile2Dataframe(self.excel_file)
        self.assignments = CreateObjectAssignments(df_assignments, all_slots)
        print("\tData read!")

    def changeDropdownOptions(self):
        # Example method to change options dynamically
        new_options = []
        for assignment in self.timetabling:
            new_options.append(assignment.name)

        self.dropdown_menu['menu'].delete(0, 'end')  # Remove current options

        for option in new_options:
            self.dropdown_menu['menu'].add_command(label=option, command=tk._setit(self.dropdown_var, option))

        self.dropdown_var.set(new_options[0])  # Set default selection

    def updateProcess(self, status):
        self.process_done.set(status)

    def getResults(self):
        if self.timetabling != None:
            # Clear previous results
            for widget in self.root.grid_slaves():
                if int(widget.grid_info()["row"]) > 7:
                    widget.grid_forget()

            last_row = 8
            name_assignment = self.dropdown_var.get()
            for assignment in self.timetabling:
                if assignment.name == name_assignment:
                    time_scheduled = assignment.period_scheduled
                    for index in time_scheduled:
                        time = time_scheduled[index]
                        day_label = tk.Label(self.root, text=time['day'], font=("Helvetica", 8))
                        day_label.grid(row=last_row+index, column=0, columnspan=2, padx=10)
                        start_label = tk.Label(self.root, text=time['Time start'], font=("Helvetica", 8))
                        start_label.grid(row=last_row+index, column=2, padx=10)
                        end_label = tk.Label(self.root, text=time['Time end'], font=("Helvetica", 8))
                        end_label.grid(row=last_row+index, column=3, padx=10)