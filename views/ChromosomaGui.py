import tkinter

import customtkinter

from models.Parameter import Parameter


class ChromosomaGui(customtkinter.CTk):
    title_font = ('Roboto', 24)
    normal_font = ('Roboto', 10)
    normal_alternative_font = ('Roboto', 14)

    def __init__(self):
        super().__init__()
        self.chromosoma_util = None
        self.title("Evo_gen v0.1")
        # self.geometry('1000x780')
        self._set_appearance_mode("dark")

        self.expression = "x**2 - 5*x + 6"

        population_size = 4
        population_size_max = 8
        cant_ind_cross = 2

        min_limit_x = 3
        max_limit_x = 7

        cross_prob = 0.90
        ind_mut_prob = 0.90
        gen_mut_prob = 0.90

        resolution_ideal = 0.05
        generations = 4

        is_min_solution = False
        self.parameter = Parameter(min_limit_x, max_limit_x, population_size, population_size_max, cross_prob,
                                   ind_mut_prob, gen_mut_prob, generations, resolution_ideal, cant_ind_cross,
                                   is_min_solution)

        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.pages_root = customtkinter.CTkFrame(self)
        self.pages_root.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        ##PAGE INITIAL
        self.pages_buttons = customtkinter.CTkFrame(self)
        self.pages_buttons.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.initial_frame = customtkinter.CTkFrame(self.pages_root)
        self.page_initial = customtkinter.CTkButton(self.pages_buttons, text="Parameters",
                                                    command=lambda: self.show_page(self.initial_frame))

        self.report_frame = customtkinter.CTkFrame(self.pages_root)
        self.page_report = customtkinter.CTkButton(self.pages_buttons, text="Report",
                                                   command=lambda: self.show_page(self.report_frame))

        self.charts_frame = customtkinter.CTkFrame(self.pages_root)
        self.page_charts = customtkinter.CTkButton(self.pages_buttons, text="Chars",
                                                   command=lambda: self.show_page(self.charts_frame))

        self.generation_population_frame = customtkinter.CTkFrame(self.pages_root)
        self.page_generation_population = customtkinter.CTkButton(self.pages_buttons, text="Generations",
                                                                  command=lambda: self.show_page(
                                                                      self.generation_population_frame))

        self.page_initial.grid(row=1, column=0, padx=10, pady=10, sticky="wn")
        self.page_report.grid(row=1, column=1, padx=10, pady=10, sticky="wn")
        self.page_charts.grid(row=1, column=2, padx=10, pady=10, sticky="wn")
        self.page_generation_population.grid(row=1, column=3, padx=10, pady=10, sticky="wn")

        self.initial_frame.grid(row=1, column=0, padx=10, pady=50, sticky="nsew")
        self.report_frame.grid(row=1, column=0, padx=10, pady=50, sticky="nsew")
        self.charts_frame.grid(row=1, column=0, padx=10, pady=50, sticky="nsew")
        self.generation_population_frame.grid(row=1, column=0, padx=10, pady=50, sticky="nsew")

        self.expression_frame = customtkinter.CTkFrame(self.initial_frame)
        self.expression_frame.grid(row=0, column=0, padx=10, pady=10, sticky="we")

        self.label_title_expression = customtkinter.CTkLabel(self.expression_frame, text="Function",
                                                             font=self.title_font)
        self.label_title_expression.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.label_expression = customtkinter.CTkLabel(self.expression_frame, text="f(x)=")
        self.label_expression.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_expression = customtkinter.CTkEntry(self.expression_frame,
                                                       textvariable=customtkinter.StringVar(value=self.expression))
        self.entry_expression.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")

        self.population_frame = customtkinter.CTkFrame(self.initial_frame)
        self.population_frame.grid(row=1, column=0, padx=10, pady=10, sticky="we")

        self.label_title_population = customtkinter.CTkLabel(self.population_frame, text="Population params",
                                                             font=self.title_font)
        self.label_title_population.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.label_population_size = customtkinter.CTkLabel(self.population_frame, text="Population initial size: ")
        self.label_population_size.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_population_size = customtkinter.CTkEntry(self.population_frame,
                                                            textvariable=customtkinter.StringVar(
                                                                value=self.parameter.pob))
        self.entry_population_size.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="ew")

        self.label_population_size_max = customtkinter.CTkLabel(self.population_frame, text="Population max size: ")
        self.label_population_size_max.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_population_size_max = customtkinter.CTkEntry(self.population_frame,
                                                                textvariable=customtkinter.StringVar(
                                                                    value=self.parameter.pob_max))
        self.entry_population_size_max.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.margin_frame = customtkinter.CTkFrame(self.initial_frame)
        self.margin_frame.grid(row=2, column=0, padx=10, pady=10, sticky="we")

        self.label_title_margins = customtkinter.CTkLabel(self.margin_frame, text="Margins X",
                                                          font=self.title_font)
        self.label_title_margins.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.label_min_x = customtkinter.CTkLabel(self.margin_frame, text="Min: ")
        self.label_min_x.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_min_x = customtkinter.CTkEntry(self.margin_frame,
                                                  textvariable=customtkinter.StringVar(
                                                      value=self.parameter.min_limit))
        self.entry_min_x.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.label_max_x = customtkinter.CTkLabel(self.margin_frame, text="Max: ")
        self.label_max_x.grid(row=1, column=2, padx=10, pady=(10, 0), sticky="w")
        self.entry_max_x = customtkinter.CTkEntry(self.margin_frame,
                                                  textvariable=customtkinter.StringVar(
                                                      value=self.parameter.max_limit))
        self.entry_max_x.grid(row=1, column=3, padx=10, pady=10, sticky="we")

        self.probability_frame = customtkinter.CTkFrame(self.initial_frame)
        self.probability_frame.grid(row=3, column=0, padx=10, pady=10, sticky="we")

        self.label_title_probability = customtkinter.CTkLabel(self.probability_frame, text="Probability",
                                                              font=self.title_font)
        self.label_title_probability.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.label_cross_prob = customtkinter.CTkLabel(self.probability_frame, text="Cross chromosome probability: ")
        self.label_cross_prob.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_cross_prob = customtkinter.CTkEntry(self.probability_frame,
                                                       textvariable=customtkinter.StringVar(
                                                           value=self.parameter.crossProb))
        self.entry_cross_prob.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.label_ind_mut_prob = customtkinter.CTkLabel(self.probability_frame,
                                                         text="Individual chromosome probability to Mut: ")
        self.label_ind_mut_prob.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_ind_mut_prob = customtkinter.CTkEntry(self.probability_frame,
                                                         textvariable=customtkinter.StringVar(
                                                             value=self.parameter.indMutProb))
        self.entry_ind_mut_prob.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.label_gen_mut_prob = customtkinter.CTkLabel(self.probability_frame,
                                                         text="Gen chromosome probability to Mut: ")
        self.label_gen_mut_prob.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_gen_mut_prob = customtkinter.CTkEntry(self.probability_frame,
                                                         textvariable=customtkinter.StringVar(
                                                             value=self.parameter.genMutProb))
        self.entry_gen_mut_prob.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.resolution_frame = customtkinter.CTkFrame(self.initial_frame)
        self.resolution_frame.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        self.label_title_resolution = customtkinter.CTkLabel(self.resolution_frame, text="Resolution",
                                                             font=self.title_font)
        self.label_title_resolution.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.label_resolution = customtkinter.CTkLabel(self.resolution_frame, text="Ideal resolution: ")
        self.label_resolution.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_resolution = customtkinter.CTkEntry(self.resolution_frame,
                                                       textvariable=customtkinter.StringVar(
                                                           value=self.parameter.resolution_ideal))
        self.entry_resolution.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Generation
        self.generation_frame = customtkinter.CTkFrame(self.initial_frame)
        self.generation_frame.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        self.label_title_generation = customtkinter.CTkLabel(self.generation_frame, text="Generation",
                                                             font=self.title_font)
        self.label_title_generation.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.label_generation = customtkinter.CTkLabel(self.generation_frame, text="Generations: ")
        self.label_generation.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_generation = customtkinter.CTkEntry(self.generation_frame,
                                                       textvariable=customtkinter.StringVar(
                                                           value=self.parameter.generations))
        self.entry_generation.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # type solution
        self.type_solution_frame = customtkinter.CTkFrame(self.initial_frame)
        self.type_solution_frame.grid(row=2, column=1, padx=10, pady=10, sticky="we")
        self.label_title_type_solution = customtkinter.CTkLabel(self.type_solution_frame, text="Type solution",
                                                                font=self.title_font)
        self.label_title_type_solution.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.type_solution_val = tkinter.IntVar()
        self.min_solution = customtkinter.CTkRadioButton(self.type_solution_frame, text="Minimize the function",
                                                         variable=self.type_solution_val, value=True,
                                                         command=self.Select_type)
        self.min_solution.grid(row=1, column=0, padx=10, pady=10, sticky="wes")
        self.min_solution.select()
        self.max_solution = customtkinter.CTkRadioButton(self.type_solution_frame, text="Maximize  the function",
                                                         variable=self.type_solution_val, value=False,
                                                         command=self.Select_type)
        self.max_solution.grid(row=1, column=1, padx=10, pady=10, sticky="wes")

        # Button
        self.button = customtkinter.CTkButton(self.initial_frame, text="Start", command=self.button_callback)
        self.button.grid(row=4, column=0, padx=10, pady=10, sticky="wes")
        self.show_page(self.initial_frame)

    def Select_type(self):
        self.parameter.is_min_solution = bool(self.type_solution_val.get())
        print(self.parameter.is_min_solution)

    def show_page(self, page):
        for child in self.pages_root.winfo_children():
            child.grid_forget()

        page.grid(row=0, column=0, sticky="nsew")

    def button_callback(self):
        print(f"expression: {self.entry_expression.get()}")
        print(f"expression: {self.expression}")
        print("Start")
