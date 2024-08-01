feather.replace()

const container = document.querySelector('.container') 

const seats = document.querySelectorAll('.row .seat:not(.occupied) ') 

const count = document.getElementById('count') 

const total = document.getElementById('total') 

const movieSelect = document.getElementById('movie') 


populateUI() 
let ticketPrice = +movieSelect.value; 

//save selected movie index & price 

function setMovieData(movieIndex, moviePrice){ 
localStorage.setItem(' selectedMovieIndex' , movieIndex) 
localStorage.setItem(' selectedMoviePrice' , moviePrice) 
} 

//updating total and count 
function updateSelectedCount(){ 
const selectedSeats = document.querySelectorAll('.row .seat.selected') 





//copy selected seats into array 
//map thru array 
//return a new array index 


const seatsIndex = [...selectedSeats].map( function(seat){ 

return [...seats].indexOf(seat) 

}) 


localStorage.setItem('selectedSeats' , JSON.stringify(seatsIndex)) 

const selectedSeatsCount = selectedSeats.length 

count.innerText = selectedSeatsCount 
total.innerText = selectedSeatsCount * ticketPrice 




} 


// get data from local storage and populate UI 
function populateUI(){ 

const selectedSeats = JSON.parse(localStorage.getItem('selectedSeats')) 

if(selectedSeats!== null && selectedSeats.length >0){ 
seats.forEach((seat, index)=>{ 
if(selectedSeats.indexOf(index)>-1) 
seat.classList.add('selected') 

}) 
} 


const selectedMovieIndex = localStorage.getItem('selectedMovieIndex') 

if(selectedMovieIndex !==null) 
movieSelect.selected = selectedMovieIndex 

} 

//movie select event 

movieSelect.addEventListener('change', e=>{ 
ticketPrice = +e.target.value 
updateSelectedCount() 
}) 

//seat click event 
const seatscontainer = document.querySelector('.seats-container') 

seatscontainer.addEventListener('click', (e) => {
    if (e.target.classList.contains('seat') && !e.target.classList.contains('occupied')) {
        // Alterna a classe do assento entre selecionado e não selecionado
        e.target.classList.toggle('selected');
        
        // Verifica se o assento foi selecionado
        if (e.target.classList.contains('selected')) {

            const username = parametrosURL.get('username');
            var urlGetSalaInfo = 'http://localhost:5000/get_sala_info';
            var id = e.target.id.slice(-1);
            var idSpan = 'span'+ id;
            var idSpanValue = document.getElementById(idSpan).textContent;
            console.log(idSpanValue)

            var data = {
                Sala: idSpanValue
              };
        
            // Quando a página carregar, faça uma solicitação ao endpoint do Flask
            fetch(urlGetSalaInfo, {
              method: 'POST',
              //credentials: 'include',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(response => {
                var numeroSala = response[0].numeroSala
                var capacidadeSala = response[0].capacidadeSala
                var refrigeracaoSala = response[0].refrigeracaoSala
                // Abre o popup apenas se o assento estiver selecionado
                Swal.fire({
                    title: 'Sala ' + numeroSala + ' selecionada',
                    html: '<p>Capacidade: '+ capacidadeSala + '</p><p>Refrigeração: ' + refrigeracaoSala +'</p>',
                    icon: 'warning',
                    input: 'password',
                    inputPlaceholder: 'Digite sua senha para confirmar a reserva',
                    showCancelButton: true,
                    confirmButtonText: 'OK',
                    preConfirm: function(password) {
                        // Ação a ser realizada quando o usuário clica em OK
                        console.log(username)
                        var urlVerificaSenha = 'http://localhost:5000/Verifica_senha'; 
                        var secret = {
                            senha: password,
                            username: username
                          };
                    
                        // Quando a página carregar, faça uma solicitação ao endpoint do Flask
                        fetch(urlVerificaSenha, {
                          method: 'POST',
                          //credentials: 'include',
                          headers: {
                              'Content-Type': 'application/json'
                          },
                          body: JSON.stringify(secret)
                        })
                        .then(response => response.json())
                        .then(response => {
                            var secret = response.mensagem
                            console.log(secret)
                            if (secret === 'True') {
                                // Se a senha for correta, execute a função
                                var inputHour = document.getElementById('hour');
                                var inputCalendario = document.getElementById('calendario');

                                var dataConsult1 = inputCalendario.value;
                                var partesData = dataConsult1.split('/');
                                var dataConsult = new Date(partesData[2], partesData[1] - 1, partesData[0]);

                                var hourConsulta1 = inputHour.value;
                                var hourConsulta = hourConsulta1.split(':'); 
                                var horaConsulta = hourConsulta[0]+ ':00:00'

                                var mesConsulta = ('0' + (dataConsult.getMonth() + 1)).slice(-2);
                                var diaConsulta = ('0' + dataConsult.getDate()).slice(-2);
                                var anoConsulta = dataConsult.getFullYear().toString().slice(-4);

                                var dataConsulta = anoConsulta + '-' + mesConsulta + '-' + diaConsulta;
                                console.log(dataConsulta)

                                console.log(password);
                                var urlReservaSala = 'http://localhost:5000/reserva_Sala'; 
                                var data = {
                                    dataConsulta: dataConsulta,
                                    horaConsulta: horaConsulta,
                                    sala: idSpanValue,
                                    username: username
                                  };
                              
                                // Quando a página carregar, faça uma solicitação ao endpoint do Flask
                                fetch(urlReservaSala, {
                                  method: 'POST',
                                  //credentials: 'include',
                                  headers: {
                                      'Content-Type': 'application/json'
                                  },
                                  body: JSON.stringify(data)
                                })
                                .then(response => response.json())
                                .then(response => {
                                    var response = response.mensagem
                                    if (response === 'True') {
                                        alert('Sala Reservada');
                                    } else {
                                        alert('Sala já reservada ou ocorreu um erro ao reservá-la');
                                    }
                                })
                            } else {
                                // Se a senha for incorreta, exiba uma mensagem de erro
                                alert('Senha incorreta!');
                            }
                        })
                    }
                });
            })
        }
        
        // Atualiza o contador de assentos selecionados e o preço total
        updateSelectedCount();
    }
});


//initial count & total set 
updateSelectedCount()