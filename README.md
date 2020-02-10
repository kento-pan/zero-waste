# Zero Waste
### No more waste - Consume your food before it goes bad!

I am running this little Flask app currently on a Raspberry Pi with uWSGI and nginx. 
It creates a SQlite3 database in which you can store a list of products and their expiry dates.

The ```notifications.py``` is executed with a cronjob once per day and exermines if there are any products in the database, that are about to expire. These products get flagged and an email notification is sent to the user. As bonus, the user receives some recipe ideas for the expiring products. 

The email settings can be set up in the ```config_mail.py```.
