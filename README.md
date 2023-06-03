# docker-wyze-plug-api
A docker container containing an API for interacting with Wyze Plugs

## Overview
The following gives a brief overview of this simple project and shows how to get started, and if something doesn't make sense, the code is very simple.

Big thank you to [Shaun Tarves](https://github.com/shauntarves) and [all the contributors](https://github.com/shauntarves/wyze-sdk/graphs/contributors) to the [wyze-sdk](https://github.com/shauntarves/wyze-sdk) project, which powers the backend of this project. Unfortunately Wyze doesn't have an official API, so this is the best we have for now.

An overview of the Docker variables used:
- USERNAME: Your Wyze username
- PASSWORD: Your Wyze password
- TOTP: The totp key given to you by Wyze when you configure an authenticator app (this program acts like an authenticator app, don't worry you can still use your authenticator app)
- ALWAYS_REFRESH: Always refresh the token each time a request is made? Defaults to True. *(optional)*
- KEY: A short key used to authenticate incoming requests to provide a small amount of security. Defaults to "mykey". *(optional)*

### Authentication
- If you use 2FA, you'll need to get a TOTP key from the Wyze. Once you get your TOTP key, you can pass it into your docker image to start the API.

```
💁‍♂️ Not sure what a TOTP key is? It's okay, I was wasn't sure at first either. The TOTP key is the key given to you by Wyze when you configure an authenticator app. If you've already configured 2FA using an authenticator app you may be able to view the code from within the app or (like me) you may have to disable the authenticator app method and reconfigure it. 
```

- If you don't use 2FA, please configure it and follow the above steps. It's a good idea to use 2FA for any account that supports it so I've made the decision not to support non-2FA accounts for this project.

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