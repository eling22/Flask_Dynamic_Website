from flask import Flask, jsonify, render_template, request, session, redirect, url_for, flash
# 引用建立商品表單類別
from forms import CreateProductForm,EditProductForm,DeleteProductForm
from forms import CreateCommentForm,EditCommentForm
# import CSRFProtect
from flask_wtf.csrf import CSRFProtect
# import firebase
import firebase_admin
from firebase_admin import credentials,firestore,auth
# import time
import time
import datetime

cred = credentials.Certificate("config/key.json")
firebase_admin.initialize_app(cred)
# define database
db = firestore.client()

app = Flask(__name__)

# let each template can use csrf
csrf = CSRFProtect(app)
csrf.init_app(app)

#  設定應用程式的SECRET_KEY
app.config['SECRET_KEY'] = 'Eileen'
login_cookie_name = "my_website_cookie"


@app.route('/hello',methods = ['POST'])
def hello():
    # print data get from front-end
    print(request.json)
    # return data to front-end
    response = jsonify({
        'text': 'hello'
    })
    return response

@app.context_processor
def check_login():
    #define sign in check state
    check_auth = {
        "is_login":False,
        "is_admin":False,
        "user": None
    }
    # get session cookies
    session_cookie = request.cookies.get(login_cookie_name)
    # vericate  session cookie
    try: 
        check_auth["user"] = auth.verify_session_cookie(session_cookie,check_revoked=True)
        #set this people's state is True
        check_auth["is_login"] = True
        return dict(check_auth = check_auth)
    except:
        #if vericate fail
        #sent check_auth to each screen
        return dict(check_auth = check_auth)

@app.route('/login',methods =["POST"])
def login():
    #get idToken from frontend
    id_token = request.json["idToken"]
    # set due date
    expires_in = datetime.timedelta(days =14)
    # get session_cookie which backend and firebase auth make for user
    session_cookie = auth.create_session_cookie(id_token,expires_in = expires_in)
    print("id_token",id_token)
    print("expires_in",expires_in)
    print("session_cookie",session_cookie)

    # prepare to response to frontend
    response = jsonify({
        'msg':"OK"
    })
    # set cookie to frontend
    response.set_cookie(login_cookie_name,session_cookie)
    return response

@app.route('/logout',methods =["POST"])
def logout():
    # get session_cookie
    session_cookie = request.cookies.get(login_cookie_name)
    # get user
    user = auth.verify_session_cookie(session_cookie)
    print("user",user)
    # let user's seeein_cookie no use
    auth.revoke_refresh_tokens(user['sub'])
    # prepare response
    response =jsonify({
        "msg":"logout"
    })
    # ley viewer's cookie expire
    response.set_cookie(login_cookie_name,expires = 0)
    return response

@app.route('/')
def index_page():
    # from products set get file in there
    docs = db.collection('products').order_by('time',direction = firestore.Query.DESCENDING ).get()
    products = list()
    for doc in docs:
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
    # create comment form
    create_comment_form = CreateCommentForm(prefix = 'create_comment')
    if create_comment_form.submit.data and create_comment_form.validate_on_submit():
        new_comment = {
            "email": create_comment_form.email.data,
            "content": create_comment_form.content.data,
            "create_at": time.time()
        }
        # put comment data sent to database path: products(folder)/{pid}(file)/comments(folder)
        db.collection(f'products/{pid}/comments').add(new_comment)
        flash("A comment has been created",'alert-primary')
        # refresh
        #return redirect(f"/product/{pid}")
        return redirect(url_for('show_product_page',pid = pid))
    # show comment
    docs = db.collection(f'products/{pid}/comments').order_by('create_at').get()
    comments = list()
    for doc in docs:
        comment = doc.to_dict()
        comment['id'] = doc.id
        # edit comment form
        comment['form'] = EditCommentForm(prefix = comment['id'])
        # if user sent edit message
        if comment['form'].submit.data and comment['form'].validate_on_submit():
            edit_comment = {
                "content": comment['form'].content.data,
            }
            db.document(f'products/{pid}/comments/{comment["id"]}').update(edit_comment)
            flash("A comment has been update",'alert-success')
            print("update")
            return redirect(url_for('show_product_page',pid = pid))
        # setting values to form
        comment['form'].content.data = comment['content']
        comments.append(comment)
    # show page
    return render_template("show_product.html", 
                            product = product,
                            create_comment_form = create_comment_form,
                            comments = comments
                            )

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
    # delete form
    delete_form = DeleteProductForm()
    if delete_form.submit.data and delete_form.validate_on_submit():
        print('this product is going to delete')
        #db.collection('products').document(pid).delete()
        db.document(f'products/{pid}').delete()
         # show a flash message
        flash(f"{product['title']} has been delete.",'alert-danger')
        # remove produvt from database
        return redirect(url_for('index_page'))
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
        # show a flash message
        flash("{} has been update.".format(data['title']),'alert-success')
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
                            delete_form = delete_form,
                            product = product)

@app.route('/create_product', methods = ['GET',"POST"])
def create_product_page():
    # 建立商品頁的路由
    # TODO: 建立商品表單的實例
    form = CreateProductForm()
    # TODO: 設定表單送出後的處理
    if(request.method == 'POST')and(form.validate_on_submit() == True):
        # get user's enter data
        title = form.title.data
        price = form.price.data
        image_url = form.img_url.data
        category = form.category.data
        description = form.description.data
        on_sale = form.on_sale.data
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
        # add data to database
        db.collection('products').add(data)
        # show a flash message
        flash(f"{format(data['title'])} has been create.",'alert-info')
        #  let user to other page
        return redirect(url_for('form_feedback'))

    return render_template('create_product.html',form = form)

@app.route('/form_feedback')
def form_feedback():
    # 商品建立成功的路由
    return render_template('form_feedback.html')


if __name__ == '__main__':
    app.run(debug=True)
