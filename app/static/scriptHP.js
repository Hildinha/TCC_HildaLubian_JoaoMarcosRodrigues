feather.replace()
const parametrosURL = new URLSearchParams(window.location.search);
const username = parametrosURL.get('username');

// Verificar se o valor do parâmetro 'name' está presente
if (username) {
  console.log('Valor do parâmetro "username":', username);
  // Adicionar o parâmetro à URL do link
  const linkHistorico = document.getElementById('historicoLink');
  linkHistorico.href = `/Hist?username=${username}`;

  const linkPagInicial = document.getElementById('PagInicialLink');
  linkPagInicial.href = `/PagInicial?username=${username}`;

  const linkSalas = document.getElementById('SalasLink');
  linkSalas.href = `/Salas?username=${username}`;

  const linkSchedule = document.getElementById('ScheduleLink');
  linkSchedule.href = `/Schedule?username=${username}`;

  const linkAdmin = document.getElementById('adminLink');
  linkAdmin.href = `/Admin?username=${username}`;

  // ... faça qualquer coisa que você precise com a variável nomeParametro
} else {
  console.log('O parâmetro "username" não está presente na URL.');
}

document.addEventListener('DOMContentLoaded', function() {
    // Quando a página carregar, faça uma solicitação ao endpoint do Flask
    fetch('http://localhost:5000/get_reservas')
      .then(response => response.json())
      .then(data => {
        // Manipule os dados recebidos e adicione linhas à tabela
        const tabela = document.getElementById('tabela-reservas').getElementsByTagName('tbody')[0];
  
        data.forEach(reserva => {
          const novaLinha = tabela.insertRow();
          novaLinha.insertCell(0).innerText = reserva.numero_sala;
          novaLinha.insertCell(1).innerText = reserva.reserva;
          novaLinha.insertCell(2).innerText = reserva.horaInicio;
          novaLinha.insertCell(3).innerText = reserva.horaFinal;
        });
      })
      .catch(error => console.error('Erro na solicitação:', error));

  });

//https://twitter.com/One_div