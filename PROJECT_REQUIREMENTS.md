Este documento apresenta a especificação detalhada do seu projeto de conclusão para as disciplinas do professor Arturo Hernandez Dominguez, integrando os conceitos de **Compiladores**, **Reuso de Software** e **Linhas de Produto de Software (LPS/Tópicos)**.

**Documentação de gestão do projeto:**

- [COMPLIANCE_AUDIT.md](./COMPLIANCE_AUDIT.md) — conformidade ✅/🟡/❌ vs. requisitos do professor  
- [SCHEDULE.md](./SCHEDULE.md) — cronograma por data  
- [ACTIVITIES.md](./ACTIVITIES.md) — sprints, responsáveis, checklist E2E  
- [ROADMAP.md](./ROADMAP.md) — entregas técnicas por fase

---

# Especificação do Projeto: Framework para Compiladores e Interpretadores Usando Microsserviços

## 1. Visão Geral
O projeto consiste no desenvolvimento de um **framework extensível** baseado em uma arquitetura de **microsserviços** para o processamento da linguagem **MiniPar 2026.1**. O framework deve ser capaz de atuar tanto como um **interpretador** (execução direta) quanto como um **compilador** (geração de código para múltiplas linguagens-alvo), gerenciando essas variações através de uma estrutura de Linha de Produto de Software (LPS).

## 2. Requisitos das Disciplinas (Integração)

Como você cursa as três disciplinas, seu projeto deve atender aos seguintes critérios específicos:

### A. Compiladores (MiniPar 2026.1 OO)
*   **Evolução da Linguagem:** Evoluir a MiniPar 2025.1 para suportar **Orientação a Objetos** completa (classes, herança com `extends`, métodos, atributos, instanciação com `new` e recursão).
*   **Paralelismo Real:** Implementar blocos `PAR` utilizando **Threads** tratadas como processos independentes que se comunicam exclusivamente via **canais de comunicação (sockets)**.
*   **Pipeline de Compilação:** O framework deve conter Analisadores Léxico, Sintático (Parser descendente recursivo), Semântico (verificação de tipos e escopo), Tabela de Símbolos e Geradores de Código.
*   **Back-ends de Performance:** Para as opções de compilador (C, C++, Rust), o sistema deve gerar código equivalente que será compilado pelo `gcc` com nível de otimização **-O2** para gerar um executável (.exe) de alta performance.

### B. Reuso de Software
*   **Componentes de Software:** Toda a arquitetura do compilador/interpretador deve ser modelada e implementada como **componentes independentes** (Léxico, Sintático, Semântico, Geradores).
*   **Padrões de Projeto:** Uso obrigatório do padrão **Template Method** para definir o esqueleto do processo de tradução, utilizando **hotspots** (pontos de adaptação) para alternar entre as variantes de saída (C, Rust, Assembly, Interpretador).
*   **Reuso Sistemático:** Reaproveitar a gramática (**BNF**) e a lógica base das implementações do MiniPar 2025.1 (Eduardo Maciel e Hélio Rego).

### C. Tópicos/LPS (Arquitetura de Microsserviços)
*   **Desacoplamento:** Cada fase do compilador e cada variante de saída deve ser um **microsserviço independente** que se comunica via APIs REST e JSON.
*   **API Gateway:** Implementar um ponto central de entrada que gerencia as requisições do frontend e roteia para os serviços adequados.
*   **Gestão de Variabilidade:** Embora o projeto use microsserviços, ele deve ser documentado como uma LPS, identificando **pontos de variação** (ex: modo de execução) e **variantes** (ex: C, Rust, Interpretador).

---

## 3. Requisitos Técnicos Obrigatórios (Testes)

O professor exige a execução bem-sucedida de dois testes complexos:

1.  **Teste de Real Paralelismo (3 Máquinas):**
    *   Um menu coordenador em um computador deve disparar o **QuickSort** no Computador 1, a **Multiplicação de Matrizes** no Computador 2 e o **Fatorial** no Computador 3.
    *   Os resultados devem ser devolvidos via **sockets** e exibidos no menu central.
2.  **Simulação de Fractal (Tapete de Sierpinski):**
    *   Implementar a lógica recursiva do Fractal em MiniPar OO.
    *   Simular a tela de saída através de uma **matriz de caracteres** (usando `.` ou `*`) exibida no console ou interface web.

---

## 4. Tecnologias Sugeridas
*   **Frontend:** Angular (Interface para edição de código e seleção de variabilidade) [Acordado em conversa].
*   **API Gateway:** Java Spring Boot.
*   **Microsserviços:** Python (FastAPI/Flask) ou Node.js (NestJS) para envelopar a lógica de compilação.
*   **Banco de Dados:** PostgreSQL (Persistência de logs e metadados).
*   **Infraestrutura:** Docker e Docker Compose para orquestração.

---

## 5. Cronograma e Entregáveis
*   **Data de Entrega:** **10 de junho**.
*   **Itens a entregar:**
    1.  Relatório Técnico no **Overleaf** (seguindo o modelo do professor para as 3 disciplinas).
    2.  Código-fonte completo no **GitHub**.
    3.  Apresentação do projeto rodando com todos os testes solicitados.

## 6. Estrutura do Relatório (Para Bruno - 3 Disciplinas)
1.  **Introdução:** Contextualização do framework e objetivos.
2.  **Metodologia Ágil:** Descrição do uso de Scrum/XP para o desenvolvimento.
3.  **Arquitetura do Sistema:** Diagramas de Microsserviços e API Gateway.
4.  **Modelagem UML:** Diagramas de Casos de Uso, Componentes e Classes.
5.  **Análise de Compiladores:** Descrição da BNF OO, AST e lógica dos back-ends.
6.  **Gestão de Reuso e Variabilidade:** Detalhamento do Template Method e Diagrama de Features da LPS.
7.  **Resultados:** Telas da interface web e logs de execução dos testes (Fractal e 3 Computadores).