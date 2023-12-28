
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# Configure MongoDB
client = MongoClient("mongodb+srv://Rahul_Asati:RahulAsati@cluster0.frousgc.mongodb.net/?retryWrites=true&w=majority")
db = client['db']

@app.route('/', methods=['GET', 'POST'])
def index():
    items_collection = db['items']
    items_list = list(items_collection.find())  # Fetch all items from the collection

    if request.method == 'POST':
        search_item = request.form.get('search_item')
        filtered_items = []

        if search_item:
            # Filter items by search_item
            for item_data in items_list:
                for item_name, item_quantity in item_data['items'].items():
                    if search_item.lower() in item_name.lower():
                        filtered_items.append({'item_name': item_name, 'item_quantity': item_quantity})
        else:
            filtered_items = None  # Reset filtered items if search_item is empty

        new_item_name = request.form.get('new_item_name')
        new_item_quantity_str = request.form.get('new_item_quantity')

        if new_item_name and new_item_quantity_str:
            try:
                new_item_quantity = int(new_item_quantity_str)
                # Insert the new item into the database
                items_collection.insert_one({'items': {new_item_name: new_item_quantity}})
                items_list = list(items_collection.find())  # Refresh the items list
            except ValueError:
                pass  # Handle invalid input for new_item_quantity

        item_name = request.form.get('item_name')
        new_quantity_str = request.form.get('new_quantity')

        if new_quantity_str is not None:
            try:
                new_quantity = int(new_quantity_str)
                # Update quantity in the database
                items_collection.update_one(
                    {'items.' + item_name: {'$exists': True}},
                    {'$set': {'items.' + item_name: new_quantity}}
                )
                items_list = list(items_collection.find())  # Refresh the items list
            except ValueError:
                pass  # Handle invalid input for new_quantity

    return render_template('index.html', items_list=items_list)

if __name__ == '__main__':
    app.run(debug=True)

