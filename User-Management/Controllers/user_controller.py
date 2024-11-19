from flask import Flask, Blueprint, request, jsonify, render_template
from Models.models import db, User, Role

from Utils.Lib import Libraries
import os

user_blueprint = Blueprint('user',__name__)



@user_blueprint.route('/')
def index():
    return render_template('index.html')


# User Controller Start
# @user_blueprint.route('/users',methods =['GET'])
# def get_users():
#     secret_key = Libraries.generate_key()
#     users = User.query.all()
#     return jsonify([{'id': user.Id, 'name': user.name,'email': user.email, 'image': user.image, 'role': user.IdRole,'password':Libraries.decrypt_data(secret_key,user.password)} for user in users])


@user_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()  # Fetch all users from the database
    
    # Construct the response
    response = []
    for user in users:
        user_data = {
            'id':user.Id ,# use 'id' assuming it’s the correct attribute name in your User model
            'name': user.name,
            'email': user.email,
            'image': user.image,
            'role': user.IdRole,
            'password': Libraries.decrypt_data(user.password),
        }
        response.append(user_data)
    
    return jsonify(response)

@user_blueprint.route('/users',methods=['POST'])
def create_user():
    if 'image' not in request.files:
        return jsonify({"error":"No images provided"}),400
    # Retrieving the image
    image_file = request.files['image']
    # Getting the image file name
    image_filename= image_file.filename
    # Save the image in Static/Images Location
        
    # Getting new user information
    new_user = User(
        name=request.form['name'],
        email = request.form['email'],
        image =image_filename,
        password = Libraries.encrypt_data(request.form['password']).decode(),
        IdRole = request.form['role']
    )
    existing_user = db.session.query(User).filter_by(email=new_user.email).first()
    if existing_user:
        return jsonify({
            'status':202,
            "error":"this email is already used"})
    
    image_file.save(os.path.join('Static/Images',image_filename))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'message':'User created!'
        }), 201

@user_blueprint.route('/edit/<int:id>', methods=['GET'])
def get_edit_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict())  # Now this works!
    else:
        return jsonify({'error': 'User not found'}), 404


@user_blueprint.route('/users/<int:id>',methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error":"User not found"}), 404
    user.name= request.form['name']
    user.email=request.form['email']
    user.IdRole = request.form['role']
    
    if 'image' in request.files:
        image_file = request.files['image']
        if image_file:
            image_filename= image_file.filename
            image_file.save(os.path.join('Static/Images',image_filename))
            user.image = image_filename
    db.session.commit()
    return jsonify({"message":"User updated !"}), 200

@user_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user :
        return jsonify({"error":"user not found"}),404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message":"User delete successfully"}),200
# User Controller End



# Role Controller Start
@user_blueprint.route('/roles',methods=['GET'])
def get_Role():
    roles = Role.query.all()
    jsonify({"id" : role.IdRole,"LibRole":role.LibRole} for role in roles)
@user_blueprint.route('/roles',methods=['POST'])
def create_role():
    role = Role.query.get(request.form['LibRole'])
    if role :
        return jsonify({"error":"this role already existed"}),401
    new_Role = Role(
        LibRole = request.form['LibRole']
    )
    
    db.session.add(new_Role)
    db.session.commit()

@user_blueprint.route('/roles/<int:id>',methods=['PUT'])
def update_role(id):
    role = Role.query.get(id)
    if role :
        return jsonify({"error":"Sorry Role already existed !"}),401
    role.LibRole = request.form['LibRole'] 
    db.session.commit()
    return jsonify({"message":"Role updated successfully "}),400