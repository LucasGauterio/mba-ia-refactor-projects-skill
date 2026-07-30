# RELATÓRIO DE AUDITORIA ARQUITETURAL

Projeto: `ecommerce-api-legacy`
Stack:   Node.js + Express
Arquivos: 3 | ~180 linhas

## Resumo
CRITICAL: 3 | HIGH: 3 | MEDIUM: 1 | LOW: 2

## Achados

### [CRITICAL] Insecure / Custom Cryptography (Criptografia Fraca / Customizada)
- **Arquivo:** [src/AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L68) e [src/utils.js](../ecommerce-api-legacy/src/utils.js#L17-L23)
- **Descrição:** Utilização de um algoritmo de criptografia customizado (`badCrypto`) baseado em codificação repetitiva Base64 sem salting para armazenar senhas de usuários no banco de dados.
- **Impacto:** Vulnerabilidade grave que permite reverter ou quebrar facilmente as senhas dos usuários por ataques de dicionário ou tabelas rainbow se a base de dados for exposta.
- **Recomendação:** Adotar algoritmos de hash seguros padrão da indústria, como PBKDF2 (nativo do Node.js via módulo `crypto`) ou `bcrypt`, utilizando salts gerados de maneira segura para cada senha.

### [CRITICAL] Hardcoded Secrets (Segredos no Código Fonte)
- **Arquivo:** [src/utils.js](../ecommerce-api-legacy/src/utils.js#L2-L5)
- **Descrição:** Chaves privadas, tokens e credenciais de produção (`paymentGatewayKey`, `dbPass`, `dbUser`) estão chumbados no código fonte em um arquivo JavaScript.
- **Impacto:** Risco severo de vazamento de segredos de infraestrutura e gateway financeiro caso o código fonte seja versionado ou compartilhado publicamente.
- **Recomendação:** Carregar todas as configurações sensíveis de variáveis de ambiente (`process.env`) e manter fallbacks seguros apenas para fins de desenvolvimento local, configurando o arquivo `.env`.

### [CRITICAL] Auth Illusion / Lack of Admin Authorization (Ausência de Autorização em Rotas Críticas)
- **Arquivo:** [src/AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L80)
- **Descrição:** A rota de relatório financeiro administrativo `/api/admin/financial-report` está exposta publicamente sem nenhum controle de acesso ou validação de token/sessão.
- **Impacto:** Qualquer usuário pode consultar dados confidenciais de faturamento e informações pessoais de estudantes matriculados apenas chamando a rota HTTP.
- **Recomendação:** Criar um middleware de autenticação/autorização que valide a presença de um token administrativo seguro (ex: `ADMIN_TOKEN` do `.env`) enviado no cabeçalho `Authorization: Bearer <token>`.

---

### [HIGH] The Blob / God Class (Classe Todo-Poderosa)
- **Arquivo:** [src/AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L4-L139)
- **Descrição:** A classe `AppManager` possui responsabilidades múltiplas: gerencia a conexão e criação de tabelas do banco de dados SQLite, define todas as rotas da aplicação, implementa regras de negócio do checkout, formata as respostas HTTP e gera logs.
- **Impacto:** Código acoplado, de difícil manutenção, com alto custo para escrita de testes unitários isolados e violação clara do Princípio de Responsabilidade Única (SRP).
- **Recomendação:** Separar o projeto seguindo o padrão MVC: configurações do banco em `config/`, queries e mapeamento em `models/`, regras de fluxo no `controllers/`, definição de rotas em `routes/` e gerenciamento global no entrypoint `app.js`.

### [HIGH] SQLite Thread-Unsafe & In-Memory Database State (Banco SQLite em Memória e Sem Persistência)
- **Arquivo:** [src/AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L7)
- **Descrição:** A conexão SQLite é aberta em memória (`:memory:`) diretamente no construtor do `AppManager`, o que faz com que todos os dados gravados sejam perdidos ao reiniciar o servidor, além de compartilhar uma única instância mutável globalmente.
- **Impacto:** Incompatibilidade com ambientes de produção e risco de erros de concorrência ou dados corrompidos.
- **Recomendação:** Configurar uma conexão persistente do SQLite apontando para um arquivo local (ex: `./lms.db`), definido dinamicamente pelas configurações da camada `config/`.

### [HIGH] Non-Atomic Multi-write Flows / Transaction Violation (Falta de Atomicidade em Operações de Escrita)
- **Arquivo:** [src/AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L50-L63)
- **Descrição:** As queries de inserção de matrículas, pagamentos e logs de auditoria no fluxo de checkout ocorrem de forma assíncrona encadeada sem estarem envelopadas sob uma transação de banco de dados.
- **Impacto:** Inconsistência relacional grave caso ocorra um erro de sistema ou queda do servidor após a inserção da matrícula mas antes do registro do pagamento.
- **Recomendação:** Implementar a execução das queries sequenciais dentro de uma transação explícita do SQLite (`BEGIN TRANSACTION`, com correspondente `COMMIT` se tudo der certo ou `ROLLBACK` em caso de erro).

---

### [MEDIUM] Query N+1 Performance Bottleneck (Gargalo de Performance Query N+1)
- **Arquivo:** [src/AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L80-L129)
- **Descrição:** Na rota de relatório financeiro `/api/admin/financial-report`, para cada curso cadastrado, o sistema realiza uma nova query para obter as matrículas. Para cada matrícula encontrada, realiza mais duas queries adicionais para buscar dados do usuário e do pagamento.
- **Impacto:** Desempenho severamente prejudicado conforme o número de matrículas e cursos aumenta devido à multiplicação exponencial de requisições ao banco.
- **Recomendação:** Otimizar a consulta reescrevendo-a com um único comando SQL utilizando `LEFT JOIN` entre as tabelas `courses`, `enrollments`, `users` e `payments`, consolidando os dados em memória em uma única passada.

---

### [LOW] Referential Integrity Failure / Cascade Deleter (Falha na Remoção Consistente)
- **Arquivo:** [src/AppManager.js](../ecommerce-api-legacy/src/AppManager.js#L131-L137)
- **Descrição:** O endpoint `DELETE /api/users/:id` executa a exclusão de um registro na tabela `users` sem limpar ou atualizar os registros dependentes nas tabelas de matrículas (`enrollments`) e pagamentos (`payments`).
- **Impacto:** Acúmulo de dados órfãos e quebra da integridade referencial funcional no banco.
- **Recomendação:** Habilitar chaves estrangeiras (`PRAGMA foreign_keys = ON;`) no SQLite e configurar a remoção correspondente em cascata no banco ou manualmente de forma transacional.

### [LOW] Hardcoded Port / Configuration Fallback (Porta TCP Sem Fallback e Debug Hardcoded)
- **Arquivo:** [src/app.js](../ecommerce-api-legacy/src/app.js#L12) e [src/utils.js](../ecommerce-api-legacy/src/utils.js#L6)
- **Descrição:** A porta do servidor está fixada como `3000` em um arquivo de configurações sem buscar flexibilidade a partir das variáveis de ambiente.
- **Impacto:** Dificulta a portabilidade do aplicativo em ambientes de nuvem/containers que impõem portas customizadas dinamicamente.
- **Recomendação:** Alterar a inicialização para ler `process.env.PORT` e permitir a parametrização apropriada do app.
