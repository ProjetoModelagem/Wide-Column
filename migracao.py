from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import psycopg2

# Configuração do Cassandra
CASSANDRA_HOST = "info"
CASSANDRA_PORT = 0000
CASSANDRA_KEYSPACE = "info"

# Conexão com o Cassandra
auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT, auth_provider=auth_provider)
session = cluster.connect(CASSANDRA_KEYSPACE)

print(f"Conectado ao Cassandra no keyspace '{CASSANDRA_KEYSPACE}'")

# Conexão com o PostgreSQL
pg_conn = psycopg2.connect(
    database="info",
    user="info",
    password="info",
    host="info", 
    port="info"       
)

pg_cursor = pg_conn.cursor()

#Função para inserir dados no Cassandra
def inserir_cassandra(prepared_stmt, parameters):
    try:
        session.execute(prepared_stmt, parameters)
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")

# Migrar alunos
def migrar_alunos():

    #prepara a query de insercao
    insert_aluno_stmt = session.prepare("""
        INSERT INTO alunos (id, nome, email, data_nascimento, data_matricula, situacao_graduacao)
        VALUES (?, ?, ?, ?, ?, ?)
    """)

    pg_cursor.execute("SELECT * FROM alunos;")
    alunos = pg_cursor.fetchall()
    for aluno in alunos:
        aluno_id = str(aluno[0])
        nome = aluno[1]
        email = aluno[2]
        data_nascimento = aluno[3]
        data_matricula = aluno[4]
        situacao_graduacao = aluno[5]

        inserir_cassandra(insert_aluno_stmt, (
            aluno_id, nome, email, data_nascimento, data_matricula, situacao_graduacao
        ))

    print("Migração da tabela 'alunos' concluída.")

# Migrar historico escolar
def migrar_historico_escolar():
    insert_historico_stmt = session.prepare("""
        INSERT INTO historico_escolar (aluno_id, ano, semestre, disciplina_id, nome_disciplina, nota_final)
        VALUES (?, ?, ?, ?, ?, ?)
    """)

    pg_cursor.execute("""
        SELECT he.aluno_id, he.ano, he.semestre, he.disciplina_id, d.nome, he.nota_final
        FROM historico_escolar he
        JOIN disciplinas d ON he.disciplina_id = d.id;
    """)
    registros = pg_cursor.fetchall()
    for registro in registros:
        aluno_id = str(registro[0])
        ano = registro[1]
        semestre = registro[2]
        disciplina_id = str(registro[3])
        nome_disciplina = registro[4]
        nota_final = registro[5]

        inserir_cassandra(insert_historico_stmt, (
            aluno_id, ano, semestre, disciplina_id, nome_disciplina, nota_final
        ))

    print("Migração da tabela 'historico_escolar' concluída.")

# Migrar professores
def migrar_professores():
    insert_professor_stmt = session.prepare("""
        INSERT INTO professores (id, nome, email, data_nascimento, data_contratacao)
        VALUES (?, ?, ?, ?, ?)
    """)

    pg_cursor.execute("SELECT * FROM professores;")
    professores = pg_cursor.fetchall()
    for professor in professores:
        professor_id = str(professor[0])
        nome = professor[1]
        email = professor[2]
        data_nascimento = professor[3]
        data_contratacao = professor[4]

        inserir_cassandra(insert_professor_stmt, (
            professor_id, nome, email, data_nascimento, data_contratacao
        ))

    print("Migração da tabela 'professores' concluída.")


# Migrar departamentos
def migrar_departamentos():
    insert_departamento_stmt = session.prepare("""
        INSERT INTO departamentos (id, nome)
        VALUES (?, ?)
    """)

    pg_cursor.execute("SELECT * FROM departamentos;")
    departamentos = pg_cursor.fetchall()
    for departamento in departamentos:
        departamento_id = str(departamento[0])
        nome = departamento[1]

        inserir_cassandra(insert_departamento_stmt, (departamento_id, nome))

    print("Migração da tabela 'departamentos' concluída.")

# Migrar chefes de departamento
def migrar_chefes_departamento():
    insert_chefe_stmt = session.prepare("""
        INSERT INTO chefes_departamento (departamento_id, professor_id, nome_departamento, nome_professor)
        VALUES (?, ?, ?, ?)
    """)

    pg_cursor.execute("""
        SELECT d.id, p.id, d.nome, p.nome
        FROM professores_departamentos pd
        JOIN departamentos d ON pd.departamento_id = d.id
        JOIN professores p ON pd.professor_id = p.id;
    """)
    registros = pg_cursor.fetchall()
    for registro in registros:
        departamento_id = str(registro[0])
        professor_id = str(registro[1])
        nome_departamento = registro[2]
        nome_professor = registro[3]

        inserir_cassandra(insert_chefe_stmt, (
            departamento_id, professor_id, nome_departamento, nome_professor
        ))

    print("Migração da tabela 'chefes_departamento' concluída.")

