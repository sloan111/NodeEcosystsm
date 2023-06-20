# NodeJS Application with Docker and Pytest
## _Michael Sloan_

This project has a multi-container application using Docker and Docker Compose, consisting of four Node.js instances. It also includes a Python pytest script for testing the application.

## Prerequisites

1. Install [Docker](https://docs.docker.com/get-docker/) (Docker Compose is typically bundled with Docker Desktop).
2. Install [Python](https://www.python.org/downloads/) with [pytest](https://docs.pytest.org/en/latest/getting-started.html). 

## Getting Started

Follow these steps to start the application:

### Command-line mode

Simply run the following command to start the application:

```
docker-compose up
```

A series of Docker containers with a Node12 environment will be spun up.  These containers can be terminated by running:

```
docker-compose down
```

### Python test mode

One can test the event logging capability of the networked application by simply running

```
pytest
```

or

```
python -m environment_test.py  
```

The Python test script will automatically spin up the networked application, test its functionality, and tear down the application.

