INVENTORY MANAGEMENT SYSTEM
Flask REST API with CLI and OpenFoodFacts integration.

SETUP
1. git clone <your-repo-url> && cd inventory-management
2. python -m venv venv && source venv/bin/activate
3. pip install -r requirements.txt
4. python app.py

API Endpoints
GET /inventory Get all items
GET /inventory/<id> Get one item
POST /inventory Add item
PATCH /inventory/<id> Update item
DELETE /inventory/<id> Delete item
GET /fetch-product/<barcode> Fetch from OpenFoodFact

CLI USAGE
# In a second terminal (while Flask is running)
python cli.py

Options: View all, View one, Add, Update, Delete, Fetch from API. 

RUN TESTS
pytest test_app.py -v

GIT WORKFLOW
git checkout -b feature/my-feature
git add . && git commit -m "Add feature"
git push origin feature/my-feature
# Open PR on GitHub → merge → delete branch