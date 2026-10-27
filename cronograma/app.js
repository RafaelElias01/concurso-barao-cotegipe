/* Rastreador de estudos – lógica da interface. Depende de window.PLANO (plano.js). */
(function () {
  'use strict';

  var PLANO = window.PLANO;
  if (!PLANO) {
    console.error('window.PLANO não carregado! Verifique plano.js');
    return;
  }

  var CHAVE = 'barao-cotegipe-odontologo-progresso-v1';
  var DIAS_SEMANA = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
  var ICONES = { edital: '📋', lei: '⚖️', livro: '📚', apostila: '📘', cursinho: '🎓', prova: '📝', web: '🌐' };
  var NOMES_TIPO = {
    edital: 'Editais e Documentos Oficiais',
    lei: 'Leis e Legislação Vigente',
    livro: 'Manuais e Guias do Ministério da Saúde / CFO',
    apostila: 'Apostilas Didáticas',
    cursinho: 'Aulas e Materiais de Cursinho',
    prova: 'Provas Anteriores da Banca',
    web: 'Portais Oficiais e Pesquisa'
  };
  var DISCS = ['SAU', 'LEG', 'ATU', 'POR', 'MAT', 'ESP', 'REV'];
  var ROTULO = { a_fazer: 'A fazer', andamento: 'Em andamento', feito: 'Concluído' };

  /* ---------- Datas (sempre locais, sem fuso/UTC) ---------- */
  function parseData(s) {
    var p = s.split('-');
    return new Date(+p[0], +p[1] - 1, +p[2]);
  }
  function fmtISO(d) {
    var m = d.getMonth() + 1, dia = d.getDate();
    return d.getFullYear() + '-' + (m < 10 ? '0' : '') + m + '-' + (dia < 10 ? '0' : '') + dia;
  }
  function hojeISO() { return fmtISO(new Date()); }
  function fmtDataCurta(iso) {
    var d = parseData(iso);
    var dd = d.getDate(), mm = d.getMonth() + 1;
    return DIAS_SEMANA[d.getDay()] + ', ' + (dd < 10 ? '0' : '') + dd + '/' + (mm < 10 ? '0' : '') + mm;
  }
  function segundaDaSemana(iso) {
    var d = parseData(iso);
    d.setDate(d.getDate() - ((d.getDay() + 6) % 7));
    return fmtISO(d);
  }
  function diasAte(isoAlvo, isoDe) {
    return Math.round((parseData(isoAlvo) - parseData(isoDe)) / 86400000);
  }
  function fmtHoras(min) {
    var h = (min || 0) / 60;
    return (Math.round(h * 10) / 10).toString().replace('.', ',') + ' h';
  }

  /* ---------- Estado e persistência ---------- */
  var estado = { tarefas: {}, dias: {} };

  function carregarLocal() {
    try {
      var bruto = localStorage.getItem(CHAVE);
      if (bruto) {
        var o = JSON.parse(bruto);
        if (o && typeof o === 'object') {
          estado.tarefas = (o.tarefas && typeof o.tarefas === 'object') ? o.tarefas : {};
          estado.dias = (o.dias && typeof o.dias === 'object') ? o.dias : {};
        }
      }
    } catch (e) {}
  }

  function salvarLocal() {
    var ok = false;
    try {
      localStorage.setItem(CHAVE, JSON.stringify(estado));
      ok = true;
    } catch (e) {}
    pedirSync();
    return ok;
  }

  /* ---------- Modo servidor (arquivo progresso.json) ---------- */
  var MODO_SERVIDOR = location.protocol === 'http:';
  var API = '/api/progresso';
  var sync = { pronto: false, pendente: false, enviando: false, timer: null, retry: null, ultimo: null };

  function hhmmss(d) {
    function z(n) { return (n < 10 ? '0' : '') + n; }
    return z(d.getHours()) + ':' + z(d.getMinutes()) + ':' + z(d.getSeconds());
  }

  function setStatus(tipo) {
    var n = document.getElementById('status-arquivo');
    if (!n) return;
    n.setAttribute('data-estado', tipo);
    if (tipo === 'salvo') {
      n.textContent = '✓ Salvo em progresso.json às ' + hhmmss(sync.ultimo || new Date());
    } else if (tipo === 'salvando') {
      n.textContent = 'Salvando progresso...';
    } else if (tipo === 'carregando') {
      n.textContent = 'Carregando progresso.json...';
    } else {
      n.textContent = '⚠️ Servidor desconectado (progresso salvo apenas no navegador)';
    }
  }

  function pedirSync() {
    if (!MODO_SERVIDOR) return;
    sync.pendente = true;
    if (!sync.pronto) return;
    setStatus('salvando');
    clearTimeout(sync.timer);
    sync.timer = setTimeout(executarSync, 300);
  }

  function executarSync() {
    if (!sync.pendente || sync.enviando) return;
    sync.enviando = true;
    sync.pendente = false;
    clearTimeout(sync.retry);

    fetch(API, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: JSON.stringify(estado)
    }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }).then(function () {
      sync.enviando = false;
      sync.ultimo = new Date();
      setStatus('salvo');
      if (sync.pendente) pedirSync();
    }).catch(function (e) {
      sync.enviando = false;
      setStatus('erro');
      sync.retry = setTimeout(function () {
        sync.pendente = true;
        executarSync();
      }, 5000);
    });
  }

  function mesclar(remoto) {
    var r = (remoto && typeof remoto === 'object') ? remoto : {};
    var rt = r.tarefas || {}, rd = r.dias || {};
    var lt = estado.tarefas, ld = estado.dias;
    var outT = {}, outD = {};
    var dadosLocaisPendentes = false;
    var idsT = Object.keys(lt).concat(Object.keys(rt));
    idsT.forEach(function (k) {
      var a = lt[k] || {}, b = rt[k] || {};
      var feito = !!(a.feito || b.feito);
      var pareiEm = a.pareiEm || b.pareiEm || '';
      outT[k] = {
        feito: feito,
        pareiEm: pareiEm
      };
      if ((feito && !b.feito) || (pareiEm && pareiEm !== (b.pareiEm || ''))) {
        dadosLocaisPendentes = true;
      }
    });
    var idsD = Object.keys(ld).concat(Object.keys(rd));
    idsD.forEach(function (k) {
      var a = ld[k] || {}, b = rd[k] || {};
      var notas = a.notas || b.notas || '';
      var minutos = a.minutosEstudados !== undefined ? a.minutosEstudados : b.minutosEstudados;
      outD[k] = {
        notas: notas,
        minutosEstudados: minutos
      };
      if ((notas && notas !== (b.notas || ''))
          || (a.minutosEstudados !== undefined && a.minutosEstudados !== b.minutosEstudados)) {
        dadosLocaisPendentes = true;
      }
    });
    estado.tarefas = outT;
    estado.dias = outD;
    try { localStorage.setItem(CHAVE, JSON.stringify(estado)); } catch (e) {}
    return dadosLocaisPendentes;
  }

  function carregarDoServidor(cb) {
    if (!MODO_SERVIDOR) {
      setStatus('offline');
      cb();
      return;
    }
    setStatus('carregando');
    fetch(API).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }).then(function (dados) {
      var dadosLocaisPendentes = mesclar(dados);
      sync.pronto = true;
      sync.ultimo = new Date();
      setStatus('salvo');
      if (dadosLocaisPendentes) pedirSync();
      cb();
    }).catch(function () {
      sync.pronto = true;
      setStatus('erro');
      cb();
    });
  }

  /* ---------- Índices e Acesso a Tarefas ---------- */
  var tarefaPorId = {};
  var diasOrdenados = PLANO.dias || [];
  diasOrdenados.forEach(function (dia) {
    (dia.tarefas || []).forEach(function (t) {
      tarefaPorId[t.id] = { tarefa: t, dia: dia };
    });
  });

  function tarefaEst(id) { return estado.tarefas[id] || {}; }
  function diaEst(data) { return estado.dias[data] || {}; }
  function statusDe(id) {
    var e = tarefaEst(id);
    if (e.feito) return 'feito';
    if (e.pareiEm && e.pareiEm.trim()) return 'andamento';
    return 'a_fazer';
  }
  function setTarefa(id, patch) {
    var cur = estado.tarefas[id] || {};
    estado.tarefas[id] = Object.assign({}, cur, patch);
  }
  function setDia(data, patch) {
    var cur = estado.dias[data] || {};
    estado.dias[data] = Object.assign({}, cur, patch);
  }

  /* ---------- Cálculos de Progresso ---------- */
  function pct(num, den) {
    if (!den) return 0;
    return Math.round((num / den) * 100);
  }

  function calcularProgresso() {
    var totalTarefas = 0, feitas = 0;
    var minTotal = 0, minFeitos = 0;
    var porDisc = {};
    DISCS.forEach(function (d) {
      porDisc[d] = { total: 0, feitas: 0, minTotal: 0, minFeitos: 0 };
    });

    diasOrdenados.forEach(function (dia) {
      (dia.tarefas || []).forEach(function (t) {
        totalTarefas++;
        var m = t.minutos || 0;
        minTotal += m;
        var st = statusDe(t.id);
        var disc = t.disciplina || 'REV';
        if (!porDisc[disc]) porDisc[disc] = { total: 0, feitas: 0, minTotal: 0, minFeitos: 0 };
        porDisc[disc].total++;
        porDisc[disc].minTotal += m;
        if (st === 'feito') {
          feitas++;
          minFeitos += m;
          porDisc[disc].feitas++;
          porDisc[disc].minFeitos += m;
        }
      });
    });

    var minEstudados = 0;
    Object.keys(estado.dias).forEach(function (d) {
      var val = estado.dias[d].minutosEstudados;
      if (val && !isNaN(val)) minEstudados += (+val);
    });

    return {
      total: totalTarefas,
      feitas: feitas,
      minTotal: minTotal,
      minFeitos: minFeitos,
      minEstudados: minEstudados,
      porDisc: porDisc
    };
  }

  /* ---------- Criação de Elementos DOM ---------- */
  function el(tag, attrs, filhos) {
    var elem = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === 'text') elem.textContent = attrs[k];
        else if (k === 'html') elem.innerHTML = attrs[k];
        else if (k === 'class') elem.className = attrs[k];
        else if (k.startsWith('data-')) elem.setAttribute(k, attrs[k]);
        else elem[k] = attrs[k];
      });
    }
    if (filhos) {
      (Array.isArray(filhos) ? filhos : [filhos]).forEach(function (f) {
        if (f) elem.appendChild(typeof f === 'string' ? document.createTextNode(f) : f);
      });
    }
    return elem;
  }

  function chipDisc(disc) {
    var nome = (PLANO.disciplinas && PLANO.disciplinas[disc]) || disc;
    return el('span', { class: 'chip', 'data-disc': disc, text: disc, title: nome });
  }

  function linkMaterial(id) {
    var m = (PLANO.materiais && PLANO.materiais[id]);
    if (!m) return null;
    var ico = ICONES[m.tipo] || '📄';
    return el('a', { href: m.link, target: '_blank', rel: 'noopener' }, [
      el('span', { text: ico + ' ' + m.nome })
    ]);
  }

  function botaoApostila(a) {
    if (!a || !a.link) return null;
    return el('a', { class: 'btn-apostila', href: a.link, target: '_blank', rel: 'noopener' }, [
      el('span', { text: '📖 ' + a.rotulo })
    ]);
  }

  /* ---------- Debounce ---------- */
  var timers = {};
  function agendar(chave, fn) {
    clearTimeout(timers[chave]);
    timers[chave] = setTimeout(fn, 400);
  }

  /* ---------- Filtros ---------- */
  var filtro = { tipo: 'todos', disc: null };

  function aplicarFiltro(hoje) {
    var out = [];
    diasOrdenados.forEach(function (dia) {
      var tarefasFiltradas = (dia.tarefas || []).filter(function (t) {
        if (filtro.disc && t.disciplina !== filtro.disc) return false;
        var st = statusDe(t.id);
        if (filtro.tipo === 'pendentes') return st !== 'feito';
        if (filtro.tipo === 'hoje') return dia.data === hoje;
        return true;
      });
      if (tarefasFiltradas.length || (filtro.tipo === 'hoje' && dia.data === hoje)) {
        out.push({ dia: dia, tarefas: tarefasFiltradas });
      }
    });
    return out;
  }

  /* ---------- Renderização ---------- */
  var refs = {}, refsDia = {};

  function renderTarefa(t) {
    var st = statusDe(t.id);
    var e = tarefaEst(t.id);
    var card = el('div', { class: 'tarefa', id: 't-' + t.id, 'data-status': st });
    var cb = el('input', { type: 'checkbox', 'aria-label': 'Marcar como concluído' });
    cb.checked = (st === 'feito');
    var statusEl = el('span', { class: 'status', text: ROTULO[st] });
    var parei = el('input', { type: 'text', placeholder: 'Parei em... (ex.: art. 7º, pág. 12, questão 5)', maxlength: '150' });
    parei.value = e.pareiEm || '';

    function atualizarVisual() {
      var s = statusDe(t.id);
      card.setAttribute('data-status', s);
      statusEl.textContent = ROTULO[s];
      atualizarDia(t.id);
      renderPainel();
      renderBanner();
      renderPendencias();
    }

    cb.addEventListener('change', function () {
      setTarefa(t.id, { feito: cb.checked });
      salvarLocal();
      atualizarVisual();
    });

    parei.addEventListener('input', function () {
      setTarefa(t.id, { pareiEm: parei.value });
      atualizarVisual();
      agendar('t' + t.id, salvarLocal);
    });

    var mats = (t.materiais || []).map(linkMaterial).filter(Boolean);
    var apos = (t.apostilas || []).map(botaoApostila).filter(Boolean);
    card.appendChild(el('div', { class: 't-topo' }, [
      cb,
      el('div', { class: 't-info' }, [
        el('div', { class: 't-titulo' }, [chipDisc(t.disciplina), t.titulo, statusEl]),
        el('div', { class: 't-detalhe', text: t.detalhe }),
        apos.length ? el('div', { class: 't-apostilas' }, apos) : null,
        mats.length ? el('div', { class: 't-mats' }, mats) : null
      ])
    ]));
    card.appendChild(el('label', { class: 'parei' }, [
      el('span', { text: '📌 Parei em: ' }),
      parei
    ]));

    refs[t.id] = card;
    return card;
  }

  function resumoDia(dia) {
    var feitas = (dia.tarefas || []).filter(function (t) { return statusDe(t.id) === 'feito'; }).length;
    return { feitas: feitas, total: (dia.tarefas || []).length };
  }

  function atualizarDia(idTarefa) {
    var item = tarefaPorId[idTarefa];
    if (!item) return;
    var dia = item.dia, d = refsDia[dia.data];
    if (!d) return;
    var r = resumoDia(dia);
    var progSpan = d.querySelector('.dia-prog');
    if (progSpan) progSpan.textContent = r.feitas + '/' + r.total + ' feitas';
    d.classList.toggle('feito', r.total > 0 && r.feitas === r.total);
  }

  function renderDia(dia, tarefas, hoje, abrir) {
    var r = resumoDia(dia);
    var ehHoje = dia.data === hoje;
    var d = el('details', {
      class: 'dia' + (ehHoje ? ' hoje' : '') + (r.total && r.feitas === r.total ? ' feito' : ''),
      id: 'dia-' + dia.data
    });
    if (abrir || ehHoje) d.open = true;

    var sum = el('summary', null, [
      el('span', { class: 'dia-data', text: fmtDataCurta(dia.data) }),
      ehHoje ? el('span', { class: 'tag-hoje', text: 'HOJE' }) : null,
      el('span', { class: 'dia-meta', text: fmtHoras(dia.totalMin) }),
      el('span', { class: 'dia-prog', text: r.feitas + '/' + r.total + ' feitas' })
    ]);
    d.appendChild(sum);

    var corpo = el('div', { class: 'dia-corpo' });
    if (dia.marcos && dia.marcos.length) {
      corpo.appendChild(el('ul', { class: 'marcos' }, dia.marcos.map(function (m) {
        return el('li', { text: m });
      })));
    }
    tarefas.forEach(function (t) { corpo.appendChild(renderTarefa(t)); });

    // Anotações e Horas Estudadas de fato
    var notas = el('textarea', { placeholder: 'Anotações, dúvidas e artigos revisados hoje...', rows: '2' });
    notas.value = diaEst(dia.data).notas || '';
    notas.addEventListener('input', function () {
      setDia(dia.data, { notas: notas.value });
      agendar('n' + dia.data, salvarLocal);
    });

    var minInput = el('input', { type: 'number', min: '0', step: '10', placeholder: '120' });
    var minVal = diaEst(dia.data).minutosEstudados;
    minInput.value = minVal !== undefined && minVal !== null ? minVal : '';
    minInput.addEventListener('input', function () {
      var v = parseInt(minInput.value, 10);
      setDia(dia.data, { minutosEstudados: isNaN(v) || v < 0 ? 0 : v });
      renderPainel();
      agendar('m' + dia.data, salvarLocal);
    });

    corpo.appendChild(el('div', { class: 'parei', style: 'margin-top:14px; padding-top:10px; border-top:1px dashed var(--borda);' }, [
      el('span', { text: '📝 Anotações do dia:' }),
      notas
    ]));
    corpo.appendChild(el('div', { class: 'parei' }, [
      el('span', { text: '⏱️ Minutos estudados de fato:' }),
      minInput
    ]));

    d.appendChild(corpo);
    refsDia[dia.data] = d;
    return d;
  }

  function renderLista() {
    var hoje = hojeISO();
    var cont = document.getElementById('lista');
    cont.textContent = '';
    refs = {};
    refsDia = {};

    var grupos = aplicarFiltro(hoje);
    if (!grupos.length) {
      cont.appendChild(el('p', { class: 'aviso', text: 'Nenhuma tarefa encontrada para este filtro.' }));
      return;
    }

    var faseAtual = null, semAtual = null, semBox = null;
    grupos.forEach(function (g) {
      var dia = g.dia;
      if (dia.fase !== faseAtual) {
        faseAtual = dia.fase;
        semAtual = null;
        cont.appendChild(el('h2', { class: 'fase', text: (PLANO.fases && PLANO.fases[dia.fase]) || ('Fase ' + dia.fase) }));
      }
      var seg = segundaDaSemana(dia.data);
      if (seg !== semAtual) {
        semAtual = seg;
        var fim = parseData(seg);
        fim.setDate(fim.getDate() + 6);
        var nome = 'Semana de ' + fmtDataCurta(seg).split(', ')[1] + ' a ' + fmtDataCurta(fmtISO(fim)).split(', ')[1];
        semBox = el('details', { class: 'semana' }, [el('summary', { text: nome })]);
        semBox.open = true;
        cont.appendChild(semBox);
      }
      semBox.appendChild(renderDia(dia, g.tarefas, hoje, filtro.tipo !== 'todos'));
    });
  }

  function renderBanner() {
    var cont = document.getElementById('banner');
    cont.textContent = '';
    var hoje = hojeISO();
    var dias = diasAte(PLANO.dataProva, hoje);
    var diaHoje = diasOrdenados.find(function (d) { return d.data === hoje; });

    var textoBanner = dias > 0 ? 'Faltam ' + dias + ' dias para a Prova Objetiva (22/11/2026)!' : (dias === 0 ? 'É HOJE O DIA DA PROVA! Boa sorte!' : 'Prova realizada em 22/11/2026.');
    var sub = diaHoje ? 'Meta de hoje: 2 tarefas planejadas (120 min).' : 'Confira suas tarefas no cronograma abaixo.';

    var box = el('div', { class: 'banner' }, [
      el('div', null, [
        el('strong', { text: '🎯 ' + textoBanner }),
        el('small', { text: sub })
      ]),
      diaHoje ? el('button', {
        class: 'btn',
        text: 'Ir para o dia de hoje',
        onclick: function () {
          var elHoje = document.getElementById('dia-' + hoje);
          if (elHoje) {
            elHoje.open = true;
            elHoje.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }
      }) : null
    ]);
    cont.appendChild(box);
  }

  function renderPainel() {
    var hoje = hojeISO(), p = calcularProgresso();
    var cont = document.getElementById('painel');
    cont.textContent = '';
    var dias = diasAte(PLANO.dataProva, hoje);
    var rotuloDias = dias > 0 ? dias + ' dias' : (dias === 0 ? 'É HOJE!' : 'Encerrado');

    function stat(n, r) {
      return el('div', { class: 'stat' }, [
        el('div', { class: 'n', text: n }),
        el('div', { class: 'r', text: r })
      ]);
    }

    cont.appendChild(stat(rotuloDias, 'até a prova (22/11/2026)'));
    cont.appendChild(stat(pct(p.feitas, p.total) + '%', 'tarefas feitas (' + p.feitas + '/' + p.total + ')'));
    cont.appendChild(stat(pct(p.minFeitos, p.minTotal) + '%', 'concluído por minutos'));
    cont.appendChild(stat(fmtHoras(p.minEstudados) + ' / ' + fmtHoras(p.minTotal), 'estudo real / planejado'));

    var box = el('div', { class: 'disc-bars' });
    box.appendChild(el('h3', { text: 'Progresso por Disciplina da Prova (5 questões cada)', style: 'margin:0 0 10px; font-size:0.95rem;' }));
    DISCS.forEach(function (d) {
      var x = p.porDisc[d];
      if (!x || !x.total) return;
      var i = el('i', { 'data-disc': d });
      i.style.width = pct(x.feitas, x.total) + '%';
      box.appendChild(el('div', { class: 'barra-linha' }, [
        el('span', { class: 'nome', text: d + ' – ' + (PLANO.disciplinas[d] || d) }),
        el('div', { class: 'barra' }, [i]),
        el('span', { text: pct(x.feitas, x.total) + '% (' + x.feitas + '/' + x.total + ')' })
      ]));
    });
    cont.appendChild(box);
  }

  function renderPendencias() {
    var cont = document.getElementById('pendencias');
    cont.textContent = '';
    var hoje = hojeISO();
    var atrasadas = [];

    diasOrdenados.forEach(function (dia) {
      if (dia.data < hoje) {
        (dia.tarefas || []).forEach(function (t) {
          if (statusDe(t.id) !== 'feito') atrasadas.push({ tarefa: t, dia: dia });
        });
      }
    });

    if (!atrasadas.length) return;

    var det = el('details', { class: 'pend' });
    det.appendChild(el('summary', { text: '⚠️ ' + atrasadas.length + ' tarefa(s) pendente(s) de dias anteriores (clique para abrir)' }));
    var ul = el('ul');
    atrasadas.forEach(function (item) {
      var li = el('li', null, [
        chipDisc(item.tarefa.disciplina),
        el('strong', { text: fmtDataCurta(item.dia.data) + ': ' }),
        el('span', { text: item.tarefa.titulo })
      ]);
      ul.appendChild(li);
    });
    det.appendChild(ul);
    cont.appendChild(det);
  }

  function renderFiltros() {
    var cont = document.getElementById('filtros');
    cont.textContent = '';

    var btnTodos = el('button', {
      type: 'button',
      'aria-pressed': filtro.tipo === 'todos' && !filtro.disc ? 'true' : 'false',
      text: 'Todas as tarefas',
      onclick: function () { filtro.tipo = 'todos'; filtro.disc = null; renderFiltros(); renderLista(); }
    });
    var btnHoje = el('button', {
      type: 'button',
      'aria-pressed': filtro.tipo === 'hoje' ? 'true' : 'false',
      text: 'Hoje',
      onclick: function () { filtro.tipo = 'hoje'; filtro.disc = null; renderFiltros(); renderLista(); }
    });
    var btnPendentes = el('button', {
      type: 'button',
      'aria-pressed': filtro.tipo === 'pendentes' ? 'true' : 'false',
      text: 'Pendentes',
      onclick: function () { filtro.tipo = 'pendentes'; filtro.disc = null; renderFiltros(); renderLista(); }
    });

    cont.appendChild(btnTodos);
    cont.appendChild(btnHoje);
    cont.appendChild(btnPendentes);

    // Botões por disciplina
    DISCS.forEach(function (d) {
      var btn = el('button', {
        type: 'button',
        'aria-pressed': filtro.disc === d ? 'true' : 'false',
        text: d,
        title: PLANO.disciplinas[d] || d,
        onclick: function () {
          filtro.disc = (filtro.disc === d ? null : d);
          filtro.tipo = 'todos';
          renderFiltros();
          renderLista();
        }
      });
      cont.appendChild(btn);
    });
  }

  /* ---------- Aba Materiais ---------- */
  function renderAbaMateriais() {
    var cont = document.getElementById('aba-materiais');
    cont.textContent = '';
    cont.appendChild(el('h2', { text: 'Materiais de Apoio e Fontes Oficiais' }));
    cont.appendChild(el('p', { class: 'aviso', text: 'Todos os materiais indicados no plano de estudos para o cargo de Odontólogo/PSF (Barão de Cotegipe - Instituto DOM):' }));

    var grid = el('div', { class: 'mats-grid' });
    Object.keys(PLANO.materiais || {}).forEach(function (k) {
      var m = PLANO.materiais[k];
      var ico = ICONES[m.tipo] || '📄';
      var tipoNome = NOMES_TIPO[m.tipo] || m.tipo;
      var card = el('div', { class: 'mat-card' }, [
        el('h3', null, [el('a', { href: m.link, target: '_blank', rel: 'noopener', text: ico + ' ' + m.nome })]),
        el('p', { text: tipoNome })
      ]);
      grid.appendChild(card);
    });
    cont.appendChild(grid);
  }

  /* ---------- Aba O Que Estudar Mais ---------- */
  function renderAbaEstudarMais() {
    var cont = document.getElementById('aba-estudar');
    cont.textContent = '';
    cont.appendChild(el('h2', { text: 'Estratégia da Prova – Banca Instituto DOM' }));

    var resumo = el('div', { class: 'stat', style: 'margin-bottom:16px;' }, [
      el('h3', { text: 'Tabela 6 – Prova Objetiva (Nível Superior - Saúde)', style: 'margin:0 0 8px;' }),
      el('p', { html: '• <strong>Total:</strong> 30 questões de 2,0 pontos cada = <strong>60 pontos no total</strong>.<br>• <strong>Nota Mínima para Aprovação:</strong> 36 pontos (60% da prova = 18 acertos).<br>• <strong>SEM Prova de Títulos:</strong> Sua nota final é 100% determinada pela Prova Objetiva!' }),
      el('p', { html: '• <strong>Atenção ao Peso das Matérias Gerais:</strong><br>&nbsp;&nbsp;- Conhecimentos Específicos de Odontologia tem <strong>5 questões</strong> (10 pontos / 16,7% da prova).<br>&nbsp;&nbsp;- As 5 disciplinas comuns somam <strong>25 questões</strong> (50 pontos / 83,3% da prova!).<br>&nbsp;&nbsp;<em>Portanto, dominar Saúde, Legislação, Português, Matemática e Atualidades é o que garante a vaga!</em>' })
    ]);
    cont.appendChild(resumo);

    var prog = calcularProgresso();
    var pendenciasBox = el('div', { class: 'disc-bars' });
    pendenciasBox.appendChild(el('h3', { text: 'Raio-X de Conclusão por Matéria' }));

    DISCS.forEach(function (d) {
      var x = prog.porDisc[d];
      if (!x || !x.total) return;
      var pCent = pct(x.feitas, x.total);
      var i = el('i', { 'data-disc': d });
      i.style.width = pCent + '%';
      pendenciasBox.appendChild(el('div', { class: 'barra-linha' }, [
        el('span', { class: 'nome', text: d + ' – ' + (PLANO.disciplinas[d] || d) }),
        el('div', { class: 'barra' }, [i]),
        el('span', { text: pCent + '% (' + x.feitas + '/' + x.total + ' feitas)' })
      ]));
    });
    cont.appendChild(pendenciasBox);
  }

  /* ---------- Navegação entre Abas ---------- */
  function configurarAbas() {
    var abas = document.querySelectorAll('.abas button');
    abas.forEach(function (b) {
      b.addEventListener('click', function () {
        abas.forEach(function (x) { x.setAttribute('aria-selected', 'false'); });
        b.setAttribute('aria-selected', 'true');
        var aba = b.getAttribute('data-aba');
        document.getElementById('aba-cronograma').hidden = (aba !== 'cronograma');
        document.getElementById('aba-materiais').hidden = (aba !== 'materiais');
        document.getElementById('aba-estudar').hidden = (aba !== 'estudar');

        if (aba === 'materiais') renderAbaMateriais();
        if (aba === 'estudar') renderAbaEstudarMais();
      });
    });
  }

  /* ---------- Exportar / Importar Backup ---------- */
  function configurarBackup() {
    var btnExp = document.getElementById('btn-exportar');
    var btnImp = document.getElementById('btn-importar');
    var inputImp = document.getElementById('arq-importar');

    btnExp.addEventListener('click', function () {
      var str = JSON.stringify(estado, null, 2);
      var blob = new Blob([str], { type: 'application/json' });
      var url = URL.createObjectURL(blob);
      var a = el('a', { href: url, download: 'progresso-barao-cotegipe-' + hojeISO() + '.json' });
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });

    btnImp.addEventListener('click', function () {
      inputImp.click();
    });

    inputImp.addEventListener('change', function () {
      var f = inputImp.files[0];
      if (!f) return;
      var reader = new FileReader();
      reader.onload = function (e) {
        try {
          var dados = JSON.parse(e.target.result);
          if (dados && typeof dados === 'object') {
            mesclar(dados);
            salvarLocal();
            renderPainel();
            renderBanner();
            renderPendencias();
            renderLista();
            alert('Progresso importado com sucesso!');
          }
        } catch (err) {
          alert('Erro ao ler o arquivo JSON: ' + err.message);
        }
      };
      reader.readAsText(f);
      inputImp.value = '';
    });
  }

  /* ---------- Inicialização ---------- */
  function iniciar() {
    carregarLocal();
    carregarDoServidor(function () {
      renderBanner();
      renderPainel();
      renderPendencias();
      renderFiltros();
      renderLista();
      configurarAbas();
      configurarBackup();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciar);
  } else {
    iniciar();
  }
})();
