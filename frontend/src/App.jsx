
import { useState } from 'react'
import './App.css'

const menuItems = [
  { id: 'inicio', icon: '⌂', label: 'Início' },
  { id: 'alunos', icon: '♙', label: 'Alunos' },
  { id: 'professores', icon: '♧', label: 'Professores' },
  { id: 'turmas', icon: '▦', label: 'Turmas' },
  { id: 'materias', icon: '📚', label: 'Matérias' },
  { id: 'sorteio', icon: '⇄', label: 'Sorteio de turmas' },
  { id: 'grade', icon: '▦', label: 'Grade horária' },
  { id: 'frequencia', icon: '✓', label: 'Frequência' },
  { id: 'historico', icon: '◷', label: 'Histórico' },
]

const series = [
  '1º Ano', '2º Ano', '3º Ano',
  '4º Ano', '5º Ano', '6º Ano',
  '7º Ano', '8º Ano', '9º Ano',
]

function App() {
  const [paginaAtiva, setPaginaAtiva] = useState('inicio')

  // Matérias
  const [materias, setMaterias] = useState([])
  const [novaMateria, setNovaMateria] = useState('')
  const [cargaHoraria, setCargaHoraria] = useState(2)

  // Professores
  const [professores, setProfessores] = useState([])
  const [nomeProfessor, setNomeProfessor] = useState('')
  const [materiasProfessor, setMateriasProfessor] = useState([])
  const [seriesProfessor, setSeriesProfessor] = useState([])
  const [matriculaProfessor, setMatriculaProfessor] = useState('')
  const [cpfProfessor, setCpfProfessor] = useState('')
  const [emailProfessor, setEmailProfessor] = useState('')
  const [nascimentoProfessor, setNascimentoProfessor] = useState('')
  const [telefoneProfessor, setTelefoneProfessor] = useState('')
  const pagina = menuItems.find(item => item.id === paginaAtiva)

  function adicionarMateria(e) {
    e.preventDefault()

    const nome = novaMateria.trim()

    if (!nome) return

    const existe = materias.some(
      materia => materia.nome.toLowerCase() === nome.toLowerCase()
    )

    if (existe) {
      alert('Essa matéria já foi cadastrada!')
      return
    }

    setMaterias(atual => [
      ...atual,
      {
        id: Date.now(),
        nome,
        aulas: Number(cargaHoraria),
      },
    ])

    setNovaMateria('')
    setCargaHoraria(2)
  }

  function excluirMateria(id) {
    setMaterias(atual => atual.filter(materia => materia.id !== id))

    // Remove a matéria também dos professores que a lecionam
    setProfessores(atual =>
      atual.map(professor => ({
        ...professor,
        materias: professor.materias.filter(item => item !== id),
      }))
    )

    setMateriasProfessor(atual => atual.filter(item => item !== id))
  }

  function alternarMateria(id) {
    setMateriasProfessor(atual =>
      atual.includes(id)
        ? atual.filter(item => item !== id)
        : [...atual, id]
    )
  }

  function alternarSerie(serie) {
    setSeriesProfessor(atual =>
      atual.includes(serie)
        ? atual.filter(item => item !== serie)
        : [...atual, serie]
    )
  }

  function adicionarProfessor(e) {
  e.preventDefault()

  if (materiasProfessor.length === 0) {
    alert('Selecione pelo menos uma matéria!')
    return
  }

  const matriculaExiste = professores.some(
    professor => professor.matricula === matriculaProfessor.trim()
  )

  if (matriculaExiste) {
    alert('Já existe um professor com essa matrícula!')
    return
  }

  setProfessores(atual => [
    ...atual,
    {
      id: Date.now(),
      matricula: matriculaProfessor.trim(),
      nome: nomeProfessor.trim(),
      cpf: cpfProfessor.trim(),
      email: emailProfessor.trim(),
      nascimento: nascimentoProfessor,
      telefone: telefoneProfessor.trim(),
      materias: [...materiasProfessor],
      series: [...seriesProfessor],
    },
  ])

  setMatriculaProfessor('')
  setNomeProfessor('')
  setCpfProfessor('')
  setEmailProfessor('')
  setNascimentoProfessor('')
  setTelefoneProfessor('')
  setMateriasProfessor([])
  setSeriesProfessor([])
}

  return (
    <div className="app">
      {/* MENU LATERAL */}
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-apple">🍎</span>
          <span>KLASSE</span>
        </div>

        <div className="sidebar-label">MENU PRINCIPAL</div>

        <nav className="navigation">
          {menuItems.map(item => (
            <button
              key={item.id}
              className={`nav-item ${
                paginaAtiva === item.id ? 'active' : ''
              }`}
              onClick={() => setPaginaAtiva(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="school-mark">K</div>
          <div>
            <strong>KLASSE</strong>
            <span>Sistema escolar</span>
          </div>
        </div>
      </aside>

      {/* CONTEÚDO PRINCIPAL */}
      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="breadcrumb">
              KLASSE / {pagina?.label.toUpperCase()}
            </span>
          </div>

          <div className="profile">
            <div className="profile-avatar">A</div>
            <div>
              <strong>Administrador</strong>
              <span>Gestão escolar</span>
            </div>
          </div>
        </header>

        {/* PÁGINA INICIAL */}
        {paginaAtiva === 'inicio' && (
          <section className="dashboard">
            <div className="welcome-card">
              <div>
                <span className="welcome-tag">BEM-VINDO AO KLASSE</span>
                <h2>
                  Educação organizada,
                  <br />
                  gestão simplificada.
                </h2>
                <p>
                  Gerencie sua escola com praticidade e carinho.
                </p>
              </div>

              <div className="welcome-apple">🍎</div>
            </div>

            <div className="section-heading">
              <div>
                <h2>Resumo escolar</h2>
                <p>Acompanhe as informações da sua escola.</p>
              </div>
            </div>

            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon peach">♙</div>
                <span>Alunos cadastrados</span>
                <strong>—</strong>
                <small>Registros no sistema</small>
              </div>

              <div className="stat-card">
                <div className="stat-icon green">♧</div>
                <span>Professores</span>
                <strong>{professores.length}</strong>
                <small>Profissionais cadastrados</small>
              </div>

              <div className="stat-card">
                <div className="stat-icon yellow">▦</div>
                <span>Matérias</span>
                <strong>{materias.length}</strong>
                <small>Disciplinas cadastradas</small>
              </div>

              <div className="stat-card">
                <div className="stat-icon pink">✓</div>
                <span>Frequência</span>
                <strong>—</strong>
                <small>Controle de presença</small>
              </div>
            </div>

            <div className="bottom-grid">
              <div className="content-card">
                <h3>Acesso rápido</h3>
                <p>Escolha uma área para começar.</p>

                <div className="quick-links">
                  <button onClick={() => setPaginaAtiva('alunos')}>
                    <span>♙</span>
                    <div>
                      <strong>Alunos</strong>
                      <small>Gerenciar cadastros</small>
                    </div>
                    <b>→</b>
                  </button>

                  <button onClick={() => setPaginaAtiva('professores')}>
                    <span>♧</span>
                    <div>
                      <strong>Professores</strong>
                      <small>Gerenciar equipe</small>
                    </div>
                    <b>→</b>
                  </button>

                  <button onClick={() => setPaginaAtiva('materias')}>
                    <span>📚</span>
                    <div>
                      <strong>Matérias</strong>
                      <small>Organizar disciplinas</small>
                    </div>
                    <b>→</b>
                  </button>
                </div>
              </div>

              <div className="content-card note-card">
                <span className="note-apple">🍎</span>
                <h3>Um espaço para aprender</h3>
                <p>
                  Tudo o que sua escola precisa, organizado em um só lugar.
                </p>
              </div>
            </div>
          </section>
        )}

        {/* PÁGINA DE MATÉRIAS */}
        {paginaAtiva === 'materias' && (
          <section className="materias-page">
            <div className="materias-intro">
              <div>
                <h2>Matérias escolares</h2>
                <p>
                  Cadastre e organize as disciplinas da escola.
                </p>
              </div>
            </div>

            <form className="materia-form" onSubmit={adicionarMateria}>
              <div className="form-field">
                <label>Nome da matéria</label>
                <input
                  value={novaMateria}
                  onChange={e => setNovaMateria(e.target.value)}
                  placeholder="Ex.: Matemática"
                  required
                />
              </div>

              <div className="form-field">
                <label>Aulas por semana</label>
                <input
                  type="number"
                  min="1"
                  max="30"
                  value={cargaHoraria}
                  onChange={e => setCargaHoraria(e.target.value)}
                  required
                />
              </div>

              <button type="submit" className="add-materia">
                + Adicionar matéria
              </button>
            </form>

            <div className="materias-list">
              <div className="materias-list-header">
                <div>
                  <h3>Disciplinas cadastradas</h3>
                  <p>{materias.length} matérias adicionadas</p>
                </div>
              </div>

              {materias.length === 0 ? (
                <div className="empty-materias">
                  <span>📚</span>
                  <h3>Nenhuma matéria cadastrada</h3>
                  <p>
                    Adicione a primeira disciplina para começar.
                  </p>
                </div>
              ) : (
                materias.map(materia => (
                  <div className="materia-item" key={materia.id}>
                    <div className="materia-symbol">📖</div>

                    <div className="materia-info">
                      <strong>{materia.nome}</strong>
                      <span>{materia.aulas} aulas por semana</span>
                    </div>

                    <button
                      type="button"
                      className="remove-materia"
                      onClick={() => excluirMateria(materia.id)}
                    >
                      Excluir
                    </button>
                  </div>
                ))
              )}
            </div>
          </section>
        )}

        {/* PÁGINA DE PROFESSORES */}
        {paginaAtiva === 'professores' && (
          <section className="materias-page">
            <div className="materias-intro">
              <div>
                <h2>Cadastro de professores</h2>
                <p>
                  Cadastre os profissionais e suas áreas de atuação.
                </p>
              </div>
            </div>

            <form
              className="professor-form"
              onSubmit={adicionarProfessor}
            >
              <div className="form-field">
                <label>Nome completo</label>
                <input
                  value={nomeProfessor}
                  onChange={e => setNomeProfessor(e.target.value)}
                  placeholder="Nome do professor"
                  required
                />
              </div>

              <div className="selection-section">
                <div className="form-field">
                  <label>Matrícula</label>
                  <input
                    value={matriculaProfessor}
                    onChange={e => setMatriculaProfessor(e.target.value)}
                    placeholder="Digite a matrícula"
                    required
                  />
                </div>

                <div className="form-field">
                  <label>CPF</label>
                  <input
                    value={cpfProfessor}
                    onChange={e => setCpfProfessor(e.target.value)}
                    placeholder="000.000.000-00"
                    required
                  />
                </div>

                <div className="form-field">
                  <label>E-mail</label>
                  <input
                    type="email"
                    value={emailProfessor}
                    onChange={e => setEmailProfessor(e.target.value)}
                    placeholder="professor@email.com"
                    required
                  />
                </div>

                <div className="form-field">
                  <label>Data de nascimento</label>
                  <input
                    type="date"
                    value={nascimentoProfessor}
                    onChange={e => setNascimentoProfessor(e.target.value)}
                    required
                  />
                </div>

                <div className="form-field">
                  <label>Telefone</label>
                  <input
                    type="tel"
                    value={telefoneProfessor}
                    onChange={e => setTelefoneProfessor(e.target.value)}
                    placeholder="(00) 00000-0000"
                    required
                  />
                </div>
                <label>Matérias que leciona *</label>

                {materias.length === 0 ? (
                  <p>
                    Cadastre matérias antes de adicionar professores.
                  </p>
                ) : (
                  <div className="selection-grid">
                    {materias.map(materia => (
                      <label
                        className="selection-option"
                        key={materia.id}
                      >
                        <input
                          type="checkbox"
                          checked={materiasProfessor.includes(materia.id)}
                          onChange={() => alternarMateria(materia.id)}
                        />
                        {materia.nome}
                      </label>
                    ))}
                  </div>
                )}
              </div>

              <div className="selection-section">
                <label>Séries em que pode atuar</label>
                <p className="field-hint">
                  Opcional. Se não selecionar nenhuma, não haverá
                  restrição por série.
                </p>

                <div className="selection-grid">
                  {series.map(serie => (
                    <label
                      className="selection-option"
                      key={serie}
                    >
                      <input
                        type="checkbox"
                        checked={seriesProfessor.includes(serie)}
                        onChange={() => alternarSerie(serie)}
                      />
                      {serie}
                    </label>
                  ))}
                </div>
              </div>

              <button type="submit" className="add-materia">
                + Cadastrar professor
              </button>
            </form>

            <div className="materias-list">
              <div className="materias-list-header">
                <div>
                  <h3>Professores cadastrados</h3>
                  <p>{professores.length} profissionais</p>
                </div>
              </div>

              {professores.length === 0 ? (
                <div className="empty-materias">
                  <span>👩‍🏫</span>
                  <h3>Nenhum professor cadastrado</h3>
                  <p>
                    Os professores adicionados aparecerão aqui.
                  </p>
                </div>
              ) : (
                professores.map(professor => (
                  <div
                    className="professor-item"
                    key={professor.id}
                  >
                    <div className="professor-avatar">P</div>

                    <div className="materia-info">
                      <strong>{professor.nome}</strong>
                      <span>Matrícula: {professor.matricula}</span>
                      <span>CPF: {professor.cpf}</span>
                      <span>E-mail: {professor.email}</span>
                      <span>Nascimento: {professor.nascimento}</span>
                      <span>Telefone: {professor.telefone}</span>

                      <span>
                        {professor.materias
                          .map(id =>
                            materias.find(m => m.id === id)?.nome
                          )
                          .filter(Boolean)
                          .join(', ')}
                      </span>

                      <div className="professor-tags">
                        {professor.series.length
                          ? professor.series.join(' · ')
                          : 'Sem restrição de série'}
                      </div>
                    </div>

                    <button
                      type="button"
                      className="remove-materia"
                      onClick={() => excluirProfessor(professor.id)}
                    >
                      Excluir
                    </button>
                  </div>
                ))
              )}
            </div>
          </section>
        )}

        {/* OUTRAS PÁGINAS */}
        {!['inicio', 'materias', 'professores'].includes(paginaAtiva) && (
          <section className="placeholder-page">
            <div className="placeholder-icon">{pagina?.icon}</div>
            <h2>{pagina?.label}</h2>
            <p>Estamos preparando esta área do KLASSE.</p>

            <button onClick={() => setPaginaAtiva('inicio')}>
              Voltar ao início
            </button>
          </section>
        )}
      </main>
    </div>
  )
}

export default App
