#! /bin/sh

# Create managers first
(cd broker_manager ; flask run -p 5001) & (flask run -p 5002) & (flask run -p 5003) ; fg