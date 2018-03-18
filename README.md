## Data Loading Server for Aqua

Loads aqua specific string program into mongo database

#### Usage

To upload data:
```
curl "http://<server name>:8000/d/01;20180316113000;0125.0;0220;0323;046.8"
```

Syntax of input string is as follows
(meter id);(date string yyyymmddHHMMSS);(first two chars for param ID) rest of string is value
  
To view catalog:
```
curl "http://<server name>:8000/catalog
````


#### Running the server
The server is integrated with supervisord.  To reload the catalog, issue the following command on the server:
 ```
 systemctl restart supervisor
 ```


