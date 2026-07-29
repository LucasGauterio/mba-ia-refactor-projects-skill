# RELATÓRIO DE AUDITORIA ARQUITETURAL

Projeto: `ecommerce-api-legacy`
Stack:   JavaScript (Node.js) + Express
Arquivos: 3 | ~183 linhas estimadas

## Resumo
CRITICAL: 3 | HIGH: 3 | MEDIUM: 1 | LOW: 2

## Achados

### [CRITICAL] Insecure / Custom Cryptography
- **Arquivo:** [utils.js](../ecommerce-api-legacy/src/utils.js#L17-L23) e [AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L68)
- **Descrição:** Armazenamento e manipulação de senhas usando um algoritmo personalizado (`badCrypto`) baseado em transformações cíclicas de strings em base64. O fluxo também fornece uma senha estática padrão (`"123456"`) caso nenhuma senha seja fornecida.
- **Impacto:** A criptografia customizada é extremamente fraca e trivial de ser revertida ou quebrada por ataques de força bruta. Se o banco de dados for exposto, todas as senhas dos usuários estarão comprometidas.
- **Recomendação:** Substituir a criptografia caseira por um algoritmo moderno e robusto baseado em salt único por usuário (ex: PBKDF2 ou bcrypt nativo do Node.js através da biblioteca `crypto`).

### [CRITICAL] Hardcoded Secrets & Info Leakage
- **Arquivo:** [utils.js](../ecommerce-api-legacy/src/utils.js#L2-L5) e [AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L45)
- **Descrição:** Credenciais administrativas de banco de dados, chaves secretas de gateways de pagamento e contas de SMTP configuradas como valores literais estáticos (chumbados) diretamente no código-fonte. Além disso, existe um log de console (`console.log`) que exibe dados de cartões de crédito e chaves privadas do gateway de pagamento durante a execução do checkout.
- **Impacto:** Vazamento de segredos para repositórios públicos e logs de depuração. Comprometimento de gateways financeiros de produção e servidores de email.
- **Recomendação:** Mover todos os segredos para variáveis de ambiente carregadas via arquivo `.env` (ex. usando `process.env`) e remover logs de console que expõem informações sensíveis de cartões de crédito e chaves privadas.

### [CRITICAL] The Blob / God Class
- **Arquivo:** [AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L1-L139)
- **Descrição:** A classe `AppManager` atua como um monolito completo que gerencia a inicialização da conexão com o banco de dados SQLite em memória, definição do esquema relacional, inserção de dados estáticos iniciais, definição de rotas do Express, tratamento de requisições HTTP e orquestração de toda a lógica de negócio do sistema.
- **Impacto:** Acoplamento extremamente elevado, impossibilidade de criar testes unitários isolados, complexidade excessiva de manutenção e alto risco de introdução de novos bugs ao alterar qualquer funcionalidade elementar.
- **Recomendação:** Refatorar a aplicação dividindo-a nas camadas clássicas de MVC (Model-View-Controller). Mover as configurações para `src/config/`, os modelos de acesso a banco para `src/models/`, a lógica de negócio para `src/controllers/` e os rotas para `src/routes/`.

---

### [HIGH] Query N+1 Performance Bottleneck
- **Arquivo:** [AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L80-L129)
- **Descrição:** O endpoint `/api/admin/financial-report` faz uma busca por todos os cursos cadastrados e, para cada curso, dispara de forma aninhada uma busca por matrículas. Em seguida, para cada matrícula, realiza mais duas buscas independentes no banco para obter detalhes do usuário e do pagamento correspondente, gerando uma explosão de conexões e queries (`1 + C + E * 2` consultas, onde C é o número de cursos e E é o total de matrículas).
- **Impacto:** Degradação massiva da performance e tempo de resposta da API à medida que a base de dados cresce. Risco elevado de esgotamento de conexões ou travamento de processos do SQLite.
- **Recomendação:** Reescrever a lógica do relatório financeiro utilizando uma única consulta SQL com JOINs entre `courses`, `enrollments`, `users` e `payments`, consolidando a agregação de dados na memória do controlador.

### [HIGH] Non-Atomic Multi-write Flows / Transaction Violation
- **Arquivo:** [AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L28-L78)
- **Descrição:** No fluxo de checkout da API, são executados múltiplos comandos SQL de escrita em sequência (inserção de usuário, matrícula, pagamento e log de auditoria) de forma solta e assíncrona, sem o uso de transações de banco de dados (`BEGIN TRANSACTION`, `COMMIT`, `ROLLBACK`).
- **Impacto:** Caso ocorra uma falha ou interrupção durante a execução dos inserts sequenciais, dados parciais ficarão persistidos no banco de dados, resultando em usuários órfãos, matrículas ativas sem registros de pagamentos válidos ou falta de logs obrigatórios de auditoria.
- **Recomendação:** Envolver o fluxo completo de escrita de checkout em uma transação atômica do SQLite (`db.serialize` executando transações), realizando o `ROLLBACK` completo das alterações em caso de qualquer exceção.

### [HIGH] Referential Integrity Failure / Cascade Deleter
- **Arquivo:** [AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L131-L137)
- **Descrição:** O endpoint de exclusão de usuário deleta o registro da tabela `users` diretamente, mas não realiza a limpeza das matrículas ou pagamentos vinculados a esse usuário, deixando registros órfãos que apontam para chaves estrangeiras inexistentes.
- **Impacto:** Inconsistência relacional severa no banco de dados. Qualquer relatório ou consulta posterior que faça JOINs estritos com usuários não retornará registros de matrículas órfãs ou poderá estourar exceções de ponteiro nulo ao tentar ler o nome ou email do usuário deletado.
- **Recomendação:** Habilitar a verificação de chaves estrangeiras no SQLite e garantir que a exclusão do usuário execute a deleção coordenada (em cascata) das tabelas dependentes (`payments` e `enrollments`) dentro de uma operação transacional.

---

### [MEDIUM] Cover Your Assets / Generic Exception Swallowing
- **Arquivo:** [AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L41) (e linhas 51, 55, 70, 84, etc.)
- **Descrição:** Tratamento de erros de banco de dados e APIs feito através de capturas genéricas que simplesmente retornam mensagens opacas para o cliente (ex: "Erro DB", "Erro Pagamento") sem efetuar qualquer tipo de log estruturado ou rastreamento interno do erro original.
- **Impacto:** Dificuldade acentuada na identificação e correção de problemas em ambiente de produção (falhas silenciosas).
- **Recomendação:** Centralizar o fluxo de captura e tratamento de erros do Express em um middleware dedicado, logando o stack trace no console e retornando um erro padronizado para o cliente.

---

### [LOW] Hardcoded Port / Configuration Fallback
- **Arquivo:** [app.js](../ecommerce-api-legacy/src/app.js#L12-L14) e [utils.js](../ecommerce-api-legacy/src/utils.js#L6)
- **Descrição:** A porta TCP do servidor Express está fixada estaticamente como `3000` nas configurações chumbadas.
- **Impacto:** Limita a portabilidade da aplicação para implantações em ambientes de nuvem, contêineres Docker ou plataformas PaaS que injetam a porta de forma dinâmica via variável de ambiente `PORT`.
- **Recomendação:** Permitir que o servidor Express escute na porta definida pela variável de ambiente `process.env.PORT`, usando `3000` apenas como fallback.

### [LOW] Inline Domain Constants / Magic Strings
- **Arquivo:** [AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L46-L48) e [AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L108)
- **Descrição:** Presença de strings estáticas espalhadas pelo código para validação de regras de domínio (ex: `'PAID'`, `'DENIED'`, `"4"` para checar prefixo do cartão).
- **Impacto:** Facilidade de introdução de bugs por pequenos erros de digitação (typos) e aumento de custos de refatoração para mudar valores de regras de negócio.
- **Recomendação:** Centralizar essas definições de domínio em um arquivo de constantes sob `src/config/constants.js`.
