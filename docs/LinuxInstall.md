# Debian/Ubuntu Installation #

## For Development ##

### Python 3 ###

* Install pip 3
  * `$ sudo apt install python3-pip`

* Update pip
  * `$ python3 -m pip install --user --upgrade pip`

### Node JS ###

* Install Node Version Manager
  * Run the install script
    * `$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.0/install.sh | bash`
    * OR
    * `$ wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.0/install.sh | bash`
  * Relaunch your terminal
  * Verify nvm installation
    * `$ command -v nvm`
  * If you run into problems see [here](https://github.com/nvm-sh/nvm).

* Install Node JS
  * `$ nvm install node`
  * Verify install
    * `$ node --version`

* Install [Yarn](https://yarnpkg.com/en/docs/install#debian-stable)