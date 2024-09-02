// Lógica para cálculo da ingestão de água
document.getElementById('agua-form').onsubmit = function (event) {
    event.preventDefault();
    const nome = document.getElementById('nome').value;
    const idadeGrupo = document.getElementById('idade_grupo').value;
    const peso = parseFloat(document.getElementById('peso').value);
    const spinner = document.getElementById('spinner');
    const result = document.getElementById('result');

    // Validações adicionais no frontend
    if (isNaN(peso) || peso <= 0) {
        result.innerText = 'Peso deve ser maior que 0';
        return;
    }

    spinner.classList.add('show');
    result.innerHTML = '';

    fetch('http://localhost:5000/calcular', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nome: nome, idade_grupo: idadeGrupo, peso: peso }),
    })
    .then((response) => response.json())
    .then((data) => {
        spinner.classList.remove('show');
        if (data.error) {
            result.innerText = data.error;
        } else {
            result.innerText = 'Ingestão diária de água: ' + data.total + ' ml por dia';
        }
    })
    .catch((error) => {
        console.error('Erro:', error);
        spinner.classList.remove('show');
        result.innerText = 'Erro ao calcular ingestão de água';
    });
};

// Abrir o modal de consulta
document.getElementById('mostrar-resultados').onclick = function () {
    document.getElementById('resultado-modal').style.display = 'flex';
};

// Fechar o modal
document.getElementById('close-modal').onclick = function () {
    document.getElementById('resultado-modal').style.display = 'none';
};

// Consultar resultados com base no nome
document.getElementById('resultado-form').onsubmit = function (event) {
    event.preventDefault();
    const nome = document.getElementById('nome-consulta').value;

    fetch(`http://localhost:5000/consultas/${nome}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        const resultList = document.getElementById('result-list');
        resultList.innerHTML = '';  // Limpa a lista antes de adicionar os resultados

        if (data.length === 0) {
            resultList.innerHTML = '<p>Nenhum resultado encontrado para esse nome</p>';
        } else {
            const table = document.createElement('table');
            table.className = 'result-table';

            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');

            const headers = ['Grupo Etário', 'Peso (kg)', 'Total (ml)'];
            headers.forEach(headerText => {
                const th = document.createElement('th');
                th.appendChild(document.createTextNode(headerText));
                headerRow.appendChild(th);
            });

            thead.appendChild(headerRow);
            table.appendChild(thead);

            const tbody = document.createElement('tbody');
            data.forEach(consulta => {
                const row = document.createElement('tr');

                const idadeGrupoCell = document.createElement('td');
                idadeGrupoCell.appendChild(document.createTextNode(consulta.idade_grupo));
                row.appendChild(idadeGrupoCell);

                const pesoCell = document.createElement('td');
                pesoCell.appendChild(document.createTextNode(consulta.peso));
                row.appendChild(pesoCell);

                const totalCell = document.createElement('td');
                totalCell.appendChild(document.createTextNode(`${consulta.total} ml`));
                row.appendChild(totalCell);

                tbody.appendChild(row);
            });

            table.appendChild(tbody);
            resultList.appendChild(table);
        }
    })
    .catch(error => {
        console.error('Erro ao consultar os resultados:', error);
        alert('Erro ao consultar os resultados. Verifique o console para mais detalhes.');
    });
};
