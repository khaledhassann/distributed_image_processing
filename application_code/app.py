from PIL import Image
import cv2
from flask import Flask, render_template, request, redirect, flash, url_for, send_file
from werkzeug.utils import secure_filename
import os
from rpc import process_image
from forms import UploadImageForm, OperationSelectionForm, DownloadImageForm

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/images/')
app.config['SECRET_KEY'] = 'rootpass'

@app.route('/', methods=["GET", "POST"])
def upload_form():

  # create an instance from my UploadFileForm class
  form = UploadImageForm()

  # acts like an onclick for the submit button
  if form.validate_on_submit():
    # get the file that was uploaded and save
    file = form.file.data
    file.save(
      os.path.join(
        os.path.abspath(os.path.dirname(__file__)), # app's root  directory
                        app.config['UPLOAD_FOLDER'],  # upload folder path
                        secure_filename(file.filename)  # secure the file so it can be saved
                    )
                )
    
    # this returns a page allowing the user to select the operation he wants on the image he uploaded
    return redirect(url_for('operation_selection', filename = secure_filename(file.filename)))
  
  # this returns the 'home' page of the application which is where the user uploads his images
  return render_template('upload.html', form = form)

@app.route('/upload_image', methods=['POST'])
def upload_image():
  if 'image' not in request.files:
    flash('No file part')
    return redirect(url_for('upload_form'))
  file = request.files['image']
  if file.filename == '':
    flash('No selected file')
    return redirect(url_for('upload_form'))
  if file:
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    flash('Image uploaded successfully!')
    return redirect(url_for('upload_form'))
  else:
    flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
    return redirect(url_for('upload_form'))

@app.route('/operation_selection/<filename>', methods=['GET','POST'])
def operation_selection(filename):

  form = OperationSelectionForm()

  if form.validate_on_submit():
    operation = form.operation.data
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    processed_image = process_image(image, operation)

    # Create folder for proccessed images
    processed_folder = os.path.join(app.static_folder, 'processed_images')
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    # # Save the processed image 
    processed_file_path = os.path.join(processed_folder, filename)
    processed_image = Image.fromarray(processed_image)
    processed_image.save(processed_file_path)

    # Return a page allowing user to download an image
    return redirect(url_for('download', filename= secure_filename(filename)))

  return render_template('operationSelection.html', form = form)

@app.route('/download/<filename>', methods=['POST', 'GET'])
def download(filename):

  form = DownloadImageForm()

  if form.validate_on_submit():
    processed_folder = os.path.join(app.static_folder, 'processed_images')
    processed_image = os.path.join(processed_folder, filename)
    return send_file(path_or_file= processed_image, mimetype = 'image/jpg', as_attachment = True)

  return render_template('download.html', form = form)


if __name__ == '__main__':
  app.run(debug=True)
