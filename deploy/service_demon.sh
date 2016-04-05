#!/bin/bash

cd /home/ashishthedev/pdfserver/
exec /home/ashishthedev/.virtualenvs/pdfserver/bin/gunicorn -c deploy/gunicorn.conf.py run:app
