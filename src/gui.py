import tkinter as tk
from tkinter import messagebox
import subprocess
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import threading, time


class Application(tk.Frame):
    BG_COLOR = "#1E1E1E"
    ALGORITHMS = [
        "Bubble Sort",
        "Insertion Sort",
        "Selection Sort",
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

        self.create_widgets()

    def create_widgets(self):
        self.paned_window()
        self.run_button()
        self.save_button()
        self.algorithm_checkbutton()
        self.data_type_slider()  # Adicione o novo método

    def paned_window(self):
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
        )
        self.run_button.grid(row=1, column=0, pady=(30, 30), padx=(20, 20), sticky="ew")

    def save_button(self):
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
        )
        self.save_button.grid(
            row=4, column=0, pady=(30, 30), padx=(20, 20), sticky="ew"
        )

    def toggle_list(self, event=None):
        if self.listbox.winfo_viewable():
            self.listbox.grid_forget()
        else:
            self.listbox.grid(row=8, column=0, sticky="nsew", padx=(20, 20))
            self.listbox.focus_set()

    def on_select(self, event):
        self.selected_algorithms = [
            self.listbox.get(i) for i in self.listbox.curselection()
        ]
        self.update_graph()

    def algorithm_checkbutton(self):
        label = tk.Label(
            self.left_frame,
            text="Select the algorithms below: ",
            font=("Times New Roman", 10),
            padx=5,
            pady=5,
            background=self.BG_COLOR,
            fg="white",
        )
        label.grid(row=6, column=0, pady=(5, 5), padx=(20, 20), sticky="ew")

        button = tk.Button(
            self.left_frame,
            text="Algorithms",
            command=self.toggle_list,
            bg="#4682B4",
            fg="white",
            activebackground="#4682B4",
            activeforeground="white",
        )
        button.grid(row=7, column=0, pady=(20, 20), padx=(20, 20), sticky="ew")

        self.listbox = tk.Listbox(
            self.left_frame,
            selectmode="multiple",
            background=self.BG_COLOR,
            fg="white",
            highlightthickness=0,
            highlightcolor=self.BG_COLOR,
            highlightbackground=self.BG_COLOR,
            border=1,
            relief=tk.RAISED,
            borderwidth=2,
        )
        for item in self.ALGORITHMS:
            self.listbox.insert("end", item)

        # self.listbox.grid_forget()  # Inicia oculto
        self.listbox.bind("<FocusOut>", self.toggle_list)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

    def compile_and_execute_sorting(self):
        self.run_button.configure(state=tk.DISABLED)

        # Criar uma nova janela para exibir os logs
        self.log_window = tk.Toplevel(self.master)
        self.log_window.geometry("400x300")
        self.log_window.title("Execution Logs")
        self.log_window.configure(bg=self.BG_COLOR)

        self.output_text = tk.Text(self.log_window, bg=self.BG_COLOR, fg="white")
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Comando para compilar
        compile_command = "g++ -std=c++17 -I.\include .\src\main.cpp .\src\FileHandler.cpp -o .\output\main"
        execute_command = f".\output\main.exe {self.data_type_algorithm}"

        # Iniciar o processo de compilação e execução
        compile_process = subprocess.Popen(
            compile_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Mesclar stdout e stderr
            text=True,
            bufsize=1,  # Definir o buffer para linha por linha
            universal_newlines=True,
        )
        compile_process.wait()  # Aguarde o término da compilação

        if compile_process.returncode != 0:
            messagebox.showerror(
                "Erro",
                "Ocorreu um erro durante a compilação, verifique os logs!",
            )
            return

        print("Compilação concluída com sucesso!")

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
                        self.output_text.insert(tk.END, line)
                        self.output_text.see(tk.END)
                        self.log_window.update_idletasks()
                        self.update_graph()
                    for line in process.stderr:
                        self.output_text.insert(tk.END, line)
                        self.output_text.see(tk.END)
                        self.log_window.update_idletasks()
                        self.update_graph()

            self.run_button.configure(state=tk.NORMAL)
            print("Execução concluída com sucesso!")

        # Iniciar uma thread para ler e exibir a saída em tempo real da compilação
        output_thread = threading.Thread(
            target=execute_program, daemon=True, name="output_thread"
        )
        output_thread.start()

    def toggle_slider(self, event=None):
        self.data_type_algorithm = "-i" if self.data_type.get() else "-s"
        if self.selected_algorithms:
            self.update_graph()

    def data_type_slider(self):
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
            font=("Times New Roman", 10),
        ).grid(row=2, column=0, sticky="ew", padx=(20, 20))
        # Rótulos para as extremidades do controle deslizante
        tk.Label(
            slider_frame, text="String", background=self.BG_COLOR, fg="white"
        ).grid(row=3, column=1, sticky="w")
        tk.Label(slider_frame, text="Int", background=self.BG_COLOR, fg="white").grid(
            row=3, column=3, sticky="e"
        )
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
        )
        slider.grid(row=2, column=2, sticky="ew")

    def save_graph(self):
        if self.fig:
            self.fig.savefig(r"output\\sorting_times.png")
            messagebox.showinfo("Sucesso", "Gráfico salvo com sucesso!")
        else:
            messagebox.showerror("Erro", "Não há gráfico para ser salvo!")

    def update_graph(self):
        if self.warning_text:
            self.warning_text.destroy()

        # Verifica se pelo menos um algoritmo foi selecionado
        if self.selected_algorithms == []:
            self.crate_warning_text("Selecione pelo menos um algoritmo!")
            if self.graph:
                self.graph.get_tk_widget().destroy()
            return

        # Lê o arquivo CSV
        try:
            if self.data_type_algorithm == "-s":
                df = pd.read_csv(r"output\sorting_times_string.csv")
            else:
                df = pd.read_csv(r"output\sorting_times_int.csv")
        except FileNotFoundError:
            messagebox.showerror(
                "Erro",
                "O arquivo CSV não foi encontrado, Use o botão Run executar os algoritmos.",
            )
            return

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

        flag = False
        # Cria um gráfico de linhas para cada algoritmo de ordenação
        for method in df["Sorting Method"].unique():
            if method in self.selected_algorithms:
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
                flag = True

        if not flag:
            self.crate_warning_text(
                "O arquivo CSV não contém dados para os algoritmos selecionados!"
            )

        ax.legend(loc="upper left", borderaxespad=4.0)
        ax.set_xlabel("Tamanho do Vetor")
        ax.set_ylabel("Tempo de Execução (ms)")
        ax.set_title("Desempenho dos Algoritmos de Ordenação")

        if self.graph:
            self.graph.get_tk_widget().destroy()  # Destrua o gráfico antigo se ele existir

        self.graph = FigureCanvasTkAgg(self.fig, master=self.panedwindow)
        self.graph.draw()
        # Adiciona o canvas no PanedWindow
        self.panedwindow.add(self.graph.get_tk_widget())

    def crate_warning_text(self, txt: str):
        self.warning_text = tk.Text(
            self.left_frame,
            bg=self.BG_COLOR,
            fg="white",
            height=10,
            width=30,
            autoseparators=True,
            wrap=tk.WORD,
        )
        self.warning_text.grid(row=9, column=0, sticky="nsew", padx=(20, 20))
        self.warning_text.insert(tk.END, txt)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sorting Algorithms")
    app = Application(master=root)
    app.mainloop()
