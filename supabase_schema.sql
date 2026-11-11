-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.professores (
  id integer NOT NULL DEFAULT nextval('professores_id_seq'::regclass),
  matricula character varying NOT NULL UNIQUE,
  cpf character varying NOT NULL UNIQUE,
  nome character varying NOT NULL,
  email character varying NOT NULL UNIQUE,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT professores_pkey PRIMARY KEY (id)
);
CREATE TABLE public.professor_disciplinas (
  id integer NOT NULL DEFAULT nextval('professor_disciplinas_id_seq'::regclass),
  professor_id integer NOT NULL,
  disciplina character varying NOT NULL,
  CONSTRAINT professor_disciplinas_pkey PRIMARY KEY (id),
  CONSTRAINT fk_prof_disciplina FOREIGN KEY (professor_id) REFERENCES public.professores(id)
);
CREATE TABLE public.professor_horarios (
  id integer NOT NULL DEFAULT nextval('professor_horarios_id_seq'::regclass),
  professor_id integer NOT NULL,
  dia_semana character varying NOT NULL,
  horario_inicio time without time zone NOT NULL,
  horario_fim time without time zone NOT NULL,
  CONSTRAINT professor_horarios_pkey PRIMARY KEY (id),
  CONSTRAINT fk_prof_horario FOREIGN KEY (professor_id) REFERENCES public.professores(id)
);
CREATE TABLE public.turmas (
  id integer NOT NULL DEFAULT nextval('turmas_id_seq'::regclass),
  nome character varying NOT NULL,
  serie character varying NOT NULL,
  ano_letivo integer NOT NULL,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT turmas_pkey PRIMARY KEY (id)
);
CREATE TABLE public.turma_professores (
  id integer NOT NULL DEFAULT nextval('turma_professores_id_seq'::regclass),
  turma_id integer NOT NULL,
  professor_id integer NOT NULL,
  disciplina character varying NOT NULL,
  CONSTRAINT turma_professores_pkey PRIMARY KEY (id),
  CONSTRAINT fk_tp_turma FOREIGN KEY (turma_id) REFERENCES public.turmas(id),
  CONSTRAINT fk_tp_professor FOREIGN KEY (professor_id) REFERENCES public.professores(id)
);
CREATE TABLE public.alunos (
  id integer NOT NULL DEFAULT nextval('alunos_id_seq'::regclass),
  matricula character varying NOT NULL UNIQUE,
  cpf character varying NOT NULL UNIQUE,
  nome character varying NOT NULL,
  data_nascimento date NOT NULL,
  serie_atual character varying NOT NULL,
  turma_atual_id integer,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT alunos_pkey PRIMARY KEY (id),
  CONSTRAINT fk_aluno_turma FOREIGN KEY (turma_atual_id) REFERENCES public.turmas(id)
);
CREATE TABLE public.historico_alunos_turmas (
  id integer NOT NULL DEFAULT nextval('historico_alunos_turmas_id_seq'::regclass),
  aluno_id integer NOT NULL,
  turma_id integer NOT NULL,
  ano_letivo integer NOT NULL,
  serie character varying NOT NULL,
  CONSTRAINT historico_alunos_turmas_pkey PRIMARY KEY (id),
  CONSTRAINT fk_hist_aluno FOREIGN KEY (aluno_id) REFERENCES public.alunos(id),
  CONSTRAINT fk_hist_turma FOREIGN KEY (turma_id) REFERENCES public.turmas(id)
);
CREATE TABLE public.notas (
  id integer NOT NULL DEFAULT nextval('notas_id_seq'::regclass),
  aluno_id integer NOT NULL,
  turma_id integer NOT NULL,
  disciplina character varying NOT NULL,
  periodo character varying NOT NULL,
  ano_letivo integer NOT NULL,
  descricao character varying NOT NULL,
  nota numeric NOT NULL CHECK (nota >= 0.00 AND nota <= 10.00),
  peso numeric DEFAULT 1.00,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT notas_pkey PRIMARY KEY (id),
  CONSTRAINT fk_nota_aluno FOREIGN KEY (aluno_id) REFERENCES public.alunos(id),
  CONSTRAINT fk_nota_turma FOREIGN KEY (turma_id) REFERENCES public.turmas(id)
);
CREATE TABLE public.frequencias (
  id integer NOT NULL DEFAULT nextval('frequencias_id_seq'::regclass),
  turma_id integer NOT NULL,
  professor_id integer NOT NULL,
  aluno_id integer NOT NULL,
  disciplina character varying NOT NULL,
  data date NOT NULL,
  presente boolean NOT NULL DEFAULT true,
  created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT frequencias_pkey PRIMARY KEY (id),
  CONSTRAINT fk_freq_turma FOREIGN KEY (turma_id) REFERENCES public.turmas(id),
  CONSTRAINT fk_freq_professor FOREIGN KEY (professor_id) REFERENCES public.professores(id),
  CONSTRAINT fk_freq_aluno FOREIGN KEY (aluno_id) REFERENCES public.alunos(id)
);
CREATE TABLE public.ocorrencias (
  id integer NOT NULL DEFAULT nextval('ocorrencias_id_seq'::regclass),
  data_hora timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
  turma_id integer NOT NULL,
  professor_id integer NOT NULL,
  titulo character varying NOT NULL,
  descricao text NOT NULL,
  gravidade character varying NOT NULL CHECK (gravidade::text = ANY (ARRAY['Baixa'::character varying, 'Média'::character varying, 'Alta'::character varying, 'Gravíssima'::character varying]::text[])),
  medidas_tomadas text,
  CONSTRAINT ocorrencias_pkey PRIMARY KEY (id),
  CONSTRAINT fk_oc_turma FOREIGN KEY (turma_id) REFERENCES public.turmas(id),
  CONSTRAINT fk_oc_professor FOREIGN KEY (professor_id) REFERENCES public.professores(id)
);
CREATE TABLE public.ocorrencia_alunos (
  id integer NOT NULL DEFAULT nextval('ocorrencia_alunos_id_seq'::regclass),
  ocorrencia_id integer NOT NULL,
  aluno_id integer NOT NULL,
  CONSTRAINT ocorrencia_alunos_pkey PRIMARY KEY (id),
  CONSTRAINT fk_oa_ocorrencia FOREIGN KEY (ocorrencia_id) REFERENCES public.ocorrencias(id),
  CONSTRAINT fk_oa_aluno FOREIGN KEY (aluno_id) REFERENCES public.alunos(id)
);


