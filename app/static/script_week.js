feather.replace()
const parametrosURL = new URLSearchParams(window.location.search);
const username = parametrosURL.get('username');

var url = 'http://localhost:5000/get_reserva_user_week';

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
  
        data.forEach(reserva => {
          const linha = document.getElementById(reserva.horaInicio);
          var dia = reserva.dia + 1;
          linha.cells[dia].textContent = reserva.numero_sala;
          linha.cells[dia].classList.add("cell-type1");
        });
      })
      .catch(error => console.error('Erro na solicitação:', error));
  });
//https://twitter.com/One_div