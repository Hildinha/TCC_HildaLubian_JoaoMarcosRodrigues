feather.replace()
const parametrosURL = new URLSearchParams(window.location.search);
const username = parametrosURL.get('username');

var url = 'http://localhost:5000/get_reserva_user';

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

} else {
  console.log('O parâmetro "username" não está presente na URL.');
}

document.addEventListener('DOMContentLoaded', function() {
    var data = {
      username: username,
    };
    // Quando a página carregar, faça uma solicitação ao endpoint do Flask
    fetch(url, {
      method: 'POST',
      //credentials: 'include',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(data => {
        // Manipule os dados recebidos e adicione linhas à tabela
        const tabela = document.getElementById('tabela-reserva-user').getElementsByTagName('tbody')[0];
  
        data.forEach(reserva => {
          const novaLinha = tabela.insertRow();
          novaLinha.insertCell(0).innerText = reserva.numero_sala;
          novaLinha.insertCell(1).innerText = reserva.data;
          novaLinha.insertCell(2).innerText = reserva.horaInicio;
          novaLinha.insertCell(3).innerText = reserva.horaFinal;
        });
      })
      .catch(error => console.error('Erro na solicitação:', error));
  });
//https://twitter.com/One_div