-- ==============================================================
-- PERMISSÕES / ROW LEVEL SECURITY (RLS)
-- Como este aplicativo desktop utiliza a chave de API pública (anon)
-- sem autenticação de usuários (login/senha), é necessário desativar
-- o RLS ou criar políticas de acesso para permitir Leitura e Escrita.
-- Execute os comandos abaixo no SQL Editor do Supabase:
-- ==============================================================

ALTER TABLE public.professores DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.alunos DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.turmas DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.turma_professores DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.historico_alunos_turmas DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.professor_disciplinas DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.professor_horarios DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.notas DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.frequencias DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.ocorrencias DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.ocorrencia_alunos DISABLE ROW LEVEL SECURITY;


-- ==============================================================
-- PERMISSÕES / ROW LEVEL SECURITY (RLS)
-- Como este aplicativo desktop utiliza a chave de API pública (anon)
-- sem autenticação de usuários (login/senha), é necessário desativar
-- o RLS ou criar políticas de acesso para permitir Leitura e Escrita.
-- Execute os comandos abaixo no SQL Editor do Supabase:
-- ==============================================================

ALTER TABLE public.professores DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.alunos DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.turmas DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.turma_professores DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.historico_alunos_turmas DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.professor_disciplinas DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.professor_horarios DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.notas DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.frequencias DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.ocorrencias DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.ocorrencia_alunos DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.alunos
ADD COLUMN IF NOT EXISTS tem_laudo BOOLEAN NOT NULL DEFAULT FALSE;