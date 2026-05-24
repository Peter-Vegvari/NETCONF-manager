<a id="readme-top"></a>

<br />
<div align="center">
  <h3 align="center">NETCONF/YANG Browser</h3>

</div>

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
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

## About The Project
This application connects to any network device supporting NETCONF/YANG management and:

1. **Reads** the device's complete YANG datastore via the NETCONF protocol
2. **Displays** the datastore in an easily navigable format
3. **Allows editing** of writable datastore elements

### Built With
* [![Python][Python]][Python-url]
* [![FastAPI][FastAPI]][FastAPI-url]
* [![Ant Design][AntDesign]][AntDesign-url]
* [![React][React.js]][React-url]
* [![TypeScript][TypeScript]][TypeScript-url]
* [![Vite][Vite]][Vite-url]
* [![Docker][Docker]][Docker-url]

## Getting Started

### Prerequisites
* Docker and Docker Compose
* Node.js 22+, Python 3.14+ and [uv](https://docs.astral.sh/uv/) for local development

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/Peter-Vegvari/NETCONF-manager.git
   ```
2. Start both services (backend on :8000, frontend on :3000)
   ```sh
   cd manager-backend && docker compose up -d
   cd ../manager-frontend && docker compose up -d
   ```

## Roadmap
- [x] NETCONF connection management
- [x] Multi-device support
- [x] YANG datastore display
- [x] Editing writable datastore elements

## License
Distributed under the MIT License. See `LICENSE` for more information.

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/Peter-Vegvari/NETCONF-manager.svg?style=for-the-badge
[contributors-url]: https://github.com/Peter-Vegvari/NETCONF-manager/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Peter-Vegvari/NETCONF-manager.svg?style=for-the-badge
[forks-url]: https://github.com/Peter-Vegvari/NETCONF-manager/network/members
[stars-shield]: https://img.shields.io/github/stars/Peter-Vegvari/NETCONF-manager.svg?style=for-the-badge
[stars-url]: https://github.com/Peter-Vegvari/NETCONF-manager/stargazers
[issues-shield]: https://img.shields.io/github/issues/Peter-Vegvari/NETCONF-manager.svg?style=for-the-badge
[issues-url]: https://github.com/Peter-Vegvari/NETCONF-manager/issues
[license-shield]: https://img.shields.io/github/license/Peter-Vegvari/NETCONF-manager.svg?style=for-the-badge
[license-url]: https://github.com/Peter-Vegvari/NETCONF-manager/blob/main/LICENSE
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[TypeScript]: https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white
[TypeScript-url]: https://www.typescriptlang.org/
[FastAPI]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Docker]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[Vite]: https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white
[Vite-url]: https://vite.dev/
[AntDesign]: https://img.shields.io/badge/Ant%20Design-0170FE?style=for-the-badge&logo=antdesign&logoColor=white
[AntDesign-url]: https://ant.design/
