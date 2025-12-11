import pytest
from backend.src.app import create_app
from backend.src.extensions import db


@pytest.fixture
def client():
    app = create_app(testing=True)

    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
        yield test_client
        with app.app_context():
            db.session.remove()
            db.drop_all()


# ------------------------------
# CADASTRO
# ------------------------------

def test_register_success(client):
    data = {
        "nome": "Joao",
        "id_usuario": "joao123",
        "senha": "123456",
        "email": "joao@example.com"
    }

    response = client.post("/api/register", json=data)

    assert response.status_code == 201
    assert response.get_json()["message"] == "Usuário cadastrado com sucesso!"


def test_register_missing_fields(client):
    data = {
        "nome": "Pedro",
        "id_usuario": "pedro123",
        "email": "pedro@example.com"
    }

    response = client.post("/api/register", json=data)

    assert response.status_code == 400
    assert "obrigatórios" in response.get_json()["error"]


def test_register_invalid_email_format(client):
    response = client.post("/api/register", json={
        "nome": "Marina",
        "id_usuario": "marina123",
        "senha": "123456",
        "email": "email-invalido"
    })

    # backend permite email qualquer
    assert response.status_code == 201



def test_register_empty_fields(client):
    response = client.post("/api/register", json={
        "nome": "",
        "id_usuario": "idvazio",
        "senha": "",
        "email": "email@example.com"
    })

    assert response.status_code == 400


# ------------------------------
# LOGIN
# ------------------------------

def test_login_success(client):
    client.post("/api/register", json={
        "nome": "Ana",
        "id_usuario": "ana123",
        "senha": "senha123",
        "email": "ana@example.com"
    })

    response = client.post("/api/login", json={
        "id_usuario": "ana123",
        "senha": "senha123"
    })

    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["message"] == "Login bem-sucedido!"
    assert json_data["user"]["id_usuario"] == "ana123"


def test_login_missing_fields(client):
    response = client.post("/api/login", json={
        "id_usuario": "joao123"
    })

    assert response.status_code == 400
    assert "obrigatórios" in response.get_json()["error"]


def test_login_wrong_password(client):
    client.post("/api/register", json={
        "nome": "Laura",
        "id_usuario": "laura123",
        "senha": "senhaCorreta",
        "email": "laura@example.com"
    })

    response = client.post("/api/login", json={
        "id_usuario": "laura123",
        "senha": "senhaErrada"
    })

    assert response.status_code == 401
    assert response.get_json()["error"].lower() == "credenciais inválidas"




def test_login_nonexistent_user(client):
    response = client.post("/api/login", json={
        "id_usuario": "naoexiste",
        "senha": "123456"
    })

    assert response.status_code == 401
    assert response.get_json()["error"].lower() == "credenciais inválidas"




def test_login_empty_fields(client):
    response = client.post("/api/login", json={
        "id_usuario": "",
        "senha": ""
    })

    assert response.status_code == 400


def test_login_invalid_json(client):
    response = client.post("/api/login", data="texto cru que não é json")

    assert response.status_code == 415


 