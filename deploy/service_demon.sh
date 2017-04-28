#!/bin/bash

cd /home/ashishthedev/pdfserver/
exec sudo /home/ashishthedev/.virtualenvs/pdfserver/bin/gunicorn -c deploy/gunicorn.conf.py run:app
