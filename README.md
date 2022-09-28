<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<br />
<div align="center">
  <a href="https://github.com/team-ondo/backend">
    <img src="docs/images/logo.png" alt="Logo" width="350" height="119">
  </a>

<h3 align="center">ondo-backend</h3>

  <p align="center">
    Backend implementation of ondo
    <br />
    <a href="https://github.com/team-ondo/backend"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/team-ondo/backend">View Demo</a>
    ·
    <a href="https://github.com/team-ondo/backend/issues">Report Bug</a>
    ·
    <a href="https://github.com/team-ondo/backend/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li>
            <a href="#prerequisites">Prerequisites</a>
            <ul>
                <li><a href="#environment">Environment</a></li>
                <li><a href="#set-up-env">Set up .env</a></li>
                <li><a href="#set-up-git-hook">Set up git hook</a></li>
            </ul>
        </li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



## About The Project

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![Python][Python]][Python-url]  
[![FastAPI][FastAPI]][FastAPI-url]  
[![Socket.io]][Socket.io-url]  
[![Postgres][Postgres]][Postgres-url]  
[![JWT][JWT]][JWT-url]  
[![Docker][Docker]][Docker-url]  
[![Visual studio code][Visual studio code]][Visual studio code-url]  

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Getting Started

### Prerequisites

#### Environment

- Install docker
- Install docker compose plugin
- Install the below vscode extension
    - [vscode-remote-extensionpack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
- Click the bottom-left corner button and select `Open Folder in Container...`

#### Set up .env

- Create a new file named `.env` at the root of the project.
- Set up the `.env` file and set the key and values like below.
    - `OPEN_WEATHER_APPID` can get from [OpenWeather](https://openweathermap.org/).
    - `JWT_SECRET_KEY` and `JWT_REFRESH_KEY` is for jwt. You can make a secure secret key by running `openssl rand -hex 32`.
    - `TWILIO` can get from [twilio](https://www.twilio.com/).

    ```env
    OPEN_WEATHER_APPID="xxxxxxxxxxxxxxxxxxxx"
    ASYNC_DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    SYNC_DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
    JWT_SECRET_KEY="xxxxxxxxxxxxxxxxxxxx"
    JWT_REFRESH_KEY="xxxxxxxxxxxxxxxxxxxx"
    TWILIO_SID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    TWILIO_AUTH_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    TWILIO_VIRTUAL_NUMBER = "+xxxxxxxxxxx"
    TWILIO_VERIFIED_NUMBER = "+xxxxxxxxxxxx"
    ```

#### Set up git hook

```sh
git config --local core.hooksPath .githooks
sudo chmod a+x .githooks/pre-push
```

### Installation

> **Note**
> If you want to check what commands are available, type `make`.

1. Create the tables
    ```sh
    make reset-table
    ```
2. Seed data
   ```sh
   make seed
   ```
3. Run server
   ```sh
   make run
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Roadmap

See the [open issues](https://github.com/team-ondo/backend/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contact

Project Link: [https://github.com/team-ondo/backend](https://github.com/team-ondo/backend)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



[contributors-shield]: https://img.shields.io/github/contributors/team-ondo/backend.svg?style=for-the-badge
[contributors-url]: https://github.com/team-ondo/backend/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/team-ondo/backend.svg?style=for-the-badge
[forks-url]: https://github.com/team-ondo/backend/network/members
[stars-shield]: https://img.shields.io/github/stars/team-ondo/backend.svg?style=for-the-badge
[stars-url]: https://github.com/team-ondo/backend/stargazers
[issues-shield]: https://img.shields.io/github/issues/team-ondo/backend.svg?style=for-the-badge
[issues-url]: https://github.com/team-ondo/backend/issues
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[FastAPI]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[Socket.io]: https://img.shields.io/badge/Socket.io-black?style=for-the-badge&logo=socket.io&badgeColor=010101
[Socket.io-url]: https://socket.io/
[Postgres]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://www.postgresql.org/
[Docker]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[JWT]: https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens
[JWT-url]: https://jwt.io/
[Visual Studio Code]: https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white
[Visual Studio Code-url]:https://code.visualstudio.com/
