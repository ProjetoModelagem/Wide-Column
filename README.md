# Projeto de Banco de Dados NoSQL com Apache Cassandra

## Integrantes do Grupo
- **Guilherme de Abreu** - RA: 22.222.028-7

## Projeto do semestre passado

- [Projeto](https://github.com/GuizinhoAB/Modelo-de-Banco-de-Dados/tree/main)

## Descrição do Projeto
Este projeto realiza a migração de dados de um banco de dados PostgreSQL para um banco de dados NoSQL utilizando o DataStax Desktop e criando um docker do Apache Cassandra. Ele manipula informações sobre alunos, professores, cursos, departamentos, disciplinas e grupos de TCC, transferindo esses dados para tabelas otimizadas para consultas específicas.

## Como Executar o Código

1. **Instalar Dependências:**
   - Utilize o Python 3.8 até o 3.12 conforme a documentação oficial do datastax, [clique aqui](https://docs.datastax.com/en/developer/python-driver/3.29/installation/index.html#windows-build).
   - Instale as bibliotecas necessárias com o seguinte comando:
     ```bash
     pip install psycopg2 cassandra-driver
     ```

2. **Configurar o PostgreSQL e o DataStax:**
   - **PostgreSQL**: Certifique-se de que seu banco de dados PostgreSQL está funcionando corretamente e possui os dados necessários.
   - **Apache Cassandra**: Siga as intruções iniciais no DataStax Desktop, com o docker criado, certifique-se de criar um keyspace.
     ```cql
     CREATE KEYSPACE meu_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};
     ```

3. **Rodar os Scripts:**
   - Para limpar tabelas existentes no Cassandra, execute:
     ```bash
     python limpeza.py
     ```

   - Primeiro, popule o banco de dados relacional PostgreSQL com o codigo do meu semestre passado.:
     ```bash
     python criacao_tabela.py
     python data_generator.py
     ```

   - Em seguida, execute os scripts para criar tabelas no Cassandra, migrar dados e realizar consultas:
     ```bash
     python criacao.py
     python migracao.py
     python queries.py
     ```

## Queries para a Criação das Tabelas Necessárias

- As queries para criar as tabelas no Cassandra estão no arquivo **criacao.py**.

## Código Desenvolvido para Extrair os Dados do Banco Relacional

- O código de migração para o Cassandra está no arquivo **migracao.py**.

## Queries que Resolvem os 5 Itens

- As consultas que atendem aos requisitos específicos estão no arquivo **queries.py**.

## Validação das Queries

- Para validar que os dados foram migrados corretamente, execute as queries no arquivo **queries.py**.
- Também pode usar ferramentas como o CQL Shell no DataStax Desktop e verificar as tabelas.

## Descrição das Tabelas

### 1. **alunos**
Armazena informações sobre os alunos, incluindo dados pessoais e situação de graduação.

```cql
CREATE TABLE alunos (
    id TEXT PRIMARY KEY,
    nome TEXT,
    email TEXT,
    data_nascimento DATE,
    data_matricula DATE,
    situacao_graduacao BOOLEAN
);
```

### 2. **historico escolar**
Armazena o histórico de disciplinas cursadas por cada aluno.

```cql
CREATE TABLE historico_escolar (
    aluno_id TEXT,
    ano INT,
    semestre INT,
    disciplina_id TEXT,
    nome_disciplina TEXT,
    nota_final FLOAT,
    PRIMARY KEY (aluno_id, ano, semestre, disciplina_id)
) WITH CLUSTERING ORDER BY (ano DESC, semestre DESC);
```

### 3. **professores**
Armazena informações sobre os professores.

```cql
CREATE TABLE professores (
    id TEXT PRIMARY KEY,
    nome TEXT,
    email TEXT,
    data_nascimento DATE,
    data_contratacao DATE
);
```

### 4. *resumo_disciplinas_professor**
Tabela de suporte para facilitar consultas sobre disciplinas ministradas por professores.

```cql
CREATE TABLE resumo_disciplinas_professor (
    professor_id TEXT,
    disciplina_id TEXT,
    nome_disciplina TEXT,
    ano INT,
    semestre INT,
    PRIMARY KEY (professor_id, disciplina_id)
);
```

### 5. **departamentos**
Armazena informações sobre os departamentos.

```cql
CREATE TABLE departamentos (
    id TEXT PRIMARY KEY,
    nome TEXT
);
```

### 6. **chefes_departamento**
Armazena informações sobre professores que são chefes de departamento.

```cql
CREATE TABLE chefes_departamento (
    departamento_id TEXT PRIMARY KEY,
    professor_id TEXT,
    nome_departamento TEXT,
    nome_professor TEXT
);
```

### 7. **grupos_tcc**
Armazena informações sobre os grupos de TCC, incluindo orientador e alunos participantes.

```cql
CREATE TABLE grupos_tcc (
    grupo_numero TEXT PRIMARY KEY,
    alunos LIST<TEXT>,
    orientador_id TEXT
);
```

### 8. **disciplinas**
Armazena informações sobre as disciplinas.

```cql
CREATE TABLE disciplinas (
    id TEXT PRIMARY KEY,
    nome TEXT,
    cursos LIST<TEXT>
);
```
### 9. **cursos**
Armazena informações sobre os cursos.

```cql
CREATE TABLE cursos (
    id TEXT PRIMARY KEY,
    nome TEXT,
    departamentos LIST<TEXT>
);
```

### 10. **alunos graduados**
Armazena informações sobre os alunos graduados.

```cql
CREATE TABLE alunos_graduados (
    id TEXT PRIMARY KEY,
    nome TEXT,
    ano_formatura INT,
    semestre_formatura INT
);
```