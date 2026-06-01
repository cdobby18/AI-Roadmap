# Grand Line Text API

A FastAPI-based REST API built from the **DevilFruit** text processing class. This project transforms a Python text-processing application into a production-style API capable of cleaning, analyzing, storing, and processing text through HTTP requests.

---

## Project Overview

The Grand Line Text API provides:

* Text cleaning and preprocessing
* Text analysis and statistics
* Language detection
* Data persistence
* Authentication and authorization
* Background task processing

The project is designed to demonstrate modern backend development practices using FastAPI.

---

## Features

### Text Processing

* Clean and normalize text
* Remove punctuation
* Remove stopwords
* Tokenize words
* Generate text statistics
* Detect language

### API Features

* RESTful API endpoints
* Interactive Swagger documentation
* Request and response validation
* JSON-based communication

### Storage

* Save processed results
* Retrieve previous results
* Delete stored records

### Security

* Basic Authentication
* JWT Authentication
* Protected API routes

### Background Processing

* Asynchronous task execution
* Job status tracking
* Server-Sent Events (SSE)

---

## Project Structure

```text
project/
│
├── main.py
├── schemas.py
├── storage.py
│
├── routes/
│   ├── process.py
│   └── analyze.py
│
├── middleware/
│   └── timer.py
│
└── auth/
    ├── jwt_handler.py
    └── jwt_bearer.py
```

---

## API Endpoints

### Public Routes

| Method | Endpoint      | Description        |
| ------ | ------------- | ------------------ |
| GET    | `/`           | Health check       |
| POST   | `/auth/login` | Generate JWT token |

### Protected Routes

| Method | Endpoint          | Description                |
| ------ | ----------------- | -------------------------- |
| POST   | `/process`        | Process text               |
| POST   | `/process/async`  | Start async processing job |
| POST   | `/analyze`        | Analyze text               |
| GET    | `/analyze/{n}`    | Get top N words            |
| GET    | `/search`         | Search stored results      |
| GET    | `/jobs/{job_id}`  | Check job status           |
| GET    | `/stream/process` | Stream processing events   |
| GET    | `/results`        | View saved results         |
| GET    | `/results/{id}`   | View a specific result     |
| DELETE | `/results/{id}`   | Delete a result            |

---

## Development Modules

### Module 1 — FastAPI Basics

* Create API endpoints
* Connect the DevilFruit class
* Return JSON responses

### Module 2 — Validation

* Pydantic models
* Request validation
* Query and path parameters

### Module 3 — Storage & Middleware

* JSON-based persistence
* API routers
* Middleware implementation
* CORS configuration

### Module 4 — Authentication

* Basic Authentication
* JWT Authentication
* Protected endpoints

### Module 5 — Background Tasks

* Async processing
* Job queues
* Server-Sent Events (SSE)

---

## Technologies Used

* Python
* FastAPI
* Pydantic
* JWT
* Bcrypt
* Python-JOSE
* JSON Storage

---

## Learning Outcomes

This project demonstrates:

* REST API Development
* FastAPI Fundamentals
* Authentication & Authorization
* Request Validation
* Middleware Implementation
* Persistent Storage
* Background Task Processing
* Production-Ready Project Structure

---

## Future Improvements

* MySQL or PostgreSQL Integration
* Redis Caching
* Docker Deployment
* Machine Learning Model Integration
* Cloud Deployment
* User Management System

---

## Author

Built as part of an AI Engineering learning journey focused on backend development, API design, and scalable AI application architecture.
