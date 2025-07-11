document.addEventListener("DOMContentLoaded", function () {
    const gitHubForm = document.getElementById('gitHubForm');

    gitHubForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const username = document.getElementById('usernameInput').value.trim();
        const repository = document.getElementById('repoInput').value.trim();
        const resultsList = document.getElementById('resultsList');

        resultsList.innerHTML = ''; // Limpar resultados anteriores

        if (!username) return;

        if (repository) {
            // Buscar commits se repositório for fornecido
            fetch(`https://api.github.com/repos/${username}/${repository}/commits`)
                .then(response => response.json())
                .then(data => {
                    if (data.message === "Not Found") {
                        addMessage(`Repositório '${repository}' não encontrado para o usuário '${username}'.`, true);
                    } else {
                        data.forEach(commit => {
                            const li = document.createElement('li');
                            li.classList.add('list-group-item');
                            li.innerHTML = `
                                <p><strong>Mensagem:</strong> ${commit.commit.message}</p>
                                <p><strong>Data:</strong> ${new Date(commit.commit.committer.date).toLocaleString()}</p>
                            `;
                            resultsList.appendChild(li);
                        });
                    }
                })
                .catch(() => {
                    addMessage('Erro ao buscar os commits.', true);
                });

        } else {
            // Buscar repositórios se somente usuário for fornecido
            fetch(`https://api.github.com/users/${username}/repos`)
                .then(response => response.json())
                .then(data => {
                    if (data.message === "Not Found") {
                        addMessage(`Usuário '${username}' não encontrado.`, true);
                    } else {
                        data.forEach(repo => {
                            const li = document.createElement('li');
                            li.classList.add('list-group-item');
                            li.innerHTML = `
                                <p><strong>Repositório:</strong> ${repo.name}</p>
                                <p><strong>Descrição:</strong> ${repo.description || 'Sem descrição'}</p>
                                <p><strong>URL:</strong> <a href="${repo.html_url}" target="_blank">${repo.html_url}</a></p>
                            `;
                            resultsList.appendChild(li);
                        });
                    }
                })
                .catch(() => {
                    addMessage('Erro ao buscar os repositórios.', true);
                });
        }

        function addMessage(message, isError = false) {
            const li = document.createElement('li');
            li.classList.add('list-group-item');
            if (isError) li.classList.add('text-danger');
            li.innerHTML = `<strong>${message}</strong>`;
            resultsList.appendChild(li);
        }
    });
});
