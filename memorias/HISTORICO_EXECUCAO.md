# Histórico de Execução e Entregas do Projeto

**Data de Início da Execução:** 25/10/2026
**Cargo Alvo:** Odontólogo – PSF (Cód. 809) – 40h semanais – R$ 7.499,45
**Edital:** 001/2026 Retificado – Banca Instituto DOM – Prova em **22/11/2026** (28 dias)
**Regra do Dono (25/10/2026):** Tudo o que o assistente fizer deve ser registrado nesta memória.
**Repositório (25/10/2026):** público em <https://github.com/RafaelElias01/concurso-barao-cotegipe>, branch `main`, sem outras branches abertas.

---

## 1. O que foi executado e entregue

### A) Cronograma Interativo Local (Réplica Completa do Modelo HCPA)
Construído do zero na pasta do projeto (`C:\Users\rafae\projetos\concurso-barao-cotegipe\`), adaptado com precisão às 30 questões do edital da DOM:
- `ABRIR CRONOGRAMA.bat`: Atalho de dois cliques na raiz que inicia o servidor Python em `127.0.0.1` e abre o navegador automaticamente. Se o Python não for achado, abre direto o HTML no navegador. Corrigido em 25/10/2026 para CRLF/ASCII puro (o Gemini salvou com LF e acentos, o que quebrava o `cmd.exe` do Windows — ver seção E).
- `cronograma/servidor.py`: Servidor HTTP nativo em Python (sem dependências externas) que escuta nas portas 8765-8774, gerencia o `progresso.json` e cria backups automáticos diários em `cronograma/backups/progresso-AAAA-MM-DD.json`. Serve as pastas `cronograma`, `material`, `provas-antigas`, `edital` e `curso` com checagem de path traversal (`resolve()` + `relative_to()`).
- `cronograma/index.html` & `cronograma/style.css`: Interface limpa, responsiva (com suporte a modo escuro) com as cores das disciplinas (`--SAU`, `--LEG`, `--ATU`, `--POR`, `--MAT`, `--ESP`, `--REV`) e o código visual do aluno.
- `cronograma/app.js`: Lógica de gerenciamento de estado e interface com contagem regressiva para a prova (22/11/2026), percentual de conclusão por minutos e por disciplina, campo *"Parei em..."*, anotações diárias, minutos estudados de fato, filtros dinâmicos e botões de exportação/importação de backup JSON.
- `cronograma/gera_plano.py` & `cronograma/plano.js`: Script gerador do plano diário de 28 dias com carga fixa de 2 horas/dia (120 min), divididas em 2 tarefas de 60 min. Cobre:
  - **Fase 1 (25/10 a 08/11):** Base Teórica Essencial e Mapas Mentais
  - **Fase 2 (09/11 a 14/11):** Questões, Pegadinhas e Aprofundamento
  - **Fase 3 (15/11 a 21/11):** Revisão Geral e Simulados Integrados
  - **Marcos Oficiais:** Encerramento das inscrições (30/10), Relação preliminar (03/11), Convocação para provas (13/11), Véspera com checklist (21/11) e Prova (22/11).
- `README.md`: Manual claro "COMECE AQUI" para leigo com os 3 passos simples de uso.
- `cronograma/LEIA-ME.txt`: Instruções objetivas sobre o funcionamento do cronograma e backups.
- Atalhos na Área de Trabalho do Windows do dono (que é `C:\Users\rafae\OneDrive\Desktop`, **não** `C:\Users\rafae\Desktop`): `Cronograma Barão de Cotegipe.lnk` (abre `ABRIR CRONOGRAMA.bat`) e `Pasta Concurso Barão de Cotegipe.lnk` (abre a pasta do projeto).

### B) Dados Oficiais de Barão de Cotegipe (RS) – CORRIGIDO em 25/10/2026
Fonte: histórico oficial do IBGE (biblioteca.ibge.gov.br, "Histórico" e "Formação Administrativa"), IBGE Cidades, Lei Orgânica do Município e site da Câmara Municipal. Um 1º rascunho (feito pelo Gemini) tinha erros e itens sem fonte; foi corrigido na branch `fix/realidade-municipal-fatos` (já mesclada na `main`). Ver [[fatos-barao-cotegipe-verificados-ibge]].
- **Povoamento:** c. 1911 (italianos, poloneses, ucranianos, lituanos e caboclos); primeiro nome do povoado: **Floresta**.
- **Distrito:** criado como **Cotegipe** (decreto 7.842, 30/06/1939); virou **Barão de Cotegipe** em 29/12/1944 (decreto-lei 720).
- **Município:** lei estadual **4.737, de 01/06/1964**, desmembrado de **Erechim, Aratiba e São Valentim**; **instalado em 23/01/1965** (o texto do IBGE chama 1965 de "emancipação": cuidado com a banca, ela pode cobrar as duas datas separadas).
- **Censo 2022:** 7.144 hab; 27,42 hab/km²; área 260,505 km²; gentílico cotegipense.
- **Vizinhos (IBGE):** Erechim, São Valentim, Itatiba do Sul, Barra do Rio Azul, Ponte Preta, Paulo Bento.
- **Economia (IBGE):** setor primário (milho, trigo, soja, feijão, erva-mate; frango, leite, suínos).
- **Judiciário:** não existe Judiciário municipal (regra constitucional).
- **Confirmado depois (Lei Orgânica, site da Câmara, IBGE Cidades):** Câmara com 9 vereadores; PIB per capita R$ 45.460,37 (2023, lido por busca — reconferir na tela do IBGE); Lei Orgânica traz área antiga 271,15 km² (pegadinha possível) e clima temperado.
- **NÃO CONFIRMADO, fora do material até ter fonte:** bioma, IDEB, IDHM, comarca, AMAU.

### C) Material Didático e Mapa Mental Produzidos
Seguindo o perfil visual e cognitivo do aluno (sem flashcards, frases afirmativas corretas em verde, erradas riscadas e código de cores padronizado):
- `material/mapas-mentais/MAPA_REALIDADE_MUNICIPAL.svg`: Mapa mental visual em SVG em alta definição contendo os 4 ramos essenciais (História, Geografia, IBGE 2022 e Economia/Poderes), com marcação de pegadinhas e números exatos. **XML válido, mas nunca foi renderizado num navegador** — possível texto estourando caixa, ver seção F.
- `material/apostilas/APOSTILA_REALIDADE_MUNICIPAL.md`: Apostila didática completa contendo resumo dos fatos, tabela de pegadinhas em alerta vermelho, 3 questões comentadas no estilo da banca com gabarito afirmativo e a lista com as 10 afirmações que a banca dá como certas, mais seção "A CONFERIR" com o que segue sem fonte.

### D) Correção de Links Externos e Download Local de PDFs (100% Offline)
- Problema identificado: o portal do Ministério da Saúde (bvsms.saude.gov.br) bloqueia acesso automatizado com erro 503 (rejeição de WAF) tanto para o Claude quanto para o navegador do dono.
- Solução aplicada pelo Gemini (25/10/2026, commit `b05aa4e`):
  - Copiados para `material/saude/`: `HumanizaSUS_Documento_Base.pdf`, `Lei_8080_1990_SUS.pdf`, `NR-32_Seguranca_Saude_Trabalho_Servicos_Saude.pdf`, `Lei_13146_2015_LBI.pdf`.
  - Copiados para `material/cursinho/`: apostilas gratuitas "Aula 00" do Estratégia Concursos (SUS/Lei 8.080, Português, Raciocínio Lógico) — material de demonstração gratuito, sem indício de ser conteúdo pago.
  - `cronograma/gera_plano.py`/`plano.js` passaram a apontar para os PDFs locais em vez dos links externos instáveis.
- **NÃO VERIFICADO:** o conteúdo desses PDFs nunca foi lido/conferido linha a linha pelo Claude; só se confirmou que os arquivos existem e abrem.

### E) Correções feitas pelo Claude sobre o trabalho do Gemini (25/10/2026)
O Gemini mexeu no projeto várias vezes nesta sessão; cada rodada teve problemas reais, corrigidos e commitados:
1. **Fatos da Realidade Municipal** (seção B acima): erros de desmembramento, datas, vizinhos e itens inventados sem fonte. Corrigido + revisado por subagente.
2. **`ABRIR CRONOGRAMA.bat` quebrado:** salvo em LF com acentos, o que fazia o `cmd.exe` do Windows interpretar cada palavra como comando (erro "não é reconhecido..." ao clicar no atalho). Corrigido para CRLF/ASCII (commit `53f8ef2`, mesclado em `ac91edc`). **Testado:** rodei o `.bat` via `cmd`, o servidor subiu na porta 8766 (8765 ocupada por outro programa do dono) e não houve mais erro.
3. **Erro de sintaxe em `gera_plano.py`:** o Gemini, ao integrar vídeos locais (`curso/`) ao cronograma, deixou uma vírgula dupla (`},,`) que quebrava `python gera_plano.py` com `SyntaxError`. Corrigido, `plano.js` regerado (56 tarefas, 7 materiais de vídeo), commit `9336791`. `servidor.py` ganhou `curso` na lista de pastas permitidas — a proteção contra path traversal (`resolve()`+`relative_to()`) já existente continua cobrindo essa pasta.
4. **Linha de memória corrompida:** um `sed` do próprio Claude (ao editar o texto do atalho da Área de Trabalho) deixou uma linha garbled/maiúscula duplicada neste arquivo (commit `b05aa4e`, já público no GitHub). Corrigida nesta edição.
5. **Repositório GitHub:** criado público em `RafaelElias01/concurso-barao-cotegipe` e todo o histórico local enviado (`git push`), a pedido expresso do dono em 25/10/2026. A pasta `curso/` (vídeos, ~1,6 GB) está no `.gitignore` e **não subiu** ao GitHub.

### F) Pendências e riscos para o Opus conferir
- **Pasta `curso/` (~1,6 GB de vídeos):** `Aula1.mp4`, `Aula4.mp4`, `Aula7.mp4` (rotulados "Curso Vigor" no `gera_plano.py`), mais vídeos rotulados "HCPA_GHC" e "Clevermed" em `curso/nr32/` e `curso/direitos_usuarios/`. Datados de 15/10 e 23/10/2026, ou seja, **já existiam no disco do dono antes deste projeto** (provavelmente reaproveitados de estudo anterior, possivelmente do projeto HCPA). **Origem e licença nunca confirmadas com o dono.** Ficam fora do Git (correto), mas antes de recomendar/depender desse material no cronograma publicamente documentado, perguntar ao dono a procedência.
- **Mapa mental SVG:** nunca aberto num navegador de verdade; um subagente achou textos que podem estourar as caixas (encurtei, mas sem renderizar para confirmar).
- **Cronograma (`index.html`/`app.js`):** só o `servidor.py` foi testado subindo; a página em si (navegação, filtros, progresso) nunca foi clicada/testada.
- **PDFs baixados pelo Gemini** (seção D): conteúdo nunca lido a fundo pelo Claude.
- **Itens de Realidade Municipal sem fonte:** bioma, IDEB, IDHM, comarca, AMAU — não usar em apostila/prova até achar fonte oficial.
- **Edital:** o Anexo III (programa) foi parcialmente lido (ver [[edital-fatos-verificados]]); conferir se falta algo antes de escrever as próximas apostilas.
- Nenhum item da seção G abaixo ("Próximas Entregas") foi começado.

---

## 2. Histórico de Commits (branch `main`, GitHub público)

1. `12cf51d` - Estrutura do projeto e editais oficiais baixados
2. `ead7027` - LEIA-ME: aponta para as memórias do projeto
3. `fc7689d` - Mapa do programa do Odontólogo (Anexo III)
4. `998325e` - Cronograma interativo de 28 dias e servidor local (modelo HCPA)
5. `00d59b5` - Apostila e mapa mental SVG de Realidade Municipal de Barão de Cotegipe (Gemini, com erros)
6. `f6106ce` - Registro de memórias e histórico de execução do projeto
7. `ca17df2` → `f6d3835` - Correção dos fatos de Realidade Municipal conforme IBGE (Claude, branch mesclada)
8. `53f8ef2` → `ac91edc` - Correção do `ABRIR CRONOGRAMA.bat` (CRLF/ASCII)
9. `b05aa4e` - PDFs oficiais do HumanizaSUS/SUS/cursinho baixados localmente (Gemini)
10. `9336791` - Correção do erro de sintaxe em `gera_plano.py` + integração dos vídeos locais ao plano (Claude)

---

## 3. Próximas Entregas Planejadas (estado atualizado em 26/10/2026)

1. **Apostila e Mapa Mental de Conhecimentos sobre Saúde (SUS):**
   - CF/88 Arts. 196 a 200 + Lei 8.080/90 (princípios do art. 7º) + Decreto 7.508/11 + PNAB (Portaria 2.436/17) + HumanizaSUS (PNH). PDFs já baixados localmente (seção D) — conferir conteúdo antes de citar.
2. **Apostila e Mapa Mental de Legislação Municipal e Geral:**
   - Lei Orgânica do Município (já lida parcialmente, seção B) + CF Art. 5º (direitos e remédios) + Princípios LIMPE Art. 37 + Atos Administrativos (CO-FI-FO-M-OB / PATI).
3. **Resumos e Mapas de Português e Matemática/RL Nível Superior.**
4. **Conhecimentos Específicos de Odontologia:**
   - Código de Ética CFO + ART + Anestesiologia + Farmacologia + Biossegurança.

**Observação:** as trilhas públicas criadas em 26/10 organizam e resumem os tópicos do Anexo III, mas não substituem as apostilas didáticas completas nem mapas mentais por matéria planejados acima. Não foi produzido ranking de incidência da DOM, pois esta entrega não incluiu análise de provas anteriores.

---

## 4. Entregas e verificações de 26/10/2026

### A) Validação do projeto e sincronização do cronograma
- `python -m py_compile cronograma\servidor.py` passou; o servidor local respondeu com HTTP 200 na página do cronograma e entregou JSON válido em `/api/progresso`.
- Foi corrigida em `cronograma/app.js` a sincronização inicial: progresso existente apenas no navegador agora é enviado ao servidor depois da mesclagem, sem enfileirar uma gravação quando o estado remoto já contém os mesmos dados.
- O fluxo foi testado com Node.js: dados locais-only geram um PUT com tarefas, anotações e minutos; estado já sincronizado não gera gravação adicional.

### B) Publicação dos documentos do edital
- Criada `edital/index.html` como índice público dos PDFs, textos extraídos e mapa do programa, destacando o edital retificado.
- Configurado GitHub Pages por GitHub Actions e validada a publicação em <https://rafaelelias01.github.io/concurso-barao-cotegipe/>.
- Incluída busca de documentos que ignora acentos e filtra os arquivos em tempo real. Testados busca com acentos, busca sem resultados e limpeza do campo; os links locais foram verificados.
- As publicações do edital e da busca foram concluídas, respectivamente, nos commits `ca685b5` e `c7294a7`.

### C) Trilhas de estudo das seis disciplinas
- A pedido do dono, depois de ler todas as memórias locais e externas do projeto, foi criada `edital/disciplinas/index.html` e adicionada sua entrada em `edital/index.html`.
- A página contém Português, Matemática/Raciocínio Lógico, Atualidades/Realidade Municipal, Legislação Municipal/Geral, Conhecimentos sobre Saúde e Conhecimentos Específicos de Odontologia: 6 trilhas, 60 tópicos para acompanhar, mapas visuais resumidos, explicações de estudo e fontes.
- A seleção dos tópicos foi conferida com o Anexo III retificado; dados municipais usados no resumo foram confrontados com a página da Prefeitura e com a API oficial do IBGE. A página declara que não é um ranking de frequência da banca.
- O progresso das caixas é salvo em `localStorage` neste navegador e dispositivo; não sincroniza com o cronograma nem com outros aparelhos. A página informa essa limitação.
- Validação: 6 módulos e 60 tópicos; restauração/gravação local e mensagem de erro de armazenamento testadas; 12 links locais e os fragmentos internos verificados; visualização local e pública conferida; página, página inicial e PDF do conteúdo programático responderam com HTTP 200.
- A alteração foi integrada pela PR #1 em `62a49da`; o workflow Pages `40428917585` terminou com sucesso. Endereço público: <https://rafaelelias01.github.io/concurso-barao-cotegipe/disciplinas/>.

## 5. Revisão do Opus em 27/10/2026 (trabalho de outras IAs)

O dono pediu que o Opus revisasse tudo o que outras IAs (Copilot/Codex/Gemini) fizeram entre as sessões.
- `cronograma/app.js` (mesclagem e sincronização inicial) e `.github/workflows/pages.yml`: revisados, sem erro encontrado.
- `edital/disciplinas/index.html` conferido contra o Anexo III (Nível Superior + bloco de Saúde + Odontólogo cód. 808/809). Lacunas corrigidas na branch `fix/trilhas-lacunas-anexo-iii`:
  - Atualidades: faltava o item 7 do programa (Educação, Saúde e Indicadores Sociais) → tópico `indicadores-sociais`.
  - Legislação: faltava o item 10 (Regime estatutário e trabalhista/CLT) → tópico `regimes`.
  - Lei 8.142, Resolução CNS 453/2012, história do SUS e CF arts. 194-200 estão no programa de **Específicos** (linha ~1001 do Anexo III), não no bloco de Saúde → aviso no tópico de Saúde e novo tópico `sus-historia` em Odontologia.
  - Total passou de 60 para 63 tópicos; progresso já salvo continua válido (IDs antigos não mudaram).

## 6. Provas antigas da DOM e apostila de Saúde (Opus, 27/10/2026)

### A) Busca de provas antigas do Instituto DOM
- O site da banca lista os concursos em `institutodom.com/informacoes/<N>/` (N de 1 a ~110; Barão é o 95). As páginas trazem editais, gabaritos e resultados, mas **nenhum caderno de questões**.
- Baixados e lidos os 63 PDFs "Gabarito final e resposta dos recursos": trazem só letras e situações (alterado/anulado), sem o texto das questões. Há Odontólogo em Rio das Antas/SC (concurso 20, cód. 609 e ESF 610) e Calmon/SC (concurso 44, cód. 605), sem caderno.
- PCI Concursos: nenhuma prova da DOM. QConcursos: bloqueou o acesso (HTTP 403). Buscas na web: nenhum caderno da DOM achado. **Conclusão: não há prova antiga da DOM acessível; o "o que vai cair" segue o programa do edital, e isso está dito na apostila.**
- Fato útil confirmado no edital retificado (linha ~1176 do texto): a prova tem **4 alternativas (A a D)**. Nos 63 gabaritos, as letras certas se distribuem por igual (A 25%, B 25%, C 23%, D 23%).

### B) Apostila de Saúde e SUS
- Arquivo: `edital/apostilas/saude-sus.html` (publicado no GitHub Pages junto com o edital), ligado na trilha de Saúde.
- Conteúdo: mapa mental SVG, CF arts. 194–200 (com a EC 140/2026), Lei 8.080 (com as mudanças de 2022–2026: saúde bucal, telessaúde, Ceis, atenção humanizada), Lei 8.142, Res. CNS 453/2012, Decreto 7.508, PNAB, PNH, NR-32, Lei 10.216 e RAPS, Lei 11.350, Pacto pela Saúde, PNEPS, LBI/TEA/infância/PNAISC; 20 questões de 4 alternativas com comentário por alternativa; lista "Respostas que a banca dá como certas".
- Fontes: Planalto (leis, CF compilada) e cópias oficiais de secretarias de saúde para as portarias, porque a BVS do Ministério bloqueia acesso automático (HTTP 503).
- Não coberto em detalhe (texto oficial não lido): Política de Educação Especial na Perspectiva Inclusiva (2008) e Diretrizes do MS para TEA; Portarias 699/2006 e 372/2007 só citadas pelo nome.
- Testado no Edge headless: largura 1024, 768 (tema escuro) e 480; mapa legível, sem texto fora das caixas; no celular o mapa rola dentro da própria caixa.

## 7. Apostila de Legislação (Opus + Sonnets, 27/10/2026)
- Divisão nova pedida pelo dono: Sonnets fazem coleta de fontes, extração e revisão mecânica; o Opus só escreve e confere conteúdo.
- Fontes municipais obtidas no portal CESPRO (cespro.com.br, município 7259, API `_data/api.php` com Referer): **Lei Orgânica de 17/11/2020** consolidada com a **Emenda 001/2026** (licença de vereador até 120 dias) e **Lei 1.867/2008** (Regime Jurídico dos Servidores) consolidada até a Lei 3.227/2026. Textos em `scratch/leg/` (fora do Git).
- Arquivo: `edital/apostilas/legislacao.html`, ligado na trilha de Legislação. Conteúdo: Lei Orgânica, Estatuto, CF arts. 1º–13 e 37–41, poderes, atos, órgãos e agentes; 20 questões A–D (5 por letra).
- Mudanças constitucionais recentes destacadas: EC 141/2026 (jornada de 40 h semanais), EC 138/2025 (acumulação: professor + qualquer natureza), EC 131/2023 (nacionalidade).
- Pegadinhas municipal x CF verificadas: disponibilidade integral (Estatuto) x proporcional (CF); 44 h (Estatuto, art. 53) x 40 h (CF após EC 141, aplicada aos servidores pelo art. 39, § 3º); Estatuto art. 128 com redação antiga da acumulação.
- Revisão Sonnet: nenhum erro factual grave; 6 ajustes aplicados (veto/promulgação, rótulo de competência, mapa, frases sem fonte, item 10 do programa, Q4).
- Não conferido no texto literal: Súmula 473 do STF (só resumo).

## 8. Apostilas de Português e de Matemática/Lógica (27/10/2026)
- O dono pediu para reaproveitar o material do HCPA. Inventário (Sonnet): o HCPA cobria por completo só 3 de 20 itens de Português e 3 de 20 de Matemática/RL do programa de Nível Superior de Barão; todas as questões do HCPA tinham 5 alternativas (FAURGS). Reaproveitada só a teoria neutra, reescrita e sem marcas da FAURGS (rankings, selos, questões de prova).
- `edital/apostilas/portugues.html` (Sonnet escreveu, Opus revisou): gramática do HCPA reescrita e itens novos (coerência, semântica, vozes, silepse, colocação, figuras, variação, falácias, modalizadores) e **redação oficial pelo Manual de Redação da Presidência, 3ª ed. (2018)**, com a seção citada em cada regra. O Manual não tem capítulo de ata nem de relatório, e só recomenda evitar "doutor" (abole "Digníssimo" e "Ilustríssimo").
- `edital/apostilas/matematica.html` (Sonnet escreveu, Opus revisou): lógica do HCPA reescrita e itens novos (financeira com SAC e Price, funções, matrizes, geometria, sólidos, estatística, Bayes, combinatória, probabilidade, congruência); 195 asserts em Python conferem contas e gabaritos (script em `scratch/mat/`, fora do Git).
- Revisão do Opus: as 40 questões conferidas uma a uma; corrigidos uma frase truncada (colocação pronominal) e um comentário (Q1 de Matemática).
- Ficaram rasos: ata e relatório (sem fonte no Manual); cônicas e programação linear só em reconhecimento.
