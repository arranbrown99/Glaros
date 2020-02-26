<!--
*** Inspired by https://github.com/othneildrew/Best-README-Template
-->
[![coverage report](https://stgit.dcs.gla.ac.uk/tp3-2019-cs27/cs27-main/badges/master/coverage.svg)](https://stgit.dcs.gla.ac.uk/tp3-2019-cs27/cs27-main/commits/master)



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://i.imgur.com/Q23c2CU.png">
    <img src="images/logo.png" alt="Logo" width="100" height="78">
  </a>

  <h3 align="center">GLAROS</h3>

  <p align="center">
    Multi-cloud dynamic service, or cloud as a platform, Glaros will migrate itself & payload throughout AWS, Azure and GCP instances.
    <br />
    <a href="https://stgit.dcs.gla.ac.uk/tp3-2019-cs27/cs27-main/-/wikis/home"><strong>Our Wiki</strong></a>
    <br />
    <br />
    <a href="http://glaros.uk">View Glaros live</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://i.imgur.com/rZ8xFGH.png)
A dashboard payload

### Built With

* [Python]()
* [Nginx]()
* [Gunicorn]()



<!-- GETTING STARTED -->
## Getting Started

To configure a Glaros, follow these instructions.

### Prerequisites

Accounts for Google Cloud Platform, Amazon Web Services, Microsoft Azure and GoDaddy.
Create a linux virtual machine on each of these cloud service providers (henceforth: CSP), preferably with a LTS Ubuntu image.
Transfer or register a domain on your GoDaddy account and in [developer.godaddy.com](https://developer.godaddy.com/key) create production API keys to manage your chosen domain.

### Installation
 
1. Clone the repo on *one* of the virtual machines.
```sh
git clone https://stgit.dcs.gla.ac.uk/tp3-2019-cs27/cs27-main.git
```

2. Set network firewall rules to accept web and ssh traffic on all virtual machines

3. 6 Ssh keys
Environment variables
Install Azure CLI on all virtual machines
~/.aws/
Install cloud sdk (google) and auth it


<!-- USAGE EXAMPLES -->
## Usage

To do




<!-- LICENSE -->
## License

Distributed under the TBD License



<!-- CONTACT -->
## Contact

Email - [tp3.cs27@gmail.com](tp3.cs27@gmail.com)

Project Link: [https://stgit.dcs.gla.ac.uk/tp3-2019-cs27/cs27-main.git](https://stgit.dcs.gla.ac.uk/tp3-2019-cs27/cs27-main.git)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Leidos]()





<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: https://i.imgur.com/rZ8xFGH.png
