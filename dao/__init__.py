import requests
import psycopg2

def conectarDB():
    return conectar_localBD()

def conectar_localBD():
    con = psycopg2.connect(
        host= 'localhost',
        database= 'compila',
        user= 'postgres',
        password= '12345'
    )
    return con

def conectar_cloudBD():
    con = psycopg2.connect(
        host= 'dpg-cnsfh76n7f5s73dau5gg-a.oregon-postgres.render.com',
        database= 'compiladores_vq62',
        user= 'compiladores_vq62_user',
        password= 'rp9gwbRJIV5JJ76Y3KgmA6GdKno9Xr8a'
    )
    return con

def conectar_database():
    return conectar_cloudBD()

def verificarUsuarioExistente(email):
    conexao = conectarDB()
    cur = conexao.cursor()
    cur.execute(f"select count(*) from usuarios where email = '{email}'")
    recset = cur.fetchall()
    conexao.close()
    if recset[0][0] == 1:
        return True
    else:
        return False

def cadastrarusuario(nome, idade, email, senha):
    if not verificarUsuarioExistente(email):
        conexao = conectarDB()
        cur = conexao.cursor()
        try:
            sql = f"INSERT INTO usuarios (nome, idade, email, senha) VALUES ('{nome}', '{idade}', '{email}', '{senha}' )"
            cur.execute(sql)
        except psycopg2.IntegrityError:
            conexao.rollback()
            exito = False
        else:
            conexao.commit()
            exito = True

        conexao.close()
        return exito
    else:
        return False

def checarlogin(email, senha):
    conexao = conectarDB()
    cur = conexao.cursor()
    cur.execute(f"select count(*) from usuarios where email = '{email}' and senha ='{senha}'")
    recset = cur.fetchall()
    conexao.close()
    if recset[0][0] == 1:
        return True
    else:
        return False


def cadastrarusuario_antigo(users:list, nome, idade, email, senha):
    novousuario = {'nome':nome, 'idade':idade, 'email':email, 'senha': senha}
    if not usuarioexiste(users, email):
        users.append(novousuario)
        return True #deu certo inserir o novo usuario no banco
    else:
        return False #deu ruim pq ja tinha um user com este email

def usuarioexiste(users:list, email):
    for user in users:
        if user['email'] == email:
            return True  # já existe um usuario com este login
    return False # nao existe ninguem com este login


def registrar_contato(nome, email, comentario, cep, email_login):
    endereco = requests.get(f'https://api.brasilaberto.com/v1/zipcode/{cep}').json()

    if 'error' not in endereco['result']:
        if endereco['result']['street'] == '':
            rua = 'nao encontrado'
        else:
            rua = endereco['result']['street']
        cidade = endereco['result']['city']
        estado = endereco['result']['state']
    else:
        #cep invalido
        return False

    conexao = conectarDB()
    cur = conexao.cursor()
    try:
        sql = (f"INSERT INTO contatos (nome, email_contato, mensagem, rua, cidade, estado, email_login)"
               f" VALUES ('{nome}', '{email}', '{comentario}', '{rua}', '{cidade}', '{estado}', '{email_login}' )")
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True

    conexao.close()
    return exito

conectar_database()