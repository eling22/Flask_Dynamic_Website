from flask import Flask, render_template, request, session, redirect, url_for, flash
# 引用建立商品表單類別
from forms import CreateProductForm
import firebase_admin
from firebase_admin import credentials,firestore

cred = credentials.Certificate("config/key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
print(dir(db))

# test_product = {
#     "title": "test_product",
#     "price": 5000,
#     "on_sale": False
# }

# db.collection("products").add(test_product)

app = Flask(__name__)

# TODO: 設定應用程式的SECRET_KEY
app.config['SECRET_KEY'] = 'Eileen'


@app.route('/')
def index_page():
    # 首頁路由
    return render_template('index.html')


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
        #  let user to other page
        return redirect(url_for('form_feedback'))

    return render_template('create_product.html',form = form)


@app.route('/form_feedback')
def form_feedback():
    # 商品建立成功的路由
    return render_template('form_feedback.html')


if __name__ == '__main__':
    app.run(debug=True)
