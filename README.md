# docker-wyze-plug-api
A docker container containing an API for interacting with Wyze Plugs

## Overview
This is a super simple project and I know the documentation needs some work; however, the following gives a brief overview of how to get started, and if something doesn't make sense, the code is very simple.

Big thank you to [Shaun Tarves](https://github.com/shauntarves) and [all the contributors](https://github.com/shauntarves/wyze-sdk/graphs/contributors) to the [wyze-sdk](https://github.com/shauntarves/wyze-sdk) project, which powers the backend of this project. Unfortunately Wyze doesn't have an official API, so this is the best we have for now and some things (like auth) are a challenge to get configured.

### Authentication
- If you use 2FA, you'll need to get a TOKEN from the Wyze API. The source code includes a start.py script that helps you do this initially by taking your Wyze username and password and prompting you to input your 2FA code. Once you get a TOKEN, you can pass it into your docker image to start the API.

- If you don't use 2FA, you can pass your USERNAME and PASSWORD directly into the container.

### Making Requests
The API is configured to run on port 5000. You'll also need to pass in a KEY variable or use the default "mykey". This key should be passed with each request to the server within a parameter called "key" as a basic authentication method. I choose to use a parameter rather than a header because my use case only allows me to send GET requests to URLs, not allowing for including headers. Ideally, this should only be run locally, so only your local network traffic would be able to intercept your key. If that's a concern, this project probably isn't a good choice for you, so feel free to fork and modify it to better fit your needs.

There's a total of 3 endpoints available:

- **/plug [GET]**<br>
Plug lists all plugs associated with your Wyze account. As with every request, you'll need to pass your key, but you can optionally also include MAC addresses comma separated to get the details of only those devices. The API response will be returned to the user. Here's an example: http://localhost:5000/plug?key=mykey&macs=XXXXXXXXX,XXXXXXXXX or http://localhost:5000/plug?key=mykey

- **/plug/on [GET]**<br>
Plug on turns on plugs. Pass in a list (can be one or many) of plug MAC addresses along with your key. Example: http://localhost:5000/plug/on?key=mykey&macs=XXXXXXXXX,XXXXXXXXX or http://localhost:5000/plug/on?key=mykey&macs=XXXXXXXXX

- **/plug/off [GET]**<br>
Plug off turns off plugs. Pass in a list (can be one or many) of plug MAC addresses along with your key. Example: http://localhost:5000/plug/off?key=mykey&macs=XXXXXXXXX,XXXXXXXXX or http://localhost:5000/plug/off?key=mykey&macs=XXXXXXXXX

## Links
- GitHub Repo: https://github.com/mackenly/docker-wyze-plug-api
- Docker Hub: https://hub.docker.com/repository/docker/mackenly/docker-wyze-plug-api/general
- Sponsor: https://github.com/sponsors/mackenly