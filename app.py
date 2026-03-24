from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from supabase import create_client  #  ADICIONADO

app = Flask(__name__)
app.secret_key = "dignidade_em_acao_r01"

#  CONFIG SUPABASE 
url = "https://hdlrzoobhldhceusesux.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhkbHJ6b29iaGxkaGNldXNlc3V4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQzMDc0MDcsImV4cCI6MjA4OTg4MzQwN30.0OpKWOyBirCOWdbZR6M7CLcojlqUNgig388hYudS9UA"
supabase = create_client(url, key)

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
DB_PATH = INSTANCE_DIR / "dignidade.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    INSTANCE_DIR.mkdir(exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voluntarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT,
            tipo_ajuda TEXT NOT NULL,
            disponibilidade TEXT NOT NULL,
            observacao TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            contato TEXT NOT NULL,
            tipo_doacao TEXT NOT NULL,
            descricao TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/voluntario", methods=["GET", "POST"])
def voluntario():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()
        tipo_ajuda = request.form.get("tipo_ajuda", "").strip()
        disponibilidade = request.form.get("disponibilidade", "").strip()
        observacao = request.form.get("observacao", "").strip()

        if not nome or not telefone or not tipo_ajuda or not disponibilidade:
            flash("Preencha os campos obrigatórios.", "erro")
            return redirect(url_for("voluntario"))

        #  (SUBSTITUI SQLITE)
        data = {
            "nome": nome,
            "telefone": telefone,
            "email": email,
            "tipo_ajuda": tipo_ajuda,
            "disponibilidade": disponibilidade,
            "observacao": observacao
        }

        # supabase.table("voluntarios").insert(data).execute()

        return redirect(url_for("sucesso", tipo="voluntario"))

    return render_template("voluntario.html")


@app.route("/doacao", methods=["GET", "POST"])
def doacao():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        contato = request.form.get("contato", "").strip()
        tipo_doacao = request.form.get("tipo_doacao", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if not nome or not contato or not tipo_doacao or not descricao:
            flash("Preencha os campos obrigatórios.", "erro")
            return redirect(url_for("doacao"))

        #  (SUBSTITUI SQLITE)
        data = {
            "nome": nome,
            "contato": contato,
            "tipo_doacao": tipo_doacao,
            "descricao": descricao
        }

        # supabase.table("doacoes").insert(data).execute()

        return redirect(url_for("sucesso", tipo="doacao"))

    return render_template("doacao.html")


@app.route("/sucesso")
def sucesso():
    tipo = request.args.get("tipo", "registro")
    return render_template("sucesso.html", tipo=tipo)


@app.route("/admin")
def admin():
    #  (SUBSTITUI SQLITE)
    response_vol = supabase.table("voluntarios").select("*").execute()
    response_do = supabase.table("doacoes").select("*").execute()

    voluntarios = response_vol.data
    doacoes = response_do.data

    total_voluntarios = len(voluntarios)
    total_doacoes = len(doacoes)

    return render_template(
        "admin.html",
        voluntarios=voluntarios,
        doacoes=doacoes,
        total_voluntarios=total_voluntarios,
        total_doacoes=total_doacoes
    )


@app.route("/detalhes")
def detalhes():
    return render_template("detalhes.html")


# Inicializa o banco local
init_db()

if __name__ == "__main__":
    app.run(debug=True)