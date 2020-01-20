
# WebServiceInt2Word

O projeto WebServiceInt2Word consiste em um Servidor de requisições HTTP, no qual para cada requisição GET recebida, um JSON deve ser retornado com o valor extenso do número inteiro passado no path da requisição.

O WebServiceInt2Word foi desenvolvido utilizando Python 3, e a construção do Web Service foi feita com o framework Flask.

O intervalo de números que podem ter seu valor escrito por extenso se limita a -99999 até 99999.

## Como rodar o WebServiceInt2Word

Basta abrir um terminal no diretório em que o projeto foi clonado, entrar no diretório src/, e executar a seguinte linha de comando:

```sh
$ python3 server.py
```

O programa será executado, e o Web Service passará a ouvir requisições na porta 3000.

## Enviando requisições para o WebServiceInt2Word

As requisições podem ser enviadas para o Web Service da seguinte forma:

```sh
$ curl http://127.0.0.1:3000/12345
$ curl http://127.0.0.1:3000/-98765
$ curl http://127.0.0.1:3000/15
```

## JSONs de retorno

Caso o número inteiro esteja dentro do intervalo definido de -99999 até 99999, o json de resposta será o seguinte:

> { "extenso": "doze mil e trezentos e quarenta e cinco" }
> { "extenso": "Menos noventa e oito mil e setecentos e sessenta e cinco" }
> { "extenso": "quinze" }

Caso um erro ocorra durante o processamento da requisição ou é enviado no path da requisição um número fora do intervalo permitido, uma resposta de erro será enviada ao usuário requisitante:

> {
&nbsp;&nbsp;&nbsp;&nbsp;   "extenso" : "",
&nbsp;&nbsp;&nbsp;&nbsp;   "mensagem" : "",
&nbsp;&nbsp;&nbsp;&nbsp;   "estado": ""
> }

onde a chave extenso sempre virá vazia (pois não foi possível realizar a conversão), a chave mensagem irá descrever o erro que ocorreu, e o estado será a resposta da requisição (400 Bad Request ou 500 Server Intern Error).

# Rodando os Testes automatizados

O desenvolvimento dos testes automazidados do WebServiceInt2Word foram também desenvolvidos em Python, utilizando o framework Pytest como base.

Para rodar todos os testes automatizados, basta abrir um terminal no diretório onde o projeto foi clonado, entrar no diretório test/, e executar o seguinte comando:

```sh
$ pytest test_int2num.py
```

ou simplesmente:
```sh
$ pytest
```

# Rodando o WebServiceInt2Word através de Docker

Caso não seja apropriado realizar as instalações de pacotes e dependências no ambiente local, o WebServiceInt2Word pode ser inicializado através de um contêiner. Para isso, faz-se necessário construir a sua imagem utilizando Docker, e posteriormente executá-la.

Para esse caso em específico, parte-se do pressuposto que a ferramenta Docker esteja instalada. Caso contrario, o passo a passo da instalação pode ser encontrado [aqui](https://docs.docker.com/install/)

Para isso, basta abrir um terminal no diretório onde o projeto foi clonado, entrar no diretório src/, e executar os seguintes comandos:

```sh
$ docker build -t docker_flask:latest .

$ docker run -d -p 3000:3000 docker_flask:latest
```

As requisições podem ser enviadas para o Servidor através de um terminal, utilizando o comando curl, ou digitando a url em um Browser, por exemplo:

> http://127.0.0.1:3000/10258
