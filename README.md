# My Social Network in Django REST
It is a simple example of social network writen in python using Django Rest Framework
The Authentication done using JWT tokens
## API Endpoints:

    POST /api/token/ 
    POST /api/token/refresh/
    
    GET /users
    GET /users/{user_id}
    POST /users/register
    GET /user
    
    GET /posts
    POST /posts
    GET /posts/{post_id}
    PUT /posts/{post_id}
    DELETE /posts/{post_id}
    
    GET /likes
    GET /likes/{like_id}
    DELETE /likes/{like_id}
    
 ## Testing bot
 The testing bot is located in `bot` directory it reads the configuration file supplied by the --path parameter.
 
 
 ## examples:
 to register a user
 
    POST /users/register 
     {
        "username": "user_0",
        "email" : "user_0@test.com",
        "password" : "test",
        "password_confirm" : "test"
     }
     
to login a user
    
    POST /api/token/
    {
        "email": "user_0@test.com",
        "password": "test"
    }
    
    This endpoint will return a JWT token
     
to create a post a user need to be registered and logged in

    POST /posts
    {
        "title": "Sample Title",
        "text": "The message of the post"
    }

to get a list of all posts
    
    GET /posts/
    
to read a single post

    GET /posts/{post_id}
