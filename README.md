# KLASSE - Sistema de Gestão e Sorteio Escolar

Projeto acadêmico estruturado seguindo os princípios da **Arquitetura Limpa (Clean Architecture)**, boas práticas de **Programação Orientada a Objetos (POO)** e integração com o banco de dados relacional **Supabase (PostgreSQL)**.

---

## 🏛️ Estrutura de Pastas (Clean Architecture)

```text
klasse/
│
├── main.py                          # Ponto de entrada (Composition Root)
├── supabase_schema.sql              # Esquema das tabelas relacionais no Supabase
├── requirements.txt                 # Dependências do projeto (supabase, python-dotenv)
├── .env.example                     # Modelo das variáveis de ambiente
├── .gitignore                       # Arquivos ignorados pelo Git (.env, caches, etc.)
├── README.md                        # Documentação da arquitetura e execução
│
└── src/
    ├── domain/                      # 1. Camada de Domínio (Entidades e Regras Centrais)
    │   ├── entities/
    │   │   ├── pessoa.py            # Classe abstrata base Pessoa com nome, cpf e métodos protegidos
    │   │   ├── aluno.py             # Entidade Aluno (matricula, cpf, data_nascimento, serie_atual, turma_atual_id)
    │   │   ├── professor.py         # Entidade Professor (matricula, cpf, email)
    │   │   ├── turma.py             # Entidade Turma (nome, serie, ano_letivo, professor, disciplina, alunos)
    │   │   ├── frequencia.py        # Entidade Frequencia (turma_id, professor_id, aluno_id, data, presente)
    │   │   └── historico_aluno_turma.py # Entidade HistoricoAlunoTurma (aluno_id, turma_id, ano_letivo, serie)
    │   └── exceptions.py            # Exceções de domínio (ValidationError, DatabaseError)
    │
    ├── application/                 # 2. Camada de Aplicação (Casos de Uso e Portas)
    │   ├── interfaces/              # Contratos/Interfaces abstratas (Repositórios)
    │   │   ├── aluno_repository.py
    │   │   ├── professor_repository.py
    │   │   ├── turma_repository.py
    │   │   ├── frequencia_repository.py
    │   │   └── historico_repository.py
    │   └── use_cases/               # Regras de Negócio da Aplicação
    │       ├── gerenciar_alunos.py       # Casos de uso de Alunos com validação e normalização de datas
    │       ├── gerenciar_professores.py  # Casos de uso de Professores
    │       ├── sortear_turmas.py         # Regra de negócio de sorteio com vínculo relacional e histórico
    │       ├── gerenciar_frequencias.py  # Casos de uso para registro de chamadas e controle de presença
    │       └── gerenciar_historico.py    # Casos de uso para consulta e filtragem do histórico escolar
    │
    ├── infrastructure/              # 3. Camada de Infraestrutura (Implementações Concretas)
    │   ├── database/
    │   │   └── supabase_client.py   # Conexão e cliente Supabase (Singleton com tratamento de erros)
    │   └── repositories/
    │       ├── in_memory_aluno_repository.py      # Repositório em memória para Alunos
    │       ├── in_memory_professor_repository.py  # Repositório em memória para Professores
    │       ├── in_memory_turma_repository.py      # Repositório em memória para Turmas
    │       ├── in_memory_frequencia_repository.py # Repositório em memória para Frequências
    │       ├── in_memory_historico_repository.py  # Repositório em memória para Histórico
    │       ├── supabase_aluno_repository.py       # Repositório Supabase (tabela public.alunos)
    │       ├── supabase_professor_repository.py   # Repositório Supabase (tabela public.professores)
    │       ├── supabase_turma_repository.py       # Repositório Supabase (tabela public.turmas)
    │       ├── supabase_frequencia_repository.py  # Repositório Supabase (tabela public.frequencias)
    │       └── supabase_historico_repository.py   # Repositório Supabase (tabela public.historico_alunos_turmas)
    │
    └── presentation/                # 4. Camada de Apresentação (Interface com Usuário - Tkinter)
        ├── app.py                   # Janela principal do Tkinter com navegação completa
        ├── components/              # Componentes de UI reutilizáveis
        │   ├── botao_personalizado.py
        │   └── tela_base.py
        └── views/                   # Telas específicas do sistema
            ├── tela_alunos.py       # Tela de cadastro com Nome, Matrícula, CPF, Nascimento e Série
            ├── tela_professores.py  # Tela de cadastro com Nome, Matrícula, CPF e E-mail
            ├── tela_sorteio.py      # Tela de configuração com Série, Ano Letivo e Professores
            ├── tela_turmas.py       # Tela de consulta com detalhes relacionais
            ├── tela_frequencia.py   # Tela de lançamento e histórico de chamada escolar
            └── tela_historico.py    # Tela de consulta de histórico de alunos em turmas com filtros
```

---

## 🗄️ Esquema Relacional do Banco de Dados

- **`professores`**: `id`, `matricula` (UNIQUE), `cpf` (UNIQUE), `nome`, `email` (UNIQUE).
- **`alunos`**: `id`, `matricula` (UNIQUE), `cpf` (UNIQUE), `nome`, `data_nascimento` (DATE), `serie_atual`, `turma_atual_id` (FK -> `turmas.id`).
- **`turmas`**: `id`, `nome`, `serie`, `ano_letivo`.
- **`turma_professores`**: vínculo relacional entre `turma_id`, `professor_id` e a `disciplina`.
- **`frequencias`**: controle de presença com `turma_id`, `professor_id`, `aluno_id`, `disciplina`, `data` e `presente`.
- **`historico_alunos_turmas`**: registro histórico de alunos vinculados a cada turma por ano letivo e série.

---

## ⚡ Conexão com o Supabase

1. Crie um arquivo `.env` na raiz do projeto:
   ```env
   SUPABASE_URL=https://seu-id-de-projeto.supabase.co
   SUPABASE_KEY=sua-chave-anon-ou-service-role
   ```
2. Caso o `.env` não seja preenchido, a aplicação utilizará automaticamente repositórios em memória.

---

## 🚀 Como Executar

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação
python main.py
```
