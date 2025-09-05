## 🧪 Full-Stack Project Template: React + Flask + PostgreSQL (Dockerized)

This repository provides a starter template for beginner-friendly full-stack applications using React (frontend), Python Flask (backend), and PostgreSQL (database).

## 📁 Project Structure

```sh
.
├── backend/            # Flask backend with API routes, models, services
├── frontend/           # React frontend with Vite build system
├── docker-compose.yml  # Docker config to spin up services

```

## Backend (Flask)

- app.py: Entry point for the Flask app

- models.py: SQLAlchemy models

- routes.py: API endpoints

- services.py: Business logic

- config.py: Environment configuration

- requirements.txt: Python dependencies


## Frontend (React)

- src/: Main React app codebase

- vite.config.js: Vite configuration

- package.json: JavaScript dependencies

## 🚀 Getting Started

1. Install [Docker](https://docs.docker.com/engine/)
2. Clone this repository


```sh
git clone https://github.com/VUTP-University/project-template.github
cd project-template
```

3. Deploy PostgreSQL database

```sh
docker compose --project-name <your-project-name> up -d
```

4. Run the Flask backend

```sh
cd backend                          # Open the backend dir
source /venv/bin/activate           # Start the Python virtual environment - for Linux and macOS
./venv/bin/Activate.ps1             # Start the Python virtual environment - for Windows
pip install -r requirements.txt     # Install the Python dependencies
python app.py                       # Run the Flask app
```

5. Run the React frontend

```sh
cd frontend                 # Open the frontend dir
npm install                 # Install the dependencies
npm run dev                 # Start the React dev server
```

6. Access:
 - Frontend: `http://localhost:5173`
 - Backend: `http://localhost:5000`


> ⚠️ **Warning**  
> This repository is intended as a _template project only_. Do not use it in production without proper customization, security reviews, and testing.




## 🧰 Tools & Technologies

- React + Vite
- Python Flask + SQLAlchemy
- PostgreSQL
- Docker + Docker Compose

## 🧑‍🎓 Perfect for Students

Whether you're building your first CRUD app or experimenting with APIs and databases, this template is designed to remove setup headaches so you can focus on learning and building. It offers:

- A clear folder structure to help understand separation of concerns between frontend, backend, and database layers.

- Pre-configured development tools, such as Vite for React and Docker for containerization—so no need to worry about local environment differences.

- Out-of-the-box integration between React, Flask, and PostgreSQL with sensible defaults to get you started fast.

- Beginner-friendly codebase, featuring clean, readable Python and JavaScript code with room to expand your app as your skills grow.

- Easy-to-follow setup via Docker Compose so students can run everything with a single command, even without deep DevOps knowledge.

## 💡 Ideas for Improvement & Contributions

This template is a living project—built to grow alongside its users. Student developers and contributors are encouraged to experiment, enhance, and share their ideas to make it even better.
