# Database project (TSOHA) - University of Helsinki

## Introduction
This is a database project for the course Tietokannat ja Web-ohjelmointi 2024 (TSOHA) at University of Helsinki. The project is a web application that represents a simple fictional game award competition. A signed up and logged in user can vote for a game and also participate in a discussion about a game. The project is written in Python and uses Flask framework. The database is implemented with PostgreSQL.

## How to get started
### Requirements
1. Python 3.6 or newer
2. PostgreSQL
3. Virtual environment (optional)

### Installation
1. Clone the repository
2. Navigate to the root folder of the project
3. Create .env file with the following content:
```
    DATABASE_URL=<your-database-local-address>
    SECRET_KEY=<your-secret-key>
```
4. Create a virtual environment with the command `python3 -m venv venv`
5. Activate the virtual environment with the command `source venv/bin/activate`
6. Install the dependencies with the command `pip install -r requirements.txt`
7. Create the database with the command `psql < schema.sql`
8. Restart terminal and activate the virtual environment again with the command `source venv/bin/activate`
9. Run the application with the command `flask run`
10. Open the application in your browser at the address `http://localhost:5000/`

### Testing
1. Try creating couple users by signin up in the upper right corner of the home page
2. Try voting and unvoting a game and see how the top 3 games changes in the home page
3. Try to open a games details by clicking `Read more` button and write a comment for the game
4. Try liking a comment if there are any
5. Try to logout and login with another user

## Database structure
### Database tables in this project
- games
- users
- gamevotes
- messages
- messagelikes

### Diagram
![Database structure](/images/db_structure.png)
Image created via [dbdiagram](https://dbdiagram.io/home) 
