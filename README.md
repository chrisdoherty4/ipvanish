# Vanish [![Build Status](https://travis-ci.org/chrisdoherty4/vanish.svg?branch=master)](https://travis-ci.org/chrisdoherty4/vanish)

Vanish is a command line tool for managing interactions with IPVanish servers.


## Installing

The package is pushed to pypi so can be installed `pip`.

```
pip install vanish
```

Having cloned the project you can install it using the setup.py module.

```
python setup.py install
```

### Usage

The tool is easy to use and comes with a help menu describing all available commands. The majority of the commands have a set of location based filters for continent, country, region, and city. The filters accept the relevant name or code that can be retrieved from the `vanish list [continent|country|region|city]` commands.

#### Examples
##### Listing locations and servers
```
vanish list servers --country UK

vanish list continents

vanish list countries --continent EU
```

##### Pinging servers
```
vanish ping --country UK

vanish ping --continent EU
```

##### Connect to a server

The tool will intelligently decide what server to connect to based on current server load and round-trip time to servers.
```
vanish connect --city Manchester

vanish connect --country US
```


## Developing

If you wish to contribute to the project please fork it and raise PRs. You will need to install the requriements from the `requirements.txt` file.

```
pip install -r requirements.txt
```

### Running the tests

Unit tests are located in the vanish/tests directory. We use the standard `unittest` module shipped with python.

You can add a new test module by creating it under the test directory and making an entry in `runner.py`.

```
suites = [
      loader.loadTestsFromModule(test_model)
      # Add testing modules here
      ]
```

Once you've added your testing module you can invoke the tests with:
```
python -m vanish.test.runner
```

### Coding style

The code should conform to `autopep8` default configuration.

```
autopep8 -i my_module.py
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Chris Doherty** - *Initial work* - [chrisdoherty4](https://github.com/chrisdoherty4)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
