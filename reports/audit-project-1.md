# RELATÓRIO DE AUDITORIA ARQUITETURAL

Projeto: `code-smells-project`
Stack:   Python + Flask
Arquivos: 5 | ~500 linhas estimadas

## Resumo
CRITICAL: 4 | HIGH: 3 | MEDIUM: 1 | LOW: 2

## Achados

### [CRITICAL] Execução de SQL Arbitrário
- **Arquivo:** [app.py](../code-smells-project/app.py#L59-L79) (rota `/admin/query`)
- **Descrição:** A rota `/admin/query` aceita SQL livre enviado pelo cliente e o executa. Permite comprometimento total e direto do banco via HTTP.
- **Impacto:** Qualquer usuário pode ler, alterar ou destruir todo o banco de dados e possivelmente executar comandos no sistema operacional dependendo das permissões do SQLite.
- **Recomendação:** Remover completamente o endpoint de execução de query arbitrária do código de produção.

### [CRITICAL] Reset de DB sem Autenticação
- **Arquivo:** [app.py](../code-smells-project/app.py#L47-L57) (rota `/admin/reset-db`)
- **Descrição:** A rota `/admin/reset-db` limpa todas as tabelas sem nenhuma autenticação, gerando perda total de dados com uma única chamada externa.
- **Impacto:** Risco extremo de negação de serviço (DoS) e perda catastrófica de dados por chamadas não autorizadas.
- **Recomendação:** Remover o endpoint ou protegê-lo com autenticação robusta (ex: tokens admin em variáveis de ambiente).

### [CRITICAL] SQL Injection por Concatenação
- **Arquivo:** [models.py](../code-smells-project/models.py#L28) e [models.py](../code-smells-project/models.py#L47-L50)
- **Descrição:** Consultas SQL montadas concatenando strings diretamente com inputs de requisição de usuário, abrindo múltiplas falhas graves de SQL Injection.
- **Impacto:** Roubo de dados, bypass de autenticação e manipulação de registros de compras e usuários.
- **Recomendação:** Substituir todas as concatenações por queries parametrizadas (Prepared Statements).

### [CRITICAL] Senhas em Texto Puro / Exposição
- **Arquivo:** [database.py](../code-smells-project/database.py#L76-L79) e [models.py](../code-smells-project/models.py#L83)
- **Descrição:** Senhas salvas sem hashing no banco e retornadas diretamente em texto limpo no payload JSON de APIs públicas.
- **Impacto:** Vazamento massivo de credenciais de usuários e quebra total de privacidade.
- **Recomendação:** Implementar hashing seguro de senhas com salting (ex: bcrypt ou pbkdf2) e remover o campo de senha do payload de retorno.

---

### [HIGH] SECRET_KEY e DEBUG Hardcoded
- **Arquivo:** [app.py](../code-smells-project/app.py#L7-L8)
- **Descrição:** Chaves criptográficas do app salvas no código-fonte e modo debug ativo, facilitando falsificação de sessões e execução remota de código.
- **Impacto:** Risco de sequestro de sessão e vazamento de informações internas em telas de erro.
- **Recomendação:** Mover chaves e sinalizadores para variáveis de ambiente via arquivo `.env`.

### [HIGH] Healthcheck com Vazamento
- **Arquivo:** [controllers.py](../code-smells-project/controllers.py#L289-L290)
- **Descrição:** Endpoint `/health` expõe explicitamente a `SECRET_KEY` e caminhos físicos do sistema no payload.
- **Impacto:** Exposição de credenciais criptográficas cruciais e detalhes de infraestrutura para atacantes.
- **Recomendação:** Retornar apenas status básico de saúde ("status": "healthy") sem segredos.

### [HIGH] Conexão SQLite Global
- **Arquivo:** [database.py](../code-smells-project/database.py#L10)
- **Descrição:** Compartilhamento global de conexão SQLite entre threads paralelas do Flask com `check_same_thread=False`, gerando instabilidade de concorrência.
- **Impacto:** Erros frequentes de travamento de escrita e corrupção física de dados.
- **Recomendação:** Inicializar a conexão por requisição usando o contexto global `g` do Flask e fechá-la no app context teardown.

---

### [MEDIUM] Pedidos sem Rollback Transacional
- **Arquivo:** [models.py](../code-smells-project/models.py#L133-L169)
- **Descrição:** Ações sequenciais de criação de pedidos e decremento de estoque sem transação lógica; falhas deixam o banco inconsistente.
- **Impacto:** Pedidos criados sem itens correspondentes ou estoque decrementado incorretamente em falhas parciais.
- **Recomendação:** Encapsular o fluxo dentro de blocos de transação SQL com `commit` e `rollback`.

---

### [LOW] Constantes de Domínio Inline
- **Arquivo:** [controllers.py](../code-smells-project/controllers.py#L52)
- **Descrição:** Strings de categorias de produtos válidas escritas inline como strings literais de validação repetidas em vários arquivos.
- **Impacto:** Erros de digitação geram inconsistências difíceis de rastrear.
- **Recomendação:** Centralizar valores de validação de domínio em arquivo de configuração/constantes.

### [LOW] Porta Hardcoded
- **Arquivo:** [app.py](../code-smells-project/app.py#L90)
- **Descrição:** Porta TCP `5000` fixada estaticamente no bootstrap da aplicação.
- **Impacto:** Impede o deploy dinâmico do app em ambientes modernos de contêineres que definem a porta via variável de ambiente.
- **Recomendação:** Ler a porta de `os.environ.get("PORT", 5000)`.
