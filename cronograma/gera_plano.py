#!/usr/bin/env python3
"""Gera cronograma/plano.js para o Concurso Barão de Cotegipe (RS) – Odontólogo/PSF.

Banca: Instituto DOM. Edital 001/2026 Retificado.
Cargo: Odontólogo – PSF (Cód. 809) – 40h – R$ 7.499,45.
Prova: 22/11/2026 (Domingo, 3h). 30 questões de 2 pts, mínimo 36/60 (60%).
Carga: 2 horas diárias (120 minutos por dia) durante 28 dias (25/10 a 21/11).
"""
import datetime as dt
import json
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent
ARQ_SAIDA = PASTA / "plano.js"

PROVA = dt.date(2026, 11, 22)
INICIO = dt.date(2026, 10, 25)

MATERIAIS = {
    # Editais e referências locais
    "edital_ret": {"nome": "Edital 001/2026 Retificado (Texto Oficial)", "link": "../edital/texto/01-edital-001-2026-RETIFICADO.txt", "tipo": "edital"},
    "mapa_prog": {"nome": "Mapa do Programa do Cargo (Anexo III)", "link": "../edital/MAPA-DO-PROGRAMA.md", "tipo": "edital"},
    "anexo_vagas": {"nome": "Anexo I – Quadro de Vagas e Requisitos", "link": "../edital/texto/10-anexo-I-quadro-de-vagas.txt", "tipo": "edital"},
    "anexo_prog": {"nome": "Anexo III – Conteúdo Programático Completo", "link": "../edital/texto/12-anexo-III-conteudo-programatico.txt", "tipo": "edital"},

    # Legislação de Saúde (bloco comum Nível Superior Saúde)
    "cf88_saude": {"nome": "CF/88 – Da Saúde (Artigos 196 a 200)", "link": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#art196", "tipo": "lei"},
    "lei8080": {"nome": "Lei Orgânica da Saúde – Lei 8.080/1990", "link": "../material/saude/Lei_8080_1990_SUS.pdf", "tipo": "lei"},
    "lei8142": {"nome": "Participação da Comunidade e Transferências – Lei 8.142/1990", "link": "https://www.planalto.gov.br/ccivil_03/leis/l8142.htm", "tipo": "lei"},
    "dec7508": {"nome": "Regulamentação do SUS – Decreto 7.508/2011", "link": "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/decreto/d7508.htm", "tipo": "lei"},
    "pnab": {"nome": "Política Nacional de Atenção Básica – Portaria 2.436/2017", "link": "https://bvsms.saude.gov.br/bvs/saudelegis/gm/2017/prt2436_22_09_2017.html", "tipo": "lei"},
    "pnh": {"nome": "HumanizaSUS – Política Nacional de Humanização (Documento Base MS)", "link": "../material/saude/HumanizaSUS_Documento_Base.pdf", "tipo": "livro"},
    "nr32": {"nome": "NR-32 – Segurança e Saúde no Trabalho em Serviços de Saúde", "link": "../material/saude/NR-32_Seguranca_Saude_Trabalho_Servicos_Saude.pdf", "tipo": "lei"},
    "lbi": {"nome": "Lei Brasileira de Inclusão da Pessoa com Deficiência – Lei 13.146/2015", "link": "../material/saude/Lei_13146_2015_LBI.pdf", "tipo": "lei"},
    "lei_tea": {"nome": "Política Nacional de Proteção dos Direitos da Pessoa com TEA – Lei 12.764/2012", "link": "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12764.htm", "tipo": "lei"},
    "raps": {"nome": "Rede de Atenção Psicossocial (RAPS) – Portaria GM/MS 3.088/2011", "link": "https://bvsms.saude.gov.br/bvs/saudelegis/gm/2011/prt3088_23_12_2011_rep.html", "tipo": "lei"},
    # Vídeos do curso (100% offline - pasta curso/)
    "v_aula1": {"nome": "Vídeo – Aula 1: Lei 8.080/90 (SUS) – Curso Vigor (112 min)", "link": "../curso/Aula1.mp4", "tipo": "video"},
    "v_aula4": {"nome": "Vídeo – Aula 4: LBI Lei 13.146/2015 – Curso Vigor (122 min)", "link": "../curso/Aula4.mp4", "tipo": "video"},
    "v_aula7": {"nome": "Vídeo – Aula 7: PNH / HumanizaSUS – Curso Vigor (110 min)", "link": "../curso/Aula7.mp4", "tipo": "video"},
    "v_bia": {"nome": "Vídeo – Português: Acentuação e Fonologia – Profª Bia Backes (67 min)", "link": "../curso/Português, profª Bia Backes_ Acentuação Gráfica e Fonologia.mp4", "tipo": "video"},
    "v_nr32": {"nome": "Vídeo – NR 32: Segurança e Saúde no Trabalho – Prof. Flávio Santos (47 min)", "link": "../curso/nr32/NR32_1_FlavioSantos_HCPA_GHC_47min.mp4", "tipo": "video"},
    "v_dir1": {"nome": "Vídeo – Direitos e Deveres dos Usuários da Saúde (22 min)", "link": "../curso/direitos_usuarios/Direitos_1_HCPA_Curso_Direitos_e_Deveres_22min.mp4", "tipo": "video"},
    "v_dir4": {"nome": "Vídeo – Carta dos Direitos (Res. CNS 553) (32 min)", "link": "../curso/direitos_usuarios/Direitos_4_Clevermed_Res_CNS_553_32min.mp4", "tipo": "video"},
    "res_cns453": {"nome": "Resolução CNS 453/2012 – Diretrizes para Conselhos de Saúde", "link": "https://conselho.saude.gov.br/resolucoes/2012/Reso453.pdf", "tipo": "lei"},

    # Aulas demonstrativas gratuitas de cursinho (Estratégia Concursos) - 100% offline
    "k_sus": {"nome": "Cursinho – SUS: Lei 8.080, Princípios e Organização (Estratégia)", "link": "../material/cursinho/especificos/Estrategia_Aula00_SUS_Lei_8080_Principios_Organizacao.pdf", "tipo": "cursinho"},
    "k_sus_cf": {"nome": "Cursinho – SUS: Reforma Sanitária e CF Arts. 196-200 (Estratégia)", "link": "../material/cursinho/especificos/Estrategia_Aula00_SUS_Reforma_Sanitaria_CF_196-200.pdf", "tipo": "cursinho"},
    "k_port_nivel": {"nome": "Cursinho – Português: Nivelamento Geral (Estratégia)", "link": "../material/cursinho/portugues/Estrategia_Aula00_Portugues_Nivelamento_geral.pdf", "tipo": "cursinho"},
    "k_port_orto": {"nome": "Cursinho – Português: Ortografia e Acentuação (Estratégia)", "link": "../material/cursinho/portugues/Estrategia_Aula00_Portugues_Ortografia_Acentuacao_Hifen.pdf", "tipo": "cursinho"},
    "k_rl_prop": {"nome": "Cursinho – RL: Proposições, Conectivos e Negação (Estratégia)", "link": "../material/cursinho/raciocinio_logico/Estrategia_Aula00_RL_Proposicoes_Conectivos_Negacao.pdf", "tipo": "cursinho"},
    "k_rl_conj": {"nome": "Cursinho – RL: Conjuntos e Diagramas (Estratégia)", "link": "../material/cursinho/raciocinio_logico/Estrategia_Aula00_RL_Conjuntos_Diagramas.pdf", "tipo": "cursinho"},
    "k_rl_basico": {"nome": "Cursinho – RL: Curso Básico com Questões Resolvidas (Estratégia)", "link": "../material/cursinho/raciocinio_logico/Estrategia_Aula00_RL_Curso_Basico_Questoes_Resolvidas.pdf", "tipo": "cursinho"},

    # Legislação Geral e Municipal
    "cf88_geral": {"nome": "CF/88 – Princípios Fundamentais (Arts. 1º a 4º) e Art. 5º", "link": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm", "tipo": "lei"},
    "cf88_sociais": {"nome": "CF/88 – Direitos Sociais (Arts. 6º a 11) e Nacionalidade (Arts. 12 e 13)", "link": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#art6", "tipo": "lei"},
    "cf88_adm": {"nome": "CF/88 – Da Administração Pública (Artigos 37 a 41)", "link": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#art37", "tipo": "lei"},
    "lei_org_bc": {"nome": "Lei Orgânica do Município de Barão de Cotegipe (RS)", "link": "https://leismunicipais.com.br/lei-organica-barao-de-cotegipe-rs", "tipo": "lei"},
    "regime_bc": {"nome": "Regime Jurídico dos Servidores Municipais de Barão de Cotegipe", "link": "https://leismunicipais.com.br/estatuto-dos-servidores-publicos-barao-de-cotegipe-rs", "tipo": "lei"},

    # Realidade Municipal e Atualidades
    "apo_realidade": {"nome": "Apostila – Realidade Municipal de Barão de Cotegipe (Fatos Oficiais e Questões)", "link": "../material/apostilas/APOSTILA_REALIDADE_MUNICIPAL.md", "tipo": "apostila"},
    "mapa_realidade": {"nome": "Mapa Mental Visual – Realidade Municipal de Barão de Cotegipe", "link": "../material/mapas-mentais/MAPA_REALIDADE_MUNICIPAL.svg", "tipo": "img"},
    "ibge_bc": {"nome": "IBGE Cidades – Barão de Cotegipe (RS): Censo 2022, Economia e Demografia", "link": "https://cidades.ibge.gov.br/brasil/rs/barao-de-cotegipe/panorama", "tipo": "web"},
    "pref_bc": {"nome": "Portal Oficial da Prefeitura Municipal de Barão de Cotegipe (RS)", "link": "https://baraodecotegipe.rs.gov.br/", "tipo": "web"},

    # Conhecimentos Específicos – Odontologia
    "codigo_etica_cfo": {"nome": "Código de Ética Odontológica – Resolução CFO 118/2012", "link": "https://transparencia.cfo.org.br/ato-normativo/?id=2081", "tipo": "lei"},
    "caderno_atencao_bucal": {"nome": "Caderno de Atenção Básica nº 17 – Saúde Bucal (Ministério da Saúde)", "link": "https://bvsms.saude.gov.br/bvs/publicacoes/saude_bucal.pdf", "tipo": "livro"},
    "manual_art": {"nome": "Manual do Tratamento Restaurador Atraumático (ART) no SUS – MS", "link": "https://bvsms.saude.gov.br/bvs/publicacoes/tratamento_restaurador_atraumatico_art.pdf", "tipo": "livro"},
    "guia_fluor": {"nome": "Guia de Recomendações sobre Fluoretos no Brasil – Ministério da Saúde", "link": "https://bvsms.saude.gov.br/bvs/publicacoes/guia_recomendacoes_fluoretos.pdf", "tipo": "livro"},
    "manual_redacao_pr": {"nome": "Manual de Redação da Presidência da República (3ª Edição Atualizada)", "link": "http://www4.planalto.gov.br/centrodeestudos/assuntos/manual-de-redacao-da-presidencia-da-republica", "tipo": "livro"}
}

DIAS_PLANO = [
    # ----------------- SEMANA 1 (25/10 a 31/10) -----------------
    {
        "data": "2026-10-25",
        "diaSemana": "Domingo",
        "fase": 1,
        "marcos": [
            "INÍCIO DO CRONOGRAMA DE 28 DIAS (Faltam 28 dias para a Prova Objetiva em 22/11/2026)",
            "Meta diária: 2 horas (120 minutos) de estudo focado e sem distrações."
        ],
        "tarefas": [
            {
                "id": "2026-10-25-0",
                "disciplina": "SAU",
                "titulo": "CF/88 Artigos 196 a 200 (A Saúde na Ordem Social) – Mapa Mental e Artigos-Chave",
                "detalhe": "Estudo dos arts. 196 a 200 da CF/88. Pontos de alta recorrência: art. 196 (Saúde é direito de todos e dever do Estado, garantida mediante políticas sociais e econômicas); art. 198 (Diretrizes: descentralização com direção única em cada esfera de governo; atendimento integral com prioridade para atividades preventivas; e participação da comunidade); art. 199 (A assistência à saúde é livre à iniciativa privada; instituições filantrópicas e sem fins lucrativos têm preferência na participação complementar; é VEDADA destinação de recursos públicos para auxílios/subvenções a instituições com fins lucrativos). Pegadinha clássica de banca: trocar 'prioridade para atividades preventivas' por 'curativas', ou dizer que empresas estrangeiras podem atuar irrestritamente sem autorização em lei.",
                "minutos": 60,
                "materiais": ["cf88_saude", "k_sus_cf", "edital_ret"]
            },
            {
                "id": "2026-10-25-1",
                "disciplina": "SAU",
                "titulo": "Lei 8.080/1990: Princípios e Diretrizes (Art. 7º) e Organização do SUS",
                "detalhe": "Foco no Art. 7º da Lei 8.080/90. Grave as palavras literais da lei: universalidade de acesso; integralidade de assistência; preservação da autonomia; IGUALDADE da assistência à saúde (atenção: 'equidade' é princípio doutrinário, a lei escreve 'igualdade'); direito à informação; divulgação de informações; utilização da epidemiologia; integração ações de saúde, meio ambiente e saneamento; conjugação de recursos; descentralização político-administrativa; e participação da comunidade. Pegadinha: a banca coloca 'centralização' ou diz que o SUS é subordinado exclusivamente à esfera federal.",
                "minutos": 60,
                "materiais": ["lei8080", "k_sus", "pnh", "v_aula1"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-10-26",
        "diaSemana": "Segunda",
        "fase": 1,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-10-26-0",
                "disciplina": "LEG",
                "titulo": "Constituição Federal: Princípios Fundamentais (Arts. 1º a 4º) e Princípios da Administração Pública (Art. 37)",
                "detalhe": "CF/88 Arts. 1º a 4º: Fundamentos (SO-CI-DI-VA-PLU: soberania, cidadania, dignidade da pessoa humana, valores sociais do trabalho e da livre iniciativa, pluralismo político); Objetivos fundamentais (CON-GA-ER-PRO: construir sociedade livre/justa/solidária, garantir desenvolvimento nacional, erradicar pobreza e marginalização, promover o bem de todos sem preconceitos). Art. 37: Princípios expressos LIMPE (Legalidade, Impessoalidade, Moralidade, Publicidade, Eficiência). Grave: Eficiência entrou com a EC 19/1998.",
                "minutos": 60,
                "materiais": ["cf88_geral", "cf88_adm"]
            },
            {
                "id": "2026-10-26-1",
                "disciplina": "LEG",
                "titulo": "Lei Orgânica do Município de Barão de Cotegipe: Autonomia, Competências e Organização dos Poderes",
                "detalhe": "Estrutura básica da Lei Orgânica Municipal: Autonomia municipal (política, administrativa e financeira); Competências privativas do Município (assuntos de interesse local, tributos municipais, serviços públicos) e comuns com Estado e União. Organização dos Poderes: Executivo (Prefeito e Vice-Prefeito) e Legislativo (Câmara Municipal de Vereadores). Não há Poder Judiciário no âmbito municipal. Vedações e proibições de acumulação de cargos remunerados aplicáveis ao servidor público.",
                "minutos": 60,
                "materiais": ["lei_org_bc"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-10-27",
        "diaSemana": "Terça",
        "fase": 1,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-10-27-0",
                "disciplina": "POR",
                "titulo": "Língua Portuguesa Nível Superior: Interpretação Textual, Intencionalidade e Operadores Argumentativos",
                "detalhe": "Análise da intencionalidade discursiva, pressupostos (informações que a frase dá como certas) vs subentendidos (inferências dependentes do contexto). Coesão textual: anáfora (retoma termo anterior) vs catáfora (antecipa termo seguinte), elipse (omissão intencional) e substituição lexical. Operadores argumentativos: conectivos de oposição (mas, porém, contudo, todavia, entretanto), concessão (embora, conquanto, ainda que, apesar de que - exigem verbo no subjuntivo!), e conclusão (portanto, logo, por conseguinte).",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            },
            {
                "id": "2026-10-27-1",
                "disciplina": "POR",
                "titulo": "Morfossintaxe: Conjunções Coordenativas e Subordinativas e o Valor Semântico das Preposições",
                "detalhe": "Tabela mental das conjunções: Coordenativas (aditivas, adversativas, alternativas, conclusivas, explicativas) vs Subordinativas adverbiais (causais, comparativas, concessivas, condicionais, conformativas, consecutivas, finais, proporcionais, temporais). Cuidado com 'como' (pode ser causal: 'Como chovia, não saí'; comparativo: 'Forte como um touro'; conformativo: 'Fiz como mandou'). Preposições essenciais e seus valores semânticos (instrumento, causa, finalidade, posse, matéria).",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-10-28",
        "diaSemana": "Quarta",
        "fase": 1,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-10-28-0",
                "disciplina": "MAT",
                "titulo": "Lógica Proposicional: Conectivos Lógicos e Tabela-Verdade Essencial",
                "detalhe": "Conectivos: Conjunção (p ∧ q: 'e' - só é V se ambos forem V); Disjunção inclusiva (p ∨ q: 'ou' - só é F se ambos forem F); Disjunção exclusiva (p ⊻ q: 'ou... ou' - é V se os valores forem diferentes); Condicional (p → q: 'se... então' - SÓ É FALSA na Vera Fischer: V → F = F; nos demais casos é VERDADEIRA!); Bicondicional (p ↔ q: 'se e somente se' - é V se ambos tiverem o mesmo valor lógico). Conceitos: Tautologia (sempre V), Contradição (sempre F), Contingência (pode ser V ou F).",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            },
            {
                "id": "2026-10-28-1",
                "disciplina": "MAT",
                "titulo": "Equivalências Lógicas Notáveis e Leis de De Morgan",
                "detalhe": "Equivalências da Condicional (caem em quase todas as provas de Raciocínio Lógico): (1) Contrapositiva: p → q ≡ ~q → ~p ('Se chove, me molho' ≡ 'Se não me molho, não chove'); (2) Regra do 'NEJOU' (Nega a primeira OU mantém a segunda): p → q ≡ ~p ∨ q. Negação da Condicional (Regra do 'MANÉ': Mantém a primeira E Nega a segunda): ~(p → q) ≡ p ∧ ~q. Leis de De Morgan: ~(p ∧ q) ≡ ~p ∨ ~q; ~(p ∨ q) ≡ ~p ∧ ~q.",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-10-29",
        "diaSemana": "Quinta",
        "fase": 1,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-10-29-0",
                "disciplina": "ATU",
                "titulo": "História, Geografia e Formação de Barão de Cotegipe (RS)",
                "detalhe": "Barão de Cotegipe (RS): Norte do RS, região do Alto Uruguai. Povoamento por volta de 1911 (povoado Floresta; italianos, poloneses, ucranianos, lituanos e caboclos). Distrito Cotegipe em 1939, Barão de Cotegipe desde 1944. Município criado pela lei estadual 4.737 de 01/06/1964 (desmembrado de Erechim, Aratiba e São Valentim) e instalado em 23/01/1965. Limites: Erechim, São Valentim, Itatiba do Sul, Barra do Rio Azul, Ponte Preta e Paulo Bento. Fonte: IBGE (histórico do município). Bioma e clima: conferir em fonte oficial.",
                "minutos": 60,
                "materiais": ["pref_bc", "ibge_bc", "apo_realidade", "mapa_realidade"]
            },
            {
                "id": "2026-10-29-1",
                "disciplina": "ATU",
                "titulo": "Dados Oficiais do IBGE de Barão de Cotegipe: População (Censo 2022), Área e Economia",
                "detalhe": "Dados do IBGE Cidades: Censo 2022: 7.144 habitantes, densidade de 27,42 hab/km², área de 260,5 km², gentílico cotegipense. Economia com predomínio do setor primário (milho, trigo, soja, feijão, erva-mate, frango, leite e suínos). Não há Poder Judiciário municipal. PIB per capita (IBGE 2023): R$ 45.460,37. Câmara com 9 vereadores. IDEB e IDHM: não confirmados.",
                "minutos": 60,
                "materiais": ["ibge_bc", "apo_realidade", "mapa_realidade"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-10-30",
        "diaSemana": "Sexta",
        "fase": 1,
        "marcos": [
            "ÚLTIMO DIA DE INSCRIÇÕES E PAGAMENTO DA TAXA DE INSCRIÇÃO (R$ 180,00)",
            "Conferir se o comprovante bancário de pagamento da taxa foi emitido com sucesso."
        ],
        "tarefas": [
            {
                "id": "2026-10-30-0",
                "disciplina": "ESP",
                "titulo": "Código de Ética Odontológica (Resolução CFO 118/2012): Direitos, Deveres e Sigilo Profissional",
                "detalhe": "Resolução CFO 118/2012. Direitos fundamentais do cirurgião-dentista (diagnosticar, planejar e executar tratamentos com liberdade de convicção; recusar ato que contrarie os ditames da consciência; guardar sigilo). Deveres fundamentais: zelar e trabalhar pelo perfeito desempenho ético da Odontologia; manter atualizados os conhecimentos; prestar assistência a paciente em perigo de vida iminente sem se preocupar com remuneração. Sigilo profissional (Cap. VI): é infração ética revelar fato de que tenha conhecimento em razão do exercício da profissão, salvo por justa causa, dever legal ou autorização expressa do paciente.",
                "minutos": 60,
                "materiais": ["codigo_etica_cfo"]
            },
            {
                "id": "2026-10-30-1",
                "disciplina": "ESP",
                "titulo": "Biossegurança e NR-32 na Clínica Odontológica da Atenção Básica",
                "detalhe": "Biossegurança no consultório odontológico: Cadeia de transmissão de infecções (direta, indireta, aerossóis e gotículas). Limpeza, desinfecção e esterilização de artigos (artigos críticos exigem esterilização em autoclave a vapor saturado sob pressão; semi-críticos desinfecção de alto nível; não-críticos limpeza e desinfecção de nível intermediário/baixo). Monitoramento da esterilização (físico, químico - integradores classe 5/6, e biológico com Geobacillus stearothermophilus semanal). Descarte de perfurocortantes (embalagem rígida até 2/3 da capacidade). NR-32: Vacinação obrigatória do profissional (Hepatite B, Tétano/Difteria, Tríplice Viral, Influenza).",
                "minutos": 60,
                "materiais": ["nr32", "v_nr32", "caderno_atencao_bucal"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-10-31",
        "diaSemana": "Sábado",
        "fase": 1,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-10-31-0",
                "disciplina": "SAU",
                "titulo": "Decreto 7.508/2011: Regiões de Saúde, Portas de Entrada e Redes de Atenção",
                "detalhe": "Decreto 7.508/2011 (regulamenta a Lei 8.080/90). Conceito de Região de Saúde: espaço geográfico contínuo para integrar planejamento e ações. Requisitos mínimos para instituir Região de Saúde: (I) atenção primária; (II) urgência e emergência; (III) atenção psicossocial; (IV) atenção ambulatorial especializada e hospitalar; (V) vigilância em saúde. Portas de Entrada às ações e serviços de saúde: atenção primária; urgência e emergência; atenção psicossocial; e especiais de acesso aberto. Protocolo de Acesso e Regulação em Saúde.",
                "minutos": 60,
                "materiais": ["dec7508"]
            },
            {
                "id": "2026-10-31-1",
                "disciplina": "SAU",
                "titulo": "Decreto 7.508/2011: COAP, Mapa da Saúde, RENAME e RENASES",
                "detalhe": "Instrumentos do Decreto 7.508: Mapa da Saúde (descrição geográfica da distribuição de recursos humanos e de ações e serviços de saúde ofertados pelo SUS e iniciativa privada); RENAME (Relação Nacional de Medicamentos Essenciais - compreende seleção de medicamentos e insumos); RENASES (Relação Nacional de Ações e Serviços de Saúde); COAP (Contrato Organizativo da Ação Pública da Saúde - acordo de colaboração firmado entre entes federativos para organizar a rede interfederativa).",
                "minutos": 60,
                "materiais": ["dec7508"]
            }
        ],
        "totalMin": 120
    },

    # ----------------- SEMANA 2 (01/11 a 07/11) -----------------
    {
        "data": "2026-11-01",
        "diaSemana": "Domingo",
        "fase": 1,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-11-01-0",
                "disciplina": "LEG",
                "titulo": "Constituição Federal: Direitos e Deveres Individuais e Coletivos (Art. 5º)",
                "detalhe": "Art. 5º da CF/88 (Caput e incisos mais cobrados em prova): Inviolabilidade do direito à vida, liberdade, igualdade, segurança e propriedade. Inviolabilidade do domicílio (a casa é asilo inviolável, ninguém nela podendo penetrar sem consentimento, salvo flagrante delito, desastre, prestar socorro, ou durante o dia por determinação judicial!). Sigilo de correspondência e comunicações telegráficas/dados/telefônicas (escuta telefônica só por ordem judicial para investigação criminal ou instrução penal). Remédios constitucionais: Habeas Corpus (liberdade de locomoção), Habeas Data (acesso/retificação de informações pessoais), Mandado de Segurança (direito líquido e certo não amparado por HC ou HD), Ação Popular (anular ato lesivo ao patrimônio público, moralidade, meio ambiente, patrimônio histórico).",
                "minutos": 60,
                "materiais": ["cf88_geral"]
            },
            {
                "id": "2026-11-01-1",
                "disciplina": "LEG",
                "titulo": "Constituição Federal: Direitos Sociais (Arts. 6º a 11) e Nacionalidade (Arts. 12 e 13)",
                "detalhe": "Art. 6º Direitos Sociais: Educação, saúde, alimentação, trabalho, moradia, transporte, lazer, segurança, previdência social, proteção à maternidade e à infância, assistência aos desamparados (mnemônico: EDU MORA LA, TRABALHA LA, TEM TRANSPORTE, SAUDE, SEGURANÇA E PREVIDENCIA, ALIMENTAÇÃO, MATERNIDADE E DESAMPARADOS). Nacionalidade (Art. 12): Brasileiros natos (ius soli e hipóteses de ius sanguinis) vs naturalizados. Cargos privativos de brasileiro nato (Art. 12, §3º - MP3.COM: Presidente e Vice-Presidente da República; Presidente da Câmara dos Deputados; Presidente do Senado Federal; Ministros do STF; Carreira diplomática; Oficial das Forças Armadas; Ministro de Estado da Defesa).",
                "minutos": 60,
                "materiais": ["cf88_sociais"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-02",
        "diaSemana": "Segunda",
        "fase": 1,
        "marcos": ["Feriado de Finados (Manter o ritmo: 2h de estudo hoje garantem aprovação!)"],
        "tarefas": [
            {
                "id": "2026-11-02-0",
                "disciplina": "ESP",
                "titulo": "Cariologia, Diagnóstico e Tratamento Restaurador Atraumático (ART) no PSF",
                "detalhe": "Etiologia da cárie dentária: biofilme açúcar-dependente (Streptococcus mutans, Lactobacillus), dinâmica des-re (desmineralização e remineralização em pH crítico 5,5 para esmalte e 6,5 para dentina/cemento). Diagnóstico precoce (lesão de mancha branca ativa: opaca, rugosa, perto da margem gengival; inativa: brilhante, lisa, pigmentada). Filosofia da Odontologia Minimamente Invasiva. ART (Tratamento Restaurador Atraumático): remoção seletiva de tecido cariado amolecido com instrumentos MANUAIS (sem motor) e selamento de fossas/fissuras e cavidades com Cimento de Ionômero de Vidro (CIV) de alta viscosidade.",
                "minutos": 60,
                "materiais": ["manual_art", "caderno_atencao_bucal"]
            },
            {
                "id": "2026-11-02-1",
                "disciplina": "ESP",
                "titulo": "Materiais Odontológicos Forradores e Restauradores e Proteção Dentinopulpar",
                "detalhe": "Proteção do complexo dentinopulpar: Cavidade rasa (sistema adesivo + resina), média (CIV + restauração), profunda sem exposição (CIV ou hidróxido de cálcio na parede de fundo + CIV de base), exposição pulpar acidental (capeamento pulpar direto com Hidróxido de Cálcio pró-análise ou MTA + CIV de base). Propriedades dos materiais: Resinas compostas (matriz orgânica Bis-GMA, partículas inorgânicas de carga, agente de união silano); CIV (liberação contínua de flúor, adesão química ao cálcio de esmalte e dentina, coeficiente de expansão térmica similar ao dente, biocompatibilidade).",
                "minutos": 60,
                "materiais": ["caderno_atencao_bucal"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-03",
        "diaSemana": "Terça",
        "fase": 1,
        "marcos": ["Divulgação da Relação Preliminar de Inscrições Homologadas pela Banca Instituto DOM."],
        "tarefas": [
            {
                "id": "2026-11-03-0",
                "disciplina": "POR",
                "titulo": "Sintaxe do Período Complexo: Orações Desenvolvidas, Reduzidas e Paralelismo Sintático",
                "detalhe": "Orações coordenadas (assindéticas e sindéticas). Orações subordinadas substantivas (subjetiva, objetiva direta, objetiva indireta, completiva nominal, predicativa, apositiva - introduzidas por conjunção integrante 'que'/'se'). Orações subordinadas adjetivas (explicativas entre vírgulas vs restritivas sem vírgulas - introduzidas por pronome relativo). Orações reduzidas de infinitivo, gerúndio e particípio. Paralelismo sintático e correlação de estruturas.",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            },
            {
                "id": "2026-11-03-1",
                "disciplina": "POR",
                "titulo": "Funções Sintáticas e Morfológicas das Partículas 'QUE' e 'SE'",
                "detalhe": "Funções do 'QUE': Conjunção integrante (substituível por 'isso': 'Quero que você passe' = 'Quero isso'); Pronome relativo (substituível por 'o qual/a qual' e introduz oração adjetiva); Substantivo ('Tem um quê de mistério'); Partícula expletiva ('Quase que caí'); Conjunção consecutiva ('Tanto gritou que ficou rouco'). Funções do 'SE': Pronome apassivador (com verbo transitivo direto e sujeito paciente: 'Vendem-se casas' = casas são vendidas); Índice de indeterminação do sujeito (com VTI, VI ou VL + verbo na 3ª pess. singular: 'Precisa-se de dentistas'); Conjunção subordinativa condicional ('Se estudar, vencerá'); Conjunção integrante ('Não sei se virá').",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-04",
        "diaSemana": "Quarta",
        "fase": 1,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-11-04-0",
                "disciplina": "MAT",
                "titulo": "Lógica de Primeira Ordem: Quantificadores Lógicos (Todo, Algum, Nenhum) e Silogismos",
                "detalhe": "Negação de quantificadores categóricos (muito cobrado!): (1) Negação de 'TODO A é B': 'ALGUM A NÃO é B' (ou 'Existe pelo menos um A que não é B' / 'Pelo menos um A não é B'). ATENÇÃO: A negação de 'Todo' NUNCA é 'Nenhum'!; (2) Negação de 'NENHUM A é B': 'ALGUM A é B'; (3) Negação de 'ALGUM A é B': 'NENHUM A é B' (ou 'Todo A não é B'). Diagramas de Euler-Venn para testar validade de silogismos categóricos.",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            },
            {
                "id": "2026-11-04-1",
                "disciplina": "MAT",
                "titulo": "Teoria dos Conjuntos: Operações, Cardinalidade e Diagramas de Venn para 2 e 3 Conjuntos",
                "detalhe": "Operações: União (A ∪ B), Intersecção (A ∩ B), Diferença (A - B: elementos que pertencem a A e não pertencem a B), Complementar. Princípio da Inclusão-Exclusão para dois conjuntos: n(A ∪ B) = n(A) + n(B) - n(A ∩ B). Para três conjuntos: n(A ∪ B ∪ C) = n(A) + n(B) + n(C) - n(A ∩ B) - n(A ∩ C) - n(B ∩ C) + n(A ∩ B ∩ C). Resolução de problemas com diagramas partindo sempre da intersecção central mais profunda.",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-05",
        "diaSemana": "Quinta",
        "fase": 1,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-11-05-0",
                "disciplina": "SAU",
                "titulo": "Política Nacional de Atenção Básica (PNAB – Portaria 2.436/2017): Princípios e Diretrizes",
                "detalhe": "PNAB Portaria 2.436/2017: A Atenção Básica é a principal porta de entrada e centro de comunicação da Rede de Atenção à Saúde (RAS). Princípios: Universalidade, Equidade e Integralidade. Diretrizes da Atenção Básica: Regionalização e Hierarquização; Territorialização; População Adscrita; Cuidado centrado na pessoa; Resolutividade; Longitudinalidade do cuidado; Coordenação do cuidado; Ordenação da rede; e Participação da comunidade. Carga horária da equipe da Estratégia Saúde da Família (ESF): 40 horas semanais para todos os profissionais.",
                "minutos": 60,
                "materiais": ["pnab", "caderno_atencao_bucal"]
            },
            {
                "id": "2026-11-05-1",
                "disciplina": "SAU",
                "titulo": "A Equipe de Saúde Bucal (eSB) na Estratégia Saúde da Família e Atribuições do Dentista",
                "detalhe": "Equipe de Saúde Bucal (eSB) no PSF/ESF: Modalidade I (Cirurgião-Dentista + Auxiliar em Saúde Bucal - ASB ou Técnico em Saúde Bucal - TSB); Modalidade II (Cirurgião-Dentista + TSB + ASB ou 2 TSBs). Atribuições do Cirurgião-Dentista no PSF: diagnóstico e tratamento de afecções bucais; realização de urgências; visitas domiciliares a pacientes acamados; atividades de educação e prevenção em escolas e creches (PSE); prescrição de medicamentos; encaminhamento responsável para CEO (Centro de Especialidades Odontológicas) via regulação.",
                "minutos": 60,
                "materiais": ["pnab", "caderno_atencao_bucal"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-06",
        "diaSemana": "Sexta",
        "fase": 1,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-11-06-0",
                "disciplina": "ATU",
                "titulo": "Atualidades Globais e Nacionais: Geopolítica, Macroeconomia e Conflitos Contemporâneos",
                "detalhe": "Geopolítica contemporânea: Reorganização da ordem mundial multipolar (EUA, China, União Europeia, expansão dos BRICS). Conflitos na Ucrânia e no Oriente Médio e seus impactos econômicos (inflação de alimentos, petróleo e fertilizantes). Economia brasileira: Metas de inflação (IPCA), Taxa Básica de Juros (Selic do Banco Central), Produto Interno Bruto (PIB) e o papel do agronegócio na balança comercial brasileira. Comércio exterior e blocos econômicos (Mercosul).",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            },
            {
                "id": "2026-11-06-1",
                "disciplina": "ATU",
                "titulo": "Ciência, Tecnologia e Inovação: Inteligência Artificial e Transformação Digital",
                "detalhe": "Avanços em inteligência artificial generativa, automação no mercado de trabalho e impactos éticos e de privacidade. Cibersegurança e proteção de dados (LGPD). Transição energética e descarbonização da economia: matriz energética brasileira (predominância hídrica, crescimento solar e eólica, biocombustíveis e hidrogênio verde). Desafios da inclusão digital e governo eletrônico no Brasil (plataformas gov.br).",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-07",
        "diaSemana": "Sábado",
        "fase": 1,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-11-07-0",
                "disciplina": "ESP",
                "titulo": "Farmacologia Odontológica: Analgésicos, Anti-inflamatórios Não Esteroidais (AINEs) e Corticoides",
                "detalhe": "Mecanismo de ação: AINEs inibem a ciclo-oxigenase (COX-1 e COX-2), bloqueando a síntese de prostaglandinas. Indicações e contraindicações clínicas: Ibuprofeno (400 a 600mg de 8/8h), Nimesulida (100mg 12/12h), Cetoprofeno (100mg 12/12h). Contraindicações de AINEs: úlcera péptica ativa, insuficiência renal grave, asma, gravidez no 3º trimestre. Dipirona (500mg a 1g) e Paracetamol (500 a 750mg) em analgesia. Corticoides em dose única pré-operatória preemptiva (Dexametasona 4 a 8mg VO) para controle do edema inflamatório em cirurgias de terceiros molares.",
                "minutos": 60,
                "materiais": ["caderno_atencao_bucal"]
            },
            {
                "id": "2026-11-07-1",
                "disciplina": "ESP",
                "titulo": "Farmacologia Odontológica: Antibioticoterapia Racional e Profilaxia da Endocardite Infecciosa",
                "detalhe": "Antibióticos de 1ª escolha em infecções odontogênicas: Amoxicilina 500mg (8/8h por 5 a 7 dias). Em caso de alergia a penicilinas: Clindamicina (300mg 6/6h), Azitromicina (500mg 1x/dia por 3 dias) ou Claritromicina (500mg 12/12h). Profilaxia antibiótica para Endocardite Infecciosa (indicações AHA/SBC: prótese valvar cardíaca, antecedente de endocardite prévia, cardiopatia congênita cianótica não reparada): Amoxicilina 2g via oral 30 a 60 minutos antes do procedimento. Se alérgico: Clindamicina 600mg ou Azitromicina 500mg 1h antes.",
                "minutos": 60,
                "materiais": ["caderno_atencao_bucal"]
            }
        ],
        "totalMin": 120
    },

    # ----------------- SEMANA 3 (08/11 a 14/11) -----------------
    {
        "data": "2026-11-08",
        "diaSemana": "Domingo",
        "fase": 1,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-11-08-0",
                "disciplina": "LEG",
                "titulo": "Atos Administrativos: Conceito, Requisitos de Validade (CO-FI-FO-M-OB) e Atributos (PATI)",
                "detalhe": "Requisitos ou elementos de validade: Competência (sujeito competente; irrenunciável, pode ser delegada/avocada se a lei não vedar), Finalidade (interesse público; desvio de finalidade gera nulidade), Forma (exteriorização do ato; em regra escrito), Motivo (situação de fato e de direito que autoriza o ato; Teoria dos Motivos Determinantes), Objeto (conteúdo do ato, efeito jurídico imediato). Atributos do ato (PATI): Presunção de legitimidade/veracidade; Autoexecutoriedade; Tipicidade; Imperatividade (poder extroverso que cria obrigações a terceiros).",
                "minutos": 60,
                "materiais": ["cf88_adm"]
            },
            {
                "id": "2026-11-08-1",
                "disciplina": "LEG",
                "titulo": "Extinção dos Atos Administrativos: Anulação vs Revogação e Convalidação",
                "detalhe": "Diferença crucial para concurso: Anulação (decorre de ILEGALIDADE; pode ser feita pela Administração - Súmulas 346 e 473 do STF - ou pelo Poder Judiciário; efeito retroativo EX TUNC, apagando os efeitos desde a origem) vs Revogação (decorre de juízo de CONVENIÊNCIA e OPORTUNIDADE; SÓ pode ser feita pela própria Administração, NUNCA pelo Judiciário em atos alheios; efeito prospectivo EX NUNC, respeitando os direitos adquiridos). Convalidação: saneamento de defeito de competência ou forma (desde que não essenciais e não causem lesão ao interesse público).",
                "minutos": 60,
                "materiais": ["cf88_adm"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-09",
        "diaSemana": "Segunda",
        "fase": 2,
        "marcos": [
            "INÍCIO DA FASE 2 – QUESTÕES, PEGADINHAS E APROFUNDAMENTO DA BANCA (Faltam 13 dias para a Prova)",
            "Foco na fixação por alternativas corretas e esquemas visuais."
        ],
        "tarefas": [
            {
                "id": "2026-11-09-0",
                "disciplina": "POR",
                "titulo": "Concordância Verbal e Nominal Avançada: Regras Especiais e Casos de Prova",
                "detalhe": "Concordância verbal: Sujeito composto anteposto ao verbo (verbo no plural); Sujeito composto posposto (verbo no plural ou concorda com o mais próximo). Expressões partitivas ('a maioria de', 'grande parte de' + plural: verbo no singular ou no plural: 'A maioria dos dentistas participou / participaram'). Sujeito com porcentagem ('1% votou', '20% votaram'; se houver especificador, concorda com ele: '1% dos alunos faltaram'). Verbo HAVER no sentido de existir ou indicando tempo decorrido é IMPESSOAL (fica estritamente na 3ª pessoa do singular: 'Havia muitas vagas', NUNCA 'Haviam'). Verbo FAZER indicando tempo ou clima também é impessoal ('Faz dez anos', 'Faz dias frios').",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            },
            {
                "id": "2026-11-09-1",
                "disciplina": "POR",
                "titulo": "Regência Verbal e Nominal e o Emprego do Acento Indicativo de Crase",
                "detalhe": "Verbos com regências notáveis: Assistir (no sentido de ver/presenciar exige preposição 'a': assistiu ao filme; no sentido de ajudar é VTD: assistiu o enfermo; no sentido de caber/pertencer exige 'a': assiste ao réu o direito). Aspirar (no sentido de desejar exige 'a': aspirava ao cargo; no sentido de sorver é VTD: aspirava o ar puro). Visar (almejar exige 'a': visava ao cargo). Obedecer/Desobedecer (exigem sempre preposição 'a': obedeceu às normas). CRASE: Fusão da preposição 'a' com artigo feminino 'a'. Nunca ocorre crase antes de verbo, antes de palavras masculinas, antes de pronomes de tratamento e pronomes indefinidos/pessoais.",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-10",
        "diaSemana": "Terça",
        "fase": 2,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-11-10-0",
                "disciplina": "MAT",
                "titulo": "Análise Combinatória: Princípio Fundamental da Contagem, Permutação e Combinação",
                "detalhe": "Como diferenciar Arranjo/Permutação de Combinação: Na Combinação, a ordem dos elementos NÃO altera o grupo (ex: formar uma comissão de 3 pessoas; escolher 3 perguntas entre 10). Fórmula: C(n, p) = n! / [p! · (n - p)!]. No Arranjo e na Permutação, a ordem dos elementos IMPORTA e cria um resultado novo (ex: senhas, números de telefone, 1º e 2º lugar, anagramas). Permutação simples: Pn = n!. Permutação com repetição: Pn^(a,b) = n! / (a! · b!).",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            },
            {
                "id": "2026-11-10-1",
                "disciplina": "MAT",
                "titulo": "Probabilidade Clássica e Condicional: Eventos Dependentes e Independentes",
                "detalhe": "Probabilidade simples: P(A) = Casos Favoráveis / Casos Possíveis (Espaço Amostral). Probabilidade da união de dois eventos: P(A ∪ B) = P(A) + P(B) - P(A ∩ B). Se mutuamente exclusivos: P(A ∪ B) = P(A) + P(B). Probabilidade condicional: P(A|B) = P(A ∩ B) / P(B) (probabilidade de ocorrer A sabendo que B já ocorreu). Evento complementar: P(~A) = 1 - P(A) (ótima estratégia para problemas do tipo 'qual a probabilidade de pelo menos um...').",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-11",
        "diaSemana": "Quarta",
        "fase": 2,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-11-11-0",
                "disciplina": "SAU",
                "titulo": "HumanizaSUS (PNH): Princípios, Método e Acolhimento com Classificação de Risco",
                "detalhe": "HumanizaSUS (Política Nacional de Humanização): Princípios: (1) Transversalidade (aumento da comunicação entre diferentes especialidades e serviços); (2) Indissociabilidade entre atenção e gestão; (3) Protagonismo, corresponsabilidade e autonomia dos sujeitos e dos coletivos. Método: Tríplice inclusão (gestores, trabalhadores e usuários no planejamento e decisões). Dispositivos centrais: Acolhimento com Classificação de Risco (a prioridade de atendimento é dada pelo GRAU DE AGRAVO/VULNERABILIDADE clínica, e NUNCA exclusivamente pela ordem de chegada!); Equipe de referência e apoio matricial; Ambiência acolhedora; Projeto Terapêutico Singular (PTS).",
                "minutos": 60,
                "materiais": ["pnh", "v_aula7"]
            },
            {
                "id": "2026-11-11-1",
                "disciplina": "SAU",
                "titulo": "Inclusão e Vulnerabilidades: LBI (Lei 13.146/2015) e TEA no SUS (Lei 12.764/2012)",
                "detalhe": "Lei Brasileira de Inclusão (Lei 13.146/2015): Avaliação da deficiência biopsicossocial realizada por equipe multiprofissional e interdisciplinar. Direito à saúde assegurado com atendimento prioritário e acessibilidade universal. Política Nacional de Proteção dos Direitos da Pessoa com TEA (Lei 12.764/2012): A pessoa com transtorno do espectro autista é considerada pessoa com deficiência para todos os efeitos legais. Garantia de diagnóstico precoce, tratamento multidisciplinar e medicamentos no SUS. Portaria 3.088/2011 (RAPS - Rede de Atenção Psicossocial) e Lei 10.216/2001 (Reforma Psiquiátrica): proteção aos direitos das pessoas portadoras de transtornos mentais.",
                "minutos": 60,
                "materiais": ["lbi", "v_aula4", "lei_tea", "raps"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-12",
        "diaSemana": "Quinta",
        "fase": 2,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-11-12-0",
                "disciplina": "ESP",
                "titulo": "Anestesiologia Odontológica: Mecanismos de Ação, Farmacologia dos Anestésicos e Vasoconstritores",
                "detalhe": "Mecanismo de ação dos anestésicos locais: bloqueio reversível dos canais de sódio voltagem-dependentes na membrana axônica neuronal, impedindo a despolarização e condução do impulso nervoso. Anestésicos tipo amida (metabolização hepática): Lidocaína (padrão ouro, segura na gestação - categoria B), Articaína (metabolização 90% plasmática por colinesterases, alta difusibilidade tecidual), Mepivacaína, Prilocaína (risco de metemoglobinemia), Bupivacaína (longa duração). Vasoconstritores: Epinefrina (estimula receptores alfa e beta; hemostasia e aumento da duração anestésica). Limite para cardiopatas compensados: 0,04mg de epinefrina (cerca de 2 tubetes de lidocaína 2% com epinefrina 1:100.000).",
                "minutos": 60,
                "materiais": ["caderno_atencao_bucal"]
            },
            {
                "id": "2026-11-12-1",
                "disciplina": "ESP",
                "titulo": "Técnicas Anestésicas e Complicações: Bloqueio do Nervo Alveolar Inferior e Acidentes",
                "detalhe": "Técnicas infiltrativas (maxila, osso poroso) vs bloqueios regionais (mandíbula, osso cortical espesso). Bloqueio do Nervo Alveolar Inferior (BNAI) e nervo lingual: reparos anatômicos (linha oblíqua, fossa pterigotemporal, prega pterigomandibular, plano oclusal a 1cm acima dos molares inferiores). Bloqueio do nervo bucal para gengiva vestibular dos molares inferiores. Acidentes e complicações: quebra de agulha, trismo (espasmo muscular por trauma no pterigoideo medial), parestesia (trauma mecânico com agulha no tronco nervoso), hematoma, paralisia facial transitória (injeção dentro da glândula parótida posterior à mandíbula), toxicidade sistêmica por injeção intravascular acidental (aspirar sempre antes de injetar!).",
                "minutos": 60,
                "materiais": ["caderno_atencao_bucal"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-13",
        "diaSemana": "Sexta",
        "fase": 2,
        "marcos": [
            "PUBLICAÇÃO DO EDITAL DE CONVOCAÇÃO PARA A PROVA OBJETIVA (Locais e Horários de Prova)",
            "Conferir no site do Instituto DOM o local exato onde fará a prova em Barão de Cotegipe."
        ],
        "tarefas": [
            {
                "id": "2026-11-13-0",
                "disciplina": "LEG",
                "titulo": "Poderes Administrativos: Vinculado, Discricionário, Hierárquico, Disciplinar, Regulamentar e de Polícia",
                "detalhe": "Diferenças fundamentais entre os poderes: Poder Vinculado (a lei fixa um único comportamento possível para a Administração, sem margem de escolha) vs Poder Discricionário (a lei confere margem de conveniência e oportunidade dentro dos limites legais). Poder Hierárquico (escalonamento de órgãos, delegar e avocar competências, dar ordens). Poder Disciplinar (punir faltas internas de servidores e pessoas com vínculo específico com a Administração; não se confunde com sanção penal). Poder Regulamentar (decretos para fiel execução da lei, sem inovar o ordenamento). Poder de Polícia (condicionar e restringir o uso de bens, direitos e liberdades em prol do interesse coletivo; atributos: discricionariedade, autoexecutoriedade e coercibilidade).",
                "minutos": 60,
                "materiais": ["cf88_adm"]
            },
            {
                "id": "2026-11-13-1",
                "disciplina": "LEG",
                "titulo": "Agentes Públicos, Regime Estatutário, Provimento, Vacância e Acumulação de Cargos",
                "detalhe": "Classificação dos agentes: políticos, administrativos (servidores estatutários e empregados públicos), honoríficos, delegados e credenciados. Provimento originário (nomeação mediante concurso público) vs derivados (readaptação, recondução, reintegração, reversão, aproveitamento). Vacância (exoneração, demissão, promoção, readaptação, aposentadoria, posse em outro cargo inacumulável, falecimento). Acumulação de cargos públicos (Regra: proibida, salvo compatibilidade de horários para: 2 cargos de professor; 1 cargo de professor com outro técnico/científico; e 2 CARGOS PRIVATIVOS DE PROFISSIONAIS DE SAÚDE com profissões regulamentadas, como é o caso de Odontólogo!).",
                "minutos": 60,
                "materiais": ["cf88_adm", "regime_bc"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-14",
        "diaSemana": "Sábado",
        "fase": 2,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-11-14-0",
                "disciplina": "ATU",
                "titulo": "Sustentabilidade, Meio Ambiente e Biomas Brasileiros",
                "detalhe": "Meio ambiente e sustentabilidade no cenário nacional: Os seis biomas brasileiros (Amazônia, Cerrado, Mata Atlântica, Caatinga, Pampa e Pantanal). No Rio Grande do Sul: biomas Pampa e Mata Atlântica. Desafios de eventos climáticos extremos (secas e enchentes no RS), segurança hídrica e conservação do solo agrícola. Acordos climáticos globais (Acordo de Paris, Conferências do Clima da ONU - COPs).",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            },
            {
                "id": "2026-11-14-1",
                "disciplina": "ATU",
                "titulo": "Direitos Humanos, Diversidade Sociocultural e Cidadania no Brasil",
                "detalhe": "Cidadania e direitos humanos: Avanços e desafios na garantia de direitos fundamentais. Movimentos sociais e políticas afirmativas no Brasil. Indicadores sociais e demografia brasileira: envelhecimento populacional acelerado (transição demográfica apontada no Censo 2022), taxa de fecundidade abaixo da taxa de reposição. Educação e saúde como pilares do Índice de Desenvolvimento Humano (IDH).",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            }
        ],
        "totalMin": 120
    },

    # ----------------- SEMANA 4 (15/11 a 21/11) -----------------
    {
        "data": "2026-11-15",
        "diaSemana": "Domingo",
        "fase": 3,
        "marcos": [
            "Feriado da Proclamação da República",
            "INÍCIO DA FASE 3 – REVISÃO GERAL E SIMULADOS FINAIS (Faltam 7 dias para a Prova)"
        ],
        "tarefas": [
            {
                "id": "2026-11-15-0",
                "disciplina": "REV",
                "titulo": "Simulado Geral Integrado: Bloco 1 (Português, Matemática/RL e Atualidades)",
                "detalhe": "Resolução de 15 questões simuladas (5 de Português, 5 de Matemática e 5 de Atualidades/Realidade Municipal). Cronometrar 1 hora e 30 minutos. Ao terminar, conferir gabarito: destacar cada resposta correta em frase afirmativa verde e revisar os erros com calma.",
                "minutos": 60,
                "materiais": ["anexo_prog", "mapa_prog"]
            },
            {
                "id": "2026-11-15-1",
                "disciplina": "REV",
                "titulo": "Simulado Geral Integrado: Bloco 2 (Legislação, Conhecimentos sobre Saúde e Específicos)",
                "detalhe": "Resolução de 15 questões simuladas (5 de Legislação Municipal/Geral, 5 de Conhecimentos sobre Saúde e 5 de Conhecimentos Específicos de Odontologia). Cronometrar 1 hora e 30 minutos. Calcular a nota final: meta mínima = 36 pontos (18 acertos em 30). Identificar temas prioritários para a semana de revisão.",
                "minutos": 60,
                "materiais": ["anexo_prog", "mapa_prog"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-16",
        "diaSemana": "Segunda",
        "fase": 3,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-11-16-0",
                "disciplina": "POR",
                "titulo": "Redação Oficial (Manual da Presidência da República 3ª Edição): Princípios e Padrão Ofício",
                "detalhe": "Manual de Redação da PR (3ª ed.): Princípios constitucionais da redação oficial (Clareza, Precisão, Objetividade, Concisão, Coesão, Impessoalidade, Formalidade e Padronização). O Padrão Ofício: uniformizou o Aviso, Ofício e Memorando (o termo 'Memorando' foi extinto no âmbito federal, mantendo-se a estrutura padrão). Elementos do documento: cabeçalho com brasão das armas, identificação do expediente, local e data, endereçamento com vocativo adequado, corpo do texto com parágrafos numerados (exceto o primeiro e o fecho), fecho para autoridades ('Respeitosamente' para autoridades de hierarquia superior; 'Atenciosamente' para autoridades de mesma hierarquia ou inferior).",
                "minutos": 60,
                "materiais": ["manual_redacao_pr"]
            },
            {
                "id": "2026-11-16-1",
                "disciplina": "POR",
                "titulo": "Pontuação Estilística e Sintática e Figuras de Linguagem Mais Cobradas",
                "detalhe": "Regras obrigatórias de pontuação: NUNCA se separa com vírgula o sujeito do seu verbo, nem o verbo do seu complemento direto ou indireto! Vírgula obrigatória para isolar vocativo, aposto explicativo, orações adjetivas explicativas, orações coordenadas adversativas ('mas', 'porém') e adjunto adverbial deslocado de grande extensão. Figuras de sintaxe/pensamento em concursos: Hipérbato (inversão da ordem direta), Anacoluto (quebra da estrutura sintática), Zeugma (omissão de termo já expresso), Paradoxo (ideias inconciliáveis) e Metonímia.",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-17",
        "diaSemana": "Terça",
        "fase": 3,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-11-17-0",
                "disciplina": "MAT",
                "titulo": "Matemática Financeira Básica: Porcentagem, Juros Simples e Compostos",
                "detalhe": "Fórmulas de ouro: Juros Simples: J = C · i · t e Montante: M = C + J = C · (1 + i · t) (atenção: taxa 'i' e tempo 't' devem estar na mesma unidade de tempo!). Juros Compostos: M = C · (1 + i)^t. Aumentos e descontos sucessivos: Fator de aumento = (1 + taxa); Fator de redução = (1 - taxa). Exemplo: aumento de 10% seguido de aumento de 20% = 1,10 · 1,20 = 1,32 (aumento real de 32%, e NUNCA a soma direta de 30%!).",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            },
            {
                "id": "2026-11-17-1",
                "disciplina": "MAT",
                "titulo": "Análise Crítica de Dados, Tabelas Estatísticas e Gráficos em Concursos",
                "detalhe": "Interpretação de gráficos de barras, colunas, setores (pizza) e linhas. Medidas de tendência central: Média aritmética simples e ponderada; Mediana (valor central com os dados ordenados em rol; se número par, média dos dois centrais); Moda (valor de maior frequência absoluta). Medidas de dispersão: Amplitude, Variância e Desvio Padrão (raiz quadrada da variância; quanto menor o desvio padrão, mais homogêneo é o conjunto de dados).",
                "minutos": 60,
                "materiais": ["anexo_prog"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-18",
        "diaSemana": "Quarta",
        "fase": 3,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-11-18-0",
                "disciplina": "ESP",
                "titulo": "Cirurgia Oral Menor na Atenção Básica: Princípios de Exodontia e Cuidados Cirúrgicos",
                "detalhe": "Tempos cirúrgicos fundamentais: Diérese (incisão/descolamento), Exérese (remoção do dente/lesão), Hemostasia e Síntese (sutura). Princípios mecânicos dos fórceps e alavancas (alavanca de primeira classe interfixa, cunha e roda/eixo). Movimentos de luxação e expansão alveolar (intrusão, lateralidade vestibular/lingual, rotação para raízes cônicas e tração). Cuidados pré-operatórios: anamnese detalhada, controle pressórico e glicêmico. Cuidados pós-operatórios: mordedura de gaze por 30-45 min, gelo nas primeiras 24-48h, repouso, dieta fria e líquida/pastosa no 1º dia, evitar bochechos vigorosos para não deslocar o coágulo sanguíneo.",
                "minutos": 60,
                "materiais": ["caderno_atencao_bucal"]
            },
            {
                "id": "2026-11-18-1",
                "disciplina": "ESP",
                "titulo": "Urgências Odontológicas, Traumatismo Alvéolo-Dentário e Complicações Cirúrgicas",
                "detalhe": "Alveolite: Alveolite seca (ausência de coágulo, osso alveolar exposto, dor latejante intensa no 3º-4º dia pós-operatório; conduta: irrigação suave com soro morno e curativo alveolar com óxido de zinco/eugenol) vs Alveolite úmida (presença de coágulo necrótico e supuração). Traumatismo alvéolo-dentário: Concussão, Subluxação, Luxação extrusiva/lateral/intrusiva e Avulsão. Protocolo padrão-ouro na Avulsão dentária: reimplante imediato no local do acidente se possível; se não, transportar em meio de conservação (leite gelado, saliva do paciente ou soro fisiológico - NUNCA em água pura ou a seco!); não raspar a raiz; contenção flexível por 7 a 14 dias.",
                "minutos": 60,
                "materiais": ["caderno_atencao_bucal"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-19",
        "diaSemana": "Quinta",
        "fase": 3,
        "marcos": [],
        "tarefas": [
            {
                "id": "2026-11-19-0",
                "disciplina": "SAU",
                "titulo": "Controle Social no SUS: Lei 8.142/1990 e Resolução CNS 453/2012 (Conselhos e Conferências)",
                "detalhe": "Lei 8.142/90: Duas instâncias colegiadas do SUS em cada esfera de governo: (1) Conferência de Saúde: reúne-se a cada 4 anos com representação dos vários segmentos sociais para avaliar a situação de saúde e propor diretrizes; (2) Conselho de Saúde: órgão permanente e deliberativo, fiscaliza o SUS e o repasse de recursos. Paridade na Composição (Resolução CNS 453/2012): 50% de entidades e movimentos representativos de USUÁRIOS; 25% de entidades de TRABALHADORES da saúde; 25% de representação de GOVERNO e prestadores de serviços de saúde privados conveniados ou sem fins lucrativos.",
                "minutos": 60,
                "materiais": ["lei8142", "res_cns453"]
            },
            {
                "id": "2026-11-19-1",
                "disciplina": "SAU",
                "titulo": "Pacto pela Saúde (Portarias GM/MS 399/2006 e 699/2006) e Redes de Atenção",
                "detalhe": "Pacto pela Saúde 2006: Três dimensões constitutivas: (1) Pacto pela Vida: compromisso com prioridades sanitárias de impacto (saúde do idoso, controle do câncer de colo de útero e mama, redução da mortalidade materna e infantil, controle de endemias como dengue, promoção da saúde e fortalecimento da atenção básica); (2) Pacto em Defesa do SUS: cidadania, mobilização social e garantia de financiamento estável; (3) Pacto de Gestão: descentralização, qualificação das relações federativas e Termo de Compromisso de Gestão.",
                "minutos": 60,
                "materiais": ["edital_ret", "anexo_prog"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-20",
        "diaSemana": "Sexta",
        "fase": 3,
        "marcos": [
            "ANTEVÉSPERA DA PROVA – Revisão focada nos pontos de maior rendimento e regras essenciais."
        ],
        "tarefas": [
            {
                "id": "2026-11-20-0",
                "disciplina": "REV",
                "titulo": "Revisão Geral das 25 Questões Básicas (Português, Matemática, Atualidades, Legislação e Saúde)",
                "detalhe": "Revisão dos esquemas das 5 matérias comuns (que representam 50 dos 60 pontos da prova!): (1) Português: crase, concordância com sujeito partitivo e haver/fazer, funções do 'que' e do 'se'; (2) Matemática: tabela-verdade da condicional (V→F=F), equivalência da contrapositiva e De Morgan, probabilidade do evento complementar; (3) Atualidades: Barão de Cotegipe (lei 1964 x instalação 1965, vizinhos, agricultura e Censo 2022); (4) Legislação: art. 5º CF (casa como asilo inviolável, remédios constitucionais) e LIMPE art. 37; (5) Saúde: Lei 8.080 art. 7º (igualdade e universalidade), Decreto 7.508 (portas de entrada e requisitos da Região de Saúde), PNAB (longitudinalidade e acolhimento com risco).",
                "minutos": 60,
                "materiais": ["anexo_prog", "mapa_prog"]
            },
            {
                "id": "2026-11-20-1",
                "disciplina": "REV",
                "titulo": "Revisão Geral dos Conhecimentos Específicos de Odontologia",
                "detalhe": "Revisão expressa do bloco Odontológico: (1) Código de Ética: infrações de propaganda e quebra de sigilo profissional; (2) ART: ionômero de alta viscosidade + instrumentos manuais; (3) Anestésicos: limite de vasoconstritor em cardiopatas (0,04mg epinefrina), agulha não quebrar não dobrando; (4) Farmacologia: antibiótico profilático da endocardite (Amoxicilina 2g 1h antes); (5) Fluoretos: flúor na água de abastecimento (0,7 ppm), dentifrício fluoretado padrão mínimo 1.000 a 1.100 ppm F para todas as idades com quantidade controlada de grão de arroz cru para bebês; (6) Biossegurança: monitoramento semanal com bioindicador em autoclave.",
                "minutos": 60,
                "materiais": ["guia_fluor", "codigo_etica_cfo", "caderno_atencao_bucal"]
            }
        ],
        "totalMin": 120
    },
    {
        "data": "2026-11-21",
        "diaSemana": "Sábado",
        "fase": 3,
        "marcos": [
            "VÉSPERA DA PROVA – Checagem de Materiais, Descanso Ativo e Confiança",
            "Separar Documento Oficial de Identidade com foto (RG ou CNH física e válida).",
            "Separar 2 ou 3 canetas esferográficas de tinta PRETA ou AZUL em tubo transparente.",
            "Confirmar o endereço e horário de abertura dos portões constante no Edital de Convocação.",
            "Alimentação leve e boa noite de sono: o conhecimento já está consolidado!"
        ],
        "tarefas": [
            {
                "id": "2026-11-21-0",
                "disciplina": "REV",
                "titulo": "Leitura Rápida dos Mapas Mentais Visuais (30 minutos) e Estratégia de Prova",
                "detalhe": "Revisão visual leve apenas passando os olhos pelos mapas mentais das 6 matérias. Fixar a estratégia da prova de 3 horas (30 questões): (1) Começar pela matéria de maior segurança (ex: Saúde e Específicos ou Português); (2) Não perder mais de 3 minutos em nenhuma questão difícil de Matemática/RL (marque para voltar depois se der tempo!); (3) Deixar ao menos 30 minutos reservados para passar as 30 respostas para o cartão-resposta oficial com calma, sem rasuras.",
                "minutos": 60,
                "materiais": ["mapa_prog"]
            },
            {
                "id": "2026-11-21-1",
                "disciplina": "REV",
                "titulo": "Preparação Logística, Mental e Descanso Pré-Prova",
                "detalhe": "Descanse a mente. Revise apenas o checklist prático: canetas transparentes testadas, garrafinha de água sem rótulo, documento oficial com foto, comprovante de inscrição, trajeto planejado para chegar com no mínimo 1 hora de antecedência. Confiança total na preparação de 28 dias!",
                "minutos": 60,
                "materiais": ["edital_ret"]
            }
        ],
        "totalMin": 120
    }
]


def gerar_plano():
    plano = {
        "titulo": "Concurso Barão de Cotegipe (RS) – Edital 001/2026 – Odontólogo/PSF",
        "cargo": "Odontólogo – PSF (Cód. 809)",
        "vagas": "1 vaga imediata ampla concorrência (40h semanais – R$ 7.499,45)",
        "banca": "Instituto DOM",
        "dataProva": str(PROVA),
        "inicio": str(INICIO),
        "questoes": 30,
        "notaMaxima": 60,
        "notaMinima": 36,
        "fases": {
            1: "Fase 1 – Base Teórica e Mapas Mentais (25/10 a 08/11)",
            2: "Fase 2 – Questões, Pegadinhas da Banca e Aprofundamento (09/11 a 14/11)",
            3: "Fase 3 – Revisão Geral e Simulados Finais (15/11 a 21/11)"
        },
        "disciplinas": {
            "SAU": "Conhecimentos sobre Saúde",
            "LEG": "Legislação Municipal e Geral",
            "ATU": "Atualidades e Realidade Municipal",
            "POR": "Língua Portuguesa (Nível Superior)",
            "MAT": "Matemática e Raciocínio Lógico (Nível Superior)",
            "ESP": "Conhecimentos Específicos (Odontólogo/PSF)",
            "REV": "Revisão / Simulado"
        },
        "pesoProva": {
            "POR": 5,
            "MAT": 5,
            "ATU": 5,
            "LEG": 5,
            "SAU": 5,
            "ESP": 5
        },
        "materiais": MATERIAIS,
        "dias": DIAS_PLANO
    }

    conteudo_js = (
        "// Gerado automaticamente pelo script gera_plano.py – Não editar manualmente\n"
        "window.PLANO = " + json.dumps(plano, ensure_ascii=False, indent=1) + ";\n"
    )

    ARQ_SAIDA.write_text(conteudo_js, encoding="utf-8")
    print(f"Sucesso! {ARQ_SAIDA} gerado com {len(DIAS_PLANO)} dias e {sum(len(d['tarefas']) for d in DIAS_PLANO)} tarefas.")


if __name__ == "__main__":
    gerar_plano()
