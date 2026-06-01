# Projeto — Gestão de Categorias

Sistema de árvore mercadológica com painel administrativo e vitrine para o cliente.

## Tecnologias
- **Backend:** Python + Flask + Jinja2
- **Banco de dados:** MySQL via XAMPP
- **Protocolo:** TCP/IP local (127.0.0.1:5000)
- **Frontend:** HTML, CSS e JavaScript

---

## Estrutura do Projeto
```
Projeto.GestãoCategoria/
├── app.py                        # Rotas Flask
├── requirements.txt              # Dependências Python
├── banco/
│   └── GestaoCategoria.sql       # Schema + dados do banco
├── templates/
│   ├── index.html        # Home (vitrine)
│   ├── index-pag2.html           # Página de filtragem
│   └── index-pagAdm.html         # Painel administrativo
└── static/
    ├── css/
    │   ├── sytle.css             # Estilos da home compartilhados
        ├── style-pag2.css        # Estilos da página de busca
        └── style_adm.css         # Estilos do painel admin
    
```

---

## Páginas
| URL | Descrição |
|-----|-----------|
| `/` | Vitrine com carrossel de categorias |
| `/categorias/buscar?q=termo` | Busca e filtragem |
| `/admin/categorias` | Painel administrativo |

---

## Instalação — Linux

### Pré-requisitos
- Python 3
- XAMPP instalado em `/opt/lampp/`

### Passo 1 — Baixar o projeto
**Com Git:**
```bash
git clone https://github.com/seu-usuario/Projeto.GestãoCategoria.git
cd Projeto.GestãoCategorias
```
**Sem Git:** baixe o ZIP pelo GitHub → **Code → Download ZIP** → extraia na pasta desejada

### Passo 2 — Criar ambiente virtual e instalar dependências
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Passo 3 — Importar o banco de dados
```bash
sudo /opt/lampp/lampp startmysql
sudo /opt/lampp/bin/mysql -u root < banco/GestaoCategoria.sql
```
Ou pelo **phpMyAdmin** em `http://localhost/phpmyadmin` → **Importar** → selecionar `banco/GestaoCategoria.sql`

### Passo 4 — Rodar o projeto
```bash
sudo /opt/lampp/lampp startmysql
source venv/bin/activate
python app.py
```

---

## Instalação — Windows

### Pré-requisitos
- [Python 3](https://www.python.org/downloads/) — marcar **"Add Python to PATH"** na instalação
- [XAMPP para Windows](https://www.apachefriends.org/)
- [VSCode](https://code.visualstudio.com/) — recomendado
  - Instalar extensão **Python** da Microsoft (`Ctrl+Shift+X` → pesquisar Python)

### Passo 1 — Baixar o projeto
**Com Git:**
```cmd
git clone https://github.com/seu-usuario/Projeto.GestãoCateogoria.git
cd Projeto.GestãoCategoria
```
**Sem Git:** baixe o ZIP pelo GitHub → **Code → Download ZIP** → extraia em `C:\xampp\htdocs\Projeto.GestãoCategoria

### Passo 2 — Abrir no VSCode
```
File → Open Folder → C:\xampp\htdocs\Projeto.GestãoCategoria
Ctrl+J  (abre o terminal)
```

### Passo 3 — Criar ambiente virtual e instalar dependências
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Passo 4 — Selecionar o interpretador Python
```
Ctrl+Shift+P → Python: Select Interpreter → .\venv\Scripts\python.exe
```

### Passo 5 — Importar o banco de dados
- Abra o **XAMPP Control Panel**
- Clique em **Start** no MySQL
- Acesse `http://localhost/phpmyadmin`
- Clique em **Importar** → selecione `banco\GestaoCategoria.sql`

### Passo 6 — Rodar o projeto
```cmd
:: XAMPP Control Panel → Start MySQL
venv\Scripts\activate
python app.py
```

Acesse: **http://127.0.0.1:5000**

---

## Todo dia para usar — Windows

```
1. XAMPP Control Panel → Start MySQL
2. VSCode → abrir pasta → Ctrl+J
3. venv\Scripts\activate
4. python app.py
5. http://127.0.0.1:5000
```

---

## Exportar o banco (para atualizar o arquivo .sql)

**Linux:**
```bash
cd /opt/lampp/htdocs/Projeto.GestãoCategoria
sudo /opt/lampp/bin/mysqldump -u root GestaoCategoria > banco/GestaoCategoria.sql
```

**Windows:**
```cmd
cd C:\xampp\htdocs\Projeto.GestãoCategoria
C:\xampp\mysql\bin\mysqldump.exe -u root GestaoCategoria > banco\GestaoCategoria.sql
```

> `GestaoCategoria` é o **nome do banco no MySQL**, não o nome da pasta do projeto.

---

## Upload manual para o GitHub (sem Git)

1. Acesse `github.com` e crie um novo repositório
2. **Deixe desmarcado:** Add README e Add .gitignore
3. Clique em **"uploading an existing file"**
4. Arraste os arquivos do projeto
5. **Não subir:** `venv/`, `static/uploads/`, `__pycache__/`
6. Mensagem: `"Projeto Gestão de Categorias - versão inicial"`
7. Clique em **"Commit changes"**

---

## Solução de problemas

### Erro de permissão ao ativar venv no Windows (PowerShell)
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Digite `S` para confirmar, depois ative normalmente.

### venv não encontrado
```bash
python3 -m venv venv   # Linux
python -m venv venv    # Windows
```

### requirements.txt não encontrado
```cmd
pip install flask pymysql werkzeug cryptography
```

### mysql.connector.errors.ProgrammingError (erro 1045)
O MySQL está com senha ou plugin de autenticação incompatível.
Execute no phpMyAdmin `http://localhost/phpmyadmin`:
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';
FLUSH PRIVILEGES;
```

### Coluna imagem não existe
```sql
USE GestaoCategoria;
ALTER TABLE Categoria ADD COLUMN imagem VARCHAR(255) DEFAULT 'default.jpg';
```

### Porta 5000 ocupada
```bash
sudo fuser -k 5000/tcp   # Linux
```
---

## Observações
- O Python precisa ser instalado pelo site `python.org` — a extensão do VSCode **não instala o Python**
- O `venv/` **nunca deve ser enviado** ao GitHub — é recriado com `pip install -r requirements.txt`
- O XAMPP é usado apenas pelo **MySQL** — o servidor web é o próprio Flask
- O projeto usa **PyMySQL** como conector ao banco (não mysql-connector-python)
- Todos os dados ficam salvos **localmente** — nenhuma informação sai da máquina