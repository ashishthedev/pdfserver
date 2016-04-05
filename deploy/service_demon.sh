#!/bin/bash

cd /home/ashishthedev/pdfserver/
exec gunicorn -c deploy/gunicorn.conf.py run:app
