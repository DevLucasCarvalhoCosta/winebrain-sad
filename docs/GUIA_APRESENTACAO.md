# 🎤 GUIA DE APRESENTAÇÃO - Projeto WineBrain

## 📋 Estrutura Sugerida (15-20 minutos)

### 1. ABERTURA (2 min)
**Slide 1: Título**
- 🍷 WineBrain - Sistema de Apoio à Decisão
- Subtítulo: Adega Bom Sabor
- Nomes da equipe

**Slide 2: Contexto e Problema**
> "A Adega Bom Sabor enfrenta três desafios principais..."
- 📉 Churn de clientes (cancelamentos)
- 💤 Baixo engajamento
- 🎯 Falta de personalização

---

### 2. OBJETIVOS (1 min)
**Slide 3: Objetivos do Sistema**
- ✅ Identificar clientes em risco
- ✅ Gerar recomendações personalizadas
- ✅ Aumentar retenção e receita
- ✅ Facilitar tomada de decisão

---

### 3. SOLUÇÃO PROPOSTA (3 min)
**Slide 4: Arquitetura do WineBrain**
[Mostrar diagrama de camadas]
- 📊 Dados (Excel → CSV)
- 🤖 Machine Learning (3 modelos)
- 🧠 Base de Conhecimento (6 regras)
- 💻 API REST (FastAPI)
- 🌐 Interface Web (React)

**Slide 5: Modelos de Decisão Implementados**
- **Descritivo**: Dashboard com KPIs
- **Preditivo**: ML para churn
- **Prescritivo**: Regras de negócio
- **Simulativo**: Análise de cenários

---

### 4. ANÁLISE DOS DADOS (2 min)
**Slide 6: Overview dos Dados**
- 100 clientes
- 100 produtos (vinhos)
- 100 compras
- Métricas principais (engajamento, gasto, compras)

**Slide 7: Principais Insights**
[Gráficos]
- Distribuição de engajamento
- Cancelamento x Engajamento
- Assinantes vs Não-assinantes
- Top produtos por país/uva

---

### 5. MACHINE LEARNING (3 min)
**Slide 8: Modelo Preditivo de Churn**
- Variável alvo: cancelou_assinatura
- Features: engajamento, gasto, compras, idade, etc.
- 3 algoritmos testados

**Slide 9: Resultados do Modelo**
[Tabela comparativa]
```
Random Forest:    Acurácia [X]%, F1 [Y]%
Decision Tree:    Acurácia [X]%, F1 [Y]%
Logistic Reg:     Acurácia [X]%, F1 [Y]%
```
[Gráfico de Feature Importance]

---

### 6. BASE DE CONHECIMENTO (2 min)
**Slide 10: Regras de Negócio**
Mostrar 2-3 regras principais:

**REGRA 1: Cliente Premium**
```
SE engajamento ≥ 8 E assinante clube
ENTÃO recomendar vinhos premium + eventos VIP
```

**REGRA 2: Risco de Cancelamento**
```
SE engajamento < 4 OU cancelou
ENTÃO cupom 20% + pesquisa + contato urgente
```

---

### 7. DEMONSTRAÇÃO AO VIVO (5 min) 🔥

**7.1 Dashboard** (1 min)
- Mostrar KPIs principais
- Gráficos de vendas
- Rankings

**7.2 Lista de Clientes** (1 min)
- Buscar cliente
- Filtros de status
- Badges de engajamento

**7.3 Detalhes + IA** (2 min)
- Abrir cliente de alto risco
- Mostrar probabilidade de churn
- Exibir recomendações geradas
- Explicar regras aplicadas

**7.4 API Swagger** (1 min)
- Abrir /docs
- Mostrar endpoints
- Executar um request ao vivo

---

### 8. RESULTADOS E IMPACTO (2 min)
**Slide 11: Resultados Alcançados**
- ✅ Sistema completo funcional
- ✅ Modelo ML com [X]% acurácia
- ✅ 6 regras de negócio
- ✅ Interface profissional
- ✅ API documentada

**Slide 12: Impacto Projetado**
```
Taxa de Churn:      30% → 20% (-33%)
Receita Anual:      R$ 19k → R$ 29k (+49%)
Ticket Médio:       R$ 197 → R$ 245 (+25%)
Custo de Retenção:  R$ 50 → R$ 30 (-40%)
```

---

### 9. ENCERRAMENTO (1 min)
**Slide 13: Conclusões**
- ✅ SAD completo e funcional
- ✅ Integração ML + Regras
- ✅ Aplicabilidade real
- ✅ Escalável e expansível

**Slide 14: Próximos Passos**
- Integração com CRM
- App mobile
- Sistema de recomendação de produtos
- Expansão para outros setores

