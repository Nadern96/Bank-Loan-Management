# Bank-Loan-Management
Django + Vuetify application to manage bank loans.

## Django + Vuetify


### Docs

* [Project description](https://drive.google.com/file/d/1JEAKSkCglm4wX2_q1uiRjT-RqZrz5NTQ/view?usp=sharing)
* [Database ERD](https://drive.google.com/file/d/1LivaDaP2BsmJnSjdDr0i-SDDe_7rsW4k/view?usp=sharing)

### Includes

* Django
* Django Restframework
* Vue Cli (default configuration)

## Prerequisites

Before getting started you should have the following installed and running:

- [X] Npm        >= 7.5.2  &nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;   [instructions](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [X] Vue Cli    >= 4.5.12 &nbsp;   &nbsp;   &nbsp;  [instructions](https://cli.vuejs.org/guide/installation.html)
- [X] Python     >= 3.7.9
- [X] pip        
- [X] virtualenv 

## Libraries

* amortization (python library to generate the amortization table)

## Setup Template

```
$ git clone https://github.com/Nadern96/Bank-Loan-Management
$ cd Bank-Loan-Management
```

Setup Vue app
```
$ cd frontend/
$ npm install
```

Setup Django app

```
$ cd backend/
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt 
$ python3 manage.py migrate
```

## Running Development Servers

```
$ python3 manage.py runserver
```

Inside frontend directory

```
$ npm run serve
```

