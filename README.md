
# Todo App API - CSoC Dev Task 3

## Introduction

Welcome to the Week 3 of CSOC Dev. In this assignment, you will be working on the Django Rest Framework. You will be implementing the same api server which we created for you in the task 1.


### Setting up the project

- Make sure `python3.7` and `pip` are installed. Install `pipenv` by running `pip install pipenv`.
- Install python dependencies using the command `pipenv install` Please use only pipenv for managing dependencies (Follow this [link](https://realpython.com/pipenv-guide/) if you are new to pipenv).
- To activate this project's virtualenv, run `pipenv shell`.
- Run `python manage.py migrate` to apply migrations.
- Start the development server using `python manage.py runserver`

### Working
The working of the api server was explained in the task 1 itself.

You'll have to add two things
- In the `/todo/create` endpoint there was just an empty `200 RESPONSE`, you'll have to return the task details also.
- Collaborator feature - In this you'll need to create a feature where a person can add, remove collaborators to a task. A collaborator when calls the `todo` endpoint. He must get the tasks he is collaborator of. He would have the access of editing and deleting the todo. But would not have the access to add more collaborators to the todo. Make the necessary endpoints.

## Tasks
- ### Complete all the basic endpoints (100 points)
- ### Collaborator feature (100 points)

## Deadline
You'll have a week to complete this task. Hence, the deadline of this task is 14th May, 2020.

## Submission
* Follow the instructions to setup and run this project.
* Complete the task by making the required changes in the files.
* When done, commit your work locally and push it to your origin (forked repository).
* Make a pull request to our repository, stating the tasks which you have completed.
* Let us review your pull request.
