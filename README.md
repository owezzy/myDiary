# myDiary

This is an online journal where users can pen down their thoughts and feelings.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
clone the repository:  
    
    git clone https://github.com/owezzy/myDiary.git

Create a python virtual environment, `cd` to repository root directory and run the following two commands:
 ```
python3 -m venv vevn

source /venv/bin/activate
```
The above creates a virtual environment `vevn` and activates it.

### Installing

Install the required packages by the app:

```
pip3 install -r requirements.txt
```

Export Flask Environments:

```
$ export FLASK_APP = app.py
```
To enable debug mode you can export the FLASK_DEBUG environment variable before running the server:

```$ export FLASK_DEBUG=1```




Then run the application:

```$ flask run```


## Built With

* [Flask](http://flask.pocoo.org/docs/0.12/quickstart/) - The web framework used
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) -  an extension for Flask that adds support for quickly building REST APIs.
* [Marshmallow](https://marshmallow.readthedocs.io/en/3.0/) - A python ecosystem that has many great libraries for data formatting and schema validation
* [Pytest]() - pytest is a mature full-featured Python testing tool that helps you write better programs.
## Authors

* **Owen Adira** 
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* owen_adira

##### checkout a live preview of the app [here](https://owezzy.github.io/myDiary/)
