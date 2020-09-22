# Finance-WebApp
A web app via which you can manage portfolios of stocks. It will allow you to check real stocks’ actual prices and portfolios’ values, it will also let you buy and sell stocks by querying IEX for stocks’ prices.

# Requirements
In order to run this app, you need to install these packages:
- cs50
- Flask
- Flask-Session
- requests

you could use the pip install. Exemple:

`pip install Flask`

# Configuring
We’ll need to register for an API key in order to be able to query IEX’s data. To do so, follow these steps:
- Visit [iexcloud.io/cloud-login#/register/](https://iexcloud.io/cloud-login#/register/).
- Enter your email address and a password, and click “Create account”.
- On the next page, scroll down to choose the Start (free) plan.
- Once you’ve confirmed your account via a confirmation email, sign in to [iexcloud.io](https://iexcloud.io/).
- Click API Tokens.
- Copy the key that appears under the Token column (it should begin with `pk_`).
- In a terminal,  execute:

`export API_KEY=value`

note: if you are in windows use `set` instead of `export`.

# Running

set the default app to run, execute:

`set FLASK_APP=application.py`

run the app,

`Flask run`

# Images
![Web view](https://github.com/iladmiral/Finance-Website/blob/master/images/Web_finance.PNG "web view")