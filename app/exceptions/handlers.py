from flask import render_template
from app.exceptions import exceptions
from app.exceptions.custom_exception import CustomException
   
# @exceptions.app_errorhandler(404)
# def not_found_error(error): 
#     print("404 error")
#     return render_template("404.html"), 404


# @exceptions.app_errorhandler(500)
# def internal_error(error):
#     print("500 error")
#     return render_template("500.html"), 500

