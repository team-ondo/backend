# backend

## DevEnvironment

- Install docker
- Install docker compose plugin
- Install the below vscode extension
  - https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack
- Click the bottom-left corner button and select `Open Folder in Container...`
- Run server
  - `make run`

## .env

Create `.env` file and set the key and values.  
`OPEN_WEATHER_APPID` can get from [OpenWeather](https://openweathermap.org/).
```env
OPEN_WEATHER_APPID="xxxxxxxxxxxxxxxxxxxx"
ASYNC_DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
SYNC_DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
```
