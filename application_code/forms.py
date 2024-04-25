from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, SelectField
from wtforms.validators import InputRequired

# class to create the upload form on the go using flask
class UploadImageForm(FlaskForm):
    file = FileField("Field", validators= [InputRequired()])
    submit = SubmitField("Choose Image")

# class to create the operation selection form on the go using flask
class OperationSelectionForm(FlaskForm):
    operation = SelectField('Operation', choices=[('edge_detection', 'Edge Detection'), ('color_inversion', 'Color Inversion')])
    submit = SubmitField("Perform Operation")

# class to create the download image form on the go using flask
class DownloadImageForm(FlaskForm):
    submit = SubmitField("Download Processed Image")