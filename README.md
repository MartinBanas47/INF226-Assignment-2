
# Oblig 2A:

## Refactor and improve the code – see the Secure by Design book for tips, document your choices in README.md
Considering the state of the app and purpose of what we should do, we decided to write the app from the scratch. We found it better to learn by creating a new app rather than refactoring the existing app and potentially missing an important functionality of the application. However, we decided to move a lot of the code into separated folders, such as templates, DTOs and forms. This should improve readability of the application. We used a database to persist information such as application data. We decided to do following changes in structure than it was chosen in original app:
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

* 'Reply' is a feature that is possible while user is looking at the message page, user can response to the received message, if the message was sent to more participants, response will be sent to every original receiver and to previous sender. 

* 'Create a message' page, user can send a message to one or more recipients with his message.

* 'Log out' button, will log out the current signed-in user and will end his session. 


## Instructions on how to test/demo it
* Clone the repository.

* Get all the required libraries.

* Run the app.

* Register test users, because database will be empty after first run. (It creates itself if it does not exist)

* Create messages. For more recipients, use seperator ';' between their names, e.g. user1;user2 


## Technical details on the implementation
* ORM framework: SQLAlchemy

* The database used to persist information: SQLite

* The framework used to run the app: Flask

* The package used for creating of the forms: Flask-WTF and WTForms

* The package used for salting and hashing passwords: BCrypt

* The package used for authentication and authorization: Flask login



## Threat model – who might attack the application? What can an attacker do? What damage could be done (in terms of confidentiality, integrity, availability)? Are there limits to what an attacker can do? Are there limits to what we can sensibly protect against?

### Who might attack the application?
* Person who wants to get information from messages inside the application
* Person who wants to send false information to other user
* Person who wants to benefit from application not working
* Person who wants to get personal information about users
* Person who would get any type of profit from the attack

### What can an attacker do?
* He can gain access to other users accounts and/or messages
* He can send messages as if they were from someone else
* He can shut down the app
* He can gain access to personal information about users

### What damage could be done (in terms of confidentiality, integrity, availability)?
* Messages could be leaked
* Personal information could be leaked
* Website could lose users and profit
* People may get incorrect information which would affect their lives

### Are there limits to what an attacker can do?
* We do not have much information about our users, so he can just get information from messages, steal someone's account, delete users and messages or shut down the app.

### Are there limits to what we can sensibly protect against?
* We can protect the app from most of the well known attacks which may be also discovered by tools such as SonarQube or OWASP ZAP

## What are the main attack vectors for the application?
In cybersecurity, an attack vector is a method of achieving unauthorized network access to launch a cyberattack. Attack vectors allow attackers to exploit system vulnerabilities to gain access to sensitive data, personally identifiable information, and other valuable information accessible after a data breach. For the main attack vectors for the application we consider weak credentials, any forms of injections, SQL injections, cross-site scripting, session hijacking, distributed denial of service(DDoS), brute force, missing or poor encryption.

## What should we do (or what have you done) to protect against attacks?
* SQL injection or other injection - We used ORM, which is design not only to make queries easier to write, but also to prevent SQL injection.
* XSS - We used Flask forms, which use Jinja2 to escape text and should prevent these attacks.
* Man in the middle attack/encryption - would be solved by HTTPS, but we did not want to pay for SSL certificate
* DDoS - Would be solved by server/cloud configuration.
* Session hijacking - Solved by SameSite attribute set as strict in cookie.
* CSRF - Used Flask's CSRF protection package
* Brute force - We added conditions to password creating, so they have to be strong


## What is the access control model?

Access control is a security technique that regulates who or what can view or use resources in a computing environment and do specific functionality of the application. It is a fundamental concept in security that minimizes risk to the business or organization. Access control model is a way how to represent privileges and hierarchy of user inside the application. In software engineering we know two base models of access control. Role-base access control and attribute-based access control. In our application we use attribute-based access control model. In this model subject requests to perform operations on objects are granted or denied based on assigned attributes(relations) of the subject. For example user can see messages in which was stated as a recipient, no other messages.

## How can you know that you security is good enough? (traceability)

We can check security of the app using penetration testing. Having done penetration testing before and after every major release, we can reduce number of security vulnerabilities. Make tests on critical parts of the code, where we can except some kind of injection or another type of the threat. Traceability also helps when vulnerability is found, because it helps us reduce amount of code in which is the problem of the application. It can also prevent developers from making the same mistake over and over by having them check previous mistakes and have them in mind when creating new features or fixing bugs. In the end we tried to secure the application as much as we could, based on a resource and time factor.