# Migrar disciplinas
def migrar_disciplinas():
    insert_disciplina_stmt = session.prepare("""
        INSERT INTO disciplinas (id, nome)
        VALUES (?, ?)
    """)

    pg_cursor.execute("SELECT * FROM disciplinas;")
    disciplinas = pg_cursor.fetchall()
    for disciplina in disciplinas:
        disciplina_id = str(disciplina[0])
        nome = disciplina[1]


        inserir_cassandra(insert_disciplina_stmt, (
            disciplina_id, nome
        ))

    print("Migração da tabela 'disciplinas' concluída.")

# Migrar cursos
def migrar_cursos():
    insert_curso_stmt = session.prepare("""
        INSERT INTO cursos (id, nome)
        VALUES (?, ?)
    """)

    pg_cursor.execute("SELECT * FROM cursos;")
    cursos = pg_cursor.fetchall()
    for curso in cursos:
        curso_id = str(curso[0])
        nome = curso[1]

        inserir_cassandra(insert_curso_stmt, (
            curso_id, nome
        ))

    print("Migração da tabela 'cursos' concluída.")

# Migrar grupos de TCC
def migrar_grupos_tcc():
    insert_grupo_stmt = session.prepare("""
        INSERT INTO grupos_tcc (grupo_numero, alunos, orientador_id)
        VALUES (?, ?, ?)
    """)

    pg_cursor.execute("SELECT DISTINCT grupo FROM grupo_tcc;")
    grupos = pg_cursor.fetchall()

    for (grupo_numero,) in grupos:
        # alunos do grupo
        pg_cursor.execute("""
            SELECT aluno_id
            FROM grupo_tcc
            WHERE grupo = %s;
        """, (grupo_numero,))
        alunos = [str(aluno_id[0]) for aluno_id in pg_cursor.fetchall()]

        # orientador
        pg_cursor.execute("""
            SELECT professor_orientador_id
            FROM grupo_tcc
            WHERE grupo = %s LIMIT 1;
        """, (grupo_numero,))
        orientador_id = pg_cursor.fetchone()[0]
        orientador_id = str(orientador_id) if orientador_id else None

        inserir_cassandra(insert_grupo_stmt, (
            str(grupo_numero), alunos, orientador_id
        ))

    print("Migração da tabela 'grupos_tcc' concluída.")

# Migrar resumo de disciplinas ministradas por professor (tabela 'suporte' por causa que estava dando erros com otimização)
def migrar_resumo_disciplinas_professor():
    insert_resumo_stmt = session.prepare("""
        INSERT INTO resumo_disciplinas_professor (professor_id, disciplina_id, nome_disciplina, ano, semestre)
        VALUES (?, ?, ?, ?, ?)
    """)

    pg_cursor.execute("""
        SELECT hdp.professor_id, hdp.disciplina_id, d.nome, hdp.ano, hdp.semestre
        FROM historico_disciplina_professores hdp
        JOIN disciplinas d ON hdp.disciplina_id = d.id;
    """)
    registros = pg_cursor.fetchall()
    for registro in registros:
        professor_id = str(registro[0])
        disciplina_id = str(registro[1])
        nome_disciplina = registro[2]
        ano = registro[3]
        semestre = registro[4]

        inserir_cassandra(insert_resumo_stmt, (
            professor_id, disciplina_id, nome_disciplina, ano, semestre
        ))

    print("Migração da tabela 'resumo_disciplinas_professor' concluída.")

# Migrar alunos graduados (outra tabela 'suporte')
def migrar_alunos_graduados():
    insert_graduados_stmt = session.prepare("""
        INSERT INTO alunos_graduados (id, nome, ano_formatura, semestre_formatura)
        VALUES (?, ?, ?, ?)
    """)
    
    pg_cursor.execute("""
        SELECT a.id, a.nome, af.ano, af.semestre
        FROM alunos_formados af
        JOIN alunos a ON af.aluno_id = a.id;
    """)
    graduados = pg_cursor.fetchall()
    for graduado in graduados:
        aluno_id = str(graduado[0])
        nome = graduado[1]
        ano_formatura = graduado[2]
        semestre_formatura = graduado[3]

        inserir_cassandra(insert_graduados_stmt, (
            aluno_id, nome, ano_formatura, semestre_formatura
        ))

    print("Migração da tabela 'alunos_graduados' concluída.")


def migrar_todos():
    migrar_alunos()
    migrar_historico_escolar()
    migrar_professores()
    migrar_departamentos()
    migrar_chefes_departamento()
    migrar_disciplinas()
    migrar_cursos()
    migrar_grupos_tcc()
    migrar_resumo_disciplinas_professor()
    migrar_alunos_graduados()
    print("Migração concluída com sucesso!")

if __name__ == "__main__":
    migrar_todos()
