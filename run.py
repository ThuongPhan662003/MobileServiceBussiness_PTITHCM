from app import create_app
import atexit
from app.database import db_instance

app = create_app()


@atexit.register
def shutdown():
    db_instance.close()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
