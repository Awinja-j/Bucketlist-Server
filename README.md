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
 
 ## Endpoints
 
 ### Registration
 *Registers a new user* 
 
 **method**
 
 POST 
 
  **URL**
  
 `/auth/register` 
 
 **Data Params**
 
 **Success Response**
 
 **Error Response**
 
 **Sample Call**
 
 
 
 ### Login
 *Returns authentication token*
 
 **method**
 
 POST  
 
 **URL**
 
 `/auth/login`
  
  **Data Params**
 
 **Success Response**
 
 **Error Response**
 
 **Sample Call**
  
  
 ### Make a new bucketlist
 *Creates a new bucket list*
 
 **method**
 
 POST 
 
 **URL**
 
 `/bucketlists/` 
 
 **Data Params**
 
 **Success Response**
 
 **Error Response**
 
 **Sample Call**
 
 ### Get all bucketlists
 *Lists all the created bucket lists by the user*
 
 **method**
 
 GET 
 
 **URL**
 
 `/bucketlists/` 
 
 **Data Params**
 
 **Success Response**
 
 **Error Response**
 
 **Sample Call***
 
 ### Gets a bucketlists
 *Gets single bucket list using its id*
 
 **method**
 
 GET 
 
 **URL**
 
 `/bucketlists/<id>` 
 
 **Data Params**
 
 **Success Response**
 
 **Error Response**
 
 **Sample Call**
 
 ### Update a bucketlist
 *Updates the title of the bucket list*
 
 **method**
 
 PUT 
 
 **URL**
 
 `/bucketlists/<id>` 
 
 **Data Params**
 
 **Success Response**
 
 **Error Response**
 
 **Sample Call**
 
 ### Delete a bucketlist
 *Deletes a single bucket list using its id*
 
 **method**
 
 DELETE 
 
 **URL**
 
 `/bucketlists/<id>` 
 
 **Data Params**
 
 **Success Response**
 
 **Error Response**
 
 **Sample Call**
 
 ### Make an item
 *Creates a new item in bucket list*
 
 **method**
 POST 
 
 **URL**
 
 `/bucketlists/<id>/items/` 
 
 **Data Params**
 
 **Success Response**
 
 **Error Response**
 
 **Sample Call**
 
 ### Edit/Update an item
 *Updates the title of a bucket list item*
 
 **method**
 PUT 
 
 **URL**
 
 `/bucketlists/<id>/items/<item_id>` 
 
 **Data Params**
 
 **Success Response**
 
 **Error Response**
 
 **Sample Call**
 
 ### Delete an item
 *Deletes an item in a bucket list*
 
 **method**
 DELETE 
 
 **URL**
 
 `/bucketlists/<id>/items/<item_id>`
   
 **Data Params**
 
 **Success Response**
 
 **Error Response**
 
 **Sample Call**


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




