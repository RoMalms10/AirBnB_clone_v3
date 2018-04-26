# API Endpoints

## Purpose
Create the API endpoints for the AirBNB clone.

## Environment
The project was tested and compiled on `Ubuntu 14.04 (trusty64)` via Vagrant run through VirtualBox.

## Languages
API was built with `Python3` and `Flask`.

## API Endpoint Path
The URL prefix for each endpoint is `/api/v1/`. All endpoints used are appended to this prefix.

## How To Start The App
From the root of the repository, use these commands to start the app:
- To use Database Storage:
```
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 python3 -m api.v1.app
```

- To use File Storage:
```
HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 python3 -m api.v1.app
```

## How to Test Endpoints
Currently, in version 1, the app will run on `localhost (0.0.0.0)` and on `port 5000`. This means that once the app is started, you can test each webpage by using the `curl` command.

## Example
In one terminal:
```
$ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
...
```
In another terminal:
```
$ curl -X GET http://0.0.0.0:5000/api/v1/status
{
  "status": "OK"
}
```

## Currently Supported Endpoints


| Endpoint | Types of Requests Available | Purpose |
| ------ | ------------ | -------------------------- |
| `/status` | `GET` | Returns the status of the API. |
| `/stats` | `GET` | Retrieves the number of each objects type in storage. |
| `/states` | `GET`, `POST` | `GET`: Retrieves the list of all `State` objects. <br> `POST`: creates a new `State` object. |
|`/states/<state_id>` | `DELETE`, `PUT`, `GET` | Based on the `<state_id>` passed:<br>`DELETE`: Deletes a `State` object.<br> `PUT`: Updates a `State` object.<br> `GET`: Retrieves a `State` object. |
| `/states/<state_id>/cities` | `GET`, `POST` | Based on the `<state_id>` passed:<br> `GET`: Retrieves the `City` objects linked to that `State`.<br> `POST`: Create a `City` object linked to that `State`. |
| `/cities/<city_id>` | `GET`, `DELETE`, `PUT` | Based on the `<city_id>` passed:<br> `GET`: Retrieves the `City` object.<br> `DELETE`: Delete that `City` object.<br> `PUT`: Update that `City` object. |
| `/amenities` | `GET`, `POST` | `GET`: Retrieves the list of all `Amenity` objects. <br> `POST`: creates a new `Amenity` object. |
|`/amenities/<amenity_id>` | `DELETE`, `PUT`, `GET` | Based on the `<amenity_id>` passed:<br>`DELETE`: Deletes an `Amenity` object.<br> `PUT`: Updates an `Amenity` object.<br> `GET`: Retrieves an `Amenity` object. |
| `/users` | `GET`, `POST` | `GET`: Retrieves the list of all `User` objects. <br> `POST`: creates a new `User` object. |
|`/users/<user_id>` | `DELETE`, `PUT`, `GET` | Based on the `<user_id>` passed:<br>`DELETE`: Deletes a `User` object.<br> `PUT`: Updates a `User` object.<br> `GET`: Retrieves a `User` object. |
| `/cities/<city_id>/places` | `GET`, `POST` | Based on the `<city_id>` passed:<br> `GET`: Retrieves the `Place` objects linked to that `City`.<br> `POST`: Create a `Place` object linked to that `City`. |
| `/places/<place_id>` | `GET`, `DELETE`, `PUT` | Based on the `<place_id>` passed:<br> `GET`: Retrieves the `Place` object.<br> `DELETE`: Delete that `Place` object.<br> `PUT`: Update that `Place` object. |
| `/places/<place_id>/reviews` | `GET`, `POST` | Based on the `<place_id>` passed:<br> `GET`: Retrieves the `Review` objects linked to that `Place`.<br> `POST`: Create a `Review` object linked to that `Place`. |
| `/reviews/<review_id>` | `GET`, `DELETE`, `PUT` | Based on the `<review_id>` passed:<br> `GET`: Retrieves the `Review` object.<br> `DELETE`: Delete that `Review` object.<br> `PUT`: Update that `Review` object. |
| `/<everything_else>`| ALL | Displays the 404 error message |

## Authors
Steven Garcia <steven.garcia@holbertonschool.com><br>
Binita Rai <binita.rai@holbertonschool.com><br>
Lindsey Hemenez <lindsey.hemenez@holbertonschool.com><br>
Robert Malmstein <robert.malmstein@holbertonschool.com><br>
Thomas Dumont <thomas.dumont@holbertonschool.com>
