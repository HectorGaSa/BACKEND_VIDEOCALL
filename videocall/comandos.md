Compruebo en el servidor que puedo llegar con la información:
```bash
python app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://188.132.129.3:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 108-047-022
79.117.236.61 - - [13/Mar/2024 21:05:25] "GET /get_user/myUserId HTTP/1.1" 404 -
79.117.236.61 - - [13/Mar/2024 21:05:39] "POST /register HTTP/1.1" 200 -
```

Lanzo este comando despúes de registrar un usuario en el servidor de señalización:

```bash
caligula@Vinicios-MacBook-Pro videochat % 
curl http://188.132.129.3:5000/get_user/myUserId

{
  "ip_address": "192.168.1.1",
  "port": 12345
}
```

En el servidor puedo ver como llega la petición del get:
```bash
79.117.236.61 - - [13/Mar/2024 21:05:39] "GET /get_user/targetUserId HTTP/1.1" 404 -
79.117.236.61 - - [13/Mar/2024 21:06:03] "GET /get_user/myUserId HTTP/1.1" 200 -
```
