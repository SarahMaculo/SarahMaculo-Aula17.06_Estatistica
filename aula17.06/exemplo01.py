from sqlalchemy import create_engine
import pandas as pd 
# pip install python-dotenv
from dotenv import load_dotenv
import os

# carrga variáveis de ambientes
load_dotenv()

def conecta_banco():
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_DATABASE')
    # URL de conexão com o banco
    engine = create_engine(
        f'mysql+pymysql://{user}:{password}@{host}/{database}' 
    )

    return engine

# início do código
# chama função e conecta ao banco
engine = conecta_banco()

try:
    df_usuarios = pd.read_sql('tb_usuarios', engine)
    df_livros = pd.read_sql('tb_livros', engine)
    df_itens = pd.read_sql('tb_itens_alugados', engine)
    df_alugados = pd.read_sql('tb_alugados', engine)
    # print(df_alugados)
 
                              
except Exception as e:
    print(f'Erro ao conectar aos dados {e}')

    
try:
    df_merge1 = pd.merge(
        df_livros, df_itens, on='id_livro' # on => onde. exemplo relacione na tabela livros e itens. mas onde? ONde => id_livros
    )
    df_merge2 = pd.merge(
        df_merge1, df_alugados, on='id_aluguel'
    )
    df_merge3 = pd.merge(
        df_merge2, df_alugados, left_on='id_usuario', right_on='id_usuario'
    )

    print(df_merge2)
except Exception as e:
    print(f'Erro ao relacionar os dataframes {e}')

# Filtro para novembro
try:
        
    df_novembro = [(
        (df_merge3['data_devolucao']>='2024-11-01') & (df_merge3['data_devolucao']<='2024-11-30')
        )]
    print(df_novembro[
        ['id_usuario', 'nome',
        'id_aluguel', 'data_aluguel', 'data_devolucao',
        'id_livro', 'titulo']
                      ])

except Exception as e:
    print(f'Erro ao rel os dataframes {e}')


