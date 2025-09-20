# Documentation for network
### fastAPI: API to expose the CRUD operations around network statistics


This application has two generic endpoints:

| Method | URL Pattern           | Description             |
|--------|-----------------------|--------------------|
| GET    | /api/v1/network/info         | Basic description of the application and container     |
| GET    | /api/v1/network/health    | Health check endpoint     |



## CRUD Endpoints:
| Method | URL Pattern           | Description             | Example             |
|--------|-----------------------|--------------------|---------------------|
| GET    | /api/v1/network         | List all network     | /api/v1/network       |
| GET    | /api/v1/network/{id}    | Get network by ID     | /api/v1/network/42    |
| POST   | /api/v1/network         | Create new network    | /api/v1/network       |
| PUT    | /api/v1/network/{id}    | Update network (full) | /api/v1/network/42    |
| PATCH  | /api/v1/network/{id}    | Update network (partial) | /api/v1/network/42 |
| DELETE | /api/v1/network/{id}    | Delete network        | /api/v1/network/42    |


### Access the info endpoint
http://home.dev.com/api/v1/network/info

### View test page
http://home.dev.com/network/test/network.html

### Swagger:
http://home.dev.com/api/v1/network/docs