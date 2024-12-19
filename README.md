![Icon](source/icons/icon.svg)

# Bot Discord Easy Creator

## Sobre:

Bot Discord Easy Creator ou BDEC, é um software gratuito para criação de bots no Discord, com interface interativa capaz
de executar o bot.

## Como iniciar (Passo a passo):

### 1º Passo: Instalando dependências e bibliotecas

##### Linguagens:

* [Python 3](https://www.python.org/downloads/)

##### Bibliotecas Python:

* Discord
* Emoji

#### Instalação:

Abra o cmd e digite:

```
pip install -r requirements.txt
```

Ou execute o arquivo: install dependencies.bat

### 2º Passo: Inserindo o token

Após você ter instalado as dependências, oque você precisa fazer é copiar o token do seu bot e inserir no arquivo
config.yaml entre as "" áspas, por exemplo:

```
token: <seu token>
```

Esse processo pode ser realizado a partir da interface.

### 3º Passo: Iniciando

Abra o cmd e digite:

```
python bot.py
```

## Customizando o bot:

Para customizar seu bot é muito simples, basta executar a interface (main.py)
e de maneira intuitiva você poderá customizar seu bot de diversas maneiras.

### Janela inicial:

Na janela inicial podemos criar, editar, excluir e visualizar as mensagens que configuramos,
podemos também executar o bot e visualizar as mensagens de retorno (logs). Ao clicar no botão de adicionar ou
editar
podemos visualizar nova janela.

### Janela de edição:

Nessa janela podemos criar ou editar uma mensagem, que configura como o bot deve reagir às mensagens enviadas no
servidor ou privado. Agora vamos introduzir como podem ser utilizados os cinco campos de preenchimento:

* Nome: O nome que deseja salvar essa mensagem.
* Mensagem esperada: Mensagem que será utilizada pelas condições de "expected message" e "not expected message", nesse
  campo se tivermos mais de uma mensagem, todas serão enviadas, separando uma mensagem com ¨ podemos definir mensagens
  aleatórias.
* Resposta: São as mensagens que devemos enviar como reposta caso todas as condições forem satisfeitas.
* Reações: O bot irá reagir com todas as reações definidas, lembrando que o limite é de 20.
* Condições: Define condições as mensagens que deverão ser respondidas.

#### Configurando a resposta:

Podemos configurar as "formas" de resposta, como:

* Resposta no grupo ou privada.
* Banimento ou expulsão como resposta.
* Onde serão adicionadas as reações (bot ou usuário).
* Delay na resposta.
* Remover ou fixar a mensagem.

## Implementações futuras:

* Customização de tema da interface.
* Seleção de linguagem da interface.
* Reação e respostas aleatórias.
