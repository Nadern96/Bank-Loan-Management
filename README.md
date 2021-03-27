# Bank-Loan-Management
Django + Vuetify application to manage bank loans.

## Django + Vuetify


### Video Demo


### Includes

* Django
* Django Restframework
* Vue Cli 3 (default configuration)

## Prerequisites

Before getting started you should have the following installed and running:

- [X] Npm - [instructions](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [X] Vue Cli 3 - [instructions](https://cli.vuejs.org/guide/installation.html)
- [X] Python
- [X] pip - $ sudo apt-get install python3-pip

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
$ pip install -r requirements.txt 
$ python manage.py migrate
```

## Running Development Servers

```
$ python manage.py runserver
```

Inside frontend directory

```
$ npm run serve
```
