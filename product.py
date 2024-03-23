from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError


class ProductForm(FlaskForm):
    variant = SelectField('Variant', choices=[("Red", "Red"), ("Blue", "Blue"), ("Green", "Green"), ("Yellow", "Yellow"), ("Pink", "Pink")])
    quantity = IntegerField('Quantity')
    product_id = IntegerField('product_id')
    submit = SubmitField('Add to Cart')

    def validate_quantity(self, field):
        if field.data is None:
            raise ValidationError('Quantity is required')
        elif field.data > 100:
            raise ValidationError('Overload')
        elif field.data < 1:
            raise ValidationError('Insert Quantity')
