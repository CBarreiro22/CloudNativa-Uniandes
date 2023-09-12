from .erros.errors import ApiError
@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "mssg": err.description,
        #"version": os.environ["VERSION"]
    }
    return jsonify(response), err.code
