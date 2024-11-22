from flask import Flask, render_template, request, redirect, url_for, flash, session
from usuarios import cadastrar_usuario, login, atualizar_usuario, deletar_usuario
from filmes import cadastrar_filme, listar_filmes_por_usuario, atualizar_filme, deletar_filme
from avaliacao import avaliar_filme_por_nome, listar_avaliacoes_por_usuario

app = Flask(__name__)
app.secret_key = "chave_secreta_para_sessoes"

# Página inicial
@app.route("/")
def index():
    if "usuario" in session:
        return redirect(url_for("home"))
    return render_template("login.html")

# Login
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

# Registro
@app.route("/register", methods=["POST"])
def registrar_usuario():
    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]
    resposta = cadastrar_usuario(nome, email, senha)

    if resposta["status"] == "sucesso":
        flash("Usuário cadastrado com sucesso!", "sucesso")
    else:
        flash(resposta["mensagem"], "erro")
    return redirect(url_for("index"))

# Página principal do usuário
@app.route("/home")
def home():
    if "usuario" not in session:
        return redirect(url_for("index"))
    usuario = session["usuario"]
    return render_template("home.html", usuario=usuario)

# Editar conta
@app.route("/edit-account", methods=["POST"])
def edit_account():
    if "usuario" not in session:
        return redirect(url_for("index"))

    usuario_id = session["usuario"]["id"]
    novo_nome = request.form["nome"]
    novo_email = request.form["email"]
    nova_senha = request.form["senha"]

    resposta = atualizar_usuario(usuario_id, novo_nome, novo_email, nova_senha)
    if resposta["status"] == "sucesso":
        # Atualiza os dados da sessão com o novo nome e email
        session["usuario"]["nome"] = novo_nome
        session["usuario"]["email"] = novo_email
        flash("Conta atualizada com sucesso!", "sucesso")
    else:
        flash(resposta["mensagem"], "erro")

    return redirect(url_for("home"))

# Excluir conta
@app.route("/delete-account", methods=["POST"])
def delete_account():
    if "usuario" not in session:
        return redirect(url_for("index"))

    usuario_id = session["usuario"]["id"]
    resposta = deletar_usuario(usuario_id)
    if resposta["status"] == "sucesso":
        session.pop("usuario", None)  # Remove o usuário da sessão
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
    resposta = listar_filmes_por_usuario(usuario_id)

    if resposta["status"] == "erro":
        filmes = []
        mensagem = resposta["mensagem"]
    else:
        filmes = resposta["filmes"]
        mensagem = None

    # Captura o ID do filme em edição (se houver)
    filme_id_em_edicao = request.args.get("editar", type=int)

    return render_template("movies.html", filmes=filmes, mensagem=mensagem, filme_id_em_edicao=filme_id_em_edicao)

# Adicionar filme
@app.route("/add-movie", methods=["POST"])
def add_movie():
    nome = request.form["nome"]
    ano = int(request.form["ano"])
    genero = request.form["genero"]
    diretor = request.form["diretor"]
    usuario_id = session["usuario"]["id"]

    resposta = cadastrar_filme(nome, ano, genero, diretor, usuario_id)
    if resposta["status"] == "sucesso":
        flash("Filme cadastrado com sucesso!", "sucesso")
    else:
        flash(resposta["mensagem"], "erro")
    return redirect(url_for("movies"))

# Editar filme
@app.route("/edit-movie/<int:filme_id>", methods=["POST"])
def edit_movie(filme_id):
    nome = request.form.get("nome")
    ano = request.form.get("ano")
    genero = request.form.get("genero")
    diretor = request.form.get("diretor")
    usuario_id = session["usuario"]["id"]

    # Verifica se todos os campos estão preenchidos
    if not nome or not ano or not genero or not diretor:
        flash("Todos os campos são obrigatórios.", "erro")
        return redirect(url_for("movies"))

    # Atualiza o filme
    resposta = atualizar_filme(filme_id, nome, int(ano), genero, diretor, usuario_id)
    if resposta["status"] == "sucesso":
        flash("Filme atualizado com sucesso!", "sucesso")
    else:
        flash(resposta["mensagem"], "erro")
    return redirect(url_for("movies"))

# Deletar filme
@app.route("/delete-movie/<int:filme_id>", methods=["POST"])
def delete_movie(filme_id):
    usuario_id = session["usuario"]["id"]
    resposta = deletar_filme(filme_id, usuario_id)
    if resposta["status"] == "sucesso":
        flash("Filme deletado com sucesso!", "sucesso")
    else:
        flash(resposta["mensagem"], "erro")
    return redirect(url_for("movies"))

# Listar avaliações
@app.route("/reviews")
def reviews():
    if "usuario" not in session:
        return redirect(url_for("index"))
    usuario_id = session["usuario"]["id"]
    resposta = listar_avaliacoes_por_usuario(usuario_id)
    if resposta["status"] == "erro":
        avaliacoes = []
        mensagem = resposta["mensagem"]
    else:
        avaliacoes = resposta["avaliacoes"]
        mensagem = None
    return render_template("reviews.html", avaliacoes=avaliacoes, mensagem=mensagem)

# Adicionar avaliação
@app.route("/add-review", methods=["POST"])
def add_review():
    nome_filme = request.form["nome_filme"]
    usuario_id = session["usuario"]["id"]
    nota = int(request.form["nota"])
    comentario = request.form["comentario"]

    resposta = avaliar_filme_por_nome(nome_filme, usuario_id, nota, comentario)
    if resposta["status"] == "sucesso":
        flash("Avaliação adicionada com sucesso!", "sucesso")
    else:
        flash(resposta["mensagem"], "erro")
    return redirect(url_for("reviews"))

# Logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Você saiu da conta.", "sucesso")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
