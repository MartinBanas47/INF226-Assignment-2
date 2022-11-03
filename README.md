
# Oblig 2A:

## Refactor and improve the code – see the Secure by Design book for tips, document your choices in README.md
Considering the state of the app and purpose of what we should do, we decided to write the app from the scratch. We found it better to learn by creating a new app rather than refactoring the existing app and potentionally missing an important functionality of the application. However, we decided to move a lot of the code into seperated folders, such as templates, DTOs and forms. This should improve readibility of the application. We used a database to persist information such as application data. We decided to do following changes in structure than it was chosen in original app:
1) The most of the app had to stay in the app.py file, because of the circular imports. Therefore, we moved all supplement parts to other files and group them in packages.
2) First were Repositories. This design pattern includes all queries and help to remove duplicate code from application. It is also helpful in case, we want to change type of storage. In that case we just rework repositories, which are layer between database and application logic.
3) In instances folder are files such as database or logs, which are not code files, but storage.
4) Templates include all html files as it is in login-server. However not all templates are there, which may cause confusion.
5) Utility functions are in Utility package to remove duplicate code. We have there validation utility, which helps in case we want to change validation rules.
6) Forms which are used in html templates are also grouped together in package to make app.py more readable.
7) Data transfer objects, which are used to send just data that is necessary to user. This way we do not give away data we do not want.
8) We did not use static files such as icon (we did not think it was appropriate for messaging app) we would put it to a folder named static.

This way we reduced number of files outside the directories which helps when we need to search for bugs. It also massively reduced duplicate code, which prevents bugs being repaired only in part of the code, instead of resolving it everywhere by just fixing it in one place.


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
In cybersecurity, an attack vector is a method of achieving unauthorized network access to launch a cyber attack. Attack vectors allow atackers to exploit system vulnerabilities to gain access to sensitive data, personally identifiable information, and other valuable information accessible after a data breach. For the main attack vectors for the application we consider weak credentials, any forms of injections, SQL injections, cross-site scripting, session hicjacking, distributed denial of service(DDoS), brute force, missing or poor encryption.

## What should we do (or what have you done) to protect against attacks?
TODO -> zalezi ake vypiseme


## What is the access control model?
TODOOOO

## How can you know that you security is good enough? (traceability)

We can check security of the app using penetration testing. Having done penetration testing before and after every major release, we can reduce number of security vulnerabilities. Make tests on critical parts of the code, where we can except some kind of injection or another type of the threat. Traceability also helps when vulnerability is found, because it helps us reduce amount of code in which is the problem of the application. It can also prevent developers from making the same mistake over and over by having them check previous mistakes and have them in mind when creating new features or fixing bugs.
TODOOOOO
