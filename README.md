# Bot Discord Easy Creator

### Sobre:
Bot Discord Easy Creator ou BDEC, tem o objetivo de ser um software gratuito pra criação de bots no Discord.

### Como iniciar (Passo a passo):
#### 1. Passo (Instalando bibliotecas):

##### Dependencias:
###### Linguagens:
* Python 3
###### Bibliotecas Python:
* Discord
* Emoji

##### Instalação:
Abra o console (cmd) e digite:
```
pip install discord
pip install emoji
```

#### 2. Passo (Inserindo o token)
Após você ter instalado as dependencias, oque você precisa fazer é copiar o token do seu bot e inserir no arquivo config.json entre as "" áspas, por exemplo:
```
{"token":"<seu token>"}
```
#### 3. Passo (Iniciando)
Inicie o 'main bot.py' pelo console usando ou usando uma IDE de sua preferencia
```
python 'main bot.py'
```
### Customizando o bot:
Você pode customizar as mensagens do bot a sua maneira, usando o arquivo json 'message and reply.json'.
a primeira chave (Example) é nome da sua mensagem (o nome da mensagem não altera nada) dentro dessa chave de deve haver outras chaves mas **apenas a chave 'expected message' é obrigatoria**, 'reply' é a resposta do bot e 'expected message' é a mensagem que ele espera, por exemplo:

###### Exemplo:
```
{"Example":{ <- Nome da sua mensagem
    "expected message":"ola", <- Mensagem esperada
    "reply":"oi"} <- Resposta do bot
}
```
###### Usando reações:
Para usar reações é muito simples, você deve inserir o codigo do emoji na chave reaction, para descobrir os codigos dos emojis acesse [Emoji]('https://www.webfx.com/tools/emoji-cheat-sheet/') **(obs: não são todos os emojis presentes no site que funcionam)**, exemplo de como usar:
```
{"Example":{
    "reaction":":simple_smile:"}
}
```
###### Usando multiplas respostas:
Usando multiplas respostas o bot ira enviar varias respostas. exemplo de como usar:
```
{"Example":{
    "multi reply":["Mensagem 1","Mensagem 2"]}
}
```
###### Usando respostas aleatorias:
Para usar mensagens aleatorias, você deve inserir uma lista nas chaves que tem suporte a respostas aleatorias, chaves que tem suporte:
* reply
* reaction
* multi reply

```
{"Example":{
    "reply":["Mensagem 1", "Mensagem2", "Mensagem3"]
    "reaction":[":cry:",":smile:",":laughing:"]
    "multi reply":[["Mensagem 1", "Mensagem2", "Mensagem3"],["Mensagem 4", "Mensagem5", "Mensagem6"]]
}}
```

Entre os items da lista o bot ira escolher um de forma aleatoria.

### Notas
O repositorio ainda não está completamente desenvolvido então muitas coisas podem mudar.