# RELATÓRIO DE AUDITORIA ARQUITETURAL

Projeto: `task-manager-api`
Stack:   Python + Flask
Arquivos: 11 | ~1163 linhas estimadas

## Resumo
CRITICAL: 3 | HIGH: 3 | MEDIUM: 2 | LOW: 2

## Achados

### [CRITICAL] Criptografia Insegura (Insecure Cryptography)
- **Arquivo:** [models/user.py](../task-manager-api/models/user.py#L29-L32)
- **Descrição:** O armazenamento de senhas dos usuários é realizado utilizando hash MD5 puro sem salt (`hashlib.md5(pwd.encode()).hexdigest()`), que é um algoritmo legado e criptograficamente quebrado.
- **Impacto:** Em caso de vazamento ou exposição da base de dados, as senhas dos usuários podem ser facilmente decifradas por ataques de dicionário ou tabelas rainbow.
- **Recomendação:** Substituir o algoritmo de hashing MD5 pela função segura PBKDF2 com salt, utilizando `generate_password_hash` e `check_password_hash` fornecidas nativamente pelo pacote `werkzeug.security`.

### [CRITICAL] Ilusão de Autenticação / Tokens Falsos (Auth Illusion / Fake Security Tokens)
- **Arquivo:** [routes/user_routes.py](../task-manager-api/routes/user_routes.py#L207-L210)
- **Descrição:** O endpoint `/login` gera um token estático sem assinatura real ou criptografia no formato `fake-jwt-token-` concatenado ao ID do usuário. Além disso, as rotas críticas de gerenciamento de tarefas, categorias e relatórios não realizam nenhuma validação ou checagem de autorização/autenticação.
- **Impacto:** Ausência de controle de acesso real. Qualquer requisição HTTP pode acessar ou modificar tarefas e dados sensíveis de qualquer usuário simplesmente informando IDs, sem que haja validação de autenticação ou propriedade dos recursos.
- **Recomendação:** Implementar um middleware/decorator de autenticação (`token_required`) que valide tokens criptograficamente assinados (como JWT ou serialização segura do `itsdangerous`) e aplicá-lo em todas as rotas sensíveis do sistema.

### [CRITICAL] Segredos Chumbados no Código (Hardcoded Secrets)
- **Arquivo:** [app.py](../task-manager-api/app.py#L13) e [services/notification_service.py](../task-manager-api/services/notification_service.py#L9-L10)
- **Descrição:** A chave secreta da aplicação (`SECRET_KEY = 'super-secret-key-123'`) e as credenciais SMTP do serviço de e-mail (`email_user = 'taskmanager@gmail.com'`, `email_password = 'senha123'`) estão declaradas e expostas de forma estática diretamente nos arquivos de código-fonte.
- **Impacto:** Vulnerabilidade grave de segurança. Qualquer pessoa com acesso ao repositório de código terá acesso às credenciais de e-mail do sistema e poderá comprometer a assinatura e integridade de sessões.
- **Recomendação:** Externalizar todos os segredos para variáveis de ambiente usando o pacote `python-dotenv` e criar um arquivo `.env` baseado no modelo existente `.env.example`.

---

### [HIGH] Gargalo de Performance de Consultas N+1 (Query N+1 Performance Bottleneck)
- **Arquivo:** [routes/task_routes.py](../task-manager-api/routes/task_routes.py#L41-L58) e [routes/report_routes.py](../task-manager-api/routes/report_routes.py#L55-L68)
- **Descrição:**
  1. Ao listar tarefas no endpoint `/tasks`, o sistema executa uma nova consulta no banco de dados para buscar o usuário correspondente (`User.query.get(t.user_id)`) e a categoria (`Category.query.get(t.category_id)`) para cada tarefa individual em um loop.
  2. No relatório consolidado (`/reports/summary`), o sistema executa uma consulta de busca de tarefas para cada usuário cadastrado para compilar estatísticas.
  3. Ao listar as categorias (`/categories`), o código executa uma query de contagem de tarefas para cada categoria retornada.
- **Impacto:** Degradação severa e exponencial da latência e da performance da API à medida que o número de tarefas e usuários cresce na base de dados, gerando centenas ou milhares de requisições desnecessárias ao banco de dados.
- **Recomendação:** Otimizar o carregamento das relações utilizando JOINs adequados (`joinedload` do SQLAlchemy) na consulta principal de tarefas, permitindo obter as informações em uma única query (Eager Loading). Para relatórios e contagens, realizar queries agregadoras agrupadas com SQL (`db.func.count`).

### [HIGH] Falha de Integridade Referencial na Exclusão (Referential Integrity Failure)
- **Arquivo:** [routes/report_routes.py](../task-manager-api/routes/report_routes.py#L211-L223)
- **Descrição:** A rota de exclusão de categoria (`/categories/<int:cat_id>`) remove o registro da categoria do banco de dados sem gerenciar as tarefas associadas a ela ou garantir que chaves estrangeiras não fiquem órfãs na tabela de tarefas.
- **Impacto:** Risco de corrupção ou inconsistência referencial no banco de dados, deixando tarefas com o campo `category_id` apontando para chaves que não existem mais.
- **Recomendação:** Adicionar restrições de integridade referencial ou gerenciar explicitamente a desassociação (definindo `category_id = None`) das tarefas associadas antes de efetivar a remoção da categoria no banco de dados.

### [HIGH] Efeitos Colaterais no Startup da Aplicação (Accidental Complexity / Startup Side-Effects)
- **Arquivo:** [app.py](../task-manager-api/app.py#L30-L31)
- **Descrição:** O script executa de forma síncrona `db.create_all()` a cada inicialização (boot) do servidor web no arquivo de entrada da aplicação.
- **Impacto:** Lentidão na inicialização da aplicação e riscos operacionais em ambientes de produção de alteração/bloqueio indesejado de esquemas de banco de dados ativos.
- **Recomendação:** Remover `db.create_all()` do arquivo de execução principal (`app.py`), delegando a criação inicial a scripts dedicados de migração de banco de dados ou ferramentas como Alembic.

---

### [MEDIUM] Falta de Camada de Controle e Lógica de Negócios Acoplada (God Class / Lack of separation)
- **Arquivo:** [routes/user_routes.py](../task-manager-api/routes/user_routes.py#L10-L211) e [routes/task_routes.py](../task-manager-api/routes/task_routes.py#L11-L299)
- **Descrição:** Toda a lógica de negócios, controle de fluxo, validações de entrada e tratamento de resposta HTTP está misturada e implementada diretamente nas rotas, mantendo a pasta `controllers/` vazia.
- **Impacto:** Código acoplado e de baixa manutenibilidade, dificultando a implementação de testes unitários isolados da camada HTTP.
- **Recomendação:** Separar adequadamente as responsabilidades movendo a lógica de tratamento e negócio das rotas para controladores específicos na pasta `src/controllers/`, deixando os arquivos de rotas responsáveis apenas por mapear endpoints HTTP e validações de tipos básicos.

### [MEDIUM] Captura Silenciosa e Genérica de Exceções (Cover Your Assets)
- **Arquivo:** [routes/task_routes.py](../task-manager-api/routes/task_routes.py#L62) e [routes/user_routes.py](../task-manager-api/routes/user_routes.py#L130)
- **Descrição:** Uso excessivo de capturas de exceções totalmente genéricas (`except:`) que ocultam a causa original do erro e retornam apenas mensagens de erro genéricas como `{"error": "Erro interno"}`.
- **Impacto:** Dificulta a depuração e monitoração de falhas em produção (deixando a equipe de desenvolvimento cega sobre bugs silenciosos ou problemas de conexão no banco).
- **Recomendação:** Capturar exceções de forma granular e implementar um Error Handler centralizado (Middleware/Decorator) que loge a pilha de erros internamente e responda com mensagens HTTP apropriadas.

---

### [LOW] Uso de Valores Literais Chumbados (Magic Strings)
- **Arquivo:** [routes/user_routes.py](../task-manager-api/routes/user_routes.py#L71) e [routes/task_routes.py](../task-manager-api/routes/task_routes.py#L110)
- **Descrição:** Regras de negócio e validações baseiam-se em valores de string chumbados diretamente no código (ex: roles de usuário `'user'`, `'admin'`, `'manager'` e status de tarefas `'pending'`, `'in_progress'`, `'done'`, `'cancelled'`).
- **Impacto:** Alto risco de bugs por pequenos erros de digitação e acoplamento desnecessário na manutenção ou adição de novas categorias/status.
- **Recomendação:** Centralizar as constantes e tipos válidos em um arquivo de configuração centralizado (ex: `src/config/constants.py`) ou declará-las como constantes estáticas nos próprios Models correspondentes.

### [LOW] Porta e Modo de Depuração Hardcoded (Hardcoded Port)
- **Arquivo:** [app.py](../task-manager-api/app.py#L34)
- **Descrição:** O bootstrap da aplicação define a porta `5000` e o modo de depuração `debug=True` de forma fixa diretamente no código.
- **Impacto:** Limita a flexibilidade de implantação em diferentes ambientes de nuvem ou em contêineres Docker que necessitam de parametrização dinâmica de portas.
- **Recomendação:** Alterar para ler as configurações de porta e modo de debug a partir de variáveis de ambiente com fallbacks adequados.
