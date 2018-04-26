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
The apps will run on `localhost (0.0.0.0)` and on `port 5000`. This means that once the app is started, you can test each webpage by using the curl command.

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

| | |
