const parametrosURL = new URLSearchParams(window.location.search);
const username = parametrosURL.get('username');

var btnConsult = document.getElementById('consultSala');
var selectElement = document.getElementById('movie');
var selectedValue = selectElement.value;
var urlGetSalas = 'http://localhost:5000/get_salas';
var urlGetSalaInicial = 'http://localhost:5000/get_salas_inicial';

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

    var inputCalendario = document.getElementById('calendario');
    var dataAtual = new Date();

    var mes = ('0' + (dataAtual.getMonth() + 1)).slice(-2);
    var dia = ('0' + dataAtual.getDate()).slice(-2);
    var ano = dataAtual.getFullYear().toString().slice(-4);
    
    var dataFormatada = dia + '/' + mes + '/' + ano;
    inputCalendario.value = dataFormatada;



    var data = {
        andarSala: selectedValue,
      };

    // Use a Fetch API para enviar os dados para o backend
    fetch(urlGetSalaInicial, {
        method: 'POST',
        //credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(response => {

        //var listaSalas = JSON.parse(response);

        response.forEach(function(item, index) {
            // Obtém o número da sala do objeto
            var numeroSala = item.numeroSala;
    
            // Obtém o ID do span correspondente
            var spanId = "span" + (index + 1);
    
            // Obtém o elemento span pelo ID
            var spanElement = document.getElementById(spanId);
    
            // Verifica se o elemento span existe antes de tentar preenchê-lo
            if (spanElement) {
                // Preenche o conteúdo do span com o número da sala
                spanElement.textContent = numeroSala;
            }
        });
    })
    .catch(error => console.error('Erro na solicitação:', error));

});

btnConsult.onclick = function() {
    var selectedValue = selectElement.value
    var inputHour = document.getElementById('hour')
    var inputCalendario = document.getElementById('calendario');

    var dataConsult1 = inputCalendario.value
    var partesData = dataConsult1.split('/');
    var dataConsult = new Date(partesData[2], partesData[1] - 1, partesData[0]);

    var hourConsulta = inputHour.value

    var mesConsulta = ('0' + (dataConsult.getMonth() + 1)).slice(-2);
    var diaConsulta = ('0' + dataConsult.getDate()).slice(-2);
    var anoConsulta = dataConsult.getFullYear().toString().slice(-4);
    
    var dataConsulta = anoConsulta + '-' + mesConsulta + '-' + diaConsulta;

    var data = {
        andarSala: selectedValue,
        hourConsulta: hourConsulta,
        dataConsulta: dataConsulta
      };

    // Quando a página carregar, faça uma solicitação ao endpoint do Flask
    fetch(urlGetSalas, {
      method: 'POST',
      //credentials: 'include',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(response => {

        //var listaSalas = JSON.parse(response);

        response.forEach(function(item, index) {
            // Obtém o número da sala do objeto
            var numeroSala = item.numeroSala;
    
            // Obtém o ID do span correspondente
            var spanId = "span" + (index + 1);
            var doorId = "door" + (index + 1);
    
            // Obtém o elemento span pelo ID
            var spanElement = document.getElementById(spanId);
            const doorElement = document.getElementById(doorId);
    
            // Verifica se o elemento span existe antes de tentar preenchê-lo
            if (spanElement) {
                // Preenche o conteúdo do span com o número da sala
                spanElement.textContent = numeroSala;
                console.log(doorElement.className)

                if (item.reservado == 'Sim') {
                    // Se estiver reservado, adicione uma classe especial à linha do span
                    doorElement.className = 'seat occupied'
                } else {
                    // Se não estiver reservado, remova a classe especial da linha do span (se existir)
                    doorElement.className = 'seat'
                }
            }
        });
    })
    .catch(error => console.error('Erro na solicitação:', error));

};

//Swal.fire({
//    title: 'Título do Alerta',
//    text: 'Conteúdo do Alerta...',
//    icon: 'warning', // Ícone do alerta (success, error, warning, info, question)
//    confirmButtonText: 'OK'
//});
//
//assento.addEventListener('click', function() {
//    if (assento.classList.contains('select')) {
//        Swal.fire({
//            title: 'Assento Selecionado',
//            text: 'Você selecionou este assento.',
//            icon: 'success',
//            confirmButtonText: 'OK'
//        });
//    }
//});