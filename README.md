# CPSC 471 Project - Group 28

## Frontend

The front end is created using React JS and it can be installed and run locally.

### Prerequisites
Before getting started, you need to have the following software installed on your machine:
- Node.js
- npm (Node Package Manager)
- git

### Installation

To install the application, follow these steps:

- Clone this repository to your local machine (i.e ```git clone...```)
- Navigate to the ```web``` folder
- Run ```npm install``` to install all the required dependencies

### Running the Application

To run the application, follow these steps:

- Ensure you are in the ```web``` folder
- Run ```npm start``` to start the application.
- Open a web browser and go to http://localhost:3000 to view the application

## Backend

The backend is created using Python3 and Postgres, and it can be installed and run locally, we used Ubunutu to configure and build the database

## Prerequisites 
Before getting started, Postgres needs to be installed locally, to do so on Ubuntu: 

`sudo apt-get install postgres postgres-contrib`

The an admin role has to be added to the db, to do this, become the postgres user using:

`sudo su postgres` 

Next, get into the psql shell with the following command: 

`~$ psql`

To create a user, do: 

`CREATE USER admin WITH PASSWORD '123';`
`ALTER USER admin WITH SUPERUSER;` 

By doing this, the database should be configured correctly with how it is set up the in code. 

## Create Tables
The tables can be created locally by running the `python3 create_tables.py` located in /server/dbfunctions
running this file will create the databases required for this project

After this, everything in the database should be configured, to run the main database routine to scrape ads from websites, run `python3 server_main.py`

