from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Configuração do Cassandra
CASSANDRA_HOST = "info"
CASSANDRA_PORT = 0000
CASSANDRA_KEYSPACE = "info"

# Conexão com o Cassandra
auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT, auth_provider=auth_provider)
session = cluster.connect(CASSANDRA_KEYSPACE)


def criar_tabelas():
    try:
        # tabela pra alunos
        session.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id TEXT PRIMARY KEY,
                nome TEXT,
                email TEXT,
                data_nascimento DATE,
                data_matricula DATE,
                situacao_graduacao BOOLEAN
            );
        """)
        print("Tabela 'alunos' criada com sucesso.")
        
        # historico escolar
        session.execute("""
            CREATE TABLE IF NOT EXISTS historico_escolar (
                aluno_id TEXT,
                ano INT,
                semestre INT,
                disciplina_id TEXT,
                nome_disciplina TEXT,
                nota_final FLOAT,
                PRIMARY KEY (aluno_id, ano, semestre, disciplina_id)
            ) WITH CLUSTERING ORDER BY (ano DESC, semestre DESC);
        """)
        print("Tabela 'historico_escolar' criada com sucesso.")
        
        #  professores
        session.execute("""
            CREATE TABLE IF NOT EXISTS professores (
                id TEXT PRIMARY KEY,
                nome TEXT,
                email TEXT,
                data_nascimento DATE,
                data_contratacao DATE
            );
        """)
        print("Tabela 'professores' criada com sucesso.")
        
        # Tabela praa suporte: Resumo de disciplinas ministradas por professor
        session.execute("""
            CREATE TABLE IF NOT EXISTS resumo_disciplinas_professor (
                professor_id TEXT,
                disciplina_id TEXT,
                nome_disciplina TEXT,
                ano INT,
                semestre INT,
                PRIMARY KEY (professor_id, disciplina_id)
            );
        """)
        print("Tabela 'resumo_disciplinas_professor' criada com sucesso.")
        
        # departamentos
        session.execute("""
            CREATE TABLE IF NOT EXISTS departamentos (
                id TEXT PRIMARY KEY,
                nome TEXT
            );
        """)
        print("Tabela 'departamentos' criada com sucesso.")
        
        # chefes de departamento
        session.execute("""
            CREATE TABLE IF NOT EXISTS chefes_departamento (
                departamento_id TEXT PRIMARY KEY,
                professor_id TEXT,
                nome_departamento TEXT,
                nome_professor TEXT
            );
        """)
        print("Tabela 'chefes_departamento' criada com sucesso.")
        
        # grupos de TCC
        session.execute("""
            CREATE TABLE IF NOT EXISTS grupos_tcc (
                grupo_numero TEXT PRIMARY KEY,
                alunos LIST<TEXT>,
                orientador_id TEXT
            );
        """)
        print("Tabela 'grupos_tcc' criada com sucesso.")
        
        # Tabela para disciplinas
        session.execute("""
            CREATE TABLE IF NOT EXISTS disciplinas (
                id TEXT PRIMARY KEY,
                nome TEXT,
                cursos LIST<TEXT>
            );
        """)
        print("Tabela 'disciplinas' criada com sucesso.")
        
        # Tabela para cursos
        session.execute("""
            CREATE TABLE IF NOT EXISTS cursos (
                id TEXT PRIMARY KEY,
                nome TEXT,
                departamentos LIST<TEXT>
            );
        """)
        print("Tabela 'cursos' criada com sucesso.")

        # Tabela de suporte para alunos graduados
        session.execute("""
            CREATE TABLE IF NOT EXISTS alunos_graduados (
                id TEXT PRIMARY KEY,
                nome TEXT,
                ano_formatura INT,
                semestre_formatura INT
            );
        """)
        print("Tabela 'alunos_graduados' criada com sucesso.")
        
    except Exception as e:
        print(f"Erro ao criar as tabelas: {e}")

criar_tabelas()

