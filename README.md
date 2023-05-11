Find My Ride
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
A web application which uses a description of your stolen/lost vehicle to scrape the web & popular buy-and-sell sites to check if it’s possibly being resold. 

### Contributors
- Jaza Khan
- Sahil Brar
- Peter Kuchel

### Prerequisites
Before getting started, you need to have the following software installed on your machine:
- Python (v3.9 or greater)
- Ubuntu (https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10#1-overview)
- Node.js
- npm
- Firefox (for the webscraper)

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Backend

The backend is created using Python3 and Postgres, and it can be installed and run locally, we used Ubunutu to configure and build the database

## Setup 
Before getting started, Postgres needs to be installed locally, to do so on Ubuntu: 
`sudo apt-get install postgres postgres-contrib`

Run the local server using:
`sudo service postgresql start`

You can verify your postgres server is online with:
`pg_lsclusters`

The an admin role has to be added to the db, to do this, become the postgres user using:
`sudo su postgres` 

Next, get into the psql shell with the following command: 
`psql`

To create a user, do: 
`CREATE USER admin WITH PASSWORD '123';`
`ALTER USER admin WITH SUPERUSER;` 

By doing this, the database should be configured correctly with how it is set up the in code. 

## Create Tables
In the root of the project (local) run the following command to ensure all required modules are installed:
`pip install -r requirements.txt`

The tables can be created locally by running:
`python server/dbfunctions/create_tables.py`
running this file will create the databases required for this project

After this, everything in the database should be configured, to run the main database routine to scrape ads from websites, run:
`python server/server_main.py`

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Frontend

The front end is created using React JS and it can be installed and run locally.

### Installation

To install the application, follow these steps:
- Navigate to the ```web``` folder
- Run ```npm install``` to install all the required dependencies

### Running the Application

To run the application, follow these steps:

- Ensure you are in the ```web``` folder
- Run ```npm start``` to start the application.
- Open a web browser and go to http://localhost:3000 to view the application
