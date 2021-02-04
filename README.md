# aprepi-django

## Configurações em Ambiente Local

### Pré-requisitos
Para rodar este projeto no modo de desenvolvimento, você vai precisar de um ambiente com Python 3.8.x
instalado.

### Instalação
1. Clone o repositório e entre na pasta:
```shell
$ git clone https://github.com/MikaelSantilio/aprepi-django.git

$ cd aprepi-django
```

2. Crie um ambiente virtual:
```shell
$ python3.8 -m venv <virtual env path>
```

3. Ative o ambiente virtual que você acabou de criar:
```shell
$ source <virtual env path>/bin/activate
```

4. Instale os pacotes de desenvolvimento local:
```shell
$ pip install -r requirements.txt
```

5. Defina as variáveis de ambiente a seguir:
```shell
export DEBUG=True
export TOKEN_MERCADO_PAGO=<TOKEN_MERCADO_PAGO>
```
> **Para ajudar com as configurações das variáveis de ambiente, você tem algumas opções**:
> - Crie um arquivo `.env` na raíz do seu projeto e defina todas as variáveis necessárias dentro dele. Então você so precisa ter `DJANGO_READ_DOT_ENV_FILE=True` em sua máquina e todas as variáveis serão lidas.
> - Use um gerenciador de ambientes como o [direnv](https://direnv.net/)
> **Para obter um token válido do Mercado Pago acesse o link**
> https://www.mercadopago.com.br/settings/account/credentials
> OBS: O token utilizado pode ser o de testes 

6. Execute as migrações:
```shell
$ python manage.py migrate
```

7. Rode o servidor de desenvolvimento:
```shell
$ python manage.py runserver 0.0.0.0:8000