# Desafio de Refatoração Arquitetural Automatizada (MVC)

Este repositório contém a implementação de uma Skill de IA para refatoração arquitetural para o padrão MVC, conforme os requisitos do desafio.

## A) Análise Manual

### 1. Projeto `code-smells-project` (Python/Flask)

1. **CRITICAL: SQL Injection em models.py**
   - **Arquivo/Linhas:** [models.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py#L28) e [models.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py#L47-L50)
   - **Justificativa:** Concatenação direta de parâmetros de entrada do usuário nas strings de consulta SQL. Permite execução de queries maliciosas e vazamento/exclusão de dados.
   
2. **CRITICAL: Backdoor de Execução de SQL Arbitrário**
   - **Arquivo/Linhas:** [app.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/app.py#L59-L79)
   - **Justificativa:** Rota `/admin/query` recebe SQL arbitrário no body e executa diretamente no banco de dados sem autenticação. Falha de segurança máxima (RCE / bypass total).

3. **CRITICAL/HIGH: Credenciais Hardcoded e Exposição de Segredos**
   - **Arquivo/Linhas:** [app.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/app.py#L7) e [controllers.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/controllers.py#L289-L290)
   - **Justificativa:** `SECRET_KEY` definida diretamente no código e exposta publicamente na resposta da rota `/health`. Facilita decodificação de cookies e ataques de personificação.

4. **HIGH/MEDIUM: Gargalo de Performance (Queries N+1)**
   - **Arquivo/Linhas:** [models.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py#L174-L201) e [models.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/models.py#L203-L233)
   - **Justificativa:** Métodos `get_pedidos_usuario` e `get_todos_pedidos` realizam uma query para obter os pedidos, outra query para obter os itens de cada pedido, e mais uma para obter o nome do produto de cada item, gerando centenas de conexões desnecessárias.

5. **MEDIUM: Insegurança no Compartilhamento de Conexão com SQLite**
   - **Arquivo/Linhas:** [database.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/database.py#L10)
   - **Justificativa:** Uso do parâmetro `check_same_thread=False` para compartilhar uma conexão global única entre requisições concorrentes no Flask, o que pode causar concorrência de escrita e corrupção no banco de dados.

6. **LOW: Hardcoded Arrays e Magic Strings**
   - **Arquivo/Linhas:** [controllers.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/controllers.py#L52)
   - **Justificativa:** Lista de categorias válidas chumbada dentro de lógica do controller em vez de constantes ou modelo.

7. **LOW: Efeitos Colaterais Acoplados**
   - **Arquivo/Linhas:** [controllers.py](file:///g:/Projects/mba-ia-refactor-projects-skill/code-smells-project/controllers.py#L208-L210)
   - **Justificativa:** Prints de simulação de envio de e-mail, SMS e Push executados diretamente dentro do controller ao criar pedido, violando separação de responsabilidades.

---

### 2. Projeto `ecommerce-api-legacy` (Node.js/Express)

1. **CRITICAL: Monolito God Class**
   - **Arquivo/Linhas:** [AppManager.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js)
   - **Justificativa:** A classe acopla inicialização de banco, configuração de rotas HTTP Express, lógica de checkout/negócio e manipulação de banco de dados diretamente. Impede testes unitários e viola o SRP.

2. **CRITICAL: Criptografia Fraca e Customizada (Homegrown)**
   - **Arquivo/Linhas:** [utils.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/utils.js#L17-L23)
   - **Justificativa:** Função `badCrypto` faz loop e base64 incompleto, resultando em hashes curtos e facilmente decifráveis para senhas de usuários.

3. **CRITICAL/HIGH: Segredos de Infraestrutura Chumbados**
   - **Arquivo/Linhas:** [utils.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/utils.js#L1-L7)
   - **Justificativa:** Chave de gateway de pagamento, SMTP e senhas de banco salvas como constantes em arquivo de controle comum (`utils.js`).

4. **HIGH/MEDIUM: Estado Global Mutável**
   - **Arquivo/Linhas:** [utils.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/utils.js#L9-L10)
   - **Justificativa:** Variáveis `globalCache` e `totalRevenue` mantidas em memória global e alteradas de forma concorrente em requisições de API, gerando riscos de corrida e inconsistência de dados no reinício da app.

5. **HIGH/MEDIUM: Callback Hell e Gargalo N+1**
   - **Arquivo/Linhas:** [AppManager.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L80-L129)
   - **Justificativa:** `/api/admin/financial-report` executa queries aninhadas recursivamente para obter cursos, matrículas, usuários e pagamentos, gerando callback hell severo e problemas de performance N+1.

6. **MEDIUM: Violação de Integridade Referencial na Exclusão**
   - **Arquivo/Linhas:** [AppManager.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L131-L137)
   - **Justificativa:** Rota `/api/users/:id` apaga o registro do usuário sem remover suas matrículas ou pagamentos vinculados, deixando chaves órfãs e dados sujos no banco.

7. **LOW: Regras de Validação de Cartão Chumbadas**
   - **Arquivo/Linhas:** [AppManager.js](file:///g:/Projects/mba-ia-refactor-projects-skill/ecommerce-api-legacy/src/AppManager.js#L46)
   - **Justificativa:** Status do pagamento determinado apenas se número do cartão inicia com "4".

---

### 3. Projeto `task-manager-api` (Python/Flask)

1. **CRITICAL: Algoritmo de Hash MD5 para Senhas**
   - **Arquivo/Linhas:** [user.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/models/user.py#L27-L32)
   - **Justificativa:** Uso do algoritmo MD5 para hashing de senhas. MD5 é criptograficamente quebrado, vulnerável a colisões e ataques de dicionário/rainbow tables.

2. **CRITICAL/HIGH: Senha de Servidor SMTP Hardcoded**
   - **Arquivo/Linhas:** [notification_service.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/services/notification_service.py#L10)
   - **Justificativa:** A senha e o e-mail de acesso ao SMTP (`senha123`) estão salvos diretamente no código-fonte do serviço.

3. **HIGH/MEDIUM: Gargalo N+1 na Rota de Tasks**
   - **Arquivo/Linhas:** [task_routes.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/routes/task_routes.py#L41-L57)
   - **Justificativa:** Na rota GET `/tasks`, o código faz queries individuais de relacionamento chamando `User.query.get` e `Category.query.get` para cada task no loop, em vez de usar `joinedload` ou joins explícitos.

4. **HIGH/MEDIUM: Processamento de SMTP Bloqueante na Thread Principal**
   - **Arquivo/Linhas:** [notification_service.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/services/notification_service.py#L15-L20)
   - **Justificativa:** Chamada ao SMTP externo é realizada de forma síncrona dentro da requisição HTTP principal. Se o servidor SMTP demorar a responder, a requisição inteira da API trava até dar timeout.

5. **MEDIUM: Blocos de Exceção Genéricos (Bare Except)**
   - **Arquivo/Linhas:** [task_routes.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/routes/task_routes.py#L62-L63)
   - **Justificativa:** Captura genérica `except:` sem especificar a exceção, ocultando a causa real de eventuais falhas internas e dificultando o debugging.

6. **LOW: Geração de Token Estático Inseguro**
   - **Arquivo/Linhas:** [user_routes.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/routes/user_routes.py#L210)
   - **Justificativa:** O endpoint de login gera um token estático trivial concatenando o ID do usuário (`'fake-jwt-token-' + str(user.id)`), que é previsível e inseguro.

7. **LOW: Duplicação de Regras de Validação**
   - **Arquivo/Linhas:** [task.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/models/task.py#L38-L48) e [helpers.py](file:///g:/Projects/mba-ia-refactor-projects-skill/task-manager-api/utils/helpers.py#L75-L89)
   - **Justificativa:** Validação de status e prioridades duplicada nas regras internas do modelo de dados e nos métodos auxiliares em `helpers.py`.

---

## B) Construção da Skill

### Decisões de Design
*A ser preenchido durante a criação da skill.*

### Catálogo de Anti-patterns
*A ser preenchido durante a criação da skill.*

### Como Garantimos que a Skill é Agnóstica
*A ser preenchido durante a criação da skill.*

### Desafios Encontrados e Resoluções
*A ser preenchido durante a criação da skill.*

---

## C) Resultados

### Resumo dos Relatórios de Auditoria
| Projeto | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---|---|---|---|---|---|
| `code-smells-project` | - | - | - | - | - |
| `ecommerce-api-legacy` | - | - | - | - | - |
| `task-manager-api` | - | - | - | - | - |

### Comparação Antes/Depois da Estrutura

#### `code-smells-project`
```
Antes:
(estrutura original)

Depois:
(estrutura refatorada)
```

#### `ecommerce-api-legacy`
```
Antes:
(estrutura original)

Depois:
(estrutura refatorada)
```

#### `task-manager-api`
```
Antes:
(estrutura original)

Depois:
(estrutura refatorada)
```

### Checklist de Validação

#### Projeto 1: `code-smells-project`
- [ ] Fase 1: Linguagem detectada corretamente
- [ ] Fase 1: Framework detectado corretamente
- [ ] Fase 1: Domínio da aplicação descrito corretamente
- [ ] Fase 1: Número de arquivos analisados condiz com a realidade
- [ ] Fase 2: Relatório segue o template definido nos arquivos de referência
- [ ] Fase 2: Cada finding tem arquivo e linhas exatos
- [ ] Fase 2: Findings ordenados por severidade (CRITICAL -> LOW)
- [ ] Fase 2: Mínimo de 5 findings identificados
- [ ] Fase 2: Detecção de APIs deprecated incluída (se aplicável)
- [ ] Fase 2: Skill pausa e pede confirmação antes da Fase 3
- [ ] Fase 3: Estrutura de diretórios segue padrão MVC
- [ ] Fase 3: Configuração extraída para módulo de config (sem hardcoded)
- [ ] Fase 3: Models criados para abstrair dados
- [ ] Fase 3: Views/Routes separadas para visualização ou roteamento
- [ ] Fase 3: Controllers concentram o fluxo da aplicação
- [ ] Fase 3: Error handling centralizado
- [ ] Fase 3: Entry point claro
- [ ] Fase 3: Aplicação inicia sem erros
- [ ] Fase 3: Endpoints originais respondem corretamente

#### Projeto 2: `ecommerce-api-legacy`
- [ ] Fase 1: Linguagem detectada corretamente
- [ ] Fase 1: Framework detectado corretamente
- [ ] Fase 1: Domínio da aplicação descrito corretamente
- [ ] Fase 1: Número de arquivos analisados condiz com a realidade
- [ ] Fase 2: Relatório segue o template definido nos arquivos de referência
- [ ] Fase 2: Cada finding tem arquivo e linhas exatos
- [ ] Fase 2: Findings ordenados por severidade (CRITICAL -> LOW)
- [ ] Fase 2: Mínimo de 5 findings identificados
- [ ] Fase 2: Detecção de APIs deprecated incluída (se aplicável)
- [ ] Fase 2: Skill pausa e pede confirmação antes da Fase 3
- [ ] Fase 3: Estrutura de diretórios segue padrão MVC
- [ ] Fase 3: Configuração extraída para módulo de config (sem hardcoded)
- [ ] Fase 3: Models criados para abstrair dados
- [ ] Fase 3: Views/Routes separadas para visualização ou roteamento
- [ ] Fase 3: Controllers concentram o fluxo da aplicação
- [ ] Fase 3: Error handling centralizado
- [ ] Fase 3: Entry point claro
- [ ] Fase 3: Aplicação inicia sem erros
- [ ] Fase 3: Endpoints originais respondem corretamente

#### Projeto 3: `task-manager-api`
- [ ] Fase 1: Linguagem detectada corretamente
- [ ] Fase 1: Framework detectado corretamente
- [ ] Fase 1: Domínio da aplicação descrito corretamente
- [ ] Fase 1: Número de arquivos analisados condiz com a realidade
- [ ] Fase 2: Relatório segue o template definido nos arquivos de referência
- [ ] Fase 2: Cada finding tem arquivo e linhas exatos
- [ ] Fase 2: Findings ordenados por severidade (CRITICAL -> LOW)
- [ ] Fase 2: Mínimo de 5 findings identificados
- [ ] Fase 2: Detecção de APIs deprecated incluída (se aplicável)
- [ ] Fase 2: Skill pausa e pede confirmação antes da Fase 3
- [ ] Fase 3: Estrutura de diretórios segue padrão MVC
- [ ] Fase 3: Configuração extraída para módulo de config (sem hardcoded)
- [ ] Fase 3: Models criados para abstrair dados
- [ ] Fase 3: Views/Routes separadas para visualização ou roteamento
- [ ] Fase 3: Controllers concentram o fluxo da aplicação
- [ ] Fase 3: Error handling centralizado
- [ ] Fase 3: Entry point claro
- [ ] Fase 3: Aplicação inicia sem erros
- [ ] Fase 3: Endpoints originais respondem corretamente
