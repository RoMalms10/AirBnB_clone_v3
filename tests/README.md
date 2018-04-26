# Tests

## Purpose
Aggregate all unit tests into the same folder. Follows the same path as the files they are testing.

## Environment
Tested on `Ubuntu 14.04 (trusty64)` via Vagrant run through VirtualBox.

## Languages
Unit tests written in `Python3`.

## How to Run Tests
In the root of the repository, use the following commands:
- To test Database Storage:
```
HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db HBNB_TYPE_STORAGE=db python3 -m unittest discover tests
```

- To test File Storage:
```
$ python3 -m unittest discover tests
```

## Authors
Steven Garcia <steven.garcia@holbertonschool.com><br>
Binita Rai <binita.rai@holbertonschool.com><br>
Lindsey Hemenez <lindsey.hemenez@holbertonschool.com><br>
Robert Malmstein <robert.malmstein@holbertonschool.com><br>
Thomas Dumont <thomas.dumont@holbertonschool.com>
