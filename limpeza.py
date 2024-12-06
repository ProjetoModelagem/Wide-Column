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

def excluir_tabelas():
    try:
        tabelas = [
            "alunos",
            "historico_escolar",
            "professores",
            "alunos_graduados"
            "resumo_disciplinas_professor",
            "departamentos",
            "chefes_departamento",
            "grupos_tcc",
            "disciplinas",
            "cursos"
        ]
        
        for tabela in tabelas:
            session.execute(f"DROP TABLE IF EXISTS {tabela};")
            print(f"Tabela '{tabela}' excluída com sucesso.")
    except Exception as e:
        print(f"Erro ao excluir as tabelas: {e}")

excluir_tabelas()
