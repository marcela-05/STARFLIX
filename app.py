from flask import Flask, render_template, request, redirect, url_for, flash, session
from usuarios import cadastrarUsuario, login, atualizarUsuario, deletarUsuario
from filmes import cadastrarFilme, listarFilme, atualizarFilme, deletarFilme
from avaliacao import avaliarFilme, listarAvaliacao
from utils import carregar_dados_do_json, salvar_dados_no_json

# Configuração do Flask
app = Flask(__name__)
app.secret_key = "chave_secreta_para_sessoes"

# Nome do arquivo JSON para persistência
ARQUIVO_JSON = "dados_starflix.json"

# Inicializar os dados do sistema
dados = carregar_dados_do_json(ARQUIVO_JSON)

@app.route("/")
def index():
    if "usuario" in session:
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def autenticar_login():
    email = request.form["email"]
    senha = request.form["senha"]
    resposta = login(email, senha)

    if resposta["status"] == "sucesso":
        session["usuario"] = resposta["usuario"]
        return redirect(url_for("home"))
    else:
        flash(resposta["mensagem"], "erro")
        return redirect(url_for("index"))

@app.route("/register", methods=["POST"])
def registrar_usuario():
    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]
    resposta = cadastrarUsuario(nome, email, senha)

    if resposta["status"] == "sucesso":
        flash("Usuário cadastrado com sucesso!", "sucesso")
    else:
        flash(resposta["mensagem"], "erro")
    return redirect(url_for("index"))

@app.route("/home")
def home():
    if "usuario" not in session:
        return redirect(url_for("index"))
    usuario = session["usuario"]
    return render_template("home.html", usuario=usuario)

@app.route("/edit-account", methods=["POST"])
def edit_account():
    if "usuario" not in session:
        return redirect(url_for("index"))

    usuario_id = session["usuario"]["id"]
    novo_nome = request.form["nome"]
    novo_email = request.form["email"]
    nova_senha = request.form["senha"]

    resposta = atualizarUsuario(usuario_id, novo_nome, novo_email, nova_senha)
    if resposta["status"] == "sucesso":
        session["usuario"]["nome"] = novo_nome
        session["usuario"]["email"] = novo_email
        flash("Conta atualizada com sucesso!", "sucesso")
    else:
        flash(resposta["mensagem"], "erro")

    return redirect(url_for("home"))

@app.route("/delete-account", methods=["POST"])
def delete_account():
    if "usuario" not in session:
        return redirect(url_for("index"))

    usuario_id = session["usuario"]["id"]
    resposta = deletarUsuario(usuario_id)
    if resposta["status"] == "sucesso":
        session.pop("usuario", None)
        flash("Conta excluída com sucesso!", "sucesso")
        return redirect(url_for("index"))
    else:
        flash(resposta["mensagem"], "erro")
        return redirect(url_for("home"))

@app.route("/movies")
def movies():
    if "usuario" not in session:
        return redirect(url_for("index"))

    usuario_id = session["usuario"]["id"]
    resposta = listarFilme(usuario_id)

    filmes = resposta.get("filmes", [])
    mensagem = resposta.get("mensagem")
    filme_id_em_edicao = request.args.get("editar", type=int)

    return render_template("movies.html", filmes=filmes, mensagem=mensagem, filme_id_em_edicao=filme_id_em_edicao)

@app.route("/add-movie", methods=["POST"])
def add_movie():
    nome = request.form["nome"]
    ano = int(request.form["ano"])
    genero = request.form["genero"]
    diretor = request.form["diretor"]
    usuario_id = session["usuario"]["id"]

    resposta = cadastrarFilme(nome, ano, genero, diretor, usuario_id)
    if resposta["status"] == "sucesso":
        flash("Filme cadastrado com sucesso!", "sucesso")
    else:
        flash(resposta["mensagem"], "erro")
    return redirect(url_for("movies"))

@app.route("/edit-movie/<int:filme_id>", methods=["POST"])
def edit_movie(filme_id):
    nome = request.form.get("nome")
    ano = request.form.get("ano")
    genero = request.form.get("genero")
    diretor = request.form.get("diretor")
    usuario_id = session["usuario"]["id"]

    if not nome or not ano or not genero or not diretor:
        flash("Todos os campos são obrigatórios.", "erro")
        return redirect(url_for("movies"))

    resposta = atualizarFilme(filme_id, nome, int(ano), genero, diretor, usuario_id)
    if resposta["status"] == "sucesso":
        flash("Filme atualizado com sucesso!", "sucesso")
    else:
        flash(resposta["mensagem"], "erro")
    return redirect(url_for("movies"))

@app.route("/delete-movie/<int:filme_id>", methods=["POST"])
def delete_movie(filme_id):
    usuario_id = session["usuario"]["id"]
    resposta = deletarFilme(filme_id, usuario_id)
    if resposta["status"] == "sucesso":
        flash("Filme deletado com sucesso!", "sucesso")
    else:
        flash(resposta["mensagem"], "erro")
    return redirect(url_for("movies"))

@app.route("/reviews")
def reviews():
    if "usuario" not in session:
        return redirect(url_for("index"))

    usuario_id = session["usuario"]["id"]
    resposta = listarAvaliacao(usuario_id)

    avaliacoes = resposta.get("avaliacoes", [])
    mensagem = resposta.get("mensagem")

    return render_template("reviews.html", avaliacoes=avaliacoes, mensagem=mensagem)

@app.route("/add-review", methods=["POST"])
def add_review():
    nome_filme = request.form["nome_filme"]
    usuario_id = session["usuario"]["id"]
    nota = int(request.form["nota"])
    comentario = request.form["comentario"]

    resposta = avaliarFilme(nome_filme, usuario_id, nota, comentario)
    if resposta["status"] == "sucesso":
        flash("Avaliação adicionada com sucesso!", "sucesso")
    else:
        flash(resposta["mensagem"], "erro")
    return redirect(url_for("reviews"))

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Você saiu da conta.", "sucesso")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
