## CTW Assignment

The goal of this take-home assignment is to create API for financial data based on the requirements instructions.

### Tools and Technology
- Python >= 3.10
- Django
- Django Rest Framework
- PostGres
- Docker and Docker-compose

### APIs
There are two endpoints -

    api/financial_data/ 
*Optional query params: start_date, end_date, symbol*

    api/statistics/
*Required query params: start_date, end_date, symbol*


### How to setup and run
- Clone the repository
```
git clone git@github.com:iqbalalo/python_assignment_ctw.git
```
- Change directory and run docker-compose
```
docker-compose up
```
### Note:
- There is a sample .env file. Production and Development server should update the environment variables separately and set into .env file.
- DB migration and getting the data from API will be done automatically when container will up. It will generate message according to success and error in terminal.
- The reasons to select Django and Django Rest Framework over Flask or FastApi or others, because of these are popular in large developer community, ready for quick prototyping and pre-build template options and classes for most use cases and easy to maintain.

## API Test

Sample Request:
```bash
curl -X GET 'http://127.0.0.1:8000/api/financial_data?symbol=IBM&limit=3&page=1'
```
Sample Response:
```
{
  "data": [
    {
      "symbol": "IBM",
      "date": "2023-04-11",
      "open_price": 130.58,
      "close_price": 130.42,
      "volume": 3131296
    },
    {
      "symbol": "IBM",
      "date": "2023-04-10",
      "open_price": 129.83,
      "close_price": 131.03,
      "volume": 2614402
    },
    {
      "symbol": "IBM",
      "date": "2023-04-06",
      "open_price": 132.16,
      "close_price": 130.5,
      "volume": 3050581
    }
  ],
  "pagination": {
    "count": 9,
    "page": 1,
    "limit": 3,
    "pages": 3
  },
  "info": {
    "error": ""
  }
}
```

Sample request:
```bash
curl -X GET http://127.0.0.1:8000/api/statistics?start_date=2023-04-01&end_date=2023-04-12&symbol=AAPL

```
Sample response:
```
{
  "data": {
    "symbol": "AAPL",
    "average_daily_open_price": 163.6341666666667,
    "average_daily_close_price": 163.84166666666667,
    "average_daily_volume": 49246628.833333336,
    "start_date": "2023-04-01",
    "end_date": "2023-04-12"
  },
  "info": {
    "error": ""
  }
}
```

## What was delivered:
Directory structure: As the project was based on Django framework, so file structure is little different than mentioned in requirement.
```
python_assignment_ctw/
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
├── .env (Uploaded to git just for assignment)
├── financial
	├── financial (project app main and settings)
		├── settings.py
		├── ... (other necessary files)
	├── api (API service codes)
		├── migrations
			├── 0001_initial.py (migration file)
		├── management/commands/
			├── get_raw_data.py
		├── models.py
		├── views.py

```

## Requirements:

- The program should be written in Python 3. 

> Done

- You are free to use any API and libraries you like, but should include a brief explanation of why you chose the API and libraries you used in README.

> *Used Django Rest Framework due to quick prototyping, easy to maintain with pre-defined templates and big developer community*

- The API key to retrieve financial data should be stored securely. Please provide a description of how to maintain the API key from both local development and production environment in README.

> API Key is saved in **.env** file with the key name **API_KEY**

- The database in Problem Statement 1 could be created using SQLite/MySQL/.. with your own choice.

> Postgres was selected

- The program should include error handling to handle cases where the API returns an error or the data is not in the correct format.

> General exception was placed to catch the error

- The program should cover as many edge cases as possible, not limited to expectations from deliverable above.

> Could not understand the question but general error cases were handled

- The program should use appropriate data structures and algorithms to store the data and perform the calculations.

> Normal calculation methods were used and program is workable fine. But scaling factors are not considered as it depends on many issues and requirements.

- The program should include appropriate documentation, including docstrings and inline comments to explain the code.

> Written
