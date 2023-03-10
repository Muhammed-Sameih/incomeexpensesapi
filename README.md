# Incomes Expenses API

<details>
<summary>Table of content</summary>

- [Description](#description)
- [Features ✨](#features-)
- [Project structure](#project-structure)
- [Installation 📥](#installation-)
- [Tech/Framework used 🧰](#techframework-used-)
- [Deployment/Live Demo](#deploymentlive-demo)
</details>

## Description

Welcome to our expenses and incomes management project! This project is designed to help users keep track of their financial transactions by allowing them to log in and perform CRUD (Create, Read, Update, Delete) operations on their expenses and incomes.

## Features ✨

1. User-centric system: This system is designed specifically to serve the needs of individuals who want to track their expenses and incomes.

2. Secure login system: Users are required to sign up and log in using their email and password before they can access the system.

3. Expense and income entry: Users can easily enter their expenses and incomes into the system, making it simple to keep track of all financial transactions.

4. CRUD operations: The system allows users to manipulate their expenses and incomes using Create, Read, Update, and Delete operations. This means users can easily edit or delete transactions as needed.

5. Statistics calculation: The system calculates user statistics for incomes and expenses over the last year. This provides users with valuable insights into their spending habits and helps them make more informed financial decisions.

### Authentication Details:

1. User can sign up and log in using two ways of authentication:
   a. Normal Authentication
   b. Social Authentication

2. User can sign up by entering the following information:
   a. Email
   b. Username
   c. Password
   d. Mobile Number

3. User can log in by using the following information:
   a. Email
   b. Password

4. User can change his password.

5. To maintain security, the user must verify their account within 30 days after signing up. If the user fails to verify their account, they will become unauthorized. However, the user can request a verification email to be sent to them.

## Project structure

<details>
<summary>Click to expand!</summary>

```bash
## Project Structure

├── authentication
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── renderers.py
│   ├── serializers.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_model.py
│   │   ├── test_setup.py
│   │   └── test_views.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── expenses
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── incomeexpensesapis
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── incomes
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
├── social_auth
│   ├── admin.py
│   ├── apps.py
│   ├── facebook.py
│   ├── google.py
│   ├── __init__.py
│   ├── models.py
│   ├── register.py
│   ├── serializers.py
│   ├── tests.py
│   ├── twitterhelper.py
│   ├── urls.py
│   └── views.py
└── userstats
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py



```

</details>

## Installation 📥

#### Clone Project

```bash
git clone https://github.com/Muhammed-Sameih/incomeexpensesapi.git
cd incomeexpensesapi
git checkout main
rm -rf .git
git init .
git branch [branch-name] # make it descriptive
git add [file]  # individual commits for each file are prefered
git commit -m "Your Commit Message"
```

### Create virtual environment and activate it

```bash
python -m venv venv
source venv/bin/activate
```

Use `.\venv\Scripts\activate` if on windows

### Install requirements

### Give Permissions to build_env.sh file

```bash
chmod +x build_env.sh
sudo ./build_env.sh
#################### OR ###################
(venv) python -m pip install pip --upgrade
(venv) python -m pip install -r requirements.txt
```

### Open VSCode & Start Coding

```bash
cd /path/incomeexpensapi
code .
```

## Tech/Framework used 🧰

- [Django framework](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Git](https://git-scm.com/)
- [Django REST Swagger](https://django-rest-swagger.readthedocs.io/en/latest/#django-rest-swagger)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [Facebook Business SDK for Python](https://github.com/facebook/facebook-python-business-sdk)
- [python-twitter’s](https://python-twitter.readthedocs.io/en/latest/)
- [Google API Client](https://github.com/googleapis/google-api-python-client)
- [VSCode](https://code.visualstudio.com/)

## Deployment/Live Demo

Deployed Website: [income expenses api]()
