# ARCHITECTURE AUDIT REPORT

Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~800 lines of code

## Summary
CRITICAL: 4 | HIGH: 4 | MEDIUM: 2 | LOW: 2 | Total: 12 findings

## Findings

### [CRITICAL] Execução de SQL Arbitrário
- **File:** [app.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/app.py#L59-L79) (rota `/admin/query`)
- **Description:** A rota `/admin/query` aceita strings SQL cruas no corpo da requisição e executa diretamente no banco de dados sem nenhuma autenticação ou validação prévia.
- **Impact:** Comprometimento total do banco de dados (leitura, escrita, deleção) por qualquer cliente HTTP externo.
- **Recommendation:** Remover completamente a rota ou substituí-la por uma interface administrativa autenticada e tipada.

---

### [CRITICAL] Reset de DB sem Autenticação
- **File:** [app.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/app.py#L47-L57) (rota `/admin/reset-db`)
- **Description:** A rota `/admin/reset-db` limpa todas as tabelas do banco de dados sem verificar se o solicitante possui credenciais de administrador.
- **Impact:** Perda total de dados de produção por meio de um simples clique ou chamada de script malicioso externa.
- **Recommendation:** Exigir autenticação administrativa forte (JWT ou token estático no header) ou desativar em ambiente de produção.

---

### [CRITICAL] Queries por Concatenação de Strings (SQL Injection)
- **File:** [models.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py#L28) e [models.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py#L47-L50)
- **Description:** Consultas SQL criadas concatenando variáveis de input do usuário diretamente na string SQL (ex: `"SELECT * FROM produtos WHERE id = " + str(id)`).
- **Impact:** Vulnerabilidade de SQL Injection geral que permite vazamento de dados privados ou bypass de validações de login.
- **Recommendation:** Utilizar Prepared Statements com placeholders de interrogação `?` nas queries SQL.

---

### [CRITICAL] Senhas em Texto Puro e Exposição na API
- **File:** [database.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/database.py#L76-L79) e [models.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py#L83)
- **Description:** Senhas de usuários e do administrador gravadas como texto plano (sem hash) nas sementes do banco e expostas no dicionário JSON de retorno da API de listagem de usuários.
- **Impact:** Exposição grave de credenciais de usuários e administradores em caso de leitura física da base ou interceptação de rede.
- **Recommendation:** Armazenar hashes seguros de senha usando salting individual (ex: via pbkdf2 no Werkzeug) e omitir as senhas nas serializações de saída.

---

### [HIGH] SECRET_KEY e DEBUG=True Hardcoded
- **File:** [app.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/app.py#L7-L8)
- **Description:** Chave secreta de sessões (`SECRET_KEY`) e modo de depuração (`DEBUG`) chumbados no código do servidor Flask.
- **Impact:** Facilita ataques de falsificação de sessão e ativa o debugger interativo em produção em caso de exceções não tratadas, abrindo brecha de execução remota de código (RCE).
- **Recommendation:** Carregar valores de configurações dinamicamente via variáveis de ambiente com `os.getenv`.

---

### [HIGH] Rota de Healthcheck Expõe Segredos
- **File:** [controllers.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/controllers.py#L289-L290)
- **Description:** Rota `/health` retorna a chave secreta criptográfica do app e o caminho absoluto do banco de dados no JSON de resposta.
- **Impact:** Vazamento direto de segredos de infraestrutura e criptografia para qualquer usuário externo.
- **Recommendation:** Omitir chaves e caminhos locais da resposta HTTP.

---

### [HIGH] Conexão SQLite Global Compartilhada
- **File:** [database.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/database.py#L10)
- **Description:** Uso da propriedade `check_same_thread=False` para compartilhar uma conexão global única entre requisições simultâneas em threads separadas do Flask.
- **Impact:** Riscos graves de concorrência, travamento de escrita e corrupção física do arquivo `.db`.
- **Recommendation:** Instanciar conexões SQLite seguras e fechá-las ao final do contexto de cada requisição HTTP (utilizando `flask.g`).

---

### [HIGH] Fluxo de Pedido sem Rollback Transacional
- **File:** [models.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py#L133-L169)
- **Description:** A criação do pedido executa inserções no pedido, nos itens e updates no estoque do produto sequencialmente sem iniciar uma transação no banco.
- **Impact:** Em caso de exceção no meio do processo, o banco ficará em estado inconsistente (ex: estoque decrementado mas item não registrado).
- **Recommendation:** Agrupar todas as operações de escrita em uma transação com commit final e rollback em caso de falha.

---

### [MEDIUM] Mistura de Responsabilidades nos Controllers
- **File:** [controllers.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/controllers.py)
- **Description:** Métodos do controller controlam roteamento HTTP, validações de payload e lógicas de queries de domínio.
- **Impact:** Alto acúmulo de débito técnico e impossibilidade de criar testes unitários.
- **Recommendation:** Separar em controllers puros que delegam lógica a models ou classes de serviço correspondentes.

---

### [MEDIUM] Gargalo N+1 nas Consultas de Pedidos
- **File:** [models.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py#L171-L233)
- **Description:** Busca de dados de relacionamento (`itens_pedido` e `produtos`) executada individualmente dentro de loops para cada pedido listado.
- **Impact:** Atraso e sobrecarga de acessos ao banco de dados com a escala de pedidos no e-commerce.
- **Recommendation:** Reescrever a consulta usando um `LEFT JOIN` unificado e mapear a árvore no Python.

---

### [MEDIUM] Schema sem Constraints Relacionais
- **File:** [database.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/database.py#L37-L53)
- **Description:** Tabelas do banco de dados criadas sem declarações de chaves estrangeiras explícitas e restrições integras.
- **Impact:** Facilita inserção de dados inconsistentes e a criação de registros filhos órfãos.
- **Recommendation:** Ativar suporte a Foreign Keys no SQLite (`PRAGMA foreign_keys = ON`) e declarar as constraints de chave no schema SQL.

---

### [LOW] Constantes de Domínio Repetidas Inline
- **File:** [controllers.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/controllers.py#L52)
- **Description:** Lista de categorias válidas chumbada diretamente na validação do controller como literal.
- **Impact:** A manutenção exige modificar múltiplos arquivos caso o catálogo mude.
- **Recommendation:** Concentrar em constantes centralizadas na configuração ou no modelo de domínio.
