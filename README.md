<!--
*** Inspired by https://github.com/othneildrew/Best-README-Template
-->
[![coverage report](https://stgit.dcs.gla.ac.uk/tp3-2019-cs27/cs27-main/badges/master/coverage.svg)](https://stgit.dcs.gla.ac.uk/tp3-2019-cs27/cs27-main/commits/master)

<!-- <img src="https://i.imgur.com/Q23c2CU.png" width="300" height="234"> -->
<div align="center">
<p align="center">
  <a href="">
    <img src="https://i.imgur.com/Q23c2CU.png" alt="Logo" width="300" height="234">
  </a>

  <h3 align="center">GLAROS</h3>

  <p align="center">
    A Multi-cloud dynamic service, or cloud as a platform, Glaros will migrate itself & payload throughout AWS, Azure and GCP instances.
    <br />
    <div>
    <a href="https://stgit.dcs.gla.ac.uk/tp3-2019-cs27/cs27-main/-/wikis/home"><strong>Read our Wiki</strong></a>
    <a href="http://glaros.uk">View Glaros live</a>
    </div>
  </p>
</p>

</div>



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
Glaros is designed to achieve three primary goals, namely
* Avoiding cloud service provider lock-in
* Get the best price for computation
* Move automonously with no human input

Glaros uses stock market data from yahoo_fin about the respective cloud providers in order to determine which service is priced best. When a more optimal platform is detected, Glaros is able to autonomously boot a virtual machine with that provider. It will then begin to SCP itself on that virtual machine, whilst updating the DNS to reflect it's new home on the internet. When it has succesfully transferred itself, it will remotely disable the old virtual machine - not leaving any remnants of itself.

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

If correctly configured, the app is truly autonomous and will require no administration. On your first instance in the project root, simply
```sh
./runglaros
```



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
