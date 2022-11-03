
# Oblig 2A:

## Refactor and improve the code – see the Secure by Design book for tips, document your choices in README.md
Considering the state of the app and purpose of what we should do, we decided to write the app from the scratch. We found it better to learn by creating a new app rather than refactoring the existing app and potentionally missing an important functionality of the application. However, we decided to move a lot of the code into seperated folders, such as templates, DTOs and forms. This should improve readibility of the application. We used a database to persist information such as authentication data and application data.




# Oblig 2B

## Application details, features
Here are the pages of the application with brief description:

* 'Welcome page' with navigation to the most important pages.

* 'Registration page' to create a new account. Registration requires a username, which has to be unique in a system and include only alphanumeric characters, and password. For storing the password we hash the salted password using library Bcrypt. Password may contain special characters to allow users creating stronger passwords. 

* 'Login' page, where we check the password and use validation of username to match the one on the registration page. If user authenticate successfully, he gets session ID which he then uses for authorization using library Flask login.

* After successful authorization user can see all messages for him on page 'Messages page'. Every message has information about it and link to message detail.

* 'Message page' shows detail of the message. 

* 'Reply' is a feature that is possible while user is looking at the message page, user can response to the received message, if the message was sent to more participants, response will be send to every original receiver and to previous sender. 

* 'Create a message' page, user can send a message to one or more recipients with his message.

* 'Log out' button, will log out the current signed in user and will end his session. 


## Instructions on how to test/demo it
* Clone the repository.

* Get all the required libraries.

* Run the app.

* Register test users, because database will be empty after first run. (It creates itself if it does not exist)

* Create messages. For more recipients, use seperator ';' between their names, e.g user1;user2 


## Technical details on the implementation
* ORM framework: SQLAlchemy

* The database used to persist information: SQLite

* The framework used to run the app: Flask

* The package used for creating of the forms: Flask-WTF and WTForms

* The packege used for salting and hashing passwords: BCrypt

* The package used for authentication and authorization: Flask login



## Threat model – who might attack the application? What can an attacker do? What damage could be done (in terms of confidentiality, integrity, availability)? Are there limits to what an attacker can do? Are there limits to what we can sensibly protect against?

## What are the main attack vectors for the application?
TODO -> mozem skopirovat https://www.upguard.com/blog/attack-vector

## What should we do (or what have you done) to protect against attacks?
TODO -> zalezi ake vypiseme

## What is the access control model?
TODOOOO

## How can you know that you security is good enough? (traceability)

We can check security of the app using penetration testing. Having done penetration testing before and after every major release, we can reduce number of security vulnerabilities. Traceability also helps when vulnerability is found, because it helps us reduce amount of code in which is the problem of the application. It can also prevent developers from making the same mistake over and over by having them check previous mistakes and have them in mind when creating new features or fixing bugs.
TODOOOOO
