# Django Analysis Project

This project is a Django-based web application for analysis, containerized with Docker.

## Project Structure

- `analyse/` - Main Django project settings and configuration.
- `analysis/` - Django app for analysis features.
- `manage.py` - Django management script.
- `requirements.txt` - Python dependencies.
- `Dockerfile` - Docker build instructions.
- `db.sqlite3` - SQLite database (for development).
- `staticfiles/` - Collected static files.

## Getting Started

### Prerequisites

- Docker
- (Optional) Python 3.11.5 if running locally

### Build and Run with Docker

1. Build the Docker image:

    ```sh
    docker build -t django-analysis .
    ```

2. Run the container:

    ```sh
    docker run -p 8000:8000 django-analysis
    ```

3. Access the app at [http://localhost:8000](http://localhost:8000)

### Development (without Docker)

1. Install dependencies:

    ```sh
    pip install -r requirements.txt
    ```

2. Run the server:

    ```sh
    python manage.py runserver
    ```

## Database

- Uses SQLite by default (`db.sqlite3`).
- Dockerfile includes Microsoft SQL Server tools for optional MSSQL support.

## License

Specify your license here.

## Contact

Add contact information
run the program by installing the following :
install python
install anaconda 
pip install django
pip install pyodbc

after installations open code in terminal run : 
   python manage.py runserver
