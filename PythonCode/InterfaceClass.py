from Libraries import *
from StoreDataFunctions import CreatSlots, Excelfile2Dataframe, CreateObjectAssignments, OtherConditions
from OptimizationFunctions import ParametersOptimizationProgram, runOptimizationProgram, ObjectiveFunction
from OtherFunctions import adjustAssignmentsWeek, getWeekDistribution

# Interface functions

class TimetablingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timetabling program")
        self.root.resizable(width=False, height=False)

        self.calendar_window = None
        self.overview_window = None
        
        self.excel_file = None
        self.excel_name = ctk.StringVar()
        self.excel_assig = ctk.StringVar()
        self.process_done = ctk.StringVar()
        self.assignment_day = ctk.StringVar()
        self.assignment_start = ctk.StringVar()
        self.assignment_end = ctk.StringVar()

        self.assignment_day1 = ctk.StringVar()
        self.assignment_day2 = ctk.StringVar()
        self.assignment_day3 = ctk.StringVar()
        self.assignment_day4 = ctk.StringVar()
        
        self.assignment_start1 = ctk.StringVar()
        self.assignment_start2 = ctk.StringVar()
        self.assignment_start3 = ctk.StringVar()
        self.assignment_start4 = ctk.StringVar()

        self.assignment_end1 = ctk.StringVar()
        self.assignment_end2 = ctk.StringVar()
        self.assignment_end3 = ctk.StringVar()
        self.assignment_end4 = ctk.StringVar()

        self.results = [None]
        self.timetabling = None
        self.assignments = None
        self.max_iterations = None
        self.tabu_list_size = None
        self.num_runs = None
        self.other_conditions = None

        self.timetabling_var = ctk.StringVar(self.root)
        self.dropdown_var = ctk.StringVar(self.root)

        self.timetabling_var.trace_add("write", lambda *args: self.getResults())
        self.timetabling_var.set("1")  # default value
        self.dropdown_var.trace_add("write", lambda *args: self.getResults())
        self.dropdown_var.set("")  # default value

        self.objective_values = []
        self.number_runs = 0
        self.number_iterations = 0
        
        self.setupInitial()

    def setupInitial(self):
        # Configure grid layout
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1, minsize=100)

        bg=ctk.CTkImage(light_image=Image.open('Images/background_app.png'), dark_image=Image.open('Images/background_app.png'), size=(500,580))
        label = ctk.CTkLabel(self.root, text='',image=bg).place(relx=0.5, rely=0.51, anchor='center')
        # Title label
        label = ctk.CTkLabel(self.root, text="TIMETABLING", font=("Roboto", 25, "bold")).grid(row=0, column=0, columnspan=5, pady=10)

        # Frame for file selection
        frame_file = ctk.CTkFrame(self.root, corner_radius=0, border_width=2, border_color='white')
        frame_file.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
        for i in range(5):
            frame_file.grid_columnconfigure(i, weight=1, minsize=100)

        ctk.CTkLabel(frame_file, text="FILE SELECTION", font=("Helvetica", 18, "bold")).grid(row=0, column=0, columnspan=3, pady=5, padx=20, sticky='w')
        
        self.button_excelfile = ctk.CTkButton(frame_file, text="Select", command=self.clickButtonExcel, font=("Helvetica", 15, 'bold'), width=180, fg_color='#104861')
        self.button_excelfile.grid(row=0, column=2, columnspan=3, pady=7)

        ctk.CTkLabel(frame_file, text="Name:", font=("Helvetica", 13, 'bold')).grid(row=1, column=1, sticky="e")
        ctk.CTkLabel(frame_file, textvariable=self.excel_name, font=("Helvetica", 13)).grid(row=1, column=2, columnspan=2)
        ctk.CTkLabel(frame_file, text="Assignments:", font=("Helvetica", 13, 'bold')).grid(row=2, column=1, pady=10, sticky="e")
        ctk.CTkLabel(frame_file, textvariable=self.excel_assig, font=("Helvetica", 13)).grid(row=2, column=2, columnspan=2)

        # Run button
        self.button_run = ctk.CTkButton(self.root, text="Run", command=self.clickButtonRun, state="disabled", font=("Helvetica", 15, 'bold'), width=205, fg_color='#104861')
        self.button_run.grid(row=2, column=0, columnspan=5, pady=10)

        # Frame for process section
        frame_process = ctk.CTkFrame(self.root, corner_radius=0, border_width=2, border_color='white')
        frame_process.grid(row=3, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
        for i in range(5):
            frame_process.grid_columnconfigure(i, weight=1, minsize=100)

        section_label = ctk.CTkLabel(frame_process, text="PROCESS", font=("Helvetica", 18, "bold"))
        section_label.grid(row=0, column=0, columnspan=3, pady=5, padx=20, sticky='w')
        
        ctk.CTkLabel(frame_process, textvariable=self.process_done, font=("Helvetica", 14, 'bold')).grid(row=0, column=4, sticky='e', padx=10)
        self.process = ctk.CTkProgressBar(frame_process,width=200,corner_radius=10,orientation='horizontal')
        self.updateProcess(0)
        self.process.grid(row=0, column=2, columnspan=3, pady=5, sticky='w')

        # Frame for results section
        frame_results = ctk.CTkFrame(self.root, corner_radius=0, border_width=2, border_color='white')
        frame_results.grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
        for i in range(5):
            frame_results.grid_columnconfigure(i, weight=1, minsize=100)

        results_label = ctk.CTkLabel(frame_results, text="ASSIGNMENT TIME", font=("Helvetica", 18, "bold"))
        results_label.grid(row=0, column=0, columnspan=3, pady=5, padx=20, sticky='w')

        self.box_timetabling = ctk.CTkComboBox(frame_results, variable=self.timetabling_var, values=["1"], width=60)
        self.box_timetabling.grid(row=0, column=4, pady=5)
        ctk.CTkLabel(frame_results, text="Timetable:", font=("Helvetica", 17, 'bold')).grid(row=0, column=3, sticky='e')

        self.box = ctk.CTkComboBox(frame_results, variable=self.dropdown_var, values=[""], width=300)
        self.box.grid(row=1, column=1, columnspan=3, pady=5)

        ctk.CTkLabel(frame_results, text="Day", font=("Helvetica", 15, 'bold')).grid(row=2, column=1)
        ctk.CTkLabel(frame_results, text="Start time", font=("Helvetica", 15, 'bold')).grid(row=2, column=2)
        ctk.CTkLabel(frame_results, text="End time", font=("Helvetica", 15, 'bold')).grid(row=2, column=3)

        ctk.CTkFrame(frame_results, corner_radius=1,width=300, height=2, fg_color='#104861').grid(row=3, column=1, columnspan=3)

        for i, (day_var, start_var, end_var) in enumerate([
            (self.assignment_day1, self.assignment_start1, self.assignment_end1),
            (self.assignment_day2, self.assignment_start2, self.assignment_end2),
            (self.assignment_day3, self.assignment_start3, self.assignment_end3),
            (self.assignment_day4, self.assignment_start4, self.assignment_end4)
        ], start=4):
            ctk.CTkLabel(frame_results, textvariable=day_var, font=("Helvetica", 13, 'bold')).grid(row=i, column=1)
            ctk.CTkLabel(frame_results, textvariable=start_var, font=("Helvetica", 13, 'bold')).grid(row=i, column=2)
            ctk.CTkLabel(frame_results, textvariable=end_var, font=("Helvetica", 13, 'bold')).grid(row=i, column=3)

        # Additional buttons
        self.button_calendar = ctk.CTkButton(self.root, text="Calendar", command=self.createCalendarInterface, state="disabled", font=("Helvetica", 15, 'bold'), width=140, fg_color='#104861')
        self.button_calendar.grid(row=5, column=0, columnspan=3, pady=10)
        
        self.button_overview = ctk.CTkButton(self.root, text="Overview", command=self.createOverviewInterface, state="disabled", font=("Helvetica", 15, 'bold'), width=140, fg_color='#104861')
        self.button_overview.grid(row=5, column=2, columnspan=3, pady=10)
        
    def getExcelFile(self):
        return self.excel_file

    def getTimetabling(self):
        return self.timetabling

    def setTimetabling(self, number):
        self.timetabling = self.results[number-1]

    def setObjectiveValues(self, objective_values):
            self.objective_values = objective_values
    
    def setNumberRuns(self, runs):
        self.number_runs = runs

    def setNumberIterations(self, iterations):
        self.number_iterations = iterations

    def clickButtonExcel(self):
        self.excel_file = self.selectExcelFile()
        self.button_calendar.configure(state="disabled")
        self.button_overview.configure(state="disabled")
        self.changeDropdownOptions(reset=1)
        self.updateProcess(0)

        if self.excel_file:
            self.readData()
            self.excel_name.set(os.path.basename(self.excel_file))
            self.excel_assig.set(str(len(self.assignments)))
            self.button_run.configure(state="normal")
        else:
            self.excel_name.set("")
            self.excel_assig.set("")
            self.button_run.configure(state="disabled")

    def clickButtonRun(self):
        ## Optimization program
        print("\n-> Running the optimization program  (...)")
        self.results = runOptimizationProgram(self, self.assignments, self.max_iterations, self.tabu_list_size, self.num_runs, self.other_conditions)
        self.setTimetabling(int(self.timetabling_var.get()))
        self.changeDropdownOptions(reset=0)
        self.button_calendar.configure(state="normal")
        self.button_overview.configure(state="normal")

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

    def changeDropdownOptions(self,reset):
        # Example method to change options dynamically
        new_options = []
        if reset == 0:
            for assignment in self.timetabling:
                new_options.append(assignment.name)
            self.box_timetabling.configure(values=[str(i) for i in range(1, len(self.results) + 1)])
        else:
            new_options = [""]
            self.assignment_day1.set(" ")
            self.assignment_day2.set(" ")
            self.assignment_day3.set(" ")
            self.assignment_day4.set(" ")
            self.assignment_start1.set(" ")
            self.assignment_start2.set(" ")
            self.assignment_start3.set(" ")
            self.assignment_start4.set(" ")
            self.assignment_end1.set(" ")
            self.assignment_end2.set(" ")
            self.assignment_end3.set(" ")
            self.assignment_end4.set(" ")
            self.box_timetabling.configure(values="1")

        self.box.configure(values=new_options)
        
    def updateProcess(self, status):
        self.process.set(status)
        self.process_done.set(f'{status*100:.2f} %')
        self.root.update()

    def getResults(self):
        timetabling_value = self.timetabling_var.get()
        if timetabling_value:  # Check if the value is not empty
            try:
                timetabling_int = int(timetabling_value)
                self.setTimetabling(timetabling_int)
            except ValueError:
                # Handle the case where conversion fails
                print("Invalid input for integer conversion")

        if self.timetabling != None:
            name_assignment = self.dropdown_var.get()

            self.assignment_day1.set(" ")
            self.assignment_day2.set(" ")
            self.assignment_day3.set(" ")
            self.assignment_day4.set(" ")
            self.assignment_start1.set(" ")
            self.assignment_start2.set(" ")
            self.assignment_start3.set(" ")
            self.assignment_start4.set(" ")
            self.assignment_end1.set(" ")
            self.assignment_end2.set(" ")
            self.assignment_end3.set(" ")
            self.assignment_end4.set(" ")

            for assignment in self.timetabling:
                if assignment.name == name_assignment:
                    time_scheduled = assignment.period_scheduled
                    for index in time_scheduled:
                        time = time_scheduled[index]
                        if index == 1:
                            self.assignment_day1.set(time['day'])
                            self.assignment_start1.set(time['Time start'])
                            self.assignment_end1.set(time['Time end'])
                        elif index == 2:
                            self.assignment_day2.set(time['day'])
                            self.assignment_start2.set(time['Time start'])
                            self.assignment_end2.set(time['Time end'])
                        elif index == 3:
                            self.assignment_day3.set(time['day'])
                            self.assignment_start3.set(time['Time start'])
                            self.assignment_end3.set(time['Time end'])
                        elif index == 4:
                            self.assignment_day4.set(time['day'])
                            self.assignment_start4.set(time['Time start'])
                            self.assignment_end4.set(time['Time end'])

        if self.overview_window and self.overview_window.winfo_exists():
            self.overview.update_display()
        
        if self.calendar_window and self.calendar_window.winfo_exists():
            self.calendar.update_display()

    def createCalendarInterface(self):
        if self.calendar_window is None or not self.calendar_window.winfo_exists():
            self.calendar_window = ctk.CTkToplevel(self.root)
            self.calendar_window.title("Calendar")
            self.calendar = CalendarInterface(self)
        else:
            self.calendar_window.deiconify()  # Restore the window if it was minimized
            self.calendar_window.lift()       # Bring it to the front

    def createOverviewInterface(self):
        if self.overview_window is None or not self.overview_window.winfo_exists():
            self.overview_window = ctk.CTkToplevel(self.root)
            self.overview_window.title("Overview")
            self.overview = OverviewInterface(self)
        else:
            self.overview_window.deiconify()  # Restore the window if it was minimized
            self.overview_window.lift()       # Bring it to the front

class CalendarInterface:
    def __init__(self, main):
        self.root = main.calendar_window
        self.root.title("Calendar")
        self.root.resizable(width=False, height=False)
        
        self.mainWindow = main

        self.setupCalendar()
    
    def setupCalendar(self):
        # Configure grid layout
        for i in range(9):
            if i==0 or i ==8:
                self.root.grid_columnconfigure(i, weight=1, minsize=10)
            else:
                self.root.grid_columnconfigure(i, weight=1, minsize=50)

        frame_title = ctk.CTkFrame(self.root, corner_radius=10, height=40)
        frame_title.grid(row=0, column=0, columnspan=9, pady=10)
        frame_title.grid_propagate(False)
        label = ctk.CTkLabel(frame_title, text="CALENDAR", font=("Roboto", 22, "bold"))
        label.place(relx=0.5, rely=0.5, anchor='center')

        # Create frames of each day
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.frames_day = []
        for i, day in enumerate(days_of_week):
            # Frame para cada dia com cantos arredondados
            self.frames_day.append(ctk.CTkFrame(self.root, corner_radius=10, width=190, height=250,border_width=2, border_color='#104861'))
            self.frames_day[i].grid(row=1, column=i+1, pady=10, padx=5)

            self.frames_day[i].pack_propagate(False)

            label_day = ctk.CTkLabel(self.frames_day[i], text=day, font=("Helvetica", 14, "bold"))
            label_day.pack(side="top", pady=5, padx=10)
            ctk.CTkFrame(self.frames_day[i], corner_radius=1,width=140, height=2, fg_color='#104861').pack(side="top", pady=5, padx=10)

        if self.mainWindow.timetabling is not None:
            assignments_week = adjustAssignmentsWeek(self.mainWindow.timetabling)
            
            # Definir cores e garantir que cada nome tenha uma cor específica
            colors = ['#1f4068',  # Azul marinho escuro
                    '#2d6a4f',  # Verde escuro profundo
                    '#6b1e4f',  # Rosa profundo
                    '#917519',  # Amarelo escuro intenso
                    '#8b4726']  # Laranja escuro

            # Extrair nomes e associá-los a cores
            names = [assignment.name for assignment in self.mainWindow.timetabling]
            unique_names = list(set(names))  # Garantir que cada nome seja único

            # Mapear nomes para cores
            assignment_colors = {}
            for i, name in enumerate(unique_names):
                assignment_colors[name] = colors[i % len(colors)]  # Garantir que as cores se repitam se necessário

            # Criar frames e labels com cores associadas aos nomes
            for i, (day, assignments) in enumerate(assignments_week.items()):
                for assignment in assignments:
                    color = assignment_colors[assignment['name']]

                    frame = ctk.CTkFrame(self.frames_day[i], corner_radius=10, width=155, height=40, fg_color=color)
                    frame.pack(side="top", padx=10, pady=2)
                    frame.pack_propagate(False)

                    label_text = f"{assignment['name']}\n{assignment['Time start']} - {assignment['Time end']}"
                    label = ctk.CTkLabel(frame, text=label_text, font=("Helvetica", 8))
                    label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Additional buttons
        self.button_googleCalendar = ctk.CTkButton(self.root, text="Google Calendar", command=self.shareGoogleCalendar, state="normal", font=("Helvetica", 13, 'bold'), width=150, fg_color='#104861')
        self.button_googleCalendar.grid(row=2, column=1, columnspan=3, pady=10, padx=10, sticky='w')

    def shareGoogleCalendar(self):
        return 0
    
    def update_display(self):
        self.setupCalendar()

class OverviewInterface:
    def __init__(self, main):
        self.root = main.overview_window
        self.root.title("Overview")
        self.root.resizable(width=False, height=False)

        self.mainWindow = main

        self.hist_ax = None
        self.hist_fig = None

        self.setupOverview()

    def getObjectiveValues(self):
        return self.mainWindow.objective_values
    
    def getNumberRuns(self):
        return self.mainWindow.number_runs
    
    def getNumberIterations(self):
        return self.mainWindow.number_iterations

    def setupOverview(self):
        # Configure grid layout
        for i in range(9):
            if i==0 or i ==8 or i==4:
                self.root.grid_columnconfigure(i, weight=1, minsize=10)
            else:
                self.root.grid_columnconfigure(i, weight=1, minsize=100)

        frame_title = ctk.CTkFrame(self.root, corner_radius=10, height=40)
        frame_title.grid(row=0, column=0, columnspan=9, pady=10, padx=10, sticky='w')
        frame_title.grid_propagate(False)
        label = ctk.CTkLabel(frame_title, text="OVERVIEW", font=("Roboto", 22, "bold")).place(relx=0.5, rely=0.5, anchor='center')

        # Frame Week distribution
        self.frame_week = ctk.CTkFrame(self.root, corner_radius=5, height=400, width=350)
        self.frame_week.grid(row=1, column=1, columnspan=3, pady=20, padx=10)
        self.frame_week.grid_propagate(False)
        for i in range(5):
            if i==0 or i==4:
                self.frame_week.grid_columnconfigure(i, weight=1, minsize=10)
            else:
                self.frame_week.grid_columnconfigure(i, weight=1, minsize=100)
        label = ctk.CTkLabel(self.frame_week, text="DISTRIBUTION", font=("Roboto", 18, "bold")).grid(row=0, column=0, columnspan=5, padx=10, pady=10,sticky='w')

        # Create and display the week histogram plot
        self.plotHistogram()

        self.frame_constraints = ctk.CTkFrame(self.root, corner_radius=5, height=400, width=350)
        self.frame_constraints.grid(row=1, column=5, columnspan=3, pady=20, padx=10)
        self.frame_constraints.grid_propagate(False)
        for i in range(5):
            if i==0 or i==4:
                self.frame_constraints.grid_columnconfigure(i, weight=1, minsize=10)
            else:
                self.frame_constraints.grid_columnconfigure(i, weight=1, minsize=100)
        label = ctk.CTkLabel(self.frame_constraints, text="OPTIMIZATION", font=("Roboto", 18, "bold")).grid(row=0, column=0, columnspan=5, padx=10, pady=10,sticky='w')

        # Create and display the objective value development plot
        self.plotObjectiveDevelopment()
        ctk.CTkLabel(self.frame_constraints, text="Minimum value:", font=("Helvetica", 13, 'bold')).grid(row=2, column=0, columnspan=2, sticky="e")
        ctk.CTkLabel(self.frame_constraints, text=min(self.getObjectiveValues()), font=("Helvetica", 13, 'bold')).grid(row=2, column=2, columnspan=2)
        ctk.CTkLabel(self.frame_constraints, text="Mean iterations:", font=("Helvetica", 13, 'bold')).grid(row=3, column=0, columnspan=2, sticky="e")
        ctk.CTkLabel(self.frame_constraints, text=np.mean(self.getNumberIterations()), font=("Helvetica", 13, 'bold')).grid(row=3, column=2, columnspan=2)
        
    def plotObjectiveDevelopment(self):
        # Create a figure with specified size
        frame_graph = ctk.CTkFrame(self.frame_constraints, corner_radius=15, border_width=4,border_color='#104861', height=180, width=290)
        frame_graph.grid(row=1, column=1, columnspan=3, pady=5)

        fig = Figure(figsize=(3.5, 1.9), dpi=100)
        ax = fig.add_subplot(111)

        # Generate and plot
        ax.scatter(range(1,self.getNumberRuns()+1), self.getObjectiveValues())
        ax.set_title("Objective Value", fontdict={'fontsize': 10, 'fontweight': 'bold'}, color='white')
        ax.tick_params(axis='x', colors='white')  # Cor das marcas no eixo x
        ax.tick_params(axis='y', colors='white')  # Cor das marcas no eixo y

        # Configurar a grade horizontal
        ax.yaxis.grid(False)  # Desativar grade no eixo y
        ax.xaxis.grid(False)  # Desativar grade no eixo x
        ax.set_ylim(bottom=0, top=max(self.getObjectiveValues())+0.1*(1+max(self.getObjectiveValues())))

        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_color('#333333')
        ax.spines['right'].set_color('#333333')
        # Remove the background color of the plot area
        ax.set_facecolor('#333333')
        fig.patch.set_facecolor('#333333')
        # Ensure y-axis has integer ticks
        ax.yaxis.get_major_locator().set_params(integer=True)

        # Convert the plot to a Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=frame_graph)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.place(relx=0.5, rely=0.5, anchor='center')

    def plotHistogram(self):
        # Create a figure with specified size
        frame_graph = ctk.CTkFrame(self.frame_week, corner_radius=15, border_width=4,border_color='#104861', height=180, width=290)
        frame_graph.grid(row=1, column=1, columnspan=3)

        if self.hist_ax is None:
            self.hist_fig = Figure(figsize=(3.5, 1.9), dpi=100)
            self.hist_ax = self.hist_fig.add_subplot(111)
        else:
            self.hist_ax.clear()

        # Generate and plot histogram
        days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        data = getWeekDistribution(self.mainWindow.timetabling)
        # Plot bar graph
        self.hist_ax.bar(days_of_week, data)
        self.hist_ax.set_title("Week distribution", fontdict={'fontsize': 10, 'fontweight': 'bold'}, color='white')
        self.hist_ax.tick_params(axis='x', colors='white')  # Cor das marcas no eixo x
        self.hist_ax.tick_params(axis='y', colors='white')  # Cor das marcas no eixo y

        # Configurar a grade horizontal
        self.hist_ax.yaxis.grid(True)  # Ativar grade no eixo y
        self.hist_ax.xaxis.grid(False)  # Desativar grade no eixo x

        self.hist_ax.spines['bottom'].set_color('white')
        self.hist_ax.spines['left'].set_color('#333333')
        self.hist_ax.spines['top'].set_color('#333333')
        self.hist_ax.spines['right'].set_color('#333333')
        # Remove the background color of the plot area
        self.hist_ax.set_facecolor('#333333')
        self.hist_fig.patch.set_facecolor('#333333')
        # Ensure y-axis has integer ticks
        self.hist_ax.yaxis.get_major_locator().set_params(integer=True)

        # Convert the plot to a Tkinter canvas
        canvas = FigureCanvasTkAgg(self.hist_fig, master=frame_graph)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.place(relx=0.5, rely=0.5, anchor='center')

    def update_display(self):
        if self.hist_ax is not None:
            self.plotHistogram()