**Slide 15: Dúvidas?**
- Obrigado!
- Contatos da equipe

---

## 💡 DICAS IMPORTANTES

### Antes da Apresentação
- [ ] Testar sistema no computador da apresentação
- [ ] Abrir todos os navegadores necessários
- [ ] Backend rodando (localhost:8000)
- [ ] Frontend rodando (localhost:3000)
- [ ] Swagger aberto em uma aba
- [ ] Dashboard aberto em outra aba
- [ ] Cliente exemplo pré-selecionado
- [ ] Ter backup em vídeo/screenshots

### Durante a Apresentação

#### ✅ FAZER
- Falar claramente e pausadamente
- Olhar para a plateia
- Usar linguagem de negócio (não só técnica)
- Destacar valor para o cliente
- Mostrar entusiasmo pelo projeto
- Ter exemplos concretos
- Demonstrar ao vivo (se possível)

#### ❌ EVITAR
- Ler slides
- Termos muito técnicos sem explicar
- Focar só em código
- Desculpas por funcionalidades faltantes
- Passar slides muito rápido
- Demonstração sem ensaiar

### Perguntas Prováveis

**1. "Por que escolheram Random Forest?"**
> "Testamos 3 algoritmos. Random Forest teve melhor F1-Score ([X]%), além de fornecer feature importance interpretável, fundamental para o negócio entender quais fatores influenciam o churn."

**2. "Como garantem que as regras não conflitam?"**
> "Implementamos um sistema de priorização (Crítica > Alta > Média > Baixa). Regras são avaliadas em ordem e consolidadas. O cliente vê todas as ações recomendadas organizadas por prioridade."

**3. "Qual o diferencial deste sistema?"**
> "Integração completa: não é só ML isolado, mas um sistema end-to-end que combina predição com regras de negócio e interface amigável. Além disso, é escalável e baseado em tecnologias modernas."

**4. "Como trataram o desbalanceamento de classes?"**
> "Utilizamos class_weight='balanced' nos modelos, que ajusta automaticamente os pesos das classes durante o treinamento, dando mais importância à classe minoritária."

**5. "E se os dados mudarem?"**
> "O sistema foi projetado para retreinamento periódico. Basta executar o script de treinamento com novos dados. A arquitetura modular facilita ajustes nas features e regras."

**6. "Qual o ROI esperado?"**
> "Com base nas projeções, reduzir churn de 30% para 20% e aumentar ticket médio em 25% pode gerar aumento de 49% na receita anual, com payback estimado em [X] meses."

**7. "Por que não usar deep learning?"**
> "Para este dataset (100 clientes), métodos tradicionais de ML são mais apropriados. Deep learning requer muito mais dados e seria overengineering. Além disso, Random Forest é mais interpretável."

**8. "Como validaram as regras de negócio?"**
> "As regras foram baseadas em: (1) insights da análise exploratória, (2) melhores práticas de CRM, (3) literatura sobre retenção de clientes, e (4) feedback de potenciais stakeholders."

---

## 🎬 ROTEIRO DE DEMONSTRAÇÃO

### Setup Pré-Demo
```
✅ Backend rodando
✅ Frontend rodando
✅ Navegador com 3 abas abertas:
   - Tab 1: Dashboard
   - Tab 2: Clientes
   - Tab 3: Swagger UI
✅ Cliente exemplo anotado (ID com alto churn)
```

### Demo Script (5 minutos)

**[00:00 - 01:00] Dashboard**
```
"Vamos ver o sistema em ação. Esta é a tela principal que o gestor 
vê ao entrar no WineBrain..."

[Apontar para KPIs]
"Aqui temos os indicadores principais: 100 clientes, taxa de 
cancelamento de X%, receita total..."

[Rolar para gráficos]
"O sistema analisa automaticamente as vendas por tipo de uva e país, 
mostrando onde focar os esforços de marketing..."
```

**[01:00 - 02:00] Lista de Clientes**
```
"Na aba de clientes, vemos todos os cadastros com suas métricas..."

[Mostrar badges]
"O sistema classifica automaticamente o engajamento: verde para alto, 
amarelo para médio, vermelho para baixo. Vemos também quem é do clube 
e quem cancelou..."

[Usar busca]
"Posso buscar rapidamente por nome ou cidade..."
```

**[02:00 - 04:00] Detalhes do Cliente**
```
[Clicar em cliente com alto risco]
"Vamos analisar este cliente específico..."

[Apontar para métricas]
"Vemos o perfil completo: total gasto, número de compras, engajamento..."

[Apontar para probabilidade de churn]
"Aqui está a magia: nosso modelo de Machine Learning identificou que 
este cliente tem 75% de probabilidade de cancelar - é um alerta crítico!"

[Mostrar recomendações]
"E o sistema não só identifica o problema, mas sugere ações concretas:
- Enviar cupom de 20%
- Fazer pesquisa de satisfação
- Incluir em programa de fidelidade

Cada ação tem prioridade e justificativa baseada nas regras de negócio..."
```

