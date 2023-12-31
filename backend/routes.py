from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return array of  pictures url"""
    pic_array = []
    if data:
        for pic in data:
            if pic["pic_url"]:
                pic_array.append(pic["pic_url"])
        return jsonify(pic_array), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """return json with picture info"""
    if data:
        for pic in data:
            if pic["id"] == id:
                return pic, 200
    return {"message": "Picture not Found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """create a new pic in data"""
    req_body = request.get_json()
    for pic in data:
        if pic["id"] == req_body["id"]:
            return {"Message": f"picture with id {pic['id']} already present"}, 302
    data.append(req_body)
    return req_body, 201
    

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    for i,pict in enumerate(data):
        if pict['id']==id:
            data[i]=request.json
            return request.json, 200
    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i,pict in enumerate(data):
        if pict['id']==id:
            temp=pict
            data.pop(i)
            return temp, 204
    return {"message": "picture not found"}, 404