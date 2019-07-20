from flask import Flask, render_template, request, session, redirect, url_for, flash
# 引用建立商品表單類別
from forms import CreateProductForm
from edit import EditProductForm
# import firebase
import firebase_admin
from firebase_admin import credentials,firestore
# import time
import time

cred = credentials.Certificate("config/key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# test_product = {
#     "title": "test_product",
#     "price": 5000,
#     "on_sale": False
# }

# db.collection("products").add(test_product)

app = Flask(__name__)

#  設定應用程式的SECRET_KEY
app.config['SECRET_KEY'] = 'Eileen'


@app.route('/')
def index_page():
    # from products set get file in there
    docs = db.collection('products').order_by('time',direction = firestore.Query.DESCENDING ).get()
    products = list()
    for doc in docs:
        print(doc.id)
        product = doc.to_dict()
        product['id'] = doc.id
        products.append(product)
    # 首頁路由
    return render_template('index.html',products = products)

@app.route('/product/<pid>', methods = ["GET","POST"])
def show_product_page(pid):
    # product page
    # through pid get data from database
    doc = db.collection('products').document(pid).get()
    # arrange format 
    product = doc.to_dict()
    product['id'] = doc.id
    # show page
    return render_template("show_product.html", product = product)


@app.route('/product/<pid>/edit', methods = ["GET","POST"])
def edit_product_page(pid):
    # edit product page
    # through pid get data from database
    doc = db.collection('products').document(pid).get()
    # arrange format 
    product = doc.to_dict()
    product['id'] = doc.id
    # define edit form
    form = EditProductForm()
    # checking form could be sent or not, if ok, sent to database 
    if (form.submit.data == True)and(form.validate_on_submit() == True):
        # get user's data and arrange to dict
        data = {
            'title': form.title.data,
            'price':form.price.data,
            'image_url':form.img_url.data,
            'description':form.description.data,
            'category': form.category.data,
            'on_sale':form.on_sale.data,
        }
        # refresh to database
        db.collection("products").document(pid).update(data)
        # go to home
        return redirect(url_for('index_page'))
    #  set form col's value
    form.title.data = product["title"]
    form.price.data = product["price"]
    form.img_url.data = product["image_url"]
    form.category.data = product["category"]
    form.description.data = product["description"]
    form.on_sale.data = product["on_sale"]
    
    return render_template('edit_product.html',
                            form = form,
                            product = product)

@app.route('/create_product', methods = ['GET',"POST"])
def create_product_page():
    # 建立商品頁的路由
    # TODO: 建立商品表單的實例
    form = CreateProductForm()
    print('request.method',request.method)
    print('form.validate_on_submit()',form.validate_on_submit())
    print('form.errors',form.errors)
    # TODO: 設定表單送出後的處理
    if(request.method == 'POST')and(form.validate_on_submit() == True):
        # get user's enter data
        title = form.title.data
        price = form.price.data
        image_url = form.img_url.data
        category = form.category.data
        description = form.description.data
        on_sale = form.on_sale.data
        print("title:",title)
        # save user's enter data to session
        session['title'] = title
        session['price'] = price
        session['image_url'] = image_url
        session['category'] = category
        session['description'] = description
        session['on_sale'] = on_sale
        # turn data to dict() format
        data = {
            'title': title,
            'price':price,
            'image_url':image_url,
            'description':description,
            'category': category,
            'on_sale':on_sale,
            'time':time.time()
        }
        db.collection('products').add(data)
        # add data to database
        #  let user to other page
        return redirect(url_for('form_feedback'))

    return render_template('create_product.html',form = form)


@app.route('/form_feedback')
def form_feedback():
    # 商品建立成功的路由
    return render_template('form_feedback.html')


if __name__ == '__main__':
    app.run(debug=True)
