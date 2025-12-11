# backend/app.py
from flask import Flask, jsonify, request, send_from_directory, session, redirect, url_for
import os
from functools import wraps
import bcrypt

# Importar o db de extensions.py
from backend.src.extensions import db

# Importações dos seus módulos reorganizados
from backend.src.services.biblioteca_service import BibliotecaService
from backend.src.models.entities import Livro, Usuario, Emprestimo, Notificacao
from backend.src.repositories.sqlalchemy_repositories import SQLAlchemyLivroRepository, SQLAlchemyUsuarioRepository, SQLAlchemyEmprestimoRepository, SQLAlchemyNotificacaoRepository
from backend.src.factories.object_factory import ObjectFactory
from backend.src.observers.log_observer import LogObserver

def create_app(testing=False):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    frontend_path = os.path.join(base_dir, 'frontend')

    app = Flask(__name__, static_folder=frontend_path, static_url_path='/')

    # CONFIG BASE
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua_chave_secreta_muito_segura_aqui')

    # CONFIG BANCO — Teste ou Produção
    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'

    db.init_app(app)

    # Instanciação dos repositórios e serviços (mantemos igual)
    livro_repo = SQLAlchemyLivroRepository()
    usuario_repo = SQLAlchemyUsuarioRepository()
    emprestimo_repo = SQLAlchemyEmprestimoRepository()
    notificacao_repo = SQLAlchemyNotificacaoRepository()

    object_factory = ObjectFactory()
    biblioteca_service = BibliotecaService(livro_repo, usuario_repo, emprestimo_repo, notificacao_repo)
    log_observer = LogObserver(notificacao_repo, object_factory)
    biblioteca_service.attach(log_observer)

    # Criar tabelas
    with app.app_context():
        db.create_all()


    # Decorador para exigir login
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    @app.route('/')
    def index():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/login')
    def login():
        return send_from_directory(app.static_folder, 'login.html')

    @app.route('/css/<path:filename>')
    def serve_css(filename):
        return send_from_directory(os.path.join(app.static_folder, 'css'), filename)

    @app.route('/js/<path:filename>')
    def serve_js(filename):
        return send_from_directory(os.path.join(app.static_folder, 'js'), filename)

    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.json
        nome = data.get('nome')
        id_usuario = data.get('id_usuario')
        senha = data.get('senha')
        email = data.get('email') # Obtém o email da requisição

        if not all([nome, id_usuario, senha, email]): # Garante que o email seja verificado
            return jsonify({"error": "Nome, ID de usuário, senha e email são obrigatórios"}), 400

        # Gerar o hash da senha
        hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # CORRIGIDO: Agora passando o email para a factory
        usuario = object_factory.create_usuario(nome, id_usuario, hashed_password, email)
        
        response_data, status_code = biblioteca_service.cadastrar_usuario(usuario)
        return jsonify(response_data), status_code

    @app.route('/api/login', methods=['POST'])
    def api_login():
        data = request.json
        id_usuario = data.get('id_usuario')
        senha = data.get('senha')

        if not id_usuario or not senha:
            return jsonify({"error": "ID de usuário e senha são obrigatórios"}), 400

        usuario = biblioteca_service.autenticar_usuario(id_usuario, senha)
        
        if usuario:
            session['user_id'] = usuario.id_usuario
            session['user_name'] = usuario.nome
            return jsonify({"message": "Login bem-sucedido!", "user": usuario.to_dict(), "user_id": usuario.id_usuario, "user_name": usuario.nome}), 200
        else:
            return jsonify({"error": "Credenciais inválidas"}), 401

    @app.route('/api/logout', methods=['POST'])
    @login_required
    def api_logout():
        session.pop('user_id', None)
        session.pop('user_name', None)
        return jsonify({"message": "Logout realizado com sucesso"}), 200

    @app.route('/api/current_user', methods=['GET'])
    @login_required
    def current_user():
        user_id = session.get('user_id')
        user_name = session.get('user_name')
        if user_id and user_name:
            return jsonify({"id_usuario": user_id, "nome": user_name}), 200
        return jsonify({"error": "Nenhum usuário logado"}), 401

    @app.route('/api/livros', methods=['GET'])
    @login_required
    def get_livros():
        livros = biblioteca_service.listar_livros_disponiveis()
        return jsonify([livro.to_dict() for livro in livros]), 200

    @app.route('/api/doar', methods=['POST'])
    @login_required
    def doar_livro():
        data = request.json
        titulo = data.get('titulo')
        autor = data.get('autor')
        isbn = data.get('isbn')
        ano_publicacao = data.get('ano_publicacao')
        id_doador = session.get('user_id') # Usa o id do doador da sessão

        if id_doador != data.get('id_doador'): # Verificação de segurança
            return jsonify({"error": "Você não pode doar livros por outro usuário."}), 403

        if not all([titulo, autor, isbn, ano_publicacao, id_doador]):
            return jsonify({"error": "Título, autor, ISBN, ano de publicação e ID do doador são obrigatórios"}), 400
        
        # CORRIGIDO: Passando o id_doador para a factory
        livro = object_factory.create_livro(titulo, autor, isbn, ano_publicacao, id_doador)
        response_data, success = biblioteca_service.doar_livro(livro, id_doador)
        status_code = 201 if success else 400
        return jsonify(response_data), status_code

    @app.route('/api/usuario/<id_usuario>/saldo', methods=['GET'])
    @login_required
    def get_saldo_usuario(id_usuario):
        if session.get('user_id') != id_usuario:
            return jsonify({"error": "Você não tem permissão para ver o saldo de outro usuário."}), 403

        response_data, success = biblioteca_service.consultar_saldo_moedas(id_usuario)
        status_code = 200 if success else 404
        return jsonify(response_data), status_code

    @app.route('/api/emprestar', methods=['POST'])
    @login_required
    def emprestar_livro():
        data = request.json
        id_usuario = data.get('id_usuario')
        isbn_livro = data.get('isbn_livro')

        if session.get('user_id') != id_usuario:
            return jsonify({"error": "Você só pode emprestar livros em seu próprio nome."}), 403

        if not all([id_usuario, isbn_livro]):
            return jsonify({"error": "ID do usuário e ISBN do livro são obrigatórios"}), 400
        
        from backend.src.commands.emprestimo_command import EmprestimoCommand
        emprestimo_command = EmprestimoCommand(biblioteca_service, id_usuario, isbn_livro)
        success = emprestimo_command.execute()

        if success:
            return jsonify({"message": "Livro emprestado com sucesso!"}), 200
        else:
            return jsonify({"error": "Não foi possível emprestar o livro. Verifique o ISBN, seu saldo ou se o livro está disponível."}), 400

    @app.route('/api/devolver', methods=['POST'])
    @login_required
    def devolver_livro():
        data = request.json
        id_usuario = data.get('id_usuario')
        isbn_livro = data.get('isbn_livro')

        if session.get('user_id') != id_usuario:
            return jsonify({"error": "Você só pode devolver livros em seu próprio nome."}), 403

        if not all([id_usuario, isbn_livro]):
            return jsonify({"error": "ID do usuário e ISBN do livro são obrigatórios"}), 400
        
        response_data, success = biblioteca_service.devolver_livro(id_usuario, isbn_livro)
        status_code = 200 if success else 400
        return jsonify(response_data), status_code

    @app.route('/api/notificacoes/<id_usuario>', methods=['GET'])
    @login_required
    def get_notificacoes_usuario(id_usuario):
        if session.get('user_id') != id_usuario:
            return jsonify({"error": "Você não tem permissão para ver as notificações de outro usuário."}), 403
        
        notificacoes = notificacao_repo.get_by_id_usuario(id_usuario)
        return jsonify([n.to_dict() for n in notificacoes]), 200

    @app.route('/api/usuarios', methods=['GET'])
    @login_required
    def get_usuarios():
        usuarios = usuario_repo.get_all()
        return jsonify([user.to_dict() for user in usuarios]), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)