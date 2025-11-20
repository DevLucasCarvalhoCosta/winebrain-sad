# ✅ CHECKLIST - Próximos Passos

## 🎯 Agora que o Projeto está Completo

### 1️⃣ INSTALAÇÃO E TESTE (OBRIGATÓRIO)

- [ ] Instalar backend
  ```cmd
  cd backend
  install.bat
  ```

- [ ] Processar dados e treinar modelo
  ```cmd
  process_data.bat
  ```
  ⚠️ **IMPORTANTE**: Anotar as métricas exibidas!
  - Acurácia: _______
  - Precisão: _______
  - Recall: _______
  - F1-Score: _______

- [ ] Instalar frontend
  ```cmd
  cd frontend
  install.bat
  ```

- [ ] Testar backend
  ```cmd
  start_backend.bat
  ```
  Verificar: http://localhost:8000/docs

- [ ] Testar frontend
  ```cmd
  start_frontend.bat
  ```
  Verificar: http://localhost:3000

---

### 2️⃣ CAPTURAR EVIDÊNCIAS

- [ ] **Dashboard**
  - [ ] Screenshot da tela principal com KPIs
  - [ ] Screenshot dos gráficos de vendas
  - [ ] Screenshot da segmentação

- [ ] **Lista de Clientes**
  - [ ] Screenshot da tabela com filtros
  - [ ] Screenshot dos badges de status

- [ ] **Detalhes do Cliente**
  - [ ] Screenshot de cliente VIP
  - [ ] Screenshot de cliente em risco com probabilidade alta
  - [ ] Screenshot das recomendações geradas

- [ ] **API Swagger**
  - [ ] Screenshot da documentação
  - [ ] Screenshot de um request/response

- [ ] **Terminal**
  - [ ] Screenshot do treinamento do modelo
  - [ ] Screenshot das métricas

---

### 3️⃣ PREENCHER MÉTRICAS NO RELATÓRIO

Abrir `docs/RELATORIO_ESTRUTURA.md` e preencher:

- [ ] Estatísticas descritivas dos dados
  - Engajamento (média, min, max, quartis)
  - Total gasto (média, min, max)
  - Distribuição de cancelamentos

- [ ] Métricas dos modelos de ML
  - Random Forest (acurácia, precisão, recall, F1)
  - Decision Tree (acurácia, precisão, recall, F1)
  - Logistic Regression (acurácia, precisão, recall, F1)

- [ ] Feature importance
  - Top 5 features e seus valores

- [ ] Análise de segmentos
  - Quantos clientes em cada segmento
  - Características de cada segmento

- [ ] Top rankings
  - Top 5 clientes
  - Top 5 produtos
  - Top 5 tipos de uva
  - Top 5 países

---

### 4️⃣ ESCREVER RELATÓRIO FINAL

- [ ] **Capa**
  - Nome do projeto
  - Instituição
  - Nomes dos alunos
  - Data

- [ ] **Introdução** (2-3 páginas)
  - Contextualização
  - Problema de negócio
  - Proposta de solução
  - Justificativa

- [ ] **Objetivos** (1 página)
  - Objetivo geral
  - Objetivos específicos

- [ ] **Fundamentação Teórica** (3-4 páginas)
  - SAD e seus componentes
  - Modelos de decisão (4 tipos)
  - Base de conhecimento
  - Machine Learning

- [ ] **Análise dos Dados** (4-5 páginas)
  - Descrição das bases
  - Análise exploratória
  - Estatísticas
  - Gráficos
  - Insights

- [ ] **Modelagem do SAD** (5-6 páginas)
  - Arquitetura do sistema
  - Tecnologias utilizadas
  - Implementação dos 4 modelos
  - Fluxo de decisão

- [ ] **Base de Conhecimento** (4-5 páginas)
  - Estrutura
  - 6 regras detalhadas
  - Motor de inferência
  - Exemplos de aplicação

- [ ] **IA** (4-5 páginas)
  - Preparação dos dados
  - 3 modelos treinados
  - Comparação
  - Modelo selecionado
  - Exemplos de predição

- [ ] **POC** (3-4 páginas)
  - Objetivos
  - Escopo
  - Demonstração funcional (com screenshots)
  - Casos de uso
  - Validação

