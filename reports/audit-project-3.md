# RELATÓRIO DE AUDITORIA ARQUITETURAL

Projeto: `task-manager-api`
Stack:   Python + Flask
Arquivos: 11 | ~1163 linhas estimadas

## Resumo
CRITICAL: 3 | HIGH: 5 | MEDIUM: 1 | LOW: 2

## Achados

### [CRITICAL] Insecure / Custom Cryptography
- **Arquivo:** [models/user.py](../task-manager-api/models/user.py#L29-L32)
- **Descrição:** Uso de hash MD5 sem salt para armazenar e comparar senhas de usuários (`hashlib.md5(pwd.encode()).hexdigest()`).
- **Impacto:** Vulnerabilidade severa. Senhas são facilmente decifradas por ataques de força bruta ou tabelas rainbow se a base de dados for comprometida.
- **Recomendação:** Utilizar algoritmos de hash seguros com salt aleatório por padrão (ex: `pbkdf2` via `werkzeug.security.generate_password_hash` e `check_password_hash`).

### [CRITICAL] Auth Illusion / Fake Security Tokens
- **Arquivo:** [routes/user_routes.py](../task-manager-api/routes/user_routes.py#L210)
- **Descrição:** Retorno de um token de autenticação estático e sem criptografia real/assinatura (`fake-jwt-token-` + user ID). Além disso, não há mecanismos de validação ou middlewares que barrem o acesso de rotas sensíveis a usuários não autenticados.
- **Impacto:** Qualquer usuário pode forjar um token ou acessar as rotas restritas sem validação real, comprometendo a integridade da aplicação.
- **Recomendação:** Substituir o token falso por autenticação JWT real (assinada criptograficamente) e criar um decorator/middleware de autenticação para validar os tokens nas rotas sensíveis.

### [CRITICAL] Hardcoded Secrets & Info Leakage
- **Arquivo:** [app.py](../task-manager-api/app.py#L13) e [services/notification_service.py](../task-manager-api/services/notification_service.py#L9-L10)
- **Descrição:** Chave secreta da aplicação (`SECRET_KEY`) e credenciais de e-mail (usuário e senha do SMTP da conta `taskmanager@gmail.com`) salvas diretamente no código de inicialização.
- **Impacto:** Vazamento de informações e segredos confidenciais em repositórios Git, facilitando o comprometimento de servidores e contas de e-mail.
- **Recomendação:** Extrair os segredos para variáveis de ambiente usando o `python-dotenv` e buscar essas variáveis via `os.getenv()`.

---

### [HIGH] The Blob / God Class
- **Arquivo:** [routes/task_routes.py](../task-manager-api/routes/task_routes.py#L1), [routes/user_routes.py](../task-manager-api/routes/user_routes.py#L1) e [routes/report_routes.py](../task-manager-api/routes/report_routes.py#L1)
- **Descrição:** Os arquivos de rotas concentram lógica de roteamento HTTP, validações de formato e dados, lógica de negócio (ex: cálculo de atraso de tarefa, hashes de senha) e manipulação direta de banco de dados (`db.session.commit()`).
- **Impacto:** Código acoplado, difícil de manter, testar de forma isolada ou reutilizar.
- **Recomendação:** Refatorar as rotas para o padrão MVC, transferindo a lógica de orquestração e negócio para os *Controllers* e a lógica de persistência e regras intrínsecas aos dados para os *Models*.

### [HIGH] Query N+1 Performance Bottleneck
- **Arquivo:** [routes/task_routes.py](../task-manager-api/routes/task_routes.py#L41-L58), [routes/report_routes.py](../task-manager-api/routes/report_routes.py#L55-L68), [routes/report_routes.py](../task-manager-api/routes/report_routes.py#L163) e [routes/user_routes.py](../task-manager-api/routes/user_routes.py#L22)
- **Descrição:** 
  - Em `get_tasks` de `task_routes.py`, realiza-se `User.query.get(t.user_id)` e `Category.query.get(t.category_id)` em um laço de repetição para cada tarefa.
  - Em `summary_report` de `report_routes.py`, faz `Task.query.filter_by(user_id=u.id).all()` para cada usuário.
  - Em `get_categories` de `report_routes.py`, executa-se uma query `count` de tarefas por categoria em um loop.
  - Em `get_users` de `user_routes.py`, lê-se a relação `u.tasks` em loop.
- **Impacto:** Execução desnecessária de centenas ou milhares de queries sequenciais (latência e carga excessiva no banco de dados).
- **Recomendação:** Utilizar técnicas de carregamento otimizado (Eager Loading) com `joinedload` ou efetuar consultas com `JOIN` agrupado para trazer todos os dados correlacionados em uma única query.

### [HIGH] Stovepipe System / Lack of Cohesive Domains
- **Arquivo:** [routes/report_routes.py](../task-manager-api/routes/report_routes.py#L157-L223)
- **Descrição:** Definição das rotas CRUD de categorias (`/categories`) inseridas dentro do domínio de relatórios (`report_routes.py`).
- **Impacto:** Confusão de domínios, dificultando a localização e manutenção de código de categorias.
- **Recomendação:** Separar as rotas de categoria para um Blueprint/arquivo próprio (`routes/category_routes.py`) e seu respectivo controlador (`controllers/category_controller.py`).

### [HIGH] Accidental Complexity / Startup Side-Effects
- **Arquivo:** [app.py](../task-manager-api/app.py#L30-L31)
- **Descrição:** Execução de `db.create_all()` diretamente na inicialização do servidor ao importar o módulo da aplicação.
- **Impacto:** Risco operacional em ambientes de produção onde o esquema deve ser gerenciado por migrations (ex: Flask-Migrate/Alembic) e pode causar lentidão na inicialização da aplicação em ambiente de múltiplos workers.
- **Recomendação:** Remover o `db.create_all()` do startup automático da aplicação e usar um comando ou script separado para inicializar a estrutura do banco de dados (ex: no `seed.py`).

### [HIGH] Referential Integrity Failure / Cascade Deleter
- **Arquivo:** [routes/user_routes.py](../task-manager-api/routes/user_routes.py#L140-L142)
- **Descrição:** Exclusão manual de tarefas de um usuário feita em um laço no nível de rota (`delete_user`).
- **Impacto:** Acoplamento de rotas e risco de integridade se tarefas forem adicionadas e órfãs se a exclusão manual falhar ou se novas relações com usuário forem estabelecidas no futuro.
- **Recomendação:** Configurar o relacionamento no Model do SQLAlchemy para propagar a deleção automaticamente (`cascade="all, delete-orphan"` no Model `User`).

---

### [MEDIUM] Cover Your Assets / Generic Exception Swallowing
- **Arquivo:** [routes/task_routes.py](../task-manager-api/routes/task_routes.py#L62), [routes/user_routes.py](../task-manager-api/routes/user_routes.py#L130) e [routes/report_routes.py](../task-manager-api/routes/report_routes.py#L186)
- **Descrição:** Blocos `except:` genéricos sem especificação do erro e que silenciam a exceção, retornando apenas mensagens como `{"error": "Erro interno"}` ou `{"error": "Erro ao atualizar"}` sem fazer qualquer log do erro real.
- **Impacto:** Dificuldade extrema para depurar bugs e monitorar erros do sistema em produção.
- **Recomendação:** Capturar exceções mais específicas ou, nos blocos genéricos, logar o traceback completo do erro no console/serviço de logging antes de responder ao cliente, ou tratar globalmente via middleware.

---

### [LOW] Inline Domain Constants / Magic Strings
- **Arquivo:** [routes/user_routes.py](../task-manager-api/routes/user_routes.py#L71) e [routes/task_routes.py](../task-manager-api/routes/task_routes.py#L110)
- **Descrição:** Strings mágicas inseridas diretamente no código para validação de status de tarefas (`['pending', 'in_progress', 'done', 'cancelled']`) e perfis de usuário (`['user', 'admin', 'manager']`).
- **Impacto:** Dificuldade de manutenção e aumento da possibilidade de bugs de digitação inconsistente em diferentes pontos do projeto.
- **Recomendação:** Centralizar estes valores em constantes globais no arquivo de configurações da aplicação (ex: em `src/config/settings.py` ou `src/config/constants.py`).

### [LOW] Hardcoded Port / Configuration Fallback
- **Arquivo:** [app.py](../task-manager-api/app.py#L34)
- **Descrição:** Configuração de porta `5000` e modo `debug=True` fixos no bootstrap da aplicação.
- **Impacto:** Restringe a portabilidade do aplicativo em ambientes de nuvem ou conteinerização onde a porta TCP deve ser configurada externamente.
- **Recomendação:** Carregar a porta e o modo de depuração de variáveis de ambiente (`PORT` e `FLASK_DEBUG`) com fallbacks seguros.
