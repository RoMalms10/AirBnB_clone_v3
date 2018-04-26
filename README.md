# AirBnb Clone - HBNB

## Purpose
Creating a copy of [Airbnb](https://www.airbnb.com/).
Only some features will be implemented and will be listed below once completed.


## Features
- Command Interpreter.
- 2 Types of Storage: Database (`MySQL`) and File (`JSON`).
- Static Landing Page in `web_static`.
- Dynamic Loading Landing Page in `web_flask`.
- API Endpoints in `api`.

### Command Interpreter

#### Description

The Command Interpreter is used to manage the whole application's functionality from the command line, such as:
+ Crete a new object.
+ Retrieve an object from a file, database, etc.
+ Execute operation on objects. e.g. Count, compute statistics, etc.
+ Update object's attributes.
+ Destroy an object.

#### Usage

To launch the console application in interactive mode simply run:

```console.py ```

or to use the non-interactive mode run:

```echo "your-command-goes-here" | ./console.py ```

#### Console Commands

Commands | Description | Usage
-------- | ----------- |-------- |
**help** or **?**| Displays the documented commands. | **help**
**quit**     | Exits the program. | **quit**
**EOF**      | Ends the program. Used when files are passed into the program. | N/A
**create**  | Creates a new instance of the \<class_name\>. followed by its parameters. Creates a Json file with the object representation. and prints the id of created object. | **create** \<class_name\>
**show**    | Prints the string representation of an instance based on the class name and id. | **show** \<class_name class_id\>
**destroy** | Deletes and instance base on the class name and id. | **destroy** \<class_name class_id\>
**all** | Prints all string representation of all instances based or not on the class name | **all** or **all** \<class_name class_id\>
**update** | Updates an instance based on the class name and id by adding or updating attribute | **update** \<class_name class_id key value\>

## Tests

If you wish to run at the test for this application all of the test are located
under the **test/** folder and can execute all of them by simply running:

```python3 -m unittest discover tests ```

from the root directory.

## Set-up

### Database Set-up
Project will be using MySQL server for its data storage which will use (at this time) a database `hbnb_dev_db` as the user `hbnb_dev`. The user's default credentials are `hbnb_dev_pwd`. 

In order to perform this configuration, you can run the following commands:

```cat setup_mysql_dev.sql | mysql -hlocalhost -uroot -p```

by providing your root password.

```echo "SHOW DATABASES;" | mysql -uhbnb_dev -p | grep hbnb_dev_db```

will show you that you successfully created your database.

```echo "SHOW GRANTS FOR 'hbnb_dev'@'localhost';" | mysql -uroot -p```

will show you the specific privileges the user has on the different databases.

## Bugs

+ No known bugs at this time.

## Authors
Steven Garcia <steven.garcia@holbertonschool.com><br>
Binita Rai <binita.rai@holbertonschool.com><br>
Lindsey Hemenez <lindsey.hemenez@holbertonschool.com><br>
Robert Malmstein <robert.malmstein@holbertonschool.com><br>
Thomas Dumont <thomas.dumont@holbertonschool.com>
