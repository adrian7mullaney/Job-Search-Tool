# CV Builder

A full-stack application for building and managing CVs.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project is a full-stack application built with Flask for the backend and React for the frontend. It allows users to create, edit, and manage their CVs.

## Features

- Create and edit CVs with a user-friendly interface
- Save CVs to PDF format for easy sharing
- User authentication and authorization
- Responsive design for mobile and desktop
- Real-time collaboration on CVs
- Template selection for different CV styles

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Celery
- **Frontend**: React, Redux, Material-UI
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **Task Queue**: Redis
- **Authentication**: JWT

## Installation

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Node.js](https://nodejs.org/) (for frontend development)

### Steps

1. Clone the repository:

    ```sh
    git clone https://github.com/<your-username>/<your-repo>.git
    cd <your-repo>
    ```

2. Install frontend dependencies:

    ```sh
    cd cv-builder-frontend
    npm install
    cd ..
    ```

3. Build and run the Docker containers:

    ```sh
    docker-compose up --build
    ```

4. Access the application:

    - Frontend: `http://localhost`
    - Backend: `http://localhost:5000`

## Usage

### API Endpoints

- `/api/process`: Process a job URL synchronously.
- `/api/async-process`: Process a job URL asynchronously.
- `/api/task-status/<task_id>`: Check the status of a Celery task.

### Example Requests

```sh
curl -X POST http://localhost/api/process -H "Content-Type: application/json" -d '{"url": "http://example.com"}'
```

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
