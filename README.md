# WattWatch
Ebike Telemetry Tool

## Overview
WattWatch is a ebike telemetry tool to capture, analyze and visualize ebike statistics. The complete tool includes two sub applications
### desktop_app
desktop_app is written in python using PyQT6. The desktop application is responsible for capturing data from the ebike and normalizing the data to send to the backend server called thundercloud

### thundercloud
thundercloud is written using FastAPI to deliver a CRUD interface for storage and analysis.

## Getting Started
### Dependencies
WattWatch utilizes python3.12 and uv for package management. Make sure that python3.12 is installed with uv:

https://github.com/astral-sh/uv


