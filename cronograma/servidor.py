#!/usr/bin/env python3
"""Servidor local do cronograma de estudos - Concurso Barão de Cotegipe (RS).

Serve a pasta do projeto (cronograma, material, provas-antigas, edital) apenas em 127.0.0.1
e guarda o progresso em cronograma/progresso.json (com backups diários automáticos).
Usa apenas a biblioteca padrão do Python.
Uso: python servidor.py [--sem-navegador]
"""
import json
import mimetypes
import os
import shutil
import sys
import threading
import webbrowser
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

PASTA = Path(__file__).resolve().parent          # ...\concurso-barao-cotegipe\cronograma
RAIZ = PASTA.parent                              # ...\concurso-barao-cotegipe
ARQ_PROGRESSO = PASTA / "progresso.json"
PASTA_BACKUPS = PASTA / "backups"
HOST = "127.0.0.1"
PORTAS = range(8765, 8775)
LIMITE_JSON = 5 * 1024 * 1024
MAX_BACKUPS = 30
PASTAS_PERMITIDAS = {"cronograma", "material", "provas-antigas", "edital", "curso"}
ARQS_RAIZ = {"LEIA-ME.md", "README.md"}
CHUNK = 256 * 1024

trava = threading.Lock()
porta_usada = 0

MIME = {
    ".mp4": "video/mp4",
    ".md": "text/markdown; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
}


def agora():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def hora():
    return datetime.now().strftime("%H:%M:%S")


def tipo_mime(caminho):
    ext = caminho.suffix.lower()
    if ext in MIME:
        return MIME[ext]
    return mimetypes.guess_type(str(caminho))[0] or "application/octet-stream"


def fazer_backup_e_limpar():
    """Copia o arquivo atual para backups/progresso-AAAA-MM-DD.json (1x por dia)."""
    if not ARQ_PROGRESSO.exists():
        return
    PASTA_BACKUPS.mkdir(exist_ok=True)
    destino = PASTA_BACKUPS / f"progresso-{datetime.now():%Y-%m-%d}.json"
    if not destino.exists():
        shutil.copy2(ARQ_PROGRESSO, destino)
    antigos = sorted(PASTA_BACKUPS.glob("progresso-????-??-??.json"))
    for velho in antigos[:-MAX_BACKUPS]:
        try:
            velho.unlink()
        except OSError:
            pass


