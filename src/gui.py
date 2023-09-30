import tkinter as tk
from tkinter import messagebox
import subprocess
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
from model import *

import os

current_dir = os.path.dirname(os.path.abspath(__file__))

STRING_PREDICTIONS_FILE = os.path.join(
    current_dir, "..", "output", "model", "sorting_times_string_predictions.csv"
)
INT_PREDICTIONS_FILE = os.path.join(
    current_dir, "..", "output", "model", "sorting_times_int_predictions.csv"
)
STRING_TIMES_FILE = os.path.join(
    current_dir, "..", "output", "times", "sorting_times_string.csv"
)
INT_TIMES_FILE = os.path.join(
    current_dir, "..", "output", "times", "sorting_times_int.csv"
)
IMAGE_DIR = os.path.join(current_dir, "..", "output", "images")


class Application(tk.Frame):
    """
    Main application class for sorting algorithm performance analysis.

    This class represents the main application window for analyzing and visualizing the performance of sorting algorithms. It provides a graphical user interface for selecting algorithms, running the sorting program, and fitting prediction models.
    """

    BG_COLOR = "#1E1E1E"
    FONT = ("Cascadia Code", 9)
    ALGORITHMS = [
        "Bubble Sort",
        "Selection Sort",
        "Insertion Sort",
        "Shell Sort",
        "Merge Sort",
        "Quick Sort",
    ]

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("1100x700")
        self.pack()
        self.master.configure(bg=self.BG_COLOR)

        self.graph = self.fig = None

        self.selected_algorithms = []
        self.data_type_algorithm = "-s"
        self.program_execute = False
        self.warning_text = None

        self.compiled_process = False
        self.image_count = 0

        self.model = SGDRegressor()
        self.poly = PolynomialFeatures(degree=2)
        self.scaler = StandardScaler()
        self.model_int_fitted = False
        self.model_string_fitted = False
        self.fit_button_state = "Model Predict"

        self.create_widgets()

    def create_widgets(self):
        """
        Create the user interface widgets.

        Creates the various user interface widgets and elements, including the PanedWindow, buttons, checkbuttons, and text area. Calls other functions to create and configure these widgets.

        Returns:
            None
        """
        self.paned_window()
        self.run_button()
        self.save_button()
        self.fit_model_button()
        self.algorithm_checkbutton()
        self.data_type_slider()
        self.crate_warning_text()

    def paned_window(self):
        """
        Create a PanedWindow for layout.

        Creates a PanedWindow to organize the layout of the application.
        Adds a left frame to the PanedWindow and configures its appearance.

        Returns:
            None
        """
        # Cria o PanedWindow
        self.panedwindow = tk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        self.panedwindow.pack(fill=tk.BOTH, expand=True)

        # Cria o frame da esquerda
        self.left_frame = tk.Frame(
            self.panedwindow,
            background=self.BG_COLOR,
            relief=tk.RAISED,
            borderwidth=1,
            height=500,
        )

        self.panedwindow.add(self.left_frame)
        self.panedwindow.paneconfig(self.left_frame, minsize=150)
        self.panedwindow.configure(
            bg=self.BG_COLOR,
            sashrelief=tk.RAISED,
            showhandle=True,
        )

    def run_button(self):
        """
        Create a 'Run' button.

        Creates a button that allows the user to run the sorting program.
        Trigger the 'compile_and_execute_sorting' function.

        Returns:
            None
        """
        self.run_button = tk.Button(
            self.left_frame,
            text="Run",
            command=self.compile_and_execute_sorting,
            bg="#778899",
            fg="white",
            activebackground="#778899",
            activeforeground="white",
            padx=5,
            pady=5,
            state=tk.NORMAL,
            disabledforeground="white",
            font=self.FONT,
        )
        self.run_button.grid(row=1, column=0, pady=(30, 30), padx=(20, 20), sticky="ew")

    def save_button(self):
        """
        Create a 'Save' button.

        Creates a button that allows the user to save the current graph as an image.
        Trigger the 'save_graph' function.

        Returns:
            None
        """
        self.save_button = tk.Button(
            self.left_frame,
            text="Save",
            command=self.save_graph,
            bg="#BDB76B",
            fg="white",
            activebackground="#BDB76B",
            activeforeground="white",
            padx=5,
            pady=5,
            state=tk.NORMAL,
            font=self.FONT,
        )
        self.save_button.grid(
            row=4, column=0, pady=(30, 15), padx=(20, 20), sticky="ew"
        )

    def fit_model_button(self):
        """
        Creates a button that allows the user to fit or predict a model based on the current button state. It sets the button's appearance, text, and behavior to trigger the 'fit_action' function.

        Returns:
            None
        """
        self.fit_model_button = tk.Button(
            self.left_frame,
            text=self.fit_button_state,
            command=self.fit_action,
            bg="#778899",
            fg="white",
            activebackground="#778899",
            activeforeground="white",
            padx=5,
            pady=5,
            state=tk.NORMAL,
            font=self.FONT,
        )
        self.fit_model_button.grid(
            row=5, column=0, pady=(15, 15), padx=(20, 20), sticky="ew"
        )

    def fit_action(self):
        """
        Handle the 'Fit Model' button action.

        Handles the action of the 'Fit Model' button. Depending on the current button state, it either fits a model with original data or updates the graph with predicted data. It toggles the button text and behavior accordingly.

        Returns:
            None
        """
        if self.fit_button_state == "Model Predict":
            self.fit_button_state = "Original Data"
            self.fit_model_button.configure(text=self.fit_button_state)
            if (self.data_type_algorithm == "-s" and not self.model_string_fitted) or (
                self.data_type_algorithm == "-i" and not self.model_int_fitted
            ):
                self.fit_model()
            else:
                self.update_graph(predict=True)
        else:
            self.fit_button_state = "Model Predict"
            self.fit_model_button.configure(text=self.fit_button_state)
            self.update_graph()

    def crate_warning_text(self):
        """
        Creates a text widget in the left frame to display warning messages and information to the user.

        Returns:
            None
        """
        self.warning_text = tk.Text(
            self.left_frame,
            bg=self.BG_COLOR,
            fg="white",
            height=10,
            width=30,
            autoseparators=True,
            wrap=tk.WORD,
            padx=5,
            pady=5,
            font=self.FONT,
        )
        self.warning_text.grid(row=12, column=0, sticky="nsew", padx=(30, 30))

    def on_select(self, event):
        """
        Handle the selection of algorithms in the listbox.

        Handles the event when the user selects one or more algorithms from the listbox.
        It updates the list of selected algorithms and triggers a graph update depending on the current fit button state.

        Args:
            event: The event that triggered the selection.

        Returns:
            None
        """
        self.selected_algorithms = [
            self.listbox.get(i) for i in self.listbox.curselection()
        ]
        if self.fit_button_state == "Model Predict":
            self.update_graph(predict=False)
        else:
            self.update_graph(predict=True)

    def algorithm_checkbutton(self):
        """
        Create a list of selectable algorithms.

        Creates a list of selectable algorithms as checkable items in the left frame.
        It sets the display attributes for the list and binds a function to handle selections.

        Returns:
            None
        """
        label = tk.Label(
            self.left_frame,
            text="Select the algorithms below: ",
            font=self.FONT,
            padx=5,
            pady=5,
            background=self.BG_COLOR,
            fg="white",
        )
        label.grid(row=6, column=0, pady=(5, 5), padx=(20, 20), sticky="ew")

        self.listbox_frame = tk.Frame(
            self.left_frame,
            background=self.BG_COLOR,
        )
        self.listbox_frame.grid(
            row=8, column=0, sticky="nsew", padx=(10, 10), pady=(10, 30)
        )

        self.listbox = tk.Listbox(
            self.listbox_frame,
            selectmode="multiple",
            background=self.BG_COLOR,
            fg="white",
            highlightthickness=0,
            highlightcolor=self.BG_COLOR,
            highlightbackground=self.BG_COLOR,
            border=1,
            relief=tk.RAISED,
            borderwidth=2,
            font=self.FONT,
            height=7,
        )
        for item in self.ALGORITHMS:
            self.listbox.insert("end", item)

        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

    def compile_sorting(self):
        """
        Compile the sorting program and execute it.

        Compiles the sorting program using the specified compile command and initiates the compilation and execution process.
        It captures the output of the compilation and checks for errors.

        Returns:
            bool: True if compilation is successful, False otherwise.
        """
        # Comando para compilar
        compile_command = "g++ -std=c++17 -I.\include .\src\main.cpp .\src\FileHandler.cpp -o .\output\main"

        # Iniciar o processo de compilação e execução
        compile_process = subprocess.Popen(
            compile_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Mesclar stdout e stderr
            text=True,
            bufsize=1,  # Definir o buffer para linha por linha
            universal_newlines=True,
        )
        compile_process.wait()

        if compile_process.returncode != 0:
            messagebox.showerror(
                "Error",
                "An error occurred during compilation, check the logs!",
            )
            return False
        else:
            print("Compilation completed successfully!")
            self.compiled_process = True
            return True

    def compile_and_execute_sorting(self):
        """
        Compile and execute the sorting program.

        Disables the "Run" and "Fit Model" buttons, compiles the sorting program, and executes it.
        The execution process captures the program's output in real-time, displaying it in the warning text area.
        After execution, it re-enables the buttons and updates the graph with the data from the CSV file.
        If the data type is "-s" or "-i," it updates flags to indicate whether the string or integer model has been fitted.

        Returns:
            None
        """
        self.run_button.configure(state=tk.DISABLED)
        self.fit_model_button.configure(state=tk.DISABLED)

        if not self.compile_sorting():
            return

        execute_command = f".\output\main.exe {self.data_type_algorithm}"

        # Função para ler e exibir a saída em tempo real
        def execute_program():
            with subprocess.Popen(
                execute_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            ) as process:
                while process.poll() is None:
                    for line in process.stdout:
                        self.warning_text.insert(tk.END, line)
                        self.warning_text.see(tk.END)
                        self.left_frame.update_idletasks()
                        ax = self.fig.axes[0]
                        ax.clear()
                        df = self.read_csv_file()
                        self.update_plot(ax, df)
            if self.data_type_algorithm == "-s":
                self.model_string_fitted = False
            else:
                self.model_int_fitted = False
            self.program_execute = True
            self.run_button.configure(state=tk.NORMAL)
            self.fit_model_button.configure(state=tk.NORMAL)
            print("Execution completed successfully!")

        # Iniciar uma thread para ler e exibir a saída em tempo real da compilação
        output_thread = threading.Thread(
            target=execute_program, daemon=True, name="output_thread"
        )
        output_thread.start()
        self.fit_button_state = "Model Predict"
        self.update_graph()

    def toggle_slider(self, event=None):
        """
        Toggle the data type slider and update the graph accordingly.

        Toggles the data type between "String" and "Int" based on the slider position.
        If the fit button state is "Original Data," it updates the graph with predicted data.
        Otherwise, it updates the graph with the original data.

        Args:
            event: Event parameter (default None).

        Returns:
            None
        """
        self.data_type_algorithm = "-i" if self.data_type.get() else "-s"
        if self.fit_button_state == "Original Data":
            self.update_graph(predict=True)
        else:
            self.update_graph()

    def data_type_slider(self):
        """
        Create and configure a data type slider.

        Creates a slider for toggling between "String" and "Int" data types. The slider allows the user to select the data type for analysis.

        Returns:
            None
        """
        self.data_type = tk.BooleanVar()
        slider_frame = tk.Frame(
            self.left_frame,
            background=self.BG_COLOR,
            padx=5,
            pady=5,
        )
        slider_frame.grid(row=3, column=0, sticky="w", padx=(20, 20))
        tk.Label(
            slider_frame,
            text="Data Type:",
            background=self.BG_COLOR,
            fg="white",
            font=self.FONT,
        ).grid(row=2, column=0, sticky="ew", padx=(20, 20))
        # Rótulos para as extremidades do controle deslizante
        tk.Label(
            slider_frame,
            text="String",
            background=self.BG_COLOR,
            fg="white",
            font=self.FONT,
        ).grid(row=3, column=1, sticky="w")
        tk.Label(
            slider_frame,
            text="Int",
            background=self.BG_COLOR,
            fg="white",
            font=self.FONT,
        ).grid(row=3, column=3, sticky="e")
        slider = tk.Scale(
            slider_frame,
            from_=0,
            to=1,
            orient=tk.HORIZONTAL,
            variable=self.data_type,
            command=self.toggle_slider,
            showvalue=0,
            resolution=1,
            sliderlength=30,
            length=80,
            background=self.BG_COLOR,
            fg="white",
            highlightthickness=0,
            troughcolor=self.BG_COLOR,
            activebackground=self.BG_COLOR,
            borderwidth=0,
            relief=tk.FLAT,
            font=self.FONT,
        )
        slider.grid(row=2, column=2, sticky="ew")

    def save_graph(self):
        """
        Save the current graph as an image file.

        Saves the current graph as a PNG image with a filename based on the current image count.
        It also increments the image count for the next save operation.
        Displays a success message if the graph is saved successfully, or an error message if there is no graph to save.

        Returns:
            None
        """
        if self.fig:
            self.fig.savefig(os.path.join(IMAGE_DIR, f"graph_{self.image_count}.png"))
            self.image_count += 1
            messagebox.showinfo("Sucess", "Graph saved successfully!")
        else:
            messagebox.showerror("Error", "There is no graph to be saved!")

    def read_csv_file(self, predict=False):
        """
        Read data from a CSV file.

        Reads data from a CSV file based on the data type and algorithm selection.
        It can read either the original data or predicted data from different CSV files.
        Displays an error message if the file is not found and provides a suggestion to run the algorithms.

        Args:
            predict (bool, optional): Whether to read predicted data. Defaults to False.

        Returns:
            pd.DataFrame or None: The DataFrame with the data or None if the file is not found.
        """
        try:
            if self.data_type_algorithm == "-s":
                return (
                    pd.read_csv(STRING_PREDICTIONS_FILE)
                    if predict
                    else pd.read_csv(STRING_TIMES_FILE)
                )
            else:
                return (
                    pd.read_csv(INT_PREDICTIONS_FILE)
                    if predict
                    else pd.read_csv(INT_TIMES_FILE)
                )
        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                "The CSV file was not found, Use the Run button to run the algorithms.",
            )
            return None

    def create_or_update_figure(self):
        """
        Create or update the graph figure.

        Creates a new graph figure if it doesn't exist or updates the existing figure for data plotting. Sets the background color, axis labels, and tick colors to improve visibility. Returns the axis object for plotting data.

        Returns:
            matplotlib.axes.Axes: The axis for plotting data.
        """
        if not self.graph:
            # Cria o FigureCanvasTkAgg apenas uma vez
            self.fig = Figure(figsize=(7, 6), dpi=100)
            ax = self.fig.add_subplot(111)

            # Define a cor de fundo do gráfico e dos eixos para preto
            ax.set_facecolor(self.BG_COLOR)
            self.fig.patch.set_facecolor(self.BG_COLOR)

            # Define a cor dos ticks e labels para branco
            ax.tick_params(
                colors="white",
                grid_color="white",
                grid_linestyle="--",
                grid_alpha=0.5,
            )
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")

            self.graph = FigureCanvasTkAgg(self.fig, master=self.panedwindow)
            # Adiciona o canvas no PanedWindow
            self.panedwindow.add(self.graph.get_tk_widget())
        else:
            ax = self.fig.axes[0]
            ax.clear()
            self.graph.draw()

        return ax

    def plot_algorithm_data(self, df, ax, method):
        """
        Plot data for a specific sorting method.

        Plots the execution time data for a given sorting method from the provided DataFrame on the given axis (ax).
        It also highlights the point with the maximum execution time and labels it on the graph.

        Args:
            df (pd.DataFrame): The DataFrame containing execution time data.
            ax (matplotlib.axes.Axes): The axis to plot the data on.
            method (str): The sorting method for which data is to be plotted.

        Returns:
            None
        """
        method_df = df[df["Sorting Method"] == method]
        ax.plot(
            method_df["Input Size"],
            method_df["Execution Time"],
            label=method,
        )
        # Encontre o valor máximo de tempo e sua posição no DataFrame
        max_time = method_df["Execution Time"].max()
        max_time_index = method_df["Execution Time"].idxmax()
        ax.plot(
            df.loc[max_time_index, "Input Size"],
            max_time,
            "ro",  # 'ro' indica um marcador vermelho circular
            markersize=4,
            label=f"Max Time: {max_time:.2f} ms",
        )
        # Adicione o valor máximo como texto ao lado do marcador
        ax.annotate(
            f"Max Time: {max_time:.2f} ms",
            xy=(df.loc[max_time_index, "Input Size"], max_time),
            xytext=(-50, 2),  # Deslocamento do texto em relação ao ponto
            textcoords="offset points",
            color="red",
        )
        ax.legend(loc="upper left", borderaxespad=4.0)
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")
        ax.set_xlabel("Vector Size")
        ax.set_ylabel("Execution Time (ms)")
        ax.set_title("Performance of Sorting Algorithms")

    def update_plot(self, ax, df):
        """
        Update the plot with selected sorting algorithms.

        Updates the existing plot with the selected sorting algorithms from the DataFrame.
        If no algorithms are selected, a message is displayed.
        It returns a flag indicating whether the plot was updated.

        Args:
            ax (matplotlib.axes.Axes): The axis to update the plot on.
            df (pd.DataFrame): The DataFrame containing execution time data.

        Returns:
            bool: True if the plot was updated, False otherwise.
        """
        flag = False
        for method in df["Sorting Method"].unique():
            if method in self.selected_algorithms:
                flag = True
                self.plot_algorithm_data(df, ax, method)
        self.graph.draw()
        return flag

    def update_graph(self, predict=False):
        """
        Update the graph with selected data.

        Updates the graph with the selected sorting algorithms' data from a CSV file.
        If no algorithms are selected or if the CSV file does not contain the required data, appropriate messages are displayed.

        Args:
            predict (bool, optional): Whether to predict data. Defaults to False.

        Returns:
            None
        """
        ax = self.create_or_update_figure()

        # Verifica se pelo menos um algoritmo foi selecionado
        if self.selected_algorithms == []:
            ax.clear()
            self.warning_text.insert(tk.END, "\nSelect at least one algorithm!")
            self.warning_text.see(tk.END)
            return

        df = self.read_csv_file(predict)
        if df is None:
            return

        flag = self.update_plot(ax, df)

        if not flag:
            ax.clear()
            self.warning_text.insert(
                tk.END,
                "\nThe CSV file does not contain data for the selected algorithms!",
            )
            self.warning_text.see(tk.END)
            return

    def fit_model(self):
        """
        Fit the model to the data.

        Reads a CSV file, fits a model, and updates the user interface accordingly.
        This method runs the fitting process in a separate thread to avoid freezing the application.

        Returns:
            None
        """
        df = self.read_csv_file()
        if df is None:
            return

        self.fit_model_button.configure(state=tk.DISABLED)
        self.warning_text.insert(
            tk.END,
            "\nFitting the model, this may take a few seconds...",
        )
        self.warning_text.see(tk.END)
        self.left_frame.update_idletasks()
        thrad = threading.Thread(target=self.fit_model_to_data, args=(df,), daemon=True)
        thrad.start()
        self.warning_text.insert(
            tk.END,
            "\nModel fitted successfully!",
        )
        self.warning_text.see(tk.END)
        self.left_frame.update_idletasks()

    def fit_model_to_data(self, df):
        """
        Fit the model to the given data.

        Initializes an empty list to store temporary DataFrames for each sorting method.
        For each unique sorting method in the input data, this method filters the data, transforms it into polynomial features, and fits a model.
        It then predicts execution times and appends the results to the temporary DataFrames. Finally, it concatenates all the temporary DataFrames into a single DataFrame and saves it to a CSV file.

        Args:
            df (pd.DataFrame): The input data as a DataFrame.

        Returns:
            None
        """
        # Inicialize uma lista vazia para armazenar os DataFrames temporários
        dfs_to_concat = []

        # Para cada algoritmo, crie um DataFrame com os dados de entrada e saída
        for method in df["Sorting Method"].unique():
            # Filtrar os dados para o método atual
            data = df[df["Sorting Method"] == method]

            X = data["Input Size"].values.reshape(-1, 1)
            y = data["Execution Time"].values

            # Transformar para características polinomiais
            X_poly = self.poly.fit_transform(X)
            X_poly = self.scaler.fit_transform(X_poly)

            self.model.fit(X_poly, y)

            # Prever os valores y
            y_poly_pred = self.model.predict(X_poly)

            # Adicionar os valores previstos a lista
            dfs_to_concat.append(
                pd.DataFrame(
                    {
                        "Sorting Method": [method] * len(X),
                        "Input Size": X.ravel(),
                        "Execution Time": y_poly_pred,
                    }
                )
            )

        # Concatenar os DataFrames temporários em um único DataFrame
        prediction_df = pd.concat(dfs_to_concat, ignore_index=True)

        # Salvar o DataFrame em um arquivo CSV
        if self.data_type_algorithm == "-s":
            prediction_df.to_csv(
                STRING_PREDICTIONS_FILE,
                index=False,
            )
        else:
            prediction_df.to_csv(
                INT_PREDICTIONS_FILE,
                index=False,
            )
        if self.data_type_algorithm == "-s":
            self.model_string_fitted = True
        else:
            self.model_int_fitted = True
        self.fit_model_button.configure(state=tk.NORMAL)
        self.update_graph(predict=True)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sorting Algorithms")
    app = Application(master=root)
    app.mainloop()
