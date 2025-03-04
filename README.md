# WattWatch
Ebike Telemetry Tool

## Overview
WattWatch is a ebike telemetry tool to capture, analyze and visualize ebike statistics. The complete tool includes two sub applications
![alt text](image.png)
### desktop_app
desktop_app is written in python using PyQT6. The desktop application is responsible for capturing data from the ebike and normalizing the data to send to the backend server called thundercloud

#### Data simulation
For the time being ride data is being simulated by providing csv files of ride data in the format timestamp, long, lat, speed, soc
This data is assumed to be captured from the ebike and managed as such.


### thundercloud
thundercloud is written using FastAPI to deliver a CRUD interface for storage and analysis.

## Getting Started
### Dependencies
WattWatch utilizes python3.12 and uv for package management. Make sure that uv is installed:

https://github.com/astral-sh/uv


### Starting dekstop_app
To start the desktop_app, navigate to the deskotp_app directory then run the main.py via uv:

```
$ cd desktop_app
$ uv run desktop_app/main.py`
```

This will install the correct version of python and all dependencies needed and start the desktop application

### Start thundercloud cloud service
To start the thundercloud service, navigate to the thundecloud folder and then start the thundercloud server via uv:
```
$ cd thundercloud
$ uv run uvicorn main:app --reload
```
