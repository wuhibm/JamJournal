# JamJournal - A Django web app
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
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

JamJournal (https://TODO.todo)

There are many music reiew sites out there But I find them to not usually be the easiest to get started with using. They can be overwhelming and difficult to adjust to so I created a simple app with two main functions:
* View and review albums
* See and interact with your friends' reviews
This simplicity makes it very easy to make an account and get started with reviewing your favorite albums. It maintains to focus of the website on the music and reviews.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* Python
* Django
* Javascript
* Bootstrap
* HTML & CSS

### Prerequisites
* <a href="https://docs.docker.com/desktop/">Docker</a>
* An app with the <a href="https://developer.spotify.com/documentation/web-api/tutorials/getting-started">Spotify API</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation 

To run this project locally on your maching first clone the repo:
`git clone https://github.com/wuhibm/JamJournal.git`
Create a .env file on the top level of the project, e.g.
`touch .env`
Use a text editor and define the following keys in the .env file e.g.
`vi .env`
* CLIENT_ID & CLIENT_SECRET (For spotiy API)
* SECRET_KEY, DEBUG, ALLOWED_HOSTS,& CSRF_TRUSTED_ORIGINS (Standard django settings)
* EMAIL_HOST, EMAIL_FROM, EMAIL_HOST_USER, EMAIL_HOST_PASSWOR (Standard django settings for emailing users)
* DB_HOST, DB_PASSWORD, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD (for the postgres database

Once you've defined a .env file, run the app with the following command
`docker compose up`
The app should be running where you have chosen to host it

<!-- ROADMAP -->
## Roadmap

- [x] Add basic social features (like, follow)
- [x] Add profile editting
- [ ] Let users connect their spotify accounts and review albums directly from their library
- [ ] Let apple music users do the same
- [ ] Transition to a React frontend and Django REST framework backend

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions to this project are welcomed and would be **greatly appreciated**.

If you have suggestions or improvements to the app, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Wuhib Mezemir - 
wuhib.mezemir@gmail.com 
<a href="https://linkedin.com/in/wuhib-mezemir">LinkedIn</a>

Project Link: [https://github.com/wuhibm/JamJournal](https://github.com/wuhibm/JamJournal)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
These are some great resources I used that made this project possible

* [Docker documentation](https://docs.docker.com/)
* [Django documentation](https://docs.djangoproject.com/en/5.2/)
* [Choose an Open Source License](https://choosealicense.com)
* [README template](https://github.com/othneildrew/Best-README-Template)
* [London App Developer for deployment with docker compose](https://www.youtube.com/watch?v=mScd-Pc_pX0&t=7075s)
* [Better stack for deployment with Nginx](https://www.youtube.com/watch?v=1v3lqIITRJA)
<p align="right">(<a href="#readme-top">back to top</a>)</p>
