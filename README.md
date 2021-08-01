# BookStore App
Django-based bookstore app with Google Books API.

#### Live on Heroku - [Click here](https://bookstore-matt.herokuapp.com/)

## Setup

If you want to run project locally do the following:

```sh
$ git clone https://github.com/mateuszwwwrobel/BookStore.git
$ cd BookStore
```

Create a virtual environment and activate it:

```sh
$ python3 -m venv <venv-name>
$ source <venv-name>/bin/activate
```

Then install the dependencies and add SECRET_KEY env variable:

```sh
(<venv-name>)$ pip install -r requirements.txt
(<venv-name>)$ export SECRET_KEY='your_secret_key_here'
```
Note the `(venv-name)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `venv`.

Once `pip` has finished downloading the dependencies run following commands:
```sh

(<venv-name>)$ python3 manage.py migrate
(<venv-name>)$ python3 manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`


### Dependencies

See requirements.txt file. 

### Running tests

In main directory run command:
```sh
(<venv-name>)$ python3 manage.py test
```

## Acknowledgments

For help with every trouble:
* [Stackoverflow](https://stackoverflow.com/)