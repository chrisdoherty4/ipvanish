# Vanish [![Build Status](https://travis-ci.org/chrisdoherty4/vanish.svg?branch=master)](https://travis-ci.org/chrisdoherty4/vanish)

Vanish is a command line tool for managing interactions with IPVanish servers.

## Getting Started

If you want to contribute to the project feel free to fork and raise PRs.

### Developing

To get up and running just fork and clone the project locally and install the requirements
using pip.

```
pip install -r requirements.txt
```

## Running the tests

Unit tests are located in the vanish/tests directory. We use the standard `unittest` module shipped with python.

You can add a new test module by creating it under the test directory and making an entry in `runner.py`.

```
suites = [
      loader.loadTestsFromModule(test_model)
      # Add testing modules here
      ]
```

### Coding style

We follow the PEP8 standard and the code will be tested against pylint. You can keep no top of styling with a tool such as `autopep8` but pylint will likely highlight further issues.

```
autopep8 my_module.py
pylnit my_modyle.py
```

## Installing

The package is pushed to pypi so can be installed `pip`.

```
pip install vanish
```

Having cloned the project you can install it using the setup.py module.

```
python setup.py install
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Chris Doherty** - *Initial work* - [chrisdoherty4](https://github.com/chrisdoherty4)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
