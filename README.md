# backend

## DevEnvironment

- Install docker
- Install docker compose plugin
- Install the below vscode extension
  - https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack
- Click the bottom-left corner button and select `Open Folder in Container...`
- Run server
  - `make run`
- Create tables
  - `make reset-table`
- Seed initial data
  - `make seed`
- Generate requirements.txt from poetry
  - `make require`

## .env

Create `.env` file and set the key and values.  
`OPEN_WEATHER_APPID` can get from [OpenWeather](https://openweathermap.org/).  
`JWT_SECRET_KEY` and `JWT_REFRESH_KEY` is for jwt. You can make a secure secret key by `openssl rand -hex 32`.

```env
OPEN_WEATHER_APPID="xxxxxxxxxxxxxxxxxxxx"
ASYNC_DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
SYNC_DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
JWT_SECRET_KEY="xxxxxxxxxxxxxxxxxxxx"
JWT_REFRESH_KEY="xxxxxxxxxxxxxxxxxxxx"
```
