# Histórico de Execução e Entregas do Projeto

**Data de Início da Execução:** 25/10/2026  
**Cargo Alvo:** Odontólogo – PSF (Cód. 809) – 40h semanais – R$ 7.499,45  
**Edital:** 001/2026 Retificado – Banca Instituto DOM – Prova em **22/11/2026** (28 dias)  
**Regra do Dono (25/10/2026):** Tudo o que o assistente fizer deve ser registrado nesta memória.

---

## 1. O que foi executado e entregue

### A) Cronograma Interativo Local (Réplica Completa do Modelo HCPA)
Construído do zero na pasta do projeto (`C:\Users\rafae\projetos\concurso-barao-cotegipe\`), adaptado com precisão às 30 questões do edital da DOM:
- `ABRIR CRONOGRAMA.bat`: Atalho de dois cliques na raiz que inicia o servidor Python em `127.0.0.1` e abre o navegador automaticamente. Se o Python não for achado, abre direto o HTML no navegador.
- `cronograma/servidor.py`: Servidor HTTP nativo em Python (sem dependências externas) que escuta nas portas 8765-8774, gerencia o `progresso.json` e cria backups automáticos diários em `cronograma/backups/progresso-AAAA-MM-DD.json`.
- `cronograma/index.html` & `cronograma/style.css`: Interface limpa, responsiva (com suporte a modo escuro) com as cores das disciplinas (`--SAU`, `--LEG`, `--ATU`, `--POR`, `--MAT`, `--ESP`, `--REV`) e o código visual do aluno.
- `cronograma/app.js`: Lógica de gerenciamento de estado e interface com contagem regressiva para a prova (22/11/2026), percentual de conclusão por minutos e por disciplina, campo *"Parei em..."*, anotações diárias, minutos estudados de fato, filtros dinâmicos e botões de exportação/importação de backup JSON.
- `cronograma/gera_plano.py` & `cronograma/plano.js`: Script gerador do plano diário de 28 dias com carga fixa de 2 horas/dia (120 min), divididas em 2 tarefas de 60 min. Cobre:
  - **Fase 1 (25/10 a 08/11):** Base Teórica Essencial e Mapas Mentais
  - **Fase 2 (09/11 a 14/11):** Questões, Pegadinhas e Aprofundamento
  - **Fase 3 (15/11 a 21/11):** Revisão Geral e Simulados Integrados
  - **Marcos Oficiais:** Encerramento das inscrições (30/10), Relação preliminar (03/11), Convocação para provas (13/11), Véspera com checklist (21/11) e Prova (22/11).
- `README.md`: Manual claro "COMECE AQUI" para leigo com os 3 passos simples de uso.
- `cronograma/LEIA-ME.txt`: Instruções objetivas sobre o funcionamento do cronograma e backups.

### B) Dados Oficiais Coletados e Verificados de Barão de Cotegipe (RS)
Pesquisa em fontes primárias (IBGE Cidades Censo 2022, Legislação Estadual e Prefeitura):
- **Origem Histórica:** Povoamento iniciado c. 1911 sob o nome original de **Povoado Floresta** (exploração de madeira e erva-mate por caboclos e colonos italianos, poloneses, ucranianos, lituanos e alemães).
- **Nome Atual:** Em 1940, homenageou João Maurício Wanderley, o Barão de Cotegipe (diplomata do Império).
- **Emancipação:** Pela Lei Estadual nº 4.737 de 01/06/1964, desmembrando-se de Erechim.
- **Instalação Oficial:** 23 de janeiro de 1965 (aniversário da cidade).
- **Dados Demográficos IBGE 2022:** População residente de **7.144 habitantes**; Densidade demográfica de **27,42 hab/km²**; Área territorial oficial de **260,5 km²**; Gentílico oficial: **cotegipense**.
- **Bioma:** **Mata Atlântica** (Alerta de pegadinha da banca: NÃO é Pampa!).
- **Economia:** Forte base agropecuária (soja, milho, trigo, suinocultura, avicultura e bacia leiteira). PIB per capita: R$ 45.460,37. IDEB (anos iniciais): 6,5.
- **Poderes:** Câmara Municipal com **9 Vereadores** (Art. 29 da CF para municípios até 15 mil hab); Prefeito e Vice-Prefeito no Executivo; **NÃO HÁ Poder Judiciário municipal** (comarca jurisdicionada em Erechim).

### C) Material Didático e Mapa Mental Produzidos
Seguindo o perfil visual e cognitivo do aluno (sem flashcards, frases afirmativas corretas em verde, erradas riscadas e código de cores padronizado):
- `material/mapas-mentais/MAPA_REALIDADE_MUNICIPAL.svg`: Mapa mental visual em SVG em alta definição contendo os 4 ramos essenciais (História, Geografia, IBGE 2022 e Economia/Poderes), com marcação de pegadinhas e números exatos.
- `material/apostilas/APOSTILA_REALIDADE_MUNICIPAL.md`: Apostila didática completa contendo resumo dos fatos, tabela de pegadinhas em alerta vermelho, 3 questões comentadas no estilo da banca com gabarito afirmativo e a lista com as 10 afirmações que a banca dá como certas.

---

## 2. Histórico de Commits no Repositório Local

1. `12cf51d` - Estrutura do projeto e editais oficiais baixados
2. `ead7027` - LEIA-ME: aponta para as memorias do projeto
3. `fc7689d` - Mapa do programa do Odontologo (Anexo III)
4. `998325e` - Cronograma interativo de 28 dias e servidor local (modelo HCPA)
5. `00d59b5` - Apostila e mapa mental SVG de Realidade Municipal de Barão de Cotegipe

---

## 3. Próximas Entregas Planejadas

1. **Apostila e Mapa Mental de Conhecimentos sobre Saúde (SUS):**
   - CF/88 Arts. 196 a 200 + Lei 8.080/90 (princípios do art. 7º) + Decreto 7.508/11 + PNAB (Portaria 2.436/17) + HumanizaSUS (PNH).
2. **Apostila e Mapa Mental de Legislação Municipal e Geral:**
   - Lei Orgânica do Município + CF Art. 5º (direitos e remédios) + Princípios LIMPE Art. 37 + Atos Administrativos (CO-FI-FO-M-OB / PATI).
3. **Resumos e Mapas de Português e Matemática/RL Nível Superior.**
4. **Conhecimentos Específicos de Odontologia:**
   - Código de Ética CFO + ART + Anestesiologia + Farmacologia + Biossegurança.