**[04:00 - 05:00] API**
```
[Abrir Swagger]
"Para desenvolvedores e integrações, temos uma API REST completa e 
documentada..."

[Expandir um endpoint]
"Posso fazer requisições ao vivo... [executar /api/clientes/1/recomendacao]

E recebo um JSON estruturado com todas as recomendações, pronto para 
ser consumido por outros sistemas..."
```

---

## 📊 SLIDES ESSENCIAIS

### Slide Modelo: Arquitetura
```
┌─────────────────────────────────────────┐
│           INTERFACE WEB (React)         │
│  Dashboard | Clientes | Recomendações   │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│           API REST (FastAPI)            │
│    Endpoints | Validação | Rotas        │
└────┬──────────────────────────────┬─────┘
     │                              │
┌────▼──────────┐        ┌──────────▼──────┐
│  ML ENGINE    │        │  RULE ENGINE    │
│  • Random     │        │  • 6 Regras     │
│    Forest     │        │  • Priorização  │
│  • Predição   │        │  • Ações        │
└───────┬───────┘        └─────────┬───────┘
        │                          │
        └──────────┬───────────────┘
                   │
        ┌──────────▼──────────┐
        │   DATA LAYER        │
        │  CSV | SQLite       │
        │  100 Clientes       │
        └─────────────────────┘
```

### Slide Modelo: Resultados
```
┌──────────────────────────────────────────┐
│        MÉTRICAS DO MODELO                │
├──────────────────────────────────────────┤
│ Modelo: Random Forest                    │
│                                          │
│ ✅ Acurácia:   [X]%                      │
│ ✅ Precisão:   [X]%                      │
│ ✅ Recall:     [X]%                      │
│ ✅ F1-Score:   [X]%                      │
│                                          │
│ Top Features:                            │
│   1. Engajamento     ([X]%)              │
│   2. Total Gasto     ([X]%)              │
│   3. Nº Compras      ([X]%)              │
└──────────────────────────────────────────┘
```

---

## ⏱️ GESTÃO DE TEMPO

| Seção | Tempo | Acumulado |
|-------|-------|-----------|
| Abertura | 2 min | 2 min |
| Objetivos | 1 min | 3 min |
| Solução | 3 min | 6 min |
| Dados | 2 min | 8 min |
| ML | 3 min | 11 min |
| Regras | 2 min | 13 min |
| **DEMO** | **5 min** | **18 min** |
| Resultados | 2 min | 20 min |

**Reserve tempo para perguntas!**

---

## 🎯 PONTOS-CHAVE A ENFATIZAR

### Para a Professora
- ✅ Todos os 4 modelos de decisão implementados
- ✅ Base de conhecimento estruturada
- ✅ IA aplicada (3 algoritmos comparados)
- ✅ POC funcional e demonstrável
- ✅ Fundamentação teórica sólida

### Para Stakeholders
- 💰 ROI calculado e projetado
- 📈 Aumento de receita esperado
- 💡 Valor de negócio claro
- ⚡ Decisões em tempo real
- 🎯 Ações personalizadas

### Para Público Técnico
- 🏗️ Arquitetura moderna e escalável
- 🔧 Tecnologias atuais (FastAPI, React)
- 📊 Pipeline de dados robusto
- 🤖 ML bem implementado
- 📚 Código limpo e documentado

---

## ✅ CHECKLIST FINAL

### 1 Semana Antes
- [ ] Relatório completo escrito
- [ ] Slides prontos
- [ ] Sistema funcionando 100%
- [ ] Dados processados
- [ ] Modelo treinado

### 1 Dia Antes
- [ ] Ensaiar apresentação (cronometrar)
- [ ] Testar demo completa
- [ ] Revisar perguntas prováveis
- [ ] Preparar backup (screenshots/vídeo)
- [ ] Confirmar equipamentos

### No Dia
- [ ] Chegar cedo
- [ ] Testar computador/projetor
- [ ] Iniciar backend e frontend
- [ ] Abrir todas as abas necessárias
- [ ] Respirar fundo e mandar bem! 🚀

---

## 🏆 MENSAGEM FINAL

Você tem um projeto **excelente**:
- ✅ Completo
- ✅ Profissional
- ✅ Demonstrável
- ✅ Bem documentado
- ✅ Com impacto real

**Confie no trabalho que fizeram!**

Boa apresentação! 🎤🍷🎓
