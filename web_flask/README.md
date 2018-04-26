# Web framework

## Purpose
Display the current default HTML landing page.

## Environment
The project was tested and compiled on `Ubuntu 14.04 (trusty64)` via Vagrant run through VirtualBox.

## Languages
Was built with `Python3`, `Flask` and `Jinja2`.

## How to Start Apps
```
$ python3 -m web_flask.[filename].py
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```

## How to Test Apps
The apps will run on `localhost (0.0.0.0)` and on `port 5000`. This means that once the app is started, you can test each webpage by using the `curl` command.

## Example
In one terminal:
```
$ python3 -m web_flask.6-number_odd_or_even
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```
In another terminal:
```
$ curl 0.0.0.0:5000/number_odd_or_even/89 ; echo ""
<!DOCTYPE html>
<HTML lang="en">
    <HEAD>
        <TITLE>HBNB</TITLE>
    </HEAD>
    <BODY>
        <H1>Number: 89 is odd</H1>
    </BODY>
</HTML>
$ curl 0.0.0.0:5000/number_odd_or_even/32 ; echo ""
<!DOCTYPE html>
<HTML lang="en">
    <HEAD>
        <TITLE>HBNB</TITLE>
    </HEAD>
    <BODY>
        <H1>Number: 32 is even</H1>
    </BODY>
</HTML>
```
## Currently Supported Endpoints

| App File Name | Endpoint | Purpose |
| -------- | ------- | --------- |
| `0-hello_route.py` | `/` | Displays `Hello HBNB!`. |
| `1-hbnb_route.py` | `/hbnb` | Displays `HBNB`. |
| `2-c_route.py` | `/c/<text>` | Displays `C` followed by the value of `text`. |
| `3-python_route.py` | `/python/(<text>)` | Displays `Python` followed by the value of `text` (`text is optional`). |
| `4-number_route.py` | `/number/<n>` | Display `n` only if it's an integer. |
| `5-number_template.py` | `/number_template/<n>` | On an HTML page from `templates/5-number.html`:<br> Displays an HTML page only if `n` is an integer. |
| `6-number_odd_or_even.py` | `/number_odd_or_even/<n>` | On an HTML page from `templates/6-number_odd_or_even.html`:<br>  Displays only if `n` is an integer and displays whether or not `n` is odd or even. |
| `7-states_list.py` | `/states_list` | On an HTML page from `templates/7-states_list.html`:<br> Displays all `State` objects. |
| `8-cities_by_states.py` | `/cities_by_states` | On an HTML page from `templates/8-cities_by_states.html`:<br> Displays `State` objects and their associated `City` objects. |
| `9-states.py` | `/states/(<id>)` | On an HTML page from `templates/9-states.html`:<br> No `<id>` - Displays all `State` objects and their associated `City` objects if no `<id>` is passed.<br> With `<id>` - Displays the `State` object and it's associated `City` objects. |
| `10-hbnb_filters.py` | `/hbnb_filters` | First version of the landing page for HBNB from `templates/10-hbnb_filters.html`. |

## Authors
Steven Garcia <steven.garcia@holbertonschool.com><br>
Binita Rai <binita.rai@holbertonschool.com><br>
Lindsey Hemenez <lindsey.hemenez@holbertonschool.com><br>
Robert Malmstein <robert.malmstein@holbertonschool.com><br>
Thomas Dumont <thomas.dumont@holbertonschool.com>
