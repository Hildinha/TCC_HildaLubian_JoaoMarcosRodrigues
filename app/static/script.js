var btnLogin = document.getElementById('do-login');
var idLogin = document.getElementById('login');
var username = document.getElementById('username');
var password = document.getElementById('password');

btnLogin.onclick = function() {
    var url = 'http://localhost:5000/login'; // Substitua pelo endereço do seu backend

    var data = {
        idLogin: idLogin.value,
        username: username.value,
        password: password.value
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

        if (resposta.mensagem === 'Login bem-sucedido!') {
            // Redirecione para a próxima página se a mensagem for 'Login bem-sucedido!'

            var redirectUrl = "/PagInicial?username=" + encodeURIComponent(username.value);
            window.location.href = redirectUrl;
        } else {
            // Faça outra coisa se a mensagem não for 'Login bem-sucedido!'
            alert('Login Inválido. Por favor, tente novamente.');
        }
    })
    .catch(error => console.error('Erro na solicitação:', error));
};



