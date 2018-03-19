OpenJudge
=========

**Refactored!**

OpenJudge has been refactored to be faster and easier to set up! This
repository was about quick contests for small groups of 20-30 people. Somewhere
along the way, I faltered and it became bloated. It's back now in a form which
is fast and light.

Screenshots
----------

![Normal Screen](screens/home.png)
![Leader Board Screen](screens/lb.png)

Usage
-----

First install MongoDB by following the instructions [in their docs](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

### Normal User usage

```bash
mkdir mycontest
cd mycontest


git clone --depth 1 https://github.com/theSage21/openJudge
cp -r openJudge/templates .  # You can write your own template here
cp -r openJudge/staticfiles .  # You can write your css/js here
cp -r openJudge/questions .  # The questions go here
cp openJudge/wrappers.json .  # language wrappers go here

# Edit files in `questions` dir as per need
pipenv install openjudge
pipenv shell
openjudge
```

That takes care of the interface. To start the code judge run `openjudge --judge` from another terminal.

```bash
cd mycontest
pipenv shell
openjudge --judge
```


### Dev usage

First install MongoDB by following the instructions [in their docs](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

```bash
sudo apt-get install python3-dev
pip install --user pipenv
git clone https://github.com/theSage21/openJudge
cd openJudge
pipenv install --python 3
```

To run openjudge two commands need to be issued.  `openjudge` and `openjudge --judge` in two separate terminals. The first is the interface and the second is the "judge".

