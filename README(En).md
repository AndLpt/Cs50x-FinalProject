# CS50X - NOTE KEEPING web app with Flask

# Video demo: https://www.youtube.com/watch?v=KoBVqtJ_5zE

# Description
This is my final project for Harvard's Cs50x course. I designed this web app to help students whose schools do not offer a grade retention platform. They can therefore keep all their grades in one place and have easy access to them. It has been design to make data manipulation by users as easy as possible.  In a few clicks users can add, delete or modify data associated with them and the update is made immediately afterwards. Once they are logged in, users also have access to a search bar that allows them to quickly get information about a particular course they have already registered.

## Final project architecture
- **Flask session**

- **static**
  - fichier.js
  - IMG_0535.pdf
  - mahbod-akhzami-Fe3xy9C9wow-unsplash.jpg
  - note.png
  - pexels-jess-bailey-designs-743986.jpg
  - style.css
- **templates**
  - grades.html
  - index.html
  - layout.html
  - login.html
  - passwordchanging.html
  - register.html
  - settings.html
- **app.py**
- **helpers.py**
- **README.md**
- **requirements.txt**
- **users.db**

## **Tools used** : Python, Flask, SQLite3, Bootstrap, HTML, Jinja2, CSS, JavaScript

## Frontend/ client side
Once they have created their account and logged in, users will be able to carry out several actions thanks to an ordered succession of pages contained **templates**:
* **layout.html** it is the main page of which the others are extensions.
* **register.html** allows the creation of an account.
* **login.html** implements the opening of a session for registered users, and also allows them to request a password change
* **passwordchanging.html** is the page where users can change their password when they no longer remember it. It therefore doesn't require them to be logged in. However they must answer the security questions correctly.

  **To have access to the following pages, the user needs to be logged in. Whatever page the user is on, they can see their data on the left column**
* **index.html** is the homepage where users can add or delete a year associated with them.
* **grades.html** is the page where users can add or delete a course. They have to choose a year and a semester for more accuracy. They can add as much courses as they want because the application is designed to be extensible.
* **settings.html** on this page users can change their answers to the security questions as well as their password.
* **results.html** is the page that handles users' requests.

## Backend/ server side
Each user-side action triggers a server-side reaction. I made sure to cover as many scenarios as possible using **app.py** and **helpers.py** files. **app.py** is the heart of the project and controls almost all server-side reactions thanks to the routes implemented via a python code. While **helpers.py** is a file where I stored custom made functions used to help run my server. Thanks to these two files I can implement the following actions:
* Control how users create accounts and log into the application.
* Define conditions that have to be met to trigger specific changes.
* The response to a user's query to a database only accessible on the server side.
* Mechanisms that allow me to select and manipulate data related to a specific user.
* The order of operations when modifying my database and how to do so.
* Managing the opening and closing of a session.
* Updating the database when necessary.

## Database structure
I designed a database to manage the storage and restrivial of users' data. **All the tables in this database can be extended according to users' needs.**
![databasestructure](/FinalProject/static/IMG_0535-1.png)

# Ways to improve the webapp
When designing this application, I set myself realistic goals in terms of my knowledge and within the timeframe I gave myself. And so, several points can and will be improved in the future.
- Given that users can add as many subjects and exams as they like, implementing a way of deleting empty columns in the event of grades being withdrawn would result in a database that take up less storage.
- Enhance the application's visual style using CSS to create a more user-friendly interface.
- Improve deletion options, in particular by allowing users to delete only certain exams from certain courses.
- The overall user experience can be enhanced by using Ajax to limit page refreshes during client/server exchanges.
