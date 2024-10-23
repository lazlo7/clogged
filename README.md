# Clogged

A simple blog API built with FastAPI

- Register posters via admin endpoints 
- Postgres database for storing persistent app data
- Session authentication via Redis
- docker(-compose) support for easy deployment

## Configuration

Environment variables used to configure the app:
- `APP_API_PORT`: port for the app to listen on
- `ADMIN_API_KEY`: API key for the admin endpoints
- `POSTGRES_HOST`: host address of the Postgres database
- `POSTGRES_PORT`: port of the Postgres database
- `POSTGRES_USER`: user of the Postgres database
- `POSTGRES_DB`: name of the Postgres database
- `POSTGRES_PASSWORD`: password for the user of the Postgres database
- `REDIS_HOST=redis`: host address of the Redis database
- `REDIS_PORT=6379`: port of the Redis database
- `REDIS_DB=0`: database number of the Redis database

Environment variables may be provided in an `.env`.  
An example is provided in the `.env.example` file.  
Definitely change `ADMIN_API_KEY` and `POSTGRES_PASSWORD` to secure values when deploying the app.  

## Running

### docker
`Dockerfile` is provided in the root directory.  
Build the image with `docker build -t clogged .` and run it with `docker run -p <host_port>:8000 clogged`, specifying the `<host_port>`.  
The used app container port will be 8000.

### docker compose
Sample `docker-compose.yml` is provided in the root directory.  
Simply run `docker compose up` in the root directory.  
The app host port will try to follow the `APP_API_PORT` environment variable, defaulting to 8000.  
The used app container port will be 8000.  

### poetry
Configure Postgres and Redis variables to match your local setup.  
Initialize poetry with `poetry install` and run the app with `poetry run start`.
