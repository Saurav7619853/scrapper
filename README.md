# scrapper

# Description

### This is the scrapper tool which is built using selenium in python.

1. Fastapi framework is used.
2. Authentication is done using JWT token.
3. Here the process involves storing the scrapped data and also sending the notification. And the way we are doing these two thing can change. Beacause of that we have used **Strategy Design Pattern** for both the activities.
4. After the hitting the endpoint and the completion of process file named **images** will get created which will contain the **downloaded image** and the final result will get stored in file called **data** under the **products.json** file in the given format like.
```
[
    {
        "product_title": "1 x GDC Extraction Forceps Lower Molars \u2013 86 Ergonomic (FX86E)",
        "product_price": "850.00",
        "path_to_image": "images/GDC-Extraction-Forceps-Lower-Molars-86A-Standard-FX86AS.jpg"
    },
    {
        "product_title": "3A MEDES Bleaching And Night Guard Sheets",
        "product_price": "1380.00",
        "path_to_image": "images/3a-medes-bleaching-and-night-guard-sheets-2-1-600x600.jpg"
    },
]


# Step By Step process to run the tool

1. Clone the repo *git clone https://github.com/Saurav7619853/scrapper.git*
2. Install the dependencies *pip install -r requirements.txt* (suggest you to create virtual env.[optional])
3. Run the server *uvicorn main:app --reload*
4. Hit the endpoint here is the curl 

```
curl --location --request POST 'http://127.0.0.1:8000/scrape/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjA4ODE3MTR9.LofPdUy_IIrMyEaUQyUNCxgsRP-e1TmRMpz3KrTxNh8' \
--header 'Content-Type: application/json' \
--data-raw '{"page_limit": 2}'```

Here in the curl jwt token is there for the authentication. You can also pass "proxy" in the payload like the page limit