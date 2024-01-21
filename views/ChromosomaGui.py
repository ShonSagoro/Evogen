import threading
import tkinter

import customtkinter
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models.Generation import Generation
from models.Parameter import Parameter
from utils.ChromosomaUtil import ChromosomaUtil


class FrameScrollBar(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = customtkinter.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)

    def set_content_frame(self, frame):
        frame.grid(row=0, column=0, sticky="nsew")


class ChromosomaGui(customtkinter.CTk):
    title_font = ('Roboto', 24)
    normal_font = ('Roboto', 10)

    def __init__(self):
        super().__init__()
        self.chromosoma_util = None
        self.title("Evo_gen v0.1")
        # self.geometry('1000x780')
        self._set_appearance_mode("dark")

        self.expression = "x**3 - x**3 * cos(5*x)"

        population_size = 8
        population_size_max = 100
        cant_ind_cross = 2

        min_limit_x = 0
        max_limit_x = 2

        ind_mut_prob = 0.10
        gen_mut_prob = 0.10

        resolution_ideal = 0.1
        generations = 100

        is_min_solution = False
        self.parameter = Parameter(min_limit_x, max_limit_x, population_size, population_size_max,
                                   ind_mut_prob, gen_mut_prob, generations, resolution_ideal, cant_ind_cross,
                                   is_min_solution)
        self.chromosomaUtil = ChromosomaUtil(self.parameter, self.expression)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.pages_root = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.pages_root.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        ##PAGE INITIAL
        self.pages_buttons = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.pages_buttons.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.initial_frame = customtkinter.CTkFrame(self.pages_root)
        self.page_initial = customtkinter.CTkButton(self.pages_buttons, text="Parameters",
                                                    command=lambda: self.show_page(self.initial_frame))

        self.report_frame = customtkinter.CTkFrame(self.pages_root, corner_radius=0, fg_color="transparent")
        self.page_report = customtkinter.CTkButton(self.pages_buttons, text="Report",
                                                   command=lambda: self.show_page(self.report_frame))

        self.charts_frame = customtkinter.CTkFrame(self.pages_root, corner_radius=0, fg_color="transparent")
        self.page_charts = customtkinter.CTkButton(self.pages_buttons, text="Chars",
                                                   command=lambda: self.show_page(self.charts_frame))

        self.generation_population_frame = customtkinter.CTkFrame(self.pages_root, corner_radius=0,
                                                                  fg_color="transparent")
        self.page_generation_population = customtkinter.CTkButton(self.pages_buttons, text="Generations",
                                                                  command=lambda: self.show_page(
                                                                      self.generation_population_frame))

        self.page_initial.grid(row=1, column=0, padx=10, pady=0, sticky="wn")
        self.page_report.grid(row=1, column=1, padx=10, pady=0, sticky="wn")
        self.page_charts.grid(row=1, column=2, padx=10, pady=0, sticky="wn")
        self.page_generation_population.grid(row=1, column=3, padx=10, pady=0, sticky="wn")

        self.initial_frame.grid(row=1, column=0, padx=10, pady=50, sticky="nsew")
        self.report_frame.grid(row=1, column=0, padx=10, pady=50, sticky="ew")
        self.charts_frame.grid(row=1, column=0, padx=10, pady=50, sticky="nsew")
        self.generation_population_frame.grid(row=1, column=0, padx=10, pady=50, sticky="nsew")

        # Expression param
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

        # Population params
        self.population_frame = customtkinter.CTkFrame(self.initial_frame)
        self.population_frame.grid(row=1, column=0, padx=10, pady=10, sticky="we")

        self.label_title_population = customtkinter.CTkLabel(self.population_frame, text="Population params",
                                                             font=self.title_font)
        self.label_title_population.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.label_population_size = customtkinter.CTkLabel(self.population_frame, text="Population initial size: ")
        self.label_population_size.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_population_size = customtkinter.CTkEntry(self.population_frame,
                                                            textvariable=customtkinter.StringVar(
                                                                value=str(self.parameter.pob)))
        self.entry_population_size.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="ew")

        self.label_population_size_max = customtkinter.CTkLabel(self.population_frame, text="Population max size: ")
        self.label_population_size_max.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_population_size_max = customtkinter.CTkEntry(self.population_frame,
                                                                textvariable=customtkinter.StringVar(
                                                                    value=self.parameter.pob_max))
        self.entry_population_size_max.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.label_cant_ind_cross = customtkinter.CTkLabel(self.population_frame, text="Cant.of individual cross: ")
        self.label_cant_ind_cross.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_cant_ind_cross = customtkinter.CTkEntry(self.population_frame,
                                                           textvariable=customtkinter.StringVar(
                                                               value=self.parameter.cant_ind_cross))
        self.entry_cant_ind_cross.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Margin Param
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
        self.generation_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.label_title_generation = customtkinter.CTkLabel(self.generation_frame, text="Generation",
                                                             font=self.title_font)
        self.label_title_generation.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")

        self.label_generation = customtkinter.CTkLabel(self.generation_frame, text="Generations: ")
        self.label_generation.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        self.entry_generation = customtkinter.CTkEntry(self.generation_frame,
                                                       textvariable=customtkinter.StringVar(
                                                           value=self.parameter.generations))
        self.entry_generation.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
        self.generation_frame.grid_columnconfigure(0, weight=1)

        # type solution
        self.type_solution_frame = customtkinter.CTkFrame(self.initial_frame)
        self.type_solution_frame.grid(row=2, column=1, padx=10, pady=10, sticky="news")
        self.label_title_type_solution = customtkinter.CTkLabel(self.type_solution_frame, text="Type solution",
                                                                font=self.title_font)
        self.label_title_type_solution.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.type_solution_val = tkinter.IntVar()
        self.min_solution = customtkinter.CTkRadioButton(self.type_solution_frame, text="Minimize the function",
                                                         variable=self.type_solution_val, value=True)
        self.min_solution.grid(row=1, column=0, padx=10, pady=10, sticky="wes")
        self.min_solution.select()
        self.max_solution = customtkinter.CTkRadioButton(self.type_solution_frame, text="Maximize  the function",
                                                         variable=self.type_solution_val, value=False)
        self.max_solution.grid(row=1, column=1, padx=10, pady=10, sticky="wes")

        self.bar_frame = customtkinter.CTkFrame(self.initial_frame)
        self.bar_frame.grid(row=3, column=1, padx=10, pady=10, sticky="news")
        self.label_title_progress = customtkinter.CTkLabel(self.bar_frame, text="Progress",
                                                           font=self.title_font)
        self.label_title_progress.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.progressbar = customtkinter.CTkProgressBar(self.bar_frame, orientation="horizontal", mode="determinate")
        self.progressbar.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.progressbar.set(0)
        self.label_progressbar = customtkinter.CTkLabel(self.bar_frame,
                                                        text="Info: Dale al boton 'start' para iniciar.")
        self.label_progressbar.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

        self.credits_frame = customtkinter.CTkFrame(self.initial_frame, fg_color="transparent")
        self.credits_frame.grid(row=4, column=1, padx=10, pady=10, sticky="news")
        self.label_credits = customtkinter.CTkLabel(self.credits_frame, text="By: Jonathan Salvador Gomez Roque")
        self.label_credits.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        # Button
        self.button = customtkinter.CTkButton(self.initial_frame, text="Start", command=self.button_callback)
        self.button.grid(row=4, column=0, padx=10, pady=10, sticky="news")
        self.show_page(self.initial_frame)

        self.chars_event = threading.Event()
        self.generations_event = threading.Event()
        self.population_event = threading.Event()

    def show_page(self, page):
        for child in self.pages_root.winfo_children():
            child.grid_forget()

        page.grid(row=0, column=0, sticky="nsew")

    def button_callback(self):
        self.page_report.configure(state="disabled")
        self.page_charts.configure(state="disabled")
        self.page_generation_population.configure(state="disabled")
        self.label_progressbar.configure(text="Info: Recolectando datos")
        self.expression = self.entry_expression.get()
        is_min_solution = bool(self.type_solution_val.get())
        population_size = int(self.entry_population_size.get())
        population_size_max = int(self.entry_population_size_max.get())
        cant_ind_cross = int(self.entry_cant_ind_cross.get())

        min_limit_x = float(self.entry_min_x.get())
        max_limit_x = float(self.entry_max_x.get())

        ind_mut_prob = float(self.entry_ind_mut_prob.get())
        gen_mut_prob = float(self.entry_gen_mut_prob.get())

        resolution_ideal = float(self.entry_resolution.get())
        generations = int(self.entry_generation.get())

        self.parameter = Parameter(min_limit_x, max_limit_x, population_size, population_size_max,
                                   ind_mut_prob, gen_mut_prob, generations, resolution_ideal, cant_ind_cross,
                                   is_min_solution)
        self.button.configure(state="disabled")
        self.chromosomaUtil = ChromosomaUtil(self.parameter, self.expression)

        self.progressbar.start()

        self.label_progressbar.configure(text="Info: Realizando operaciones")
        threading.Thread(target=self.init_chromosoma_util).start()

    def init_chromosoma_util(self):
        self.chromosomaUtil.init()

        self.label_progressbar.configure(text="Info: graficando")
        self.put_the_chars(self.charts_frame)
        self.page_charts.configure(state="normal")

        self.label_progressbar.configure(text="Info: Reportando")
        self.put_generations_cards(self.report_frame)
        self.page_report.configure(state="normal")

        self.label_progressbar.configure(text="Info: Reporte mas extendido")
        self.put_population_generation(self.generation_population_frame)
        self.page_generation_population.configure(state="normal")

        self.progressbar.set(0.5)

        self.button.configure(state="normal")
        self.progressbar.stop()
        self.progressbar.set(1)
        self.label_progressbar.configure(text="Info: Listo, checa el resto de pestañas")

    def put_the_chars(self, parent):
        scrollbar_frame = FrameScrollBar(parent, width=700, height=600, corner_radius=0, fg_color="transparent")
        scrollbar_frame.grid(row=0, column=0, padx=10, pady=50, sticky="nsew")

        figures_frame = customtkinter.CTkFrame(scrollbar_frame)
        figures_frame.grid(row=0, column=0, sticky="nsew")

        for row, fig in enumerate(self.chromosomaUtil.generated_figures):
            figure_frame = customtkinter.CTkFrame(figures_frame)
            figure_frame.grid(row=row, column=0, sticky="nsew")
            self.show_figure_in_frame(fig, figure_frame)
        self.chars_event.set()

    def show_figure_in_frame(self, fig, parent):
        canvas = FigureCanvasTkAgg(fig, master=parent)
        plt.close(fig)
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def put_generations_cards(self, parent):
        cards_frame = FrameScrollBar(parent, width=600, height=600, corner_radius=0, fg_color="transparent")
        cards_frame.grid(row=0, column=0, padx=20, pady=20)

        content_frame = customtkinter.CTkFrame(cards_frame)
        content_frame.grid(row=0, column=0, sticky="news")
        content_frame.grid_columnconfigure(0, weight=1)

        self.put_generations(self.chromosomaUtil.generations[-1], content_frame, 0)
        self.put_generations(self.chromosomaUtil.generations[0], content_frame, 1)

        cards_frame.grid_rowconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(0, weight=1)
        self.generations_event.set()

    def put_generations(self, gen: Generation, parent, row):
        generation_frame = customtkinter.CTkFrame(parent, width=600)
        generation_frame.grid(row=row, column=0, pady=10, padx=10, sticky="ew")

        label_title_generation = customtkinter.CTkLabel(generation_frame, text=f"Generation {gen.id} :",
                                                        font=self.title_font)
        label_title_generation.grid(row=0, column=0, pady=(10, 0), padx=10, sticky="w")
        generation_frame.grid_columnconfigure(0, weight=1)

        report_frame = customtkinter.CTkFrame(generation_frame, width=600)
        report_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nwes")
        report_frame.grid_columnconfigure(0, weight=1)

        label_info_better = customtkinter.CTkLabel(report_frame, text=f"Better f(x): {gen.better.fx}")
        label_info_better.grid(row=1, column=0, pady=(10, 0), padx=10, sticky="we")

        label_info_worst = customtkinter.CTkLabel(report_frame, text=f"Worst f(x): {gen.worst.fx}")
        label_info_worst.grid(row=2, column=0, pady=(10, 0), padx=10, sticky="we")

        label_info_betterx = customtkinter.CTkLabel(report_frame, text=f"Better x: {gen.better.x}")
        label_info_betterx.grid(row=3, column=0, pady=(10, 0), padx=10, sticky="we")

        label_info_worstx = customtkinter.CTkLabel(report_frame, text=f"Worst x: {gen.worst.x}")
        label_info_worstx.grid(row=4, column=0, pady=(10, 0), padx=10, sticky="we")

        label_info_prom = customtkinter.CTkLabel(report_frame, text=f"Prom f(x): {gen.prom}")
        label_info_prom.grid(row=5, column=0, pady=(10, 0), padx=10, sticky="we")
        self.label_progressbar.configure(text=f"Info: Reportando:{gen.id}")

    def put_population_generation(self, parent):
        cards_frame = FrameScrollBar(parent, width=800, height=600, corner_radius=0, fg_color="transparent")
        cards_frame.grid(row=0, column=0, padx=20, pady=20)

        content_frame = customtkinter.CTkFrame(cards_frame)
        content_frame.grid(row=0, column=0, sticky="nsew")

        self.put_population_card(self.chromosomaUtil.generations[-1], content_frame, 0)
        self.put_population_card(self.chromosomaUtil.generations[0], content_frame, 1)

        cards_frame.grid_rowconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(0, weight=1)
        self.population_event.set()

    def put_population_card(self, gen: Generation, parent, row):
        self.label_progressbar.configure(text=f"Info:Haciendo el reporte extendido:{gen.id}")
        generation_frame = customtkinter.CTkFrame(parent)
        generation_frame.grid(row=row, column=0, pady=10, padx=10, sticky="ew")

        label_title_generation = customtkinter.CTkLabel(generation_frame, text=f"Generation {gen.id} :",
                                                        font=self.title_font)
        label_title_generation.grid(row=0, column=0, pady=(10, 0), padx=10, sticky="w")

        label_info_better = customtkinter.CTkLabel(generation_frame, text=f"Better f(x): {gen.better.fx}")
        label_info_better.grid(row=1, column=0, pady=(10, 0), padx=10, sticky="w")
        label_info_betterx = customtkinter.CTkLabel(generation_frame, text=f"Better x: {gen.better.x}")
        label_info_betterx.grid(row=2, column=0, pady=(10, 0), padx=10, sticky="w")

        label_info_worst = customtkinter.CTkLabel(generation_frame, text=f"Worst f(x): {gen.worst.fx}")
        label_info_worst.grid(row=3, column=0, pady=(10, 0), padx=10, sticky="w")

        label_info_worstx = customtkinter.CTkLabel(generation_frame, text=f"Worst x {gen.worst.x}")
        label_info_worstx.grid(row=4, column=0, pady=(10, 0), padx=10, sticky="w")

        label_info_prom = customtkinter.CTkLabel(generation_frame, text=f"Prom f(x): {gen.prom}")
        label_info_prom.grid(row=5, column=0, pady=(10, 0), padx=10, sticky="w")

        label_info_population_title = customtkinter.CTkLabel(generation_frame, text="Poputations :{")
        label_info_population_title.grid(row=6, column=0, pady=(10, 0), padx=10, sticky="w")
        self.put_population(gen, generation_frame, 5)
        label_info_population_title = customtkinter.CTkLabel(generation_frame, text="}")
        label_info_population_title.grid(row=7, column=0, pady=(10, 0), padx=10, sticky="w")
        self.label_progressbar.configure(text=f"Info: Reportando extenso listo:{gen.id}")

    def put_population(self, gen: Generation, parent, row):
        population_frame = customtkinter.CTkFrame(parent)
        population_frame.grid(row=row, column=0, pady=10, padx=10, sticky="ew")
        for row, crom in enumerate(gen.chromosomas):
            label_info_chromosome = customtkinter.CTkLabel(population_frame, text=f"{(row + 1)}: {crom.__str__()}")
            label_info_chromosome.grid(row=row, column=0, pady=(10, 0), padx=10, sticky="w")
            self.label_progressbar.configure(text=f"Info:añadiendo al cromosoma: {row}, de la generacion:{gen.id}")

