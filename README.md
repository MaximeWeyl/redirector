This is a basic URL redirection service.
It stores associations between apps and redirection URLs, 
for apps with changing URLs.

You can then use GET requests to redirect to the URL of an app, or POST/PUT
requests to modify the URL of an app.

This might be useful for having a single fixed URL to an app whose URL changes.
The use case was to provide a fixed URL to simple apps hosted in OVHcloud AI-Training, 
because the URL is linked to the job's ID, which is renewed at each job run. In such a
context, *redirector* can be used to provide a fixed URL to the app, as long as it gets
the right POST/PUT requests to update the URL properly.

# Launch

## With python 

You can just run the ```main.py```.
The dependencies are handled by poetry, so you can install them 
with ```poetry install```, or use any other method you like.

You can change the default port by setting the ```PORT``` 
environment variable.

You can change the location of the json "database" by setting the 
```CONFIG_FILE_PATH``` environment variable.

## With docker 

```
docker run -e BASIC_AUTH_USERNAME=user -e BASIC_AUTH_PASSWORD=password -e CONFIG_FILE_PATH=/database/redirects.json -v redirector:/database -p 8080:8080 ghcr.io/maximeweyl/redirector:workflow
```

## With OVHcloud AI-Training job

```
ovhai job run -e BASIC_AUTH_USERNAME=user -e BASIC_AUTH_PASSWORD=password -e CONFIG_FILE_PATH=/database/redirects.json -v redirector@GRA:/database --unsecure-http ghcr.io/maximeweyl/redirector:workflow
```

# Create/update a redirection

To POST or PUT a new redirection, use the ```/app/<application>``` url, where ```<application>``` is the name of the application.
The body of the request should have this form (json-formatted): 

```
{
    "url": "https://my-url.com"
}
```

You must use basic authentication ('Authorization' header) for creating/updating a redirection.
Alternatively, you can also use the headers ```XX-redirector-user``` and ```XX-redirector-password```.

The default username is 'admin' with the default password 'admin'.
You can change the default username and password by using these environment variables:

- BASIC_AUTH_USERNAME
- BASIC_AUTH_PASSWORD

# Use a redirection

Just make a GET request to the same URL used when creating or updating the redirection.
The browser will be redirected to the new URL, that will be displayed in the address bar.
So your user should bookmark the redirector URL, and not the URL after redirection.

# See the entire configuration

You can make a GET request to the ```/config``` url, and you will get 
a json with the entire configuration of redirections.
You will see that updates do not erase previous ones, the current values
is just the last one of each redirection list.


# Limitations

- The redirection does not hide the real URL. 
  The user will be redirected to the URL and will be able to see 
  it in its address bar.
- The app is really simple, and was not tested under heavy load.
- The redirections are stored in a simple json file. While simple and
  easy to read, this is not a really safe solution. 
  Remember this is all really basic.
- It uses a basic flask development server. No really you should not use
  this for something too serious.
- I do not give any warranty of any sort, and I am not responsible for any
  damage caused by this service
