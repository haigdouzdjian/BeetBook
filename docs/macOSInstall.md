# MacOS Installation #

## For Development ##

* Use [Homebrew](https://brew.sh/)

### Python 3 ###

* Install Python3 using brew
  * `$ brew install python3`
  * Verify install
  * `$ python3 --version`

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

* Install Yarn
  * `$ brew install yarn`
