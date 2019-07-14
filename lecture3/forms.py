from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets.html5 import NumberInput


class CreateProductForm(FlaskForm):
    # TODO: 建立商品的表單
    # 名稱(title)
    title = StringField('Enter title', validators=[DataRequired()])
    # 縮圖網址(img_url)
    img_url = StringField('Image Url')
    # 價格(price)
    price = IntegerField('Price',
    validators=[
        DataRequired(),
        NumberRange(1,50000)],
    widget = NumberInput())
    # 是否銷售中(on_sale)
    on_sale = BooleanField('On sale?')
    # 類別(category[Electronics, Handmade, Industrial, Sports, Toys, Others])
    category = SelectField("Category",choices = [
        # (real_value, user_see)
        ('electronics','Electronics'),
        ('handmade','Handmade'),
        ('industrial','Industrial')
    ])
    # 敘述(description)
    description = TextAreaField("Description")
    # form button
    submit = SubmitField('Create a product') 
    pass
