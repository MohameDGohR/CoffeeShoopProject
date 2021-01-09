import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

'''@app.route('/drinks')
@requires_auth('get:drinks-detail')
def drink(jwt):
   
   print(jwt)
   return 'Not Implemented'''





    

    
     


## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def drink_all():
    try:
        ls= Drink.query.all()
        
        
        drinks = [ x.short() for x in ls ]
        #print(drinks)
       
        return jsonify({
            "success":True,
            "drinks" :drinks })
    except:
        abort(422)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drink_detail(payload):
    try:
        ls= Drink.query.all()
        if len(ls)  == 0 :
            abort(404)
        drinks = [ x.long() for x in ls ]
        #print(payload)
    except:
        abort(422) 
    return jsonify({
            "success": True,
            "drinks" :drinks })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    body = request.get_json()
    if 'recipe' not in body or 'title' not in body :
        abort(400)
    try:
        title = body.get('title', None)
        recipenonstr = body.get('recipe', None)
           
        if  title is   None  or recipenonstr is   None   :
            abort(400)
        recipe =str(recipenonstr).replace("'",'"')
        if not  recipe.__contains__('[') and not recipe.__contains__(']'):
            recipe = '['+recipe+']'
         
        drink = Drink(title= title ,recipe = recipe)  
        drink.long()
        
        drink.insert() 
          
        return jsonify({
            "success":True,
            "drinks":drink.long()
            })              
    except:
        abort(422)
    



'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload,id):
    body = request.get_json()
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None :
        abort(404) 
    
    
    try:
        if 'recipe' not in body and  'title' not in body :
             abort(400)
        title = body.get('title', None)
        recipenonstr = body.get('recipe', None)
        if  title is   None  and recipenonstr is   None   :
            abort(400)
        if title is not None :
             drink.title=title
        if  recipenonstr is not  None  :
            recipe =str(recipenonstr).replace("'",'"')
            drink.recipe =recipe 
        drink.update()
           
        drink.long()
        drinking=[]
        drinking.append(drink.long())
     
        return jsonify({
            "success": True,
            "drinks":drinking
            })
         
    except:
        abort(422)




'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload,id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if  drink is  None :
            abort(404)
    try:
          
        drink.delete()
        
        return jsonify({
            "success":True,
            "deleted":id
        })
    except:
        abort(422)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Drinks not found"
        }), 404

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(401)
def authentication_Error(error):
    
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "unauthenticated  user  you must do login first"
        }), 401


@app.errorhandler(403)
def authentication_Error(error):
    return jsonify({
        "success": False, 
        "error": 403,
        "message": "you have not permisssion to do this action"
        }), 403
@app.errorhandler(400)
def BadRequest_Error(error):
    
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "your request missing data"
        }), 400
@app.errorhandler(AuthError)
def Authe_Error(error):
    #print(error)
    return jsonify({
        "success": False, 
        "error": error.error,
        "message": error.description
        }),error.status_code
   

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
