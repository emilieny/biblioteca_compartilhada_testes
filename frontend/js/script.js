// script.js

document.addEventListener('DOMContentLoaded', () => {
    // Elementos globais
    const loggedInUserNameSpan = document.getElementById('loggedInUserName');
    const userBalanceSpan = document.getElementById('userBalance');
    const logoutButton = document.getElementById('logoutButton');
    const livrosListDiv = document.getElementById('livrosList');
    const usuariosListDiv = document.getElementById('usuariosList');
    const doarLivroForm = document.getElementById('doarLivroForm');
    const doacaoMessageDiv = document.getElementById('doacaoMessage');
    const emprestarLivroForm = document.getElementById('emprestarLivroForm');
    const emprestimoMessageDiv = document.getElementById('emprestimoMessage');
    const devolverLivroForm = document.getElementById('devolverLivroForm');
    const devolucaoMessageDiv = document.getElementById('devolucaoMessage');
    // Adicionado para Notificações
    const notificacoesListDiv = document.getElementById('notificacoesList'); // NOVO
    const notificacoesSection = document.getElementById('notificacoesSection'); // NOVO

    // Novos elementos para menu e perfil
    const menuBtns = document.querySelectorAll('.menu-btn');
    const sections = {
        perfilSection: document.getElementById('perfilSection'),
        livrosSection: document.getElementById('livrosSection'),
        doarSection: document.getElementById('doarSection'),
        emprestimosSection: document.getElementById('emprestimosSection'),
        devolucaoSection: document.getElementById('devolucaoSection'),
        notificacoesSection: notificacoesSection // NOVO: Adicionar a seção de notificações
    };
    const perfilNome = document.getElementById('perfilNome');
    const perfilId = document.getElementById('perfilId');
    const perfilSaldo = document.getElementById('perfilSaldo');
    const logoutButtonPerfil = document.getElementById('logoutButtonPerfil'); // Botão de logout no perfil

    let userId = null; // Variável para armazenar o ID do usuário logado
    let userName = null; // Variável para armazenar o nome do usuário logado

    // Função para mostrar mensagens temporárias
    function showMessage(element, message, type) {
        element.textContent = message;
        element.className = `message ${type}`;
        element.style.display = 'block';
        setTimeout(() => {
            element.style.display = 'none';
        }, 5000);
    }

    // Função para buscar e exibir o usuário logado
    async function fetchCurrentUser() {
        try {
            const response = await fetch('/api/current_user');
            if (response.ok) {
                const data = await response.json();
                userId = data.id_usuario;
                userName = data.nome;
                if (loggedInUserNameSpan) {
                    loggedInUserNameSpan.textContent = userName;
                }
                return true;
            } else {
                console.error('Nenhum usuário logado ou sessão expirada.');
                window.location.href = '/login'; // Redirecionar para login se não houver usuário
                return false;
            }
        } catch (error) {
            console.error('Erro ao buscar usuário atual:', error);
            window.location.href = '/login';
            return false;
        }
    }

    // Função para carregar o saldo do usuário
    async function loadUserBalance() {
        if (!userId) {
            console.log("UserID não disponível para carregar saldo.");
            return;
        }
        try {
            const response = await fetch(`/api/usuario/${userId}/saldo`);
            if (response.ok) {
                const data = await response.json();
                if (userBalanceSpan) {
                    userBalanceSpan.textContent = data.saldo_moedas;
                }
                if (perfilSaldo) {
                    perfilSaldo.textContent = data.saldo_moedas;
                }
            } else {
                console.error('Erro ao carregar saldo:', response.statusText);
                // Tratar erro, talvez mostrar mensagem ao usuário
            }
        } catch (error) {
            console.error('Erro de rede ao carregar saldo:', error);
        }
    }

    // Função para carregar a lista de livros
    async function loadLivros() {
        try {
            const response = await fetch('/api/livros');
            const livros = await response.json();
            if (livrosListDiv) {
                livrosListDiv.innerHTML = ''; // Limpa a lista existente
                if (livros.length === 0) {
                    livrosListDiv.innerHTML = '<p>Nenhum livro disponível no momento.</p>';
                    return;
                }
                livros.forEach(livro => {
                    const livroDiv = document.createElement('div');
                    livroDiv.className = 'livro-item';
                    // URL da capa do Open Library
                    const capaUrl = livro.isbn ? `https://covers.openlibrary.org/b/isbn/${livro.isbn}-L.jpg` : '';
                    livroDiv.innerHTML = `
                        <img src="${capaUrl}" alt="Capa do Livro" class="livro-capa" style="width:100px; height:auto; display:block; margin-bottom:10px; object-fit:contain; background:#f5f6fa; border-radius:6px; box-shadow:0 2px 6px rgba(0,0,0,0.04);">
                        <h3>${livro.titulo}</h3>
                        <p><strong>Autor:</strong> ${livro.autor}</p>
                        <p><strong>ISBN:</strong> ${livro.isbn}</p>
                        <p><strong>Ano:</strong> ${livro.ano_publicacao}</p>
                        <p class="status-${livro.disponivel ? 'disponivel' : 'indisponivel'}">
                            ${livro.disponivel ? 'Disponível' : 'Indisponível'}
                        </p>
                    `;
                    livrosListDiv.appendChild(livroDiv);
                });
            }
        } catch (error) {
            console.error('Erro ao carregar livros:', error);
            if (livrosListDiv) {
                livrosListDiv.innerHTML = '<p>Erro ao carregar livros. Tente novamente mais tarde.</p>';
            }
        }
    }

    

    // Função para preencher os dados do perfil
    async function fillPerfil() {
        if (perfilNome && perfilId && perfilSaldo) {
            perfilNome.textContent = userName;
            perfilId.textContent = userId;
            // O saldo será carregado por loadUserBalance()
        }
    }

    // Função para carregar e exibir notificações
    async function loadNotificacoes() {
        if (!userId) {
            console.log("UserID não disponível para carregar notificações.");
            if (notificacoesListDiv) {
                notificacoesListDiv.innerHTML = '<p>Faça login para ver suas notificações.</p>';
            }
            return;
        }
        try {
            const response = await fetch(`/api/notificacoes/${userId}`);
            if (response.ok) {
                const notificacoes = await response.json();
                if (notificacoesListDiv) {
                    notificacoesListDiv.innerHTML = '';
                    if (notificacoes.length === 0) {
                        notificacoesListDiv.innerHTML = '<p>Você não tem novas notificações.</p>';
                    } else {
                        notificacoes.forEach(notificacao => {
                            const notifDiv = document.createElement('div');
                            notifDiv.className = `notificacao-item ${notificacao.lida ? 'lida' : 'nao-lida'}`;
                            notifDiv.innerHTML = `
                                <p><strong>${notificacao.tipo_evento}:</strong> ${notificacao.mensagem}</p>
                                <small>${new Date(notificacao.data_criacao).toLocaleString()}</small>
                            `;
                            notificacoesListDiv.appendChild(notifDiv);
                            // Exibe pop-up para notificações não lidas
                            if (!notificacao.lida) {
                                mostrarNotificacao(`${notificacao.tipo_evento}: ${notificacao.mensagem}`);
                            }
                        });
                    }
                }
            } else {
                console.error('Erro ao carregar notificações:', response.statusText);
                if (notificacoesListDiv) {
                    notificacoesListDiv.innerHTML = '<p>Erro ao carregar notificações. Tente novamente mais tarde.</p>';
                }
            }
        } catch (error) {
            console.error('Erro de rede ao carregar notificações:', error);
            if (notificacoesListDiv) {
                notificacoesListDiv.innerHTML = '<p>Erro de rede ao carregar notificações.</p>';
            }
        }
    }

// Função aprimorada para mostrar pop-ups de notificação no topo direito
function mostrarNotificacao(mensagem) {
    let popup = document.getElementById('notificacao-popup');
    if (!popup) {
        popup = document.createElement('div');
        popup.id = 'notificacao-popup';
        popup.className = 'notificacao-popup';
        document.body.appendChild(popup);
    }
    popup.textContent = mensagem;
    popup.style.display = 'block';
    popup.classList.add('mostrar');
    // Remove qualquer timeout anterior
    if (popup._timeoutId) clearTimeout(popup._timeoutId);
    popup._timeoutId = setTimeout(() => {
        popup.classList.remove('mostrar');
        setTimeout(() => { popup.style.display = 'none'; }, 400);
    }, 3000);
}

    // Lógica para alternar seções do dashboard
    menuBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            menuBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            const targetSectionId = this.getAttribute('data-section');
            for (const sectionKey in sections) {
                if (sections[sectionKey]) {
                    sections[sectionKey].style.display = 'none';
                }
            }

            if (sections[targetSectionId]) {
                sections[targetSectionId].style.display = 'block';
                // Recarregar dados específicos da seção se necessário
                if (targetSectionId === 'livrosSection') {
                    loadLivros();
                } else if (targetSectionId === 'perfilSection') {
                    fillPerfil();
                    loadUserBalance(); // Garante que o saldo do perfil esteja atualizado
                } else if (targetSectionId === 'usuariosSection') {
                    loadUsuarios();
                } else if (targetSectionId === 'notificacoesSection') { // NOVO: Carregar notificações ao abrir a seção
                    loadNotificacoes();
                } else if (targetSectionId === 'devolucaoSection') {
                    // Poderia adicionar lógica específica para devolução se necessário
                }
            }
        });
    });

    // Listener para o botão de logout no header
    if (logoutButton) {
        logoutButton.addEventListener('click', async () => {
            try {
                const response = await fetch('/api/logout', { method: 'POST' });
                if (response.ok) {
                    window.location.href = '/login';
                } else {
                    alert('Erro ao fazer logout.');
                }
            } catch (error) {
                console.error('Erro de rede ao fazer logout:', error);
                alert('Erro de rede ao fazer logout.');
            }
        });
    }

    // Listener para o botão de logout no perfil
    if (logoutButtonPerfil) {
        logoutButtonPerfil.addEventListener('click', async () => {
            try {
                const response = await fetch('/api/logout', { method: 'POST' });
                if (response.ok) {
                    window.location.href = '/login';
                } else {
                    alert('Erro ao fazer logout.');
                }
            } catch (error) {
                console.error('Erro de rede ao fazer logout:', error);
                alert('Erro de rede ao fazer logout.');
            }
        });
    }

    // Listener para o formulário de Doar Livro
    if (doarLivroForm) {
        doarLivroForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const titulo = document.getElementById('titulo').value;
            const autor = document.getElementById('autor').value;
            const isbn = document.getElementById('isbn').value;
            const anoPublicacao = parseInt(document.getElementById('anoPublicacao').value);

            try {
                const response = await fetch('/api/doar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        titulo,
                        autor,
                        isbn,
                        ano_publicacao: anoPublicacao,
                        id_doador: userId // Garante que o ID do usuário logado é enviado
                    })
                });
                const data = await response.json();
                if (response.ok) {
                    showMessage(doacaoMessageDiv, data.message, 'success');
                    doarLivroForm.reset();
                    loadLivros(); // Recarrega a lista de livros
                    loadUserBalance(); // Atualiza o saldo do usuário
                    // Buscar notificações novas e exibir pop-up
                    await exibirNovasNotificacoesPopUp();
                } else {
                    showMessage(doacaoMessageDiv, data.error, 'error');
                    if (data.error) mostrarNotificacao(data.error);
                }
            } catch (error) {
                showMessage(doacaoMessageDiv, 'Erro de rede ao doar livro.', 'error');
                mostrarNotificacao('Erro de rede ao doar livro.');
            }
        });
    }

    // Listener para o formulário de Emprestar Livro
    if (emprestarLivroForm) {
        emprestarLivroForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const isbnLivro = document.getElementById('emprestimoIsbn').value;
            try {
                const response = await fetch('/api/emprestar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id_usuario: userId, isbn_livro: isbnLivro }) // Garante que o ID do usuário logado é enviado
                });
                const data = await response.json();
                if (response.ok) {
                    showMessage(emprestimoMessageDiv, data.message, 'success');
                    emprestarLivroForm.reset();
                    loadLivros();
                    loadUserBalance();
                    // Buscar notificações novas e exibir pop-up
                    await exibirNovasNotificacoesPopUp();
                } else {
                    showMessage(emprestimoMessageDiv, data.error, 'error');
                    if (data.error) mostrarNotificacao(data.error);
                }
            } catch (error) {
                showMessage(emprestimoMessageDiv, 'Erro de rede ao emprestar livro.', 'error');
                mostrarNotificacao('Erro de rede ao emprestar livro.');
            }
        });
    }

    // Listener para o formulário de Devolver Livro
    if (devolverLivroForm) {
        devolverLivroForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const isbnLivro = document.getElementById('devolucaoIsbn').value;
            try {
                const response = await fetch('/api/devolver', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id_usuario: userId, isbn_livro: isbnLivro }) // Garante que o ID do usuário logado é enviado
                });
                const data = await response.json();
                if (response.ok) {
                    showMessage(devolucaoMessageDiv, data.message, 'success');
                    devolverLivroForm.reset();
                    loadLivros();
                    loadUserBalance();
                    // Buscar notificações novas e exibir pop-up
                    await exibirNovasNotificacoesPopUp();
                } else {
                    showMessage(devolucaoMessageDiv, data.error, 'error');
                    if (data.error) mostrarNotificacao(data.error);
                }
            } catch (error) {
                showMessage(devolucaoMessageDiv, 'Erro de rede ao devolver livro.', 'error');
                mostrarNotificacao('Erro de rede ao devolver livro.');
            }
        });
    }
    // Função utilitária para buscar notificações não lidas e exibir como pop-up
    async function exibirNovasNotificacoesPopUp() {
        if (!userId) return;
        try {
            const response = await fetch(`/api/notificacoes/${userId}`);
            if (response.ok) {
                const notificacoes = await response.json();
                // Ordena por data (mais recente primeiro)
                notificacoes.sort((a, b) => new Date(b.data_criacao) - new Date(a.data_criacao));
                // Busca a primeira não lida com mensagem válida
                const nova = notificacoes.find(n => !n.lida && n.mensagem && n.mensagem.trim() !== '');
                if (nova) {
                    const texto = `${nova.tipo_evento ? nova.tipo_evento + ': ' : ''}${nova.mensagem}`;
                    console.log('Pop-up:', texto); // debug
                    mostrarNotificacao(texto);
                } else {
                    console.log('Nenhuma notificação não lida com mensagem encontrada:', notificacoes);
                }
            }
        } catch (e) {
            console.error('Erro ao buscar notificações para pop-up:', e);
        }
    }

    // Carregar dados iniciais ao carregar a página principal
    // Assegura que o userId seja carregado antes de outras funções que dependem dele
    fetchCurrentUser().then(isLoggedIn => {
        if (isLoggedIn) {
            loadUserBalance();
            loadLivros();
            if (sections.usuariosSection) loadUsuarios();
            if (sections.perfilSection) fillPerfil();
            if (sections.notificacoesSection) loadNotificacoes(); // Carregar notificações ao iniciar
        }
    });
});