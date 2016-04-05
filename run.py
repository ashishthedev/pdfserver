
import pdfserver
import config.default as defaultconfig
import os


app = pdfserver.create_app(defaultconfig)

if not os.path.exists(defaultconfig.WKHTML_BINARY):
    raise Exception("{} not present".format(defaultconfig.WKHTML_BINARY))

# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8181, debug=True)
