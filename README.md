# Intro

Create rules for the wordpress woocommerce addon "weight based shipping rules" from shipping rates defined in CSV files.

# Prerequisites

* sudo pip install selenium
* [Woocommerce weight based shipping plugin](https://wordpress.org/plugins/weight-based-shipping-for-woocommerce/)
* 2 CSV files, one containing shipping rates, the other containing zones. See demo folder for examples

# Usage

python weight-based-shipping-for-woocommerce-import.py http://mywordpressurl.example.com wpusername wppassword demo/rates.csv demo/zones.csv "Shipping name shown in the back end" "Shipping Name that the customer will see";

# Contributing

Currently the only way to get the rules into the database is using Selenium to insert them through the wordpress front end, which, for obvious reasons is not the best approach, but the approach I settled with because of time limitations. 

If you would like to improve on this method, refer to the code stubs in files MySqlUploader.py and RequestUploader.py, submit a pull request and IT WILL BE ASSIMILATED!
