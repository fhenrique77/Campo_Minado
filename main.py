import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

import pygame
from PIL import Image, ImageTk

from game import Game

SUPER_USER = "admin"
MENU_MUSIC = "menu_music.mp3"
MENU_VOLUME_DEFAULT = 35


class Aplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Campo Minado")

        pygame.mixer.init()

        self.conn = sqlite3.connect("usuarios.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.superuser_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Menu")
        self.notebook.add(self.tab2, text="Score")
        self.notebook.add(
            self.superuser_tab,
            text="Super Usuário",
            state="hidden",
        )

        self.music_volume_var = tk.IntVar(value=MENU_VOLUME_DEFAULT)
        self.play_menu_music()
        
        # Inicia a tela com um tamanho padrão para evitar tela muito esmagada e centraliza elementos
        self.geometry("800x600")
        self.minsize(600, 400)
        
        self.bg_image_original = Image.open("campo minado.png")
        self.bg_photo_tab1 = None
        self.bg_photo_tab2 = None

        self.background_label_tab1 = tk.Label(self.tab1)
        self.background_label_tab1.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label_tab1.lower()
        
        self.background_label_tab2 = tk.Label(self.tab2)
        self.background_label_tab2.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label_tab2.lower()

        self.tab1.bind("<Configure>", self.resize_background)
        self.tab2.bind("<Configure>", self.resize_background)

        # Configurar Estilos Modernos
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("vista")
        except tk.TclError:
            pass
        
        self.style.configure("Menu.TFrame", background="#f8f9fa", relief="raised", borderwidth=1)
        self.style.configure("Menu.TLabel", background="#f8f9fa", font=("Segoe UI", 11))
        self.style.configure("Menu.TRadiobutton", background="#f8f9fa", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", background="#f8f9fa", font=("Segoe UI", 16, "bold"))
        self.style.configure("Menu.TButton", font=("Segoe UI", 10, "bold"))

        # --- MENU TAB ---
        self.menu_card = ttk.Frame(self.tab1, style="Menu.TFrame", padding=20)
        self.menu_card.place(relx=0.5, rely=0.5, anchor="center", width=350)

        self.title_label = ttk.Label(self.menu_card, text="Nova Partida", style="Title.TLabel")
        self.title_label.pack(pady=(0, 15))

        self.username_label = ttk.Label(self.menu_card, text="Nome de usuário:", style="Menu.TLabel")
        self.username_label.pack(anchor="w", padx=10)

        self.username_entry = ttk.Entry(self.menu_card, font=("Segoe UI", 11))
        self.username_entry.pack(fill="x", padx=10, pady=(0, 15))

        self.difficulty_label = ttk.Label(self.menu_card, text="Dificuldade:", style="Menu.TLabel")
        self.difficulty_label.pack(anchor="w", padx=10)

        self.difficulty_var = tk.StringVar(value="Fácil")

        diff_frame = ttk.Frame(self.menu_card, style="Menu.TFrame")
        diff_frame.pack(fill="x", padx=10, pady=(0, 15))

        self.difficulty_facil = ttk.Radiobutton(
            diff_frame, text="Fácil", variable=self.difficulty_var, value="Fácil", style="Menu.TRadiobutton"
        )
        self.difficulty_facil.grid(row=0, column=0, sticky="w", padx=5, pady=2)

        self.difficulty_medio = ttk.Radiobutton(
            diff_frame, text="Médio", variable=self.difficulty_var, value="Médio", style="Menu.TRadiobutton"
        )
        self.difficulty_medio.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        self.difficulty_dificil = ttk.Radiobutton(
            diff_frame, text="Difícil", variable=self.difficulty_var, value="Difícil", style="Menu.TRadiobutton"
        )
        self.difficulty_dificil.grid(row=1, column=0, sticky="w", padx=5, pady=2)

        self.difficulty_impossivel = ttk.Radiobutton(
            diff_frame, text="Impossível", variable=self.difficulty_var, value="Impossível", style="Menu.TRadiobutton"
        )
        self.difficulty_impossivel.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        self.volume_label = ttk.Label(self.menu_card, text="Volume da música:", style="Menu.TLabel")
        self.volume_label.pack(anchor="w", padx=10)

        self.volume_scale = ttk.Scale(
            self.menu_card, from_=0, to=100, orient=tk.HORIZONTAL,
            variable=self.music_volume_var, command=self.update_music_volume
        )
        self.volume_scale.pack(fill="x", padx=10, pady=(0, 20))

        self.start_button = ttk.Button(self.menu_card, text="Iniciar Jogo", style="Menu.TButton", command=self.start_game)
        self.start_button.pack(fill="x", padx=10, pady=(0, 10))

        # --- SCORE TAB ---
        self.score_card = ttk.Frame(self.tab2, style="Menu.TFrame", padding=20)
        self.score_card.place(relx=0.5, rely=0.5, anchor="center")

        self.game_label = ttk.Label(self.score_card, text="Placar de Jogadores", style="Title.TLabel")
        self.game_label.pack(pady=(0, 15))

        self.scoreboard_tree = ttk.Treeview(
            self.score_card,
            columns=("username", "partidas", "vitorias", "derrotas"),
            height=8
        )
        self.scoreboard_tree.pack(fill="x", pady=(0, 15))

        self.scoreboard_tree.heading("#0", text="")
        self.scoreboard_tree.heading("username", text="Usuário")
        self.scoreboard_tree.heading("partidas", text="Partidas")
        self.scoreboard_tree.heading("vitorias", text="Vitórias")
        self.scoreboard_tree.heading("derrotas", text="Derrotas")

        self.scoreboard_tree.column("#0", width=0, stretch=tk.NO)
        self.scoreboard_tree.column("username", anchor=tk.W, width=150)
        self.scoreboard_tree.column("partidas", anchor=tk.CENTER, width=70)
        self.scoreboard_tree.column("vitorias", anchor=tk.CENTER, width=70)
        self.scoreboard_tree.column("derrotas", anchor=tk.CENTER, width=70)

        self.update_scoreboard()

        self.change_name_button = ttk.Button(self.score_card, text="Mudar Nome", style="Menu.TButton", command=self.change_name)
        self.change_name_button.pack(fill="x", pady=(0, 5))

        # --- SUPERUSER TAB ---
        self.superuser_card = ttk.Frame(self.superuser_tab, style="Menu.TFrame", padding=20)
        self.superuser_card.place(relx=0.5, rely=0.5, anchor="center")

        self.superuser_label = ttk.Label(self.superuser_card, text="Gerenciamento de Usuários", style="Title.TLabel")
        self.superuser_label.pack(pady=(0, 15))

        self.superuser_tree = ttk.Treeview(
            self.superuser_card,
            columns=("username", "partidas", "vitorias", "derrotas"),
            height=10
        )
        self.superuser_tree.pack(fill="x", pady=(0, 15))

        self.superuser_tree.heading("#0", text="")
        self.superuser_tree.heading("username", text="Usuário")
        self.superuser_tree.heading("partidas", text="Partidas")
        self.superuser_tree.heading("vitorias", text="Vitórias")
        self.superuser_tree.heading("derrotas", text="Derrotas")

        self.superuser_tree.column("#0", width=0, stretch=tk.NO)
        self.superuser_tree.column("username", anchor=tk.W, width=150)
        self.superuser_tree.column("partidas", anchor=tk.CENTER, width=70)
        self.superuser_tree.column("vitorias", anchor=tk.CENTER, width=70)
        self.superuser_tree.column("derrotas", anchor=tk.CENTER, width=70)

        self.superuser_tree.bind("<Double-1>", self.on_double_click)

        self.delete_all_button = ttk.Button(
            self.superuser_card, text="Excluir Todos os Usuários", style="Menu.TButton", command=self.delete_all_users
        )
        self.delete_all_button.pack(fill="x", pady=(0, 5))

    def play_menu_music(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(MENU_MUSIC)
            self.update_music_volume()
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Erro ao carregar ou tocar a música do menu: {e}")

    def update_music_volume(self, value=None):
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(self.music_volume_var.get() / 100)

    def stop_music(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    def resize_background(self, event):
        # Evita redimensionamentos com tamanhos inválidos
        if event.width <= 1 or event.height <= 1:
            return
            
        widget_id = str(event.widget)
        
        # Redimensiona a imagem para a nova resolução do widget (tab) mantendo o fundo
        resized_img = self.bg_image_original.resize((event.width, event.height), Image.Resampling.LANCZOS)
        
        if widget_id == str(self.tab1):
            self.bg_photo_tab1 = ImageTk.PhotoImage(resized_img)
            self.background_label_tab1.config(image=self.bg_photo_tab1)
        elif widget_id == str(self.tab2):
            self.bg_photo_tab2 = ImageTk.PhotoImage(resized_img)
            self.background_label_tab2.config(image=self.bg_photo_tab2)

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                username TEXT PRIMARY KEY,
                partidas INTEGER DEFAULT 0,
                vitorias INTEGER DEFAULT 0,
                derrotas INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def update_scoreboard(self):
        self.scoreboard_tree.delete(*self.scoreboard_tree.get_children())
        self.cursor.execute(
            "SELECT username, partidas, vitorias, derrotas "
            "FROM usuarios ORDER BY vitorias DESC"
        )
        for row in self.cursor.fetchall():
            self.scoreboard_tree.insert(
                "", tk.END, values=(row[0], row[1], row[2], row[3])
            )

    def start_game(self):
        username = self.username_entry.get().strip()

        self.stop_music()

        if username == SUPER_USER:
            self.admin_panel()
            return

        if not username:
            messagebox.showerror(
                "Erro", "Por favor, insira um nome de usuário."
            )
            return

        difficulty = self.difficulty_var.get()

        if difficulty == "Fácil":
            size = (10, 10)
            prob = 0.15
        elif difficulty == "Médio":
            size = (20, 20)
            prob = 0.25
        elif difficulty == "Difícil":
            size = (30, 30)
            prob = 0.55
        elif difficulty == "Impossível":
            size = (40, 40)
            prob = 0.85

        self.cursor.execute(
            "SELECT * FROM usuarios WHERE username = ?", (username,)
        )
        user = self.cursor.fetchone()

        if user is None:
            self.cursor.execute(
                "INSERT INTO usuarios "
                "(username, partidas, vitorias, derrotas) "
                "VALUES (?, ?, ?, ?)",
                (username, 0, 0, 0),
            )
            self.conn.commit()

        self.cursor.execute(
            "UPDATE usuarios SET partidas = partidas + 1 WHERE username = ?",
            (username,),
        )
        self.conn.commit()

        pygame.display.set_caption("Campo Minado")

        g = Game(size, prob)
        g.run()
        
        # Voltar a tocar a música do menu após a partida
        self.play_menu_music()

        if g.board.getWon():
            self.cursor.execute(
                "UPDATE usuarios SET vitorias = vitorias + 1 WHERE username = ?",
                (username,),
            )
        elif g.board.getLost():
            self.cursor.execute(
                "UPDATE usuarios SET derrotas = derrotas + 1 WHERE username = ?",
                (username,),
            )
        self.conn.commit()
        self.update_scoreboard()

    def admin_panel(self):
        self.notebook.tab(self.superuser_tab, state="normal")
        self.notebook.select(self.superuser_tab)
        self.update_superuser_tree()

    def update_superuser_tree(self):
        self.superuser_tree.delete(*self.superuser_tree.get_children())
        self.cursor.execute(
            "SELECT username, partidas, vitorias, derrotas FROM usuarios"
        )
        for row in self.cursor.fetchall():
            self.superuser_tree.insert(
                "", tk.END, values=(row[0], row[1], row[2], row[3])
            )

    def on_double_click(self, event):
        item = self.superuser_tree.selection()[0]
        column = self.superuser_tree.identify_column(event.x)
        values = self.superuser_tree.item(item, "values")

        if column == "#1":
            self.edit_cell(item, column, "username", values[0], values[0])
        elif column == "#2":
            self.edit_cell(item, column, "partidas", values[0], values[1])
        elif column == "#3":
            self.edit_cell(item, column, "vitorias", values[0], values[2])
        elif column == "#4":
            self.edit_cell(item, column, "derrotas", values[0], values[3])

    def edit_cell(self, item, column, db_column, username, old_value):
        edit_window = tk.Toplevel(self)
        edit_window.title(f"Editar {db_column}")

        tk.Label(edit_window, text=f"Editar {db_column} de {username}:").pack()

        new_value_entry = tk.Entry(edit_window)
        new_value_entry.insert(0, old_value)
        new_value_entry.pack()

        def save_new_value():
            new_value = new_value_entry.get()

            if db_column == "username":
                self.cursor.execute(
                    "SELECT username FROM usuarios WHERE username = ?",
                    (new_value,),
                )
                if self.cursor.fetchone() is not None:
                    messagebox.showerror(
                        "Erro", "Esse nome de usuário já existe."
                    )
                    return

                current_values = list(self.superuser_tree.item(item, "values"))
                current_values[0] = new_value
                self.superuser_tree.item(item, values=current_values)

                self.cursor.execute(
                    "UPDATE usuarios SET username = ? WHERE username = ?",
                    (new_value, username),
                )
            else:
                current_values = list(self.superuser_tree.item(item, "values"))
                if column == "#2":
                    current_values[1] = new_value
                elif column == "#3":
                    current_values[2] = new_value
                elif column == "#4":
                    current_values[3] = new_value
                self.superuser_tree.item(item, values=current_values)

                self.cursor.execute(
                    f"UPDATE usuarios SET {db_column} = ? WHERE username = ?",
                    (new_value, username),
                )

            self.conn.commit()

            messagebox.showinfo(
                "Sucesso", f"{db_column} atualizado para {new_value}"
            )
            edit_window.destroy()
            self.show_restart_message()

        tk.Button(edit_window, text="Salvar", command=save_new_value).pack()

    def show_restart_message(self):
        messagebox.showinfo(
            "Atenção", "Reinicie o jogo para atualizar os dados."
        )

    def delete_all_users(self):
        if messagebox.askyesno(
            "Confirmação",
            "Tem certeza de que deseja excluir todos os usuários?",
        ):
            self.cursor.execute("DELETE FROM usuarios")
            self.conn.commit()
            self.update_superuser_tree()
            self.update_scoreboard()
            messagebox.showinfo(
                "Sucesso", "Todos os usuários foram excluídos com sucesso."
            )

    def change_name(self):
        selected = self.scoreboard_tree.selection()
        if not selected:
            messagebox.showerror(
                "Erro", "Selecione um usuário para mudar o nome."
            )
            return

        item = selected[0]
        current_values = self.scoreboard_tree.item(item, "values")
        current_username = current_values[0]

        change_window = tk.Toplevel(self)
        change_window.title(f"Mudar Nome de {current_username}")

        tk.Label(change_window, text="Novo Nome de Usuário:").pack()

        new_name_entry = tk.Entry(change_window)
        new_name_entry.pack()

        def save_new_name():
            new_name = new_name_entry.get().strip()

            if not new_name:
                messagebox.showerror(
                    "Erro", "O nome de usuário não pode ser vazio."
                )
                return

            self.cursor.execute(
                "SELECT username FROM usuarios WHERE username = ?",
                (new_name,),
            )
            if self.cursor.fetchone() is not None:
                messagebox.showerror("Erro", "Esse nome de usuário já existe.")
                return

            current_values = list(self.scoreboard_tree.item(item, "values"))
            current_values[0] = new_name

            self.scoreboard_tree.item(item, values=tuple(current_values))

            self.cursor.execute(
                "UPDATE usuarios SET username = ? WHERE username = ?",
                (new_name, current_username),
            )
            self.conn.commit()

            messagebox.showinfo(
                "Sucesso", "Nome de usuário alterado com sucesso."
            )
            change_window.destroy()

        tk.Button(change_window, text="Salvar", command=save_new_name).pack()


if __name__ == "__main__":
    app = Aplicacao()
    app.mainloop()
