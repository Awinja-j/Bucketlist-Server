# Bucketlist API
## Introduction

According to Merriam-Webster Dictionary, a Bucket List is a list of things that one has not done before but wants to do before dying.
This is an API for an online Bucket List service using Flask.

## Requirements

The building blocks used are:
  1. python version 3.6
  2. Flask
  3. PostgresSQL

## Installation

 The following set of steps are necessary to facilitate running the application locally:

   - clone the following repo
        `https://github.com/Awinja-Andela/Bucketlist-Server.git`
        
   - cd into `Bucketlist-Server` and create a VirtualEnvironment using the following command:
        `virtualenv <name_of_env>`
   - To activate the virtualenv, cd into the `<name_of_env>/bin/` and use the following command:
        `source activate`
   - To install all app requirements
        `pip install -r requirements.txt`
   - Create the database and run migrations
   
        `$ python manage.py db init`

        `$ python manage.py db migrate`

        `$ python manage.py db upgrade`

 __You are now set!__
 you can now run the server using `python manage.py runserver` command
 
* POST  `/auth/login` Logs a user in
* POST `/auth/register` Register a user
* POST `/bucketlists/` Create a new bucket list
* GET `/bucketlists/` List all the created bucket lists
* GET `/bucketlists/<id>` Get single bucket list
* PUT `/bucketlists/<id>` Update this bucket list
* DELETE `/bucketlists/<id>` Delete this single bucket list
* POST `/bucketlists/<id>/items/` Create a new item in bucket list
* PUT `/bucketlists/<id>/items/<item_id>` Update a bucket list item
* DELETE `/bucketlists/<id>/items/<item_id>`  Delete an item in a bucket list

## Pagination

users can specify the number of results they would like to have via a GET parameter limit. 
The default number of results is 20 and the maximum number of results is 100.

#### Sample Request

`GET http://localhost:5000/bucketlists?limit=20`

#### Response
20 bucket list records belonging to the logged in user.


## Searching by Name
searching for bucket lists based on the title using a GET parameter q.

#### Sample Request

`GET http://localhost:5555/bucketlists?q=bucket1`

#### Response
Bucket lists with the string “bucket1” in their name.




