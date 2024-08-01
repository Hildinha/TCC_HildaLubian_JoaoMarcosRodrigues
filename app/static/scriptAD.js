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


function exibirOcultarDiv() {
  var select = document.getElementById("option");
  var div1 = document.getElementById("div1"); 
  var div2 = document.getElementById("div2");  
  var div3 = document.getElementById("div3");  
  var div4 = document.getElementById("div4"); 

  if (select.value === "1") {
     div1.style.display = "block"; // Exibe o div se a opção 2 for selecionada
  } else {
     div1.style.display = "none"; // Oculta o div para as outras opções
  }

  if (select.value === "2") {
     div2.style.display = "block"; // Exibe o div se a opção 2 for selecionada
  } else {
     div2.style.display = "none"; // Oculta o div para as outras opções
  }

  if (select.value === "3") {
     div3.style.display = "block"; // Exibe o div se a opção 2 for selecionada
  } else {
     div3.style.display = "none"; // Oculta o div para as outras opções
  }

  if (select.value === "4") {
     div4.style.display = "block"; // Exibe o div se a opção 2 for selecionada
  } else {
     div4.style.display = "none"; // Oculta o div para as outras opções
  }
}

// Adiciona um evento de mudança ao select
document.getElementById("option").addEventListener("change", exibirOcultarDiv);

// Chama a função inicialmente para garantir que o estado inicial do div corresponda à opção selecionada
exibirOcultarDiv();


//Ação Cadastro

var btnCadastro = document.getElementById('confirmCadastro');
var btnCard = document.getElementById('lerCartao');
var idcadastroUser = document.getElementById('cadastroUser');
var idcadastroPass = document.getElementById('cadastroPass');
var idfuncoes = document.getElementById('funcoes');

btnCadastro.onclick = function() {
   var url = 'http://localhost:5000/Cadastro'; // Substitua pelo endereço do seu backend

   var data = {
      idcadastroUser: idcadastroUser.value,
      idcadastroPass: idcadastroPass.value,
   };

   // Use a Fetch API para enviar os dados para o backend
   fetch(url, {
       method: 'POST',
       //credentials: 'include',
       headers: {
           'Content-Type': 'application/json'
       },
       body: JSON.stringify(data)
   })
   .then(response => response.json())
   .then(resposta => {
       // Manipule a resposta do backend aqui
       console.log(resposta);

       if (resposta.mensagem === 'Cadastro bem-sucedido!') {
           // Redirecione para a próxima página se a mensagem for 'Cadastro bem-sucedido!'

           alert('Usuário cadastrado com sucesso.');
       } else {
           // Faça outra coisa se a mensagem não for 'Login bem-sucedido!'
           alert('Login Inválido. Por favor, tente novamente.');
       }
   })
   .catch(error => console.error('Erro na solicitação:', error));
};

btnCard.onclick = function() {
    var url = 'http://localhost:5000/leitura_card'; // Substitua pelo endereço do seu backend
 
    var data = {
       idcadastroUser: idcadastroUser.value,
       idcadastroPass: idcadastroPass.value,
    };
 
    // Use a Fetch API para enviar os dados para o backend
    fetch(url, {
        method: 'POST',
        //credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(resposta => {
        // Manipule a resposta do backend aqui
        console.log(resposta);
 
        if (resposta === 200) {
            // Redirecione para a próxima página se a mensagem for 'Cadastro bem-sucedido!'
 
            alert('Leitura Habilitada');
        } else {
            // Faça outra coisa se a mensagem não for 'Login bem-sucedido!'
            alert('Por favor, tente novamente.');
        }
    })
    .catch(error => console.error('Erro na solicitação:', error));
 };


//Ação Exclusão de Cadastro

var btnExcluirCadastro = document.getElementById('excluirCadastro');
var idexclusaoUser = document.getElementById('exclusaoUser');

btnExcluirCadastro.onclick = function() {
   var url = 'http://localhost:5000/exclusaoCadastro'; // Substitua pelo endereço do seu backend

   var data = {
      idexclusaoUser: idexclusaoUser.value
   };

   // Use a Fetch API para enviar os dados para o backend
   fetch(url, {
       method: 'POST',
       //credentials: 'include',
       headers: {
           'Content-Type': 'application/json'
       },
       body: JSON.stringify(data)
   })
   .then(response => response.json())
   .then(resposta => {
       // Manipule a resposta do backend aqui
       console.log(resposta);

       if (resposta.mensagem === 'Cadastro excluído com sucesso!') {
           // Redirecione para a próxima página se a mensagem for 'Cadastro bem-sucedido!'

           alert('Usuário excluído com sucesso.');
       } else {
           // Faça outra coisa se a mensagem não for 'Login bem-sucedido!'
           alert('Login Inválido. Por favor, tente novamente.');
       }
   })
   .catch(error => console.error('Erro na solicitação:', error));
};


//Ação Reset Cadastro

var btnresetCadastro = document.getElementById('resetCadastro');
var idresetUser = document.getElementById('resetUser');
var idresetPass = document.getElementById('resetPass');

btnresetCadastro.onclick = function() {
   var url = 'http://localhost:5000/resetCadastro'; // Substitua pelo endereço do seu backend

   var data = {
      idresetUser: idresetUser.value,
      idresetPass: idresetPass.value,
   };

   // Use a Fetch API para enviar os dados para o backend
   fetch(url, {
       method: 'POST',
       //credentials: 'include',
       headers: {
           'Content-Type': 'application/json'
       },
       body: JSON.stringify(data)
   })
   .then(response => response.json())
   .then(resposta => {
       // Manipule a resposta do backend aqui
       console.log(resposta);

       if (resposta.mensagem === 'Troca de senha bem-sucedida!') {
           // Redirecione para a próxima página se a mensagem for 'Cadastro bem-sucedido!'

           alert('Senha resetada com sucesso.');
       } else {
           // Faça outra coisa se a mensagem não for 'Login bem-sucedido!'
           alert('Login Inválido. Por favor, tente novamente.');
       }
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