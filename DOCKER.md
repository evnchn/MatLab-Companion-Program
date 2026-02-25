# Docker Guide for MatLab Companion Program

## About

MatLab Companion Program is a NiceGUI web application that provides a fast, searchable interface for looking up MATLAB function documentation. It parses a bundled XML reference file and lets users search for MATLAB functions by name, displaying direct links to the official MathWorks documentation along with each function's purpose.

## Building the Docker Image

From the project root directory, run:

```bash
docker build -t matlab-companion .
```

## Running the Container

```bash
docker run -p 8080:8080 matlab-companion
```

The application will be available at [http://localhost:8080](http://localhost:8080).

## Port Mapping

The NiceGUI web server listens on port **8080** inside the container. The `-p 8080:8080` flag maps the container's port 8080 to port 8080 on your host machine.

To use a different host port (for example, 3000), run:

```bash
docker run -p 3000:8080 matlab-companion
```

Then access the application at [http://localhost:3000](http://localhost:3000).
