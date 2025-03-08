Professors Rating Service - Client Application

Required package

    pip install requests

Instructions for using the Client

Commands:
1. register
    - Register a new user with the service
    - No arguments needed
    - You will be prompted to enter a username, email, and password

2. login <url>
    - Log in to the service
    - Required argument: url (e.g, scxxyyyy.pythonanywhere.com)  
    - Use your student ID to replace scxxyyyy
    - You will be prompted to enter username and password

3. logout
    - Log out from the current session
    - No arguments needed

4. list
    - View a list of all module instances and the professor(s) teaching them
    - No arguments needed

5. view
    - View the rating of all professors
    - No arguments needed

6. average <professorID> <module_code>
    - View the average rating of a specific professor in a specific module
    - Required arguments:
        > professorID (e.g, JE1)
        > module_code (e.g, CD1)

7. rate <professorID> <module_code> <year> <semester> <rating>
    - Rate the teaching of a specific professor in a specific module instance
    - Required arguments:
        > professorID (e.g, JE1)
        > module_code (e.g, CD1)
        > year (e.g, 2018)
        > semester (e.g, 1 or 2)
        > rating (a number from 1 to 5)

8. help
    - Display help information for all Commands
    - No arguments needed

9. exit or quit
    - Exit the client application
    - No arguments needed

PythonAnywhere Domain
sc22mibs.pythonanywhere.com

Admin Account Details
Username: ihtisyam
Password: Shahrulnizam123

Additional Information
    - You must register and log in before you can rate professors
    - The rating scale is from 1 to 5, where 1 is the lowest and 5 is the highest rating
    - All data filteration and calculations are performed on server side
    - The client application simply displays data returned by the server and check login validation