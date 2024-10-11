document.getElementById('agendar-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const nome = document.getElementById('nome').value;
    const data = document.getElementById('data').value;
    const hora = document.getElementById('hora').value;

    // Simulando uma chamada para o back-end (substitua pela sua API)
    fetch('/agendar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nome, data, hora }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('agendar-response').innerText = data.message;
        carregarConsultas();
    });
});

// Carregar consultas agendadas
function carregarConsultas() {
    fetch('/consultas')
        .then(response => response.json())
        .then(consultas => {
            const tbody = document.getElementById('consultas-body');
            tbody.innerHTML = '';

            consultas.forEach(consulta => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${consulta.id}</td>
                    <td>${consulta.nome}</td>
                    <td>${consulta.data}</td>
                    <td>${consulta.hora}</td>
                    <td><button onclick="cancelarConsulta(${consulta.id})">Cancelar</button></td>
                `;
                tbody.appendChild(row);
            });
        });
}

// Cancelar consulta
function cancelarConsulta(id) {
    fetch('/cancelar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('cancelar-response').innerText = data.message;
        carregarConsultas();
    });
}

// Carregar consultas ao iniciar
carregarConsultas();