def gravar_progresso(dados):
    dados = dict(dados)
    dados["salvoEm"] = agora()
    texto = json.dumps(dados, ensure_ascii=False, indent=1)
    with trava:
        fazer_backup_e_limpar()
        tmp = PASTA / "progresso.json.tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(texto)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, ARQ_PROGRESSO)
    return dados["salvoEm"]


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "CronogramaLocal/1.0"

    def log_message(self, fmt, *args):
        pass

    def _hosts_validos(self):
        return {f"127.0.0.1:{porta_usada}", f"localhost:{porta_usada}"}

    def _origem_ok(self):
        host = self.headers.get("Host")
        if host is not None and host.lower() not in self._hosts_validos():
            return False
        origem = self.headers.get("Origin")
        if origem is None:
            return True
        return origem.lower() in {f"http://{h}" for h in self._hosts_validos()}

    def _json(self, status, obj, extra=None):
        corpo = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(corpo)

    def _erro(self, status, msg):
        self._json(status, {"ok": False, "erro": msg})

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        try:
            if not self._origem_ok():
                return self._erro(403, "acesso negado: origem nao permitida")
            caminho = urlsplit(self.path).path
            if caminho == "/api/progresso":
                return self._get_progresso()
            if caminho in ("/", ""):
                self.send_response(302)
                self.send_header("Location", "/cronograma/")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            self._estatico(caminho)
        except (ConnectionError, TimeoutError):
            pass

    def _get_progresso(self):
        with trava:
            try:
                texto = ARQ_PROGRESSO.read_text(encoding="utf-8")
                json.loads(texto)
            except FileNotFoundError:
                texto = '{"tarefas":{},"dias":{}}'
            except (OSError, ValueError) as e:
                return self._erro(500, f"progresso.json ilegivel: {e}")
        corpo = texto.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(corpo)

    def _resolver(self, caminho_url):
        rel = unquote(caminho_url)
        if "\x00" in rel or "\\" in rel:
            return None
        partes = [p for p in rel.split("/") if p not in ("", ".")]
        if ".." in partes:
            return None
        if partes and partes[0] not in PASTAS_PERMITIDAS and not (len(partes) == 1 and partes[0] in ARQS_RAIZ):
            return None
        if any(p.startswith(".") for p in partes):
            return None
        try:
            alvo = (RAIZ.joinpath(*partes)).resolve()
        except (OSError, RuntimeError):
            return None
        return alvo if self._permitido(alvo) else None

    @staticmethod
    def _permitido(alvo):
        try:
            rel = alvo.relative_to(RAIZ.resolve())
        except ValueError:
            return False
        partes = rel.parts
        if not partes or any(p.startswith(".") for p in partes):
            return False
        if len(partes) == 1:
            return partes[0] in ARQS_RAIZ or partes[0] in PASTAS_PERMITIDAS
        if partes[0] not in PASTAS_PERMITIDAS:
            return False
        if alvo.name.startswith(ARQ_PROGRESSO.name):
            return False
        try:
            alvo.relative_to(PASTA_BACKUPS.resolve())
            return False
        except ValueError:
            pass
        return True

    def _estatico(self, caminho_url):
        alvo = self._resolver(caminho_url)
        if alvo is None:
            return self._erro(403, "acesso negado")
        if alvo.is_dir():
            if not caminho_url.endswith("/"):
                self.send_response(301)
                self.send_header("Location", caminho_url + "/")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            try:
                alvo = (alvo / "index.html").resolve()
            except (OSError, RuntimeError):
                return self._erro(403, "acesso negado")
            if not self._permitido(alvo):
                return self._erro(403, "acesso negado")
        if not alvo.is_file():
            return self._erro(404, "arquivo nao encontrado")
        try:
            tamanho = alvo.stat().st_size
            f = open(alvo, "rb")
        except OSError:
            return self._erro(404, "arquivo nao encontrado")
        with f:
            inicio, fim, status = 0, tamanho - 1, 200
            rng = self.headers.get("Range")
            if rng and rng.startswith("bytes=") and "," not in rng:
                try:
                    a, b = rng[6:].strip().split("-", 1)
                    if a == "":
                        n = int(b)
                        if n <= 0:
                            raise ValueError
                        inicio, fim = max(0, tamanho - n), tamanho - 1
                    else:
                        inicio = int(a)
                        fim = min(int(b), tamanho - 1) if b else tamanho - 1
                    if inicio > fim or inicio >= tamanho:
                        raise ValueError
                    status = 206
                except ValueError:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{tamanho}")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
            n_bytes = fim - inicio + 1 if tamanho else 0
            self.send_response(status)
            self.send_header("Content-Type", tipo_mime(alvo))
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(n_bytes))
            if status == 206:
                self.send_header("Content-Range", f"bytes {inicio}-{fim}/{tamanho}")
            if alvo.suffix.lower() in (".html", ".js", ".css", ".json"):
                self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            if self.command == "HEAD":
                return
            f.seek(inicio)
            restante = n_bytes
            while restante > 0:
                bloco = f.read(min(CHUNK, restante))
                if not bloco:
                    break
                self.wfile.write(bloco)
                restante -= len(bloco)

    def do_PUT(self):
        try:
            self._put()
        except (ConnectionError, TimeoutError):
            pass

    def _put(self):
        if not self._origem_ok():
            return self._erro(403, "origem nao permitida")
        if urlsplit(self.path).path != "/api/progresso":
            return self._erro(404, "nao encontrado")
        try:
            tam = int(self.headers.get("Content-Length", ""))
        except ValueError:
            return self._erro(411, "Content-Length obrigatorio")
        if tam < 0:
            return self._erro(400, "tamanho invalido")
        if tam > LIMITE_JSON:
            self.close_connection = True
            return self._erro(413, "maior que 5 MB")
        bruto = self.rfile.read(tam)
        try:
            dados = json.loads(bruto.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return self._erro(400, "JSON invalido")
        if (not isinstance(dados, dict)
                or not isinstance(dados.get("tarefas"), dict)
                or not isinstance(dados.get("dias"), dict)):
            return self._erro(400, "estrutura invalida: esperado objeto com tarefas e dias")
        try:
            salvo_em = gravar_progresso(dados)
        except OSError as e:
            print(f"[{hora()}] ERRO ao gravar progresso.json: {e}", flush=True)
            return self._erro(500, "falha ao gravar o arquivo")
        print(f"[{hora()}] Progresso salvo ({len(dados['tarefas'])} tarefas, {len(dados['dias'])} dias)", flush=True)
        self._json(200, {"ok": True, "salvoEm": salvo_em})

    def do_POST(self):
        self._erro(405, "metodo nao permitido")

    do_DELETE = do_PATCH = do_POST


class Servidor(ThreadingHTTPServer):
    allow_reuse_address = False
    daemon_threads = True

    def handle_error(self, request, client_address):
        exc = sys.exc_info()[1]
        if isinstance(exc, (ConnectionAbortedError, ConnectionResetError, BrokenPipeError)):
            return
        super().handle_error(request, client_address)


def main():
    global porta_usada
    sem_navegador = "--sem-navegador" in sys.argv[1:]
    srv = None
    for p in PORTAS:
        try:
            srv = Servidor((HOST, p), Handler)
            porta_usada = p
            break
        except OSError:
            print(f"Porta {p} ocupada, tentando a proxima...")
    if srv is None:
        print(f"Nao foi possivel abrir nenhuma porta entre {PORTAS[0]} e {PORTAS[-1]}.")
        sys.exit(1)
    url = f"http://127.0.0.1:{porta_usada}/cronograma/"
    print(f"============================================================")
    print(f" Cronograma Barão de Cotegipe - Odontólogo/PSF")
    print(f" Rodando em: {url}")
    print(f" Progresso salvo em: {ARQ_PROGRESSO}")
    print(f" Para encerrar: feche esta janela ou pressione Ctrl+C.")
    print(f"============================================================", flush=True)
    if not sem_navegador:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrado.")
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()
