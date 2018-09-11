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
$ export FLASK_APP = app/app.py
```
To enable debug mode you can export the FLASK_DEBUG environment variable before running the server:

```$ export FLASK_DEBUG=1```




Then run the application:

```$ flask run```

Test the API endpoints using Postman:

| Endpoint               |             Functionality    |                          Note                          |
| ----------------------:|:----------------------------:|:------------------------------------------------------:|
| POST /auth/signup      | Register a User              |                                                        |
| POST /auth/login       | Login a User                 |                                                        |
| GET /entries           | Fetch all entries for a user |                                                        |
| GET /entries/<Id>      | Fetch the details of an entry|                                                        |
| DELETE /entries/<Id>   | Delete an entry              |                                                        |
| POST /entries          | Add an entry                 |                                                        |
| PUT /entries/<Id>      |Modify a diary entry          | entry can only be modified the same day it was created |
## Built With
##### Backend-end
* [Flask](http://flask.pocoo.org/docs/0.12/quickstart/) - The web framework used
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) -  an extension for Flask that adds support for quickly building REST APIs.
* [Marshmallow](https://marshmallow.readthedocs.io/en/3.0/) - A python ecosystem that has many great libraries for data formatting and schema validation
* [Pytest](http://doc.pytest.org/en/latest/contents.html) - pytest is a mature full-featured Python testing tool that helps you write better programs.
* [PostgreSQL-10](https://www.postgresql.org/about/news/1786/) - PostgreSQL is a powerful, open source object-relational database system for reliability, feature robustness, and performance.
*[Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io) - 
##### Frontend-end
*[HTML 5]()
*[CSS 3]()
*[Jquery]()


## Authors
* **Owen Adira** 
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* owen_adira

##### checkout a live preview of the app [here](https://owezzy.github.io/myDiary/)
