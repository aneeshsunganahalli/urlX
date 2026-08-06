To distribute the load among my server docker instances, I’m using Nginx as my load balancer. By default I’m using the Round Robin Load Balancing technique, among my 5 docker containers. 

Location directives are setup in such a way that any request with /server/ will hit the [[URL Shortener]] API and other paths will be proxied to my frontend instead. Kept a rate limiting to 10 req/s using the IP address but allow for bursts of upto 20 req/s

```nginx title:default.conf
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s; # Specifies IPv4 binary address, mem limit and allowed rate

server {
    listen 80; # Listens for HTTP

    resolver 127.0.0.11 valid=5s; # Docker's internal DNS, lets nginx find container names like client 

    location ~ ^/server/(.*)$ { # Location directive that triggers when path has /server/ to my API
        limit_req zone=mylimit burst=20 nodelay; # Rate limit to absorb bursts

        # Captures everything after /server/ and appends it to $backend
        set $path $1;
        set $backend "http://server:8000/$path";
        
        proxy_pass $backend; # Proxies request to backend docker container
        
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / { # Handles any other path to my frontend
        set $frontend "http://client:3000";
        proxy_pass $frontend;
        
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```


