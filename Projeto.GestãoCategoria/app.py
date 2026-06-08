import os
import pymysql
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
app = Flask(__name__)
# CONFIGURAÇÃO DE UPLOAD DE IMAGENS
UPLOAD_FOLDER = os.path.join('static', 'uploads', 'categorias')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# CONFIGURAÇÃO DO BANCO DE DADOS
DB_CONFIG = {
    "host":"localhost",
    "user":"root",
    "password": "",
    "database":"GestaoCategoria"
}

def conectar_BD():
    return pymysql.connect(
        host = DB_CONFIG['host'],
        user = DB_CONFIG['user'],
        password = DB_CONFIG['password'],
        database = DB_CONFIG['database'],
        cursorclass = pymysql.cursors.Cursor  # retorna tuplas como antes
    )

def buscar_todas_categorias():
    conexao = conectar_BD()
    cursor  = conexao.cursor()
    cursor.execute("""
        SELECT idCategoria, nome, descricao, idCategoria_pai, imagem
          FROM Categoria
         ORDER BY idCategoria_pai IS NOT NULL, nome
    """)
    categorias = cursor.fetchall()
    cursor.close()
    conexao.close()
    return categorias

# Página Inicial (Home)
@app.route('/')
def index():
    conexao = conectar_BD()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT idCategoria, nome, descricao,idCategoria_pai, imagem FROM Categoria"
    )
    categorias_do_banco = cursor.fetchall()
    cursor.close()
    conexao.close()   
    return render_template('index.html', todas_categorias=categorias_do_banco)

# Página de Pesquisa / Filtragem (Cliente)
@app.route('/categorias/buscar')
def buscar_categoria():
    termo = request.args.get('q', '').strip()
    tipo = request.args.get('tipo', 'todas')

    conexao = conectar_BD()
    cursor = conexao.cursor()

    # LÓGICA DE RESULTADOS POR TIPO DE FILTRO
    if tipo == 'principais':
        # Mostra categorias PAI diretamente relacionadas ao termo:
        # 1- Pais cujo nome bate com o termo  OU
        # 2- Pais que possuem filhas cujo nome bate com o termo
        # Ex: buscar "mochila de estudante" (filha de Escolar)
        # retorna "Escolar" (o pai)
        if termo:
            sql = """
                SELECT DISTINCT p.idCategoria, p.nome, p.descricao,
                                p.idCategoria_pai, p.imagem
                  FROM Categoria p
                 WHERE p.idCategoria_pai IS NULL
                   AND (
                         p.nome LIKE %s
                         OR p.idCategoria IN (
                             SELECT idCategoria_pai
                               FROM Categoria
                              WHERE nome LIKE %s
                                AND idCategoria_pai IS NOT NULL
                         )
                       )
            """
            cursor.execute(sql, (f'%{termo}%', f'%{termo}%'))
        else:
            cursor.execute("""
                SELECT idCategoria, nome, descricao, idCategoria_pai, imagem
                  FROM Categoria
                 WHERE idCategoria_pai IS NULL
                 ORDER BY nome
            """)

    elif tipo == 'sub':
        #Mostra subcategorias do PAI pesquisado (via Explorar)
        #Filhas diretas da categoria cujo nome bate com o termo  OU
        #Subcategorias cujo nome bate com o termo
        if termo:
            sql = """
                SELECT idCategoria, nome, descricao, idCategoria_pai, imagem
                  FROM Categoria
                 WHERE idCategoria_pai IS NOT NULL
                   AND (
                         nome LIKE %s
                         OR idCategoria_pai IN (
                             SELECT idCategoria
                               FROM Categoria
                              WHERE nome LIKE %s
                                AND idCategoria_pai IS NULL
                         )
                       )
                 ORDER BY nome
            """
            cursor.execute(sql, (f'%{termo}%', f'%{termo}%'))
        else:
            cursor.execute("""
                SELECT idCategoria, nome, descricao, idCategoria_pai, imagem
                  FROM Categoria
                 WHERE idCategoria_pai IS NOT NULL
                 ORDER BY nome
            """)

    else:
        #Busca direta pelo nome
        if termo:
            cursor.execute("""
                SELECT idCategoria, nome, descricao, idCategoria_pai, imagem
                  FROM Categoria
                 WHERE nome LIKE %s
                 ORDER BY idCategoria_pai IS NOT NULL, nome
            """, (f'%{termo}%',))
        else:
            cursor.execute("""
                SELECT idCategoria, nome, descricao, idCategoria_pai, imagem
                  FROM Categoria
                 ORDER BY idCategoria_pai IS NOT NULL, nome
            """)

    resultados = cursor.fetchall()

    # SUBCATEGORIAS PARA O PAINEL LATERAL (sempre visíveis)
    # Mostra filhas do pai pesquisado; se não houver, mostra todas.
    if termo:
        cursor.execute("""
            SELECT f.idCategoria, f.nome, f.descricao,
                   f.idCategoria_pai, f.imagem, p.nome AS nome_pai
              FROM Categoria f
              JOIN Categoria p ON f.idCategoria_pai = p.idCategoria
             WHERE p.nome LIKE %s
             ORDER BY f.nome
        """, (f'%{termo}%',))
        subcategorias_filtro = cursor.fetchall()
        # Se nenhuma filha do pai foi encontrada, busca o pai da subcategoria pesquisada
        if not subcategorias_filtro:
            cursor.execute("""
                SELECT f.idCategoria, f.nome, f.descricao,
                       f.idCategoria_pai, f.imagem, p.nome AS nome_pai
                  FROM Categoria f
                  JOIN Categoria p ON f.idCategoria_pai = p.idCategoria
                 WHERE f.nome LIKE %s
                 ORDER BY f.nome
            """, (f'%{termo}%',))
            subcategorias_filtro = cursor.fetchall()
    else:
        cursor.execute("""
            SELECT f.idCategoria, f.nome, f.descricao,
                   f.idCategoria_pai, f.imagem, p.nome AS nome_pai
              FROM Categoria f
              JOIN Categoria p ON f.idCategoria_pai = p.idCategoria
             ORDER BY p.nome, f.nome
        """)
        subcategorias_filtro = cursor.fetchall()

    cursor.close()
    conexao.close()

    todas = buscar_todas_categorias()

    return render_template('index-pag2.html',
                           resultados=resultados,
                           termo_busca=termo,
                           tipo_filtro=tipo,
                           todas_categorias=todas,
                           subcategorias_filtro=subcategorias_filtro)


