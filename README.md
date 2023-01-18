# Flask REST API 
A REST API built with Flask and an SQLite database <br /> 

## Initialising and starting the project 
Install dependencies 
```
pip install -r ./requirements.txt 
``` 
Clear and initialise database 
```
flask --app flaskr init-db 
``` 
Start the server 
```
flask --app flaskr run
```


## API endpoints 

### 1. POST ` /api/auth/login `
Logins a user with given credentials, returns a token string if credentials match the data in the database and an error with status code 400 otherwise 

Request form data:
- username: string
- password: string 

Response: 
- success: True/False  
- error: string 
- token: string

### 2. POST ` /api/auth/register `
Registers new user with provided username and password, returns error with status code 400 if user with given username has already been registered <br/>

Request form data:
- username: string
- password: string 
- name: string 
- is_worker: bool 

Response: 
- success: True/False  
- error: string 

### 3. GET ` /api/users/userData$user_id `
Finds and returns data of the user with specified user_id in the database, returns user data in user_data field, or an error with status code 400 if user with such id was not found  <br/>

Request headers: 
- token: string

Response: 
- success: True/False  
- error: string 
- user_data 

### 4. GET ` /api/users/createdOrders$user_id `
Returns a list of orders created by user with specified user_id, or an error with status code 400 if user with such id was not found  <br/>

Request headers: 
- token: string

Response: 
- success: True/False  
- error: string 
- created_orders: list 

### 5. GET ` /api/users/availableWorkers/`
Finds and returns a list of workers that do not have assigned orders, the time limits of which intersect with timestamps given in request form data <br/>

Request form data: 
- time_start: date
- time_finish: date

Response: 
- success: True/False  
- error: string 
- available_workers: list 

### 6. GET ` /api/users/workerGrades$worker_id `
Finds and returns a list of grades that were given to orders completed by the worker with given id, along with an average grade. Returns an error with status code 400 if worker with such id was not found  <br/>

Response: 
- success: True/False  
- error: string 
- grades: list 
- average_grade: number  

### 7. POST ` /api/orders/createOrder `
Creates a new order with specified data  <br/>

Request headers: 
- token: string 

Request form data:
- title 
- description 
- address_from 
- address_to 
- time_start 
- time_finish 

Response: 
- success: True/False  
- error: string  

### 8. GET ` /api/orders/orderData$order_id `
Finds and returns data of an order with specified order_id, or an error with status code 400 id order was not found <br/>

Request headers: 
- token: string 

Response: 
- success: True/False  
- error: string  
- order_data: dict 

### 9. DELETE ` /api/orders/deleteOrder$order_id `
Deletes an order with specified order_id, return an error if order was not found or if the ownew of the token is not the creator of the order <br/>

Request headers: 
- token: string 

Response: 
- success: True/False  
- error: string  

### 10. PATCH ` /api/orders/assignOrder$worker_id$order_id `
Assigns order with given order_id to a worker with given user_id, returns an error of the worker has already assigned orders that intersect woth the given order's time limits <br/>

Request headers: 
- token: string 

Response: 
- success: True/False  
- error: string  

### 11. PATCH ` /api/orders/completeOrder$order_id `
Sets the completion state of given order to completed, returns an error if order was not yet assigned or if the owner of the token is not the creator <br/>

Request headers: 
- token: string 

Response: 
- success: True/False  
- error: string  

### 12. POST ` /api/reviews/createReview `
Creates a new review for the given order with specified data, returns an error if the order has not been completed  <br/>

Request headers: 
- token: string 

Request form data:
- order_id: string 
- grade: number 
- comment: string

Response: 
- success: True/False  
- error: string  

## Database structure 

### "users" table 
- user_id 
- username 
- password 
- name 
- is_worker 
### "orders" table 
- order_id 
- title 
- description 
- address_from 
- address_to 
- time_start 
- time_finish 
- assinged_to 
- completed 
### "reviews" table 
- review_id 
- author_id 
- order_id 
- grade
- comment
  