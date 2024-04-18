"""
This file is used to create an instance of the Executor class from the flask_executor package.
This instance is used to create a background task that will run the evaluator.
This is done to prevent the server from being blocked while the model is being trained.
"""

from flask_executor import Executor

executor = Executor()
