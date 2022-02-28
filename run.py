import os
from app import app
from initial_data import insert_init_data
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5001))
	insert_init_data()
	app.run(host='0.0.0.0', port=port)
