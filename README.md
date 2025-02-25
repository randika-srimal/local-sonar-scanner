# Sonarqube Scanner - Local

## Getting Started

1. Clone the repo.
2. Run `docker compose up -d --build` to build and spin up the docker containers.
3. Navigate to SonarQube postgres adminer via [http://localhost:9001](http://localhost:9001).
4. On login screen select `PostgreSQL` as System, enter `postgres` as server, enter `postgres` as username and password. Then click "Login".
5. Create a database named `sonar`. Please note that, if the DB has been configured by a supervisor. Then you will have to import it instead of creating new DB.
6. Re run `docker compose up -d` command to spin up sonarqube container with the postgres database.
7. Navigate to Sonarqube dashboard via [http://localhost:9000](http://localhost:9000). The default username/password will be "admin/admin". After entering default passwords you may need to setup a new password.

### How to scan a project

1. Setup the project if the project has not yet configured in SonarQube. Select `Local Project` and proceed as instructed.
2. Generate a project analyse token after setting up the project in SonarQube.
3. Add the generated project specific token and key in to `.env` file.
4. Add the absoulte path for the project directory as `PROJECT_DIRECTORY_PATH`.

```env
PROJECT_DIRECTORY_PATH=./
PROJECT_KEY=
PROJECT_TOKEN=
```

5. Re run `docker compose up -d` command to spin up the containers with proper details.
6. Run `docker compose exec scanner sonar-scanner`. This command will start scanning the project and generate a report which you may access via [http://localhost:9000](http://localhost:9000).

### How to export a report

Run `docker compose exec scripts python ./scripts/sonar-export.py`. This will export a Excel file containing all the issues.