- [ ] **Resultados** (3-4 páginas)
  - Métricas do modelo
  - Features importantes
  - Distribuição de segmentos
  - Insights de negócio
  - Projeções de impacto

- [ ] **Considerações Finais** (2-3 páginas)
  - Síntese
  - Objetivos alcançados
  - Lições aprendidas
  - Trabalhos futuros

- [ ] **Referências**
  - Bibliografia completa

- [ ] **Anexos**
  - Link do código
  - Manual do usuário
  - Documentação da API

---

### 5️⃣ PREPARAR APRESENTAÇÃO

- [ ] **Criar Slides** (15-20 slides)
  - Seguir estrutura do `docs/GUIA_APRESENTACAO.md`
  - Incluir screenshots do sistema
  - Gráficos e tabelas de resultados
  - Manter visual limpo e profissional

- [ ] **Preparar Demo**
  - Testar sistema no computador de apresentação
  - Ter backend e frontend rodando
  - Abrir todas as abas necessárias
  - Escolher cliente exemplo (alto risco)

- [ ] **Ensaiar**
  - Praticar apresentação completa
  - Cronometrar (15-20 min)
  - Treinar transições de tela
  - Preparar respostas para perguntas

- [ ] **Backup**
  - Criar vídeo da demo (plano B)
  - Ter PDF dos slides
  - Screenshots de tudo
  - Código em pendrive

---

### 6️⃣ VALIDAÇÃO FINAL

- [ ] **Relatório**
  - Revisar ortografia
  - Verificar formatação
  - Numerar figuras e tabelas
  - Conferir referências
  - Gerar PDF final

- [ ] **Código**
  - Comentários claros
  - README atualizado
  - Sem erros ao executar
  - Tudo commitado (se usar Git)

- [ ] **Apresentação**
  - Slides finalizados
  - Demo testada
  - Tempo adequado
  - Perguntas preparadas

---

## 📅 CRONOGRAMA SUGERIDO

### Semana 1
- ✅ Instalação e testes
- ✅ Captura de evidências
- ✅ Coleta de métricas

### Semana 2
- 📝 Escrever relatório (Introdução → Análise)
- 🎨 Começar slides

### Semana 3
- 📝 Escrever relatório (Modelagem → Resultados)
- 🎨 Finalizar slides

### Semana 4
- 📝 Revisar e finalizar relatório
- 🎤 Ensaiar apresentação
- ✅ Validação final

---

## 🎯 PRIORIDADES

### CRÍTICO ⚠️
1. Instalar e rodar o sistema
2. Coletar métricas reais
3. Capturar screenshots
4. Escrever relatório

### IMPORTANTE ⭐
5. Criar slides
6. Preparar demo
7. Ensaiar apresentação

### OPCIONAL 💡
8. Melhorias no código
9. Funcionalidades extras
10. Testes adicionais

---

## ✅ QUANDO TUDO ESTIVER PRONTO

- [ ] Relatório impresso e encadernado
- [ ] Slides no formato correto
- [ ] Sistema testado e funcionando
- [ ] Demo ensaiada
- [ ] Perguntas preparadas
- [ ] Backup completo
- [ ] Equipe confiante

---

## 🏆 LEMBRETE FINAL

Vocês têm um projeto **COMPLETO** e **PROFISSIONAL**:

✅ Todos os requisitos atendidos
✅ 4 modelos de decisão implementados
✅ IA aplicada (3 algoritmos)
✅ Base de conhecimento (6 regras)
✅ POC funcional
✅ Interface moderna
✅ API documentada
✅ Código limpo

**Confiem no trabalho que fizeram! 🚀**

---

## 📞 Em Caso de Dúvidas

1. Consultar `QUICK_START.md` (instalação)
2. Consultar `RELATORIO_ESTRUTURA.md` (estrutura)
3. Consultar `GUIA_APRESENTACAO.md` (apresentação)
4. Verificar comentários no código
5. Revisar este checklist

---

**Data de início**: ___/___/2025
**Data de entrega**: ___/___/2025
**Data de apresentação**: ___/___/2025

---

**BOA SORTE! 🍷🎓**
