# Data Science & Analytics (Analytics Portal)

---

## Setup & Execute

---

#### Environment Setup

Before moving to the project initialization we need complete prerequisite requirements.

- Install [python](https://www.python.org/downloads/).
- Install [mysql](https://www.mysql.com/downloads/).
- Install [docker](https://docs.docker.com/engine/install/).

Setup environment `setting.ini` in the project folder.

```md
- Create `.env` file.
- Copy content of `local.env` file to `.env` file.
- Update `.env` value with the required parameters. 
```

#### Execute

Start application on local system:

```sh
git clone <repo-link>
cd DSA-AP-Backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver 127.0.0.1:8010
```

Migrate database schema to database:

````sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
````

Start application using docker/docker-compose:

```sh
git clone 
cd DSA-AP-Backend
docker build –t DSA-AP-Backend:latest
docker run -p 80:8010 DSA-AP-Backend
```

Link for application [http://127.0.0.1:8010](http://127.0.0.1:8010).

## Architecture

---

Please open the [this]() file in draw.io (web/system.

#### Project Structure

#### Add new Application

```sh
 python manage.py startapp app
```

```md
.
├── /assets
└── /src
    ├── /cognitive
    ├── /login
    ├── /management
    ├── /portal
    └── manage.py
```

#### Convert file into Data

Python code used for file conversion to byte data:

````python
with open("../assets/file.ext", "rb") as file:
    data = file.read()
    
print(data)
````

## Contributing & Feedback

---

- Ask a question on [Teams](https://teams.microsoft.com/l/team/***).
- [Request a new feature](***https://***).

## Code of Conduct

---

This project has adopted the [*** Code of Conduct](CODEOFCONDUCT.md), and project resource is available to everyone inside the organization under fair use. For more information see the [project wiki](https://******.visualstudio.com/Data-Science-and-Analytics/_wiki/) or contact [data.analytics@******.com](mailto:data.analytics@******.com) with any additional questions or comments.

## License

---

Copyright (c) *** All rights reserved.
# DSA-AP-Backend
