import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import pygame
from game import Game

SUPER_USER = "admin"  # Nome do super usuário
MENU_MUSIC = 'menu_music.mp3'  # Arquivo de música para o menu e score


class Aplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Campo Minado")

        # Inicializar Pygame mixer para tocar música
        pygame.mixer.init()

        # Conexão com o banco de dados
        self.conn = sqlite3.connect("usuarios.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Crie um notebook com três guias
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.superuser_tab = ttk.Frame(self.notebook)  # Aba do super usuário

        self.notebook.add(self.tab1, text="Menu")
        self.notebook.add(self.tab2, text="Score")
        self.notebook.add(self.superuser_tab, text="Super Usuário",
                          state="hidden")  # Aba oculta inicialmente

        # Reproduzir música ao entrar no Menu
        self.play_menu_music()

        # Definir função para carregar a imagem após a janela estar completamente renderizada
        self.after(100, self.load_background_image)

        # Widgets do menu (tab1) centralizados
        self.username_label = tk.Label(
            self.tab1, text="Nome de usuário:", bg="white")
        self.username_label.place(relx=0.5, rely=0.35, anchor="center")

        self.username_entry = tk.Entry(self.tab1)
        self.username_entry.place(
            relx=0.5, rely=0.4, anchor="center", width=200)

        self.difficulty_label = tk.Label(
            self.tab1, text="Dificuldade:", bg="white")
        self.difficulty_label.place(relx=0.5, rely=0.45, anchor="center")

        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("Fácil")

        self.difficulty_facil = tk.Radiobutton(
            self.tab1, text="Fácil", variable=self.difficulty_var, value="Fácil", bg="white")
        self.difficulty_facil.place(relx=0.5, rely=0.5, anchor="center")

        self.difficulty_medio = tk.Radiobutton(
            self.tab1, text="Médio", variable=self.difficulty_var, value="Médio", bg="white")
        self.difficulty_medio.place(relx=0.5, rely=0.55, anchor="center")

        self.difficulty_dificil = tk.Radiobutton(
            self.tab1, text="Difícil", variable=self.difficulty_var, value="Difícil", bg="white")
        self.difficulty_dificil.place(relx=0.5, rely=0.6, anchor="center")

        self.difficulty_impossivel = tk.Radiobutton(
            self.tab1, text="Impossível", variable=self.difficulty_var, value="Impossível", bg="white")
        self.difficulty_impossivel.place(relx=0.5, rely=0.65, anchor="center")

        self.start_button = tk.Button(
            self.tab1, text="Iniciar Jogo", command=self.start_game)
        self.start_button.place(relx=0.5, rely=0.75, anchor="center")

        # Widgets da aba "Score" (tab2) centralizados
        self.game_label = tk.Label(self.tab2, text="SCORE", bg="white")
        self.game_label.place(relx=0.5, rely=0.1, anchor="center")

        # Tabela de pontuação
        self.scoreboard_tree = ttk.Treeview(self.tab2, columns=(
            "username", "partidas", "vitorias", "derrotas"))
        self.scoreboard_tree.place(
            relx=0.5, rely=0.5, anchor="center", width=500)

        self.scoreboard_tree.heading("#0", text="")
        self.scoreboard_tree.heading("username", text="Usuário")
        self.scoreboard_tree.heading("partidas", text="Partidas")
        self.scoreboard_tree.heading("vitorias", text="Vitórias")
        self.scoreboard_tree.heading("derrotas", text="Derrotas")

        self.scoreboard_tree.column("#0", width=0, stretch=tk.NO)
        self.scoreboard_tree.column("username", anchor=tk.W, width=150)
        self.scoreboard_tree.column("partidas", anchor=tk.E, width=50)
        self.scoreboard_tree.column("vitorias", anchor=tk.E, width=50)
        self.scoreboard_tree.column("derrotas", anchor=tk.E, width=50)

        self.update_scoreboard()

        # Adicionando botão de "Mudar Nome" na aba de Score
        self.change_name_button = tk.Button(
            self.tab2, text="Mudar Nome", command=self.change_name)
        self.change_name_button.place(relx=0.5, rely=0.85, anchor="center")

        # Widgets da aba "Super Usuário"
        self.superuser_label = tk.Label(
            self.superuser_tab, text="Gerenciamento de Usuários", bg="white")
        self.superuser_label.place(relx=0.5, rely=0.1, anchor="center")

        self.superuser_tree = ttk.Treeview(self.superuser_tab, columns=(
            "username", "partidas", "vitorias", "derrotas"))
        self.superuser_tree.place(
            relx=0.5, rely=0.5, anchor="center", width=500)

        self.superuser_tree.heading("#0", text="")
        self.superuser_tree.heading("username", text="Usuário")
        self.superuser_tree.heading("partidas", text="Partidas")
        self.superuser_tree.heading("vitorias", text="Vitórias")
        self.superuser_tree.heading("derrotas", text="Derrotas")

        self.superuser_tree.column("#0", width=0, stretch=tk.NO)
        self.superuser_tree.column("username", anchor=tk.W, width=150)
        self.superuser_tree.column("partidas", anchor=tk.E, width=50)
        self.superuser_tree.column("vitorias", anchor=tk.E, width=50)
        self.superuser_tree.column("derrotas", anchor=tk.E, width=50)

        # Adicionar evento de clique para edição
        self.superuser_tree.bind("<Double-1>", self.on_double_click)

        # Adicionar botão para excluir todos os usuários
        self.delete_all_button = tk.Button(
            self.superuser_tab, text="Excluir Todos os Usuários", command=self.delete_all_users)
        self.delete_all_button.place(relx=0.5, rely=0.85, anchor="center")

    def play_menu_music(self):
        """Função para tocar a música do menu e score"""
        try:
            pygame.mixer.music.load(MENU_MUSIC)  # Carregar música
            pygame.mixer.music.play(-1)  # Tocar em loop infinito
        except pygame.error as e:
            print(f"Erro ao carregar ou tocar a música do menu: {e}")

    def stop_music(self):
        """Função para parar a música"""
        if pygame.mixer.get_init():  # Verifica se o mixer foi inicializado
            pygame.mixer.music.stop()

    def load_background_image(self):
        width_tab1 = self.tab1.winfo_width()
        height_tab1 = self.tab1.winfo_height()

        width_tab2 = self.tab2.winfo_width()
        height_tab2 = self.tab2.winfo_height()

        if width_tab1 == 1 or height_tab1 == 1 or width_tab2 == 1 or height_tab2 == 1:
            self.after(100, self.load_background_image)
            return

        try:
            self.background_image_tab1 = Image.open("campo minado.png")
            self.background_image_tab1 = self.background_image_tab1.resize(
                (width_tab1, height_tab1), Image.Resampling.LANCZOS)
            self.background_image_tab1 = ImageTk.PhotoImage(
                self.background_image_tab1)

            self.background_label_tab1 = tk.Label(
                self.tab1, image=self.background_image_tab1)
            self.background_label_tab1.place(relwidth=1, relheight=1)
            self.background_label_tab1.lower()
        except Exception as e:
            print(f"Erro ao carregar a imagem da tab1: {e}")
            self.background_label_tab1 = tk.Label(
                self.tab1, text="Erro ao carregar a imagem de fundo")
            self.background_label_tab1.place(relwidth=1, relheight=1)

        try:
            self.background_image_tab2 = Image.open("campo minado.png")
            self.background_image_tab2 = self.background_image_tab2.resize(
                (width_tab2, height_tab2), Image.Resampling.LANCZOS)
            self.background_image_tab2 = ImageTk.PhotoImage(
                self.background_image_tab2)

            self.background_label_tab2 = tk.Label(
                self.tab2, image=self.background_image_tab2)
            self.background_label_tab2.place(relwidth=1, relheight=1)
            self.background_label_tab2.lower()
        except Exception as e:
            print(f"Erro ao carregar a imagem da tab2: {e}")
            self.background_label_tab2 = tk.Label(
                self.tab2, text="Erro ao carregar a imagem de fundo")
            self.background_label_tab2.place(relwidth=1, relheight=1)

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
            "SELECT username, partidas, vitorias, derrotas FROM usuarios ORDER BY vitorias DESC")
        for row in self.cursor.fetchall():
            self.scoreboard_tree.insert(
                "", tk.END, values=(row[0], row[1], row[2], row[3]))

    def start_game(self):
        username = self.username_entry.get().strip()

        # Parar a música ao iniciar o jogo
        self.stop_music()

        # Verificar se o super usuário foi digitado
        if username == SUPER_USER:
            self.admin_panel()  # Chama a função correta para o super usuário
            return

        if not username:
            messagebox.showerror(
                "Erro", "Por favor, insira um nome de usuário.")
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

        # Verificar se o usuário existe no banco de dados
        self.cursor.execute(
            "SELECT * FROM usuarios WHERE username = ?", (username,))
        user = self.cursor.fetchone()

        if user is None:
            # Se o usuário não existir, inseri-lo no banco de dados com 0 partidas, 0 vitórias e 0 derrotas
            self.cursor.execute(
                "INSERT INTO usuarios (username, partidas, vitorias, derrotas) VALUES (?, ?, ?, ?)", (username, 0, 0, 0))
            self.conn.commit()

        # Atualizar o número de partidas do usuário
        self.cursor.execute(
            "UPDATE usuarios SET partidas = partidas + 1 WHERE username = ?", (username,))
        self.conn.commit()

        # Garantir que o Pygame não seja reiniciado desnecessariamente
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Campo Minado')

        g = Game(size, prob)
        g.run()  # Executa o jogo

        # Verifica se o jogador venceu ou perdeu
        if g.board.getWon():
            self.cursor.execute(
                "UPDATE usuarios SET vitorias = vitorias + 1 WHERE username = ?", (username,))
        elif g.board.getLost():
            self.cursor.execute(
                "UPDATE usuarios SET derrotas = derrotas + 1 WHERE username = ?", (username,))
        self.conn.commit()
        self.update_scoreboard()

    def admin_panel(self):
        """Função chamada quando o super usuário acessa o painel administrativo"""
        self.notebook.tab(self.superuser_tab,
                          state="normal")  # Torna a aba "Super Usuário" visível
        # Seleciona a aba de super usuário
        self.notebook.select(self.superuser_tab)
        # Atualiza a tabela de usuários para o super usuário editar
        self.update_superuser_tree()

    def update_superuser_tree(self):
        self.superuser_tree.delete(*self.superuser_tree.get_children())
        self.cursor.execute(
            "SELECT username, partidas, vitorias, derrotas FROM usuarios")
        for row in self.cursor.fetchall():
            self.superuser_tree.insert(
                "", tk.END, values=(row[0], row[1], row[2], row[3]))

    def on_double_click(self, event):
        """Função para permitir edição direta nas células do Treeview"""
        item = self.superuser_tree.selection()[0]
        column = self.superuser_tree.identify_column(
            event.x)  # Coluna que foi clicada

        # Pega o item selecionado e a coluna correspondente
        values = self.superuser_tree.item(item, "values")

        # Determine qual coluna foi clicada (nome de usuário, partidas, vitórias ou derrotas)
        if column == "#1":  # Nome de Usuário
            self.edit_cell(item, column, "username", values[0], values[0])
        elif column == "#2":  # Partidas
            self.edit_cell(item, column, "partidas", values[0], values[1])
        elif column == "#3":  # Vitórias
            self.edit_cell(item, column, "vitorias", values[0], values[2])
        elif column == "#4":  # Derrotas
            self.edit_cell(item, column, "derrotas", values[0], values[3])

    def edit_cell(self, item, column, db_column, username, old_value):
        """Abre uma Entry para editar a célula selecionada"""
        edit_window = tk.Toplevel(self)
        edit_window.title(f"Editar {db_column}")

        tk.Label(edit_window, text=f"Editar {db_column} de {username}:").pack()

        new_value_entry = tk.Entry(edit_window)
        new_value_entry.insert(0, old_value)
        new_value_entry.pack()

        def save_new_value():
            new_value = new_value_entry.get()

            # Se o super usuário estiver editando o nome do usuário
            if db_column == "username":
                # Verifica se o nome já existe no banco de dados
                self.cursor.execute(
                    "SELECT username FROM usuarios WHERE username = ?", (new_value,))
                if self.cursor.fetchone() is not None:
                    messagebox.showerror(
                        "Erro", "Esse nome de usuário já existe.")
                    return

                # Atualiza o valor no Treeview
                current_values = list(self.superuser_tree.item(item, "values"))
                current_values[0] = new_value
                self.superuser_tree.item(item, values=current_values)

                # Atualiza o banco de dados
                self.cursor.execute(
                    "UPDATE usuarios SET username = ? WHERE username = ?", (new_value, username))
            else:
                # Atualiza o valor no Treeview
                current_values = list(self.superuser_tree.item(item, "values"))
                if column == "#2":  # Partidas
                    current_values[1] = new_value
                elif column == "#3":  # Vitórias
                    current_values[2] = new_value
                elif column == "#4":  # Derrotas
                    current_values[3] = new_value
                self.superuser_tree.item(item, values=current_values)

                # Atualiza o banco de dados
                self.cursor.execute(
                    f"UPDATE usuarios SET {db_column} = ? WHERE username = ?", (new_value, username))

            self.conn.commit()

            messagebox.showinfo(
                "Sucesso", f"{db_column} atualizado para {new_value}")
            edit_window.destroy()

            # Exibe mensagem solicitando reiniciar o jogo
            self.show_restart_message()

        tk.Button(edit_window, text="Salvar", command=save_new_value).pack()

    def show_restart_message(self):
        """Exibe uma mensagem solicitando reiniciar o jogo"""
        messagebox.showinfo(
            "Atenção", "Reinicie o jogo para atualizar os dados.")

    def delete_all_users(self):
        """Função para deletar todos os usuários do banco de dados"""
        if messagebox.askyesno("Confirmação", "Tem certeza de que deseja excluir todos os usuários?"):
            self.cursor.execute("DELETE FROM usuarios")
            self.conn.commit()
            self.update_superuser_tree()
            self.update_scoreboard()
            messagebox.showinfo(
                "Sucesso", "Todos os usuários foram excluídos com sucesso.")

    def change_name(self):
        """Função para permitir que o usuário mude seu nome na aba de Score"""
        # Verifica se um item está selecionado
        selected = self.scoreboard_tree.selection()
        if not selected:
            messagebox.showerror(
                "Erro", "Selecione um usuário para mudar o nome.")
            return

        item = self.scoreboard_tree.selection()[0]
        current_values = self.scoreboard_tree.item(item, "values")
        current_username = current_values[0]

        change_window = tk.Toplevel(self)
        change_window.title(f"Mudar Nome de {current_username}")

        tk.Label(change_window, text="Novo Nome de Usuário:").pack()

        new_name_entry = tk.Entry(change_window)
        new_name_entry.pack()

        def save_new_name():
            # Extrai o novo nome digitado
            new_name = new_name_entry.get().strip()

            # Validações
            if not new_name:
                messagebox.showerror(
                    "Erro", "O nome de usuário não pode ser vazio.")
                return

            # Verifica se o novo nome já existe no banco de dados
            self.cursor.execute(
                "SELECT username FROM usuarios WHERE username = ?", (new_name,))
            if self.cursor.fetchone() is not None:
                messagebox.showerror("Erro", "Esse nome de usuário já existe.")
                return

            # Converte o tuple em lista para permitir modificações
            current_values = list(self.scoreboard_tree.item(item, "values"))
            current_values[0] = new_name  # Atualiza o nome de usuário na lista

            # Atualiza o nome no Treeview
            self.scoreboard_tree.item(item, values=tuple(
                current_values))  # Converte de volta para tuple

            # Atualiza o banco de dados
            self.cursor.execute(
                "UPDATE usuarios SET username = ? WHERE username = ?", (new_name, current_username))
            self.conn.commit()

            messagebox.showinfo(
                "Sucesso", "Nome de usuário alterado com sucesso.")
            change_window.destroy()

        tk.Button(change_window, text="Salvar", command=save_new_name).pack()


if __name__ == "__main__":
    app = Aplicacao()
    app.mainloop()