#Painel Admin
@app.route('/admin/categorias')
def exibir_painel():
    conexao = conectar_BD()
    cursor  = conexao.cursor()
    cursor.execute(
        "SELECT idCategoria, nome, descricao, idCategoria_pai, imagem FROM Categoria"
    )
    lista_categorias = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template('index-pagAdm.html', categorias=lista_categorias)

#Incluir categoria (Admin) — COM UPLOAD DE IMAGEM
@app.route('/admin/categorias/cadastrar', methods=['POST'])
def cadastrar_categoria():
    nome      = request.form.get("nome")
    descricao = request.form.get("descricao")
    id_pai    = request.form.get("idPai") or None
    
    # 1. TRATAMENTO DO UPLOAD DA IMAGEM (DIRETO E SEM FILTROS)
    arquivo_imagem = request.files.get('imagem')
    nome_imagem    = None  # Padrão inicial no banco
    
    # Se o usuário enviou um arquivo e ele tem um nome
    if arquivo_imagem and arquivo_imagem.filename != '':
        nome_seguro = secure_filename(arquivo_imagem.filename)
        prefixo_categoria = secure_filename(nome)
        nome_imagem = f"{prefixo_categoria}_{nome_seguro}"
        
        # Garante a criação da pasta static/uploads/categorias/
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Salva o arquivo físico (.jpeg, .png, etc.)
        arquivo_imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_imagem))
        
    # 2. OPERAÇÃO NO BANCO DE DADOS (PyMySQL)
    conexao = conectar_BD()
    if not conexao:
        return "Erro ao conectar ao banco de dados.", 500
        
    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Categoria (nome, descricao, idCategoria_pai, imagem) VALUES (%s, %s, %s, %s)",
                (nome, descricao, id_pai, nome_imagem)
            )
        conexao.commit()
    except Exception as e:
        conexao.rollback()
        print(f"❌ Erro ao cadastrar no banco: {e}")
        return f"Erro interno: {e}", 500
    finally:
        conexao.close()
        
    return redirect(url_for('exibir_painel'))
#Editar categoria (Adm)
@app.route('/admin/categorias/editar', methods=['POST'])
def editar_categoria():
    id_categoria = request.form.get("idCategoria")
    nome = request.form.get("nome")
    descricao = request.form.get("descricao")
    id_pai= request.form.get("idPai") or None
    conexao = conectar_BD()
    cursor  = conexao.cursor()
    cursor.execute("""
        UPDATE Categoria
           SET nome = %s,
               descricao = %s,
               idCategoria_pai = %s
         WHERE idCategoria = %s
    """, (nome, descricao, id_pai, id_categoria))
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect(url_for('exibir_painel'))
#Excluir categoria (Adm)
@app.route('/admin/categorias/excluir/<int:id_categoria>')
def excluir_categoria(id_categoria):
    conexao = conectar_BD()
    cursor  = conexao.cursor()
    cursor.execute(
        "DELETE FROM Categoria WHERE idCategoria = %s", (id_categoria,)
    )
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect(url_for('exibir_painel'))

#INICIALIZAÇÃO
if __name__ == '__main__':
    app.run(debug=True)
