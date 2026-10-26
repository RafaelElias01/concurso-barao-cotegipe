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
- Atalhos na Área de Trabalho (no Windows do dono ela é a pasta OneDrive/Desktop do usuário, não C:/Users/rafae/Desktop): `Cronograma Barão de Cotegipe.lnk` (abre `ABRIR CRONOGRAMA.bat`) e `Pasta Concurso Barão de Cotegipe.lnk` (abre a pasta do projeto).
AFAEDESKTOP`): `CRONOGRAMA BARãO DE COTEGIPE.LNK` (ABRE `ABRIR CRONOGRAMA.BAT`) E `PASTA CONCURSO BARãO DE COTEGIPE.LNK` (ABRE A PASTA DO PROJETO).

### B) Dados Oficiais de Barão de Cotegipe (RS) – CORRIGIDO em 25/10/2026
Fonte: histórico oficial do IBGE (biblioteca.ibge.gov.br, "Histórico" e "Formação Administrativa") e IBGE Cidades. Um 1º rascunho (feito pelo Gemini) tinha erros e itens sem fonte; foi corrigido na branch `fix/realidade-municipal-fatos`.
- **Povoamento:** c. 1911 (italianos, poloneses, ucranianos, lituanos e caboclos); primeiro nome do povoado: **Floresta**.
- **Distrito:** criado como **Cotegipe** (decreto 7.842, 30/06/1939); virou **Barão de Cotegipe** em 29/12/1944 (decreto-lei 720).
- **Município:** lei estadual **4.737, de 01/06/1964**, desmembrado de **Erechim, Aratiba e São Valentim**; **instalado em 23/01/1965** (o texto do IBGE chama 1965 de "emancipação": cuidado com a banca).
- **Censo 2022:** 7.144 hab; 27,42 hab/km²; área 260,505 km²; gentílico cotegipense.
- **Vizinhos (IBGE):** Erechim, São Valentim, Itatiba do Sul, Barra do Rio Azul, Ponte Preta, Paulo Bento.
- **Economia (IBGE):** setor primário (milho, trigo, soja, feijão, erva-mate; frango, leite, suínos).
- **Judiciário:** não existe Judiciário municipal (regra constitucional).
- **Confirmado depois (Lei Orgânica, site da Câmara, IBGE Cidades):** Câmara com 9 vereadores; PIB per capita R$ 45.460,37 (2023); Lei Orgânica traz área antiga 271,15 km² (pegadinha) e clima temperado.
- **NÃO CONFIRMADO (fora do material):** bioma, IDEB, IDHM, comarca, AMAU.

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

### D) Correção de Links Externos e Download Local de PDFs (100% Offline)
- Problema identificado: O portal do Ministério da Saúde (bvsms.saude.gov.br) bloqueou o acesso externo com erro 503 / WAF rejection ao tentar abrir o PDF do HumanizaSUS.
- Solução aplicada:
  - Copiados para a pasta local material/saude/: HumanizaSUS_Documento_Base.pdf, Lei_8080_1990_SUS.pdf, NR-32_Seguranca_Saude_Trabalho_Servicos_Saude.pdf, Lei_13146_2015_LBI.pdf.
  - Copiados para material/cursinho/: apostilas completas da Aula 00 do Estratégia de SUS (Lei 8.080 e CF arts 196-200), Português e Raciocínio Lógico.
  - Atualizados cronograma/gera_plano.py e cronograma/plano.js para que todos os links abram os arquivos PDF locais pelo servidor local, sem depender de internet nem de sites governamentais instáveis.
