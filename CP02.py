import requests
import cx_Oracle

# Função para ler o arquivo de texto contendo o login do GitHub
def ler_arquivo(path):
    with open(path, 'r') as file:
        return file.readline().strip()

# Função para obter informações do usuário do GitHub através da API
def obter_informacoes_github(login):
    url = f'https://api.github.com/users/{login}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Falha ao obter informações do GitHub. Código de resposta: {response.status_code}')

# Função para conectar ao banco de dados Oracle e inserir as informações do usuário
def inserir_dados(usuario_info):
    dsn = cx_Oracle.makedsn(host='oracle.fiap.com.br', port=1521, sid='ORCL')
    conexao = cx_Oracle.connect(user='rm554113', password='081093', dsn=dsn)
    cursor = conexao.cursor()

    sql = '''
    INSERT INTO tb_github_user (nome, repositorios, seguidores, seguindo) 
    VALUES (:nome, :repositorios, :seguidores, :seguindo)
    '''
    cursor.execute(sql, {
        'nome': usuario_info.get('name', ''),
        'repositorios': usuario_info.get('public_repos', 0),
        'seguidores': usuario_info.get('followers', 0),
        'seguindo': usuario_info.get('following', 0)
    })

    conexao.commit()
    cursor.close()
    conexao.close()

# Caminho para o arquivo de login
path = 'C:\\temp\\github_user.txt'

try:
    # Ler o login do GitHub do arquivo
    login_github = ler_arquivo(path)
    # Obter informações do usuário do GitHub
    info_github = obter_informacoes_github(login_github)
    # Inserir usuário no banco de dados Oracle
    inserir_dados(info_github)
    print('Informações do usuário inseridas no banco de dados com sucesso!')
except Exception as e:
    print(f'Erro ao executar o programa: {e}')

