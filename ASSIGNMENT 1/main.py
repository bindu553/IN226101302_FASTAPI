from fastapi import FastAPI, Query

app = FastAPI()

products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub',         'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set',          'price':  49, 'category': 'Stationery',  'in_stock': True },
    {'id': 5, 'name': 'Laptop Stand',        'price': 2499, 'category': 'Electronics', 'in_stock': True },
    {'id': 6, 'name': 'Mechanical Keyboard', 'price': 3499, 'category': 'Electronics', 'in_stock': True },
    {'id': 7, 'name': 'Webcam',              'price': 1999, 'category': 'Electronics', 'in_stock': True }
]

# ── Endpoint 0 — Home 
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

# ── Endpoint 1 — Return all products 
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

# ── New Endpoint — Filter products by category ─────────────────
@app.get('/products/category/{category_name}')
def get_products_by_category(category_name: str):
    
    filtered_products = [p for p in products if p['category'].lower() == category_name.lower()]
    
    if not filtered_products:
        return {'error': 'No products found in this category'}
    
    return {
        'category': category_name,
        'products': filtered_products,
        'count': len(filtered_products)
    }
#new endpoint to check in_stock=true
@app.get('/products/instock')
def get_in_stock_products():
    
    in_stock_products = [p for p in products if p['in_stock'] is True]
    
    return {
        'in_stock_products': in_stock_products,
        'count': len(in_stock_products)
    }
#new endpint store summary
@app.get('/store/summary')
def get_store_summary():
    
    total_products = len(products)
    in_stock_count = len([p for p in products if p['in_stock'] is True])
    out_of_stock_count = len([p for p in products if p['in_stock'] is False])
    
    # Get unique categories using set comprehension
    unique_categories = list(set([p['category'] for p in products]))
    
    return {
        'store_name': 'My E-commerce Store',
        'total_products': total_products,
        'in_stock': in_stock_count,
        'out_of_stock': out_of_stock_count,
        'categories': unique_categories
    }
#new endpoint search products by name
@app.get('/products/search/{keyword}')
def search_products_by_name(keyword: str):
    
    # Convert keyword to lowercase for case-insensitive search
    search_term = keyword.lower()
    
    # Filter products where name contains the keyword (case-insensitive)
    matched_products = [
        p for p in products 
        if search_term in p['name'].lower()
    ]
    
    if not matched_products:
        return {'message': 'No products matched your search'}
    
    return {
        'keyword': keyword,
        'matched_products': matched_products,
        'count': len(matched_products)
    }
# new Endpoint Best deal and premium pick (cheapest & most expensive)
@app.get('/products/deals')
def get_product_deals():

    # Find cheapest product using min() function
    cheapest_product = min(products, key=lambda p: p['price'])
    
    # Find most expensive product using max() function
    most_expensive_product = max(products, key=lambda p: p['price'])
    
    return {
        'best_deal': cheapest_product,
        'premium_pick': most_expensive_product
    }
