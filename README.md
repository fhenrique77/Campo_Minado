# 💣 Campo Minado (Minesweeper)

Um projeto completo do clássico jogo **Campo Minado** desenvolvido em Python! O jogo combina **Pygame** para a renderização gráfica da partida e interações no tabuleiro, e **Tkinter** para proporcionar uma interface de usuário moderna com menu de seleção e sistema de placares.

## ✨ Funcionalidades

- **Menu Interativo**: Interface desenvolvida em Tkinter com design em `ttk` Native/Vista, proporcionando um visual familiar e elegante do Windows.
- **Sistema de Usuários e Scoreboard**: Registro de partidas, vitórias e derrotas geridos em um banco de dados **SQLite** local. Seu progresso fica guardado!
- **HUD (Mostrador de Status)**: Cronômetro de tempo real e contador de bandeiras em formato inteligente acoplado à janela principal do tabuleiro.
- **Várias Dificuldades**: Níveis Fácil, Médio, Difícil e Impossível alterando automaticamente a geração procedural do campo minado.
- **Painel Administrativo**: Digite `admin` no usuário para visualizar a tabela de todos os jogadores, editar ou excluir contas.
- **Áudios e Efeitos**: Som de vitória, derrota e trilha sonora de menu dinâmicas.

## 🚀 Como baixar e executar

### Pré-requisitos
- **Python** (Recomendado 3.12 ou compatível) instalado.

### Passos da Instalação

1. Clone o repositório na sua máquina local:
   ```bash
   git clone https://github.com/fhenrique77/Campo_Minado.git
   cd Campo_Minado
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```powershell
   # Windows (PowerShell)
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   *(Caso utilize prompt de comando padrão ou bash, o comando de ativação pode variar de acordo).*

3. Instale as bibliotecas necessárias (\`pygame\` e \`Pillow\`):
   ```bash
   pip install -r Dados_txt/requirements.txt
   ```

4. Inicie o jogo executando o arquivo principal:
   ```bash
   python main.py
   ```

## 🎮 Como Jogar

1. No menu principal, informe o seu nome de usuário. Se você ganhar ou perder, os dados da partida serão salvos na aba "Score".
2. Selecione a dificuldade que mais lhe agradar e regule o volume da música de fundo.
3. Pressione **Iniciar Jogo**. 
4. Quando o mapa for gerado:
   - **Botão Esquerdo do Mouse**: Clica para escavar em uma célula. Tente não explodir nada!
   - **Botão Direito do Mouse**: Coloca ou retira uma bandeira 🚩 provável em cima do ladrilho.

## 🛠️ Bibliotecas & Tecnologias Utilizadas

- **[Python 3](https://www.python.org/)** - Base de toda lógica.
- **[Pygame](https://www.pygame.org/)** - Loop principal de rendering, captura de eventos pelo mouse (cliques) e controle do mixer de som.
- **[Tkinter / ttk](https://docs.python.org/3/library/tkinter.ttk.html)** - Utilizado para o Menu da aplicação.
- **[Pillow](https://pillow.readthedocs.io/)** - Tratamento do painel de fundo (responsividade das texturas de fundo do menu).
- **[SQLite3](https://docs.python.org/3/library/sqlite3.html)** - Banco de dados embutido leve utilizado para manter a consistência dos dados de pontuação (`usuarios.db`).

---
🌟 **Desenvolvido por [Felipe Henrique](https://github.com/fhenrique77)**
