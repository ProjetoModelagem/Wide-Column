from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import random

# Configuração do Cassandra
CASSANDRA_HOST = "info"
CASSANDRA_PORT = 0000
CASSANDRA_KEYSPACE = "info"

# Conexão com o Cassandra
auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT, auth_provider=auth_provider)
session = cluster.connect(CASSANDRA_KEYSPACE)


# obtem um valor aleatorio de uma tabela
def obter_registro_aleatorio(tabela, coluna):
    query = f"SELECT {coluna} FROM {tabela} LIMIT 100;"
    rows = session.execute(query)
    valores = [row[0] for row in rows if row[0] is not None]
    return random.choice(valores) if valores else None


# Query que resolve o 1
def historico_escolar_aleatorio():
    aluno_id = obter_registro_aleatorio("historico_escolar", "aluno_id")
    if aluno_id:
        query = """
        SELECT disciplina_id, nome_disciplina, semestre, ano, nota_final
        FROM historico_escolar
        WHERE aluno_id = ?;
        """
        rows = session.execute(session.prepare(query), [aluno_id])
        print(f"\nHistórico escolar do aluno ID {aluno_id}:")
        for row in rows:
            print(f"Código: {row.disciplina_id}, Nome: {row.nome_disciplina}, Semestre: {row.semestre}, Ano: {row.ano}, Nota Final: {row.nota_final}")
    else:
        print("Nenhum aluno encontrado para consulta.")


# Query que resolve o 2
def historico_professor_aleatorio():
    professor_id = obter_registro_aleatorio("resumo_disciplinas_professor", "professor_id")
    if professor_id:
        query = """
        SELECT disciplina_id, nome_disciplina, ano, semestre
        FROM resumo_disciplinas_professor
        WHERE professor_id = ?;
        """
        rows = session.execute(session.prepare(query), [professor_id])
        print(f"\nHistórico de disciplinas ministradas pelo professor ID {professor_id}:")
        for row in rows:
            print(f"Disciplina: {row.nome_disciplina}, Ano: {row.ano}, Semestre: {row.semestre}")
    else:
        print("Nenhum professor encontrado para consulta.")

# Query que resolve o 3
def lista_alunos_graduados():
    query = """
    SELECT id, nome, ano_formatura, semestre_formatura
    FROM alunos_graduados;
    """
    rows = session.execute(query)
    print("\nAlunos formados:")
    for row in rows:
        print(f"ID: {row.id}, Nome: {row.nome}, Ano: {row.ano_formatura}, Semestre: {row.semestre_formatura}")



# Query que resolve o 4
def lista_chefes_departamento():
    query = """
    SELECT professor_id, nome_professor, nome_departamento
    FROM chefes_departamento;
    """
    rows = session.execute(query)
    print("\nProfessores que são chefes de departamento:")
    for row in rows:
        print(f"Professor ID: {row.professor_id}, Nome: {row.nome_professor}, Departamento: {row.nome_departamento}")



# Query que resolve o 5
def grupo_tcc_aleatorio():
    grupo_numero = obter_registro_aleatorio("grupos_tcc", "grupo_numero")
    if grupo_numero:
        query = """
        SELECT alunos, orientador_id
        FROM grupos_tcc
        WHERE grupo_numero = ?;
        """
        row = session.execute(session.prepare(query), [grupo_numero]).one()
        if row:
            print(f"\nGrupo de TCC número {grupo_numero}:")
            print(f"Orientador ID: {row.orientador_id}")
            print("Alunos:")
            for aluno_id in row.alunos:
                aluno_query = "SELECT nome FROM alunos WHERE id = ?;"
                aluno_result = session.execute(session.prepare(aluno_query), [aluno_id]).one()
                nome_aluno = aluno_result.nome if aluno_result else "Nome não encontrado"
                print(f"- ID: {aluno_id}, Nome: {nome_aluno}")
        else:
            print("Nenhuma informação encontrada para o grupo.")
    else:
        print("Nenhum grupo encontrado para consulta.")


if __name__ == "__main__":
    historico_escolar_aleatorio()
    historico_professor_aleatorio()
    lista_alunos_graduados()
    lista_chefes_departamento()
    grupo_tcc_aleatorio()
