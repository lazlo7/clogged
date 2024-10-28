# Clogged

A simple blog API built with FastAPI

- Featuring support for many posters, tagged posts and many more
- Register posters via admin endpoints 
- Postgres database for storing persistent app data
- Session-based authentication via Redis and XSS post validation
- Easily configurable via pydantic-settings
- OpenAPI scheme generation and Rapidoc for easy API deocumentation and expirementing
- docker(-compose) support for easy deployment

## Configuration

Environment variables used to configure the app:
- `CLOGGED_API_PORT`: port for the app to listen on
- `CLOGGED_IS_DEVELOPMENT`: whether to run the app in development mode, defaults to `0`
- `CLOGGED_ENABLE_API_DOCS`: whether to enable OpenAPI documentation generation  
  and two endpoints \- `/openapi.json` and `/docs` for serving Rapidocs UI, defaults to `1` if in development mode 
- `CLOGGED_ADMIN_API_KEY`: API key for the admin endpoints
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

## Documentation and Experimenting

Set `CLOGGED_ENABLE_API_DOCS` or `CLOGGED_IS_DEVELOPMENT` to `1` to enable OpenAPI scheme generation and documentation endpoint.  
You can then browse and experiment with the API at `/docs` via Rapidoc UI. 
