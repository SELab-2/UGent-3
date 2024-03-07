"""
This module contains the functions to interact with the database. It contains functions to
delete, insert and query entries from the database. The functions are used by the routes
to interact with the database.
"""

from typing import Dict, List, Union
from urllib.parse import urljoin
from flask import jsonify
from sqlalchemy import and_
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.query import Query
from sqlalchemy.exc import SQLAlchemyError
from project.db_in import db
from project.utils.misc import map_all_keys_to_url, models_to_dict, filter_model_fields

def delete_by_id_from_model(
        model: DeclarativeMeta,
        column_name: str,
        column_id: int,
        base_url: str):
    """
    Deletes an entry from the database giving the model corresponding to a certain table,
    a column name and its value.

    Args:
        model: DeclarativeMeta - The model corresponding to the table to delete from.
        column_name: str - The name of the column to delete from.
        id: int - The id of the entry to delete.

    Returns:
        A message indicating that the resource was deleted successfully if the operation was
        successful, otherwise a message indicating that something went wrong while deleting from
        the database.
    """
    try:
        result: DeclarativeMeta = model.query.filter(
            getattr(model, column_name) == column_id
            ).first()

        if not result:
            return {
                "message": "Resource not found",
                 "url": base_url}, 404
        db.session.delete(result)
        db.session.commit()
        return {"message": "Resource deleted successfully",
                "url": base_url}, 200
    except SQLAlchemyError:
        return {"error": "Something went wrong while deleting from the database.",
                "url": base_url}, 500

def insert_into_model(model: DeclarativeMeta,
                      data: Dict[str, Union[str, int]],
                      response_url_base: str,
                      url_id_field: str,
                      required_fields: List[str] = None):
    """
    Inserts a new entry into the database giving the model corresponding to a certain table
    and the data to insert.

    Args:
        model: DeclarativeMeta - The model corresponding to the table to insert into.
        data: Dict[str, Union[str, int]] - The data to insert into the table.
        response_url_base: str - The base url to use in the response.

    Returns:
        The new entry inserted into the database if the operation was successful, otherwise
        a message indicating that something went wrong while inserting into the database.
    """
    try:
        if required_fields is None:
            required_fields = []
        # Check if all non-nullable fields are present in the data
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {"error": f"Missing required fields: {', '.join(missing_fields)}",
                    "url": response_url_base}, 400

        filtered_data = filter_model_fields(model, data)
        new_instance: DeclarativeMeta = model(**filtered_data)
        db.session.add(new_instance)
        db.session.commit()
        return jsonify({
                "data": new_instance,
                "message": "Object created succesfully.",
                "url": urljoin(response_url_base, str(getattr(new_instance, url_id_field)))}), 201
    except SQLAlchemyError as e:
        print("error")
        print(e)
        return jsonify({"error": "Something went wrong while inserting into the database.",
                "url": response_url_base}), 500

def query_selected_from_model(model: DeclarativeMeta,
                              response_url: str,
                              url_mapper: Dict[str, str] = None,
                              select_values: List[str] = None,
                              filters: Dict[str, Union[str, int]]=None):
    """
    Query entries from the database giving the model corresponding to a certain table and
    the filters to apply to the query.


    Args:
        model: DeclarativeMeta - The model corresponding to the table to query from.
        response_url: str - The base url to use in the response.
        url_mapper: Dict[str, str] - A dictionary to map the keys of the response to urls.
        select_values: List[str] - The columns to select from the table.
        filters: Dict[str, Union[str, int]] - The filters to apply to the query.
    
    Returns:
        The entries queried from the database if they exist, otherwise a message indicating
        that the resource was not found.
    """
    try:
        query: Query = model.query
        if filters:
            filtered_filters = filter_model_fields(model, filters)
            conditions: List[bool] = []
            for key, value in filtered_filters.items():
                conditions.append(getattr(model, key) == value)
            query = query.filter(and_(*conditions))

        if select_values:
            query = query.with_entities(*[getattr(model, value) for value in select_values])
            query_result = query.all()
            results = []
            for instance in query_result:
                selected_instance = {}
                for value in select_values:
                    selected_instance[value] = getattr(instance, value)
                results.append(selected_instance)
        else:
            results = models_to_dict(query.all())
        if url_mapper:
            results = map_all_keys_to_url(url_mapper, results)
        response = {"data": results,
                    "message": "Resources fetched successfully",
                    "url": response_url}
        return jsonify(response), 200
    except SQLAlchemyError:
        return {"error": "Something went wrong while querying the database.",
                "url": response_url}, 500

def query_by_id_from_model(model: DeclarativeMeta,
                           column_name: str,
                           column_id: int,
                           base_url: str):
    """
    Query an entry from the database giving the model corresponding to a certain table,
    a column name and its value.

    Args:
        model: DeclarativeMeta - The model corresponding to the table to query from.
        column_name: str - The name of the column to query from.
        id: int - The id of the entry to query.
        not_found_message: str - The message to return if the entry is not found.
    
    Returns:
        The entry queried from the database if it exists, otherwise a message indicating
        that the resource was not found.

    """
    try:
        result: Query = model.query.filter(getattr(model, column_name) == column_id).first()
        if not result:
            return {"message": "Resource not found", "url": base_url}, 404
        return jsonify({
            "data": result,
            "message": "Resource fetched correctly",
            "url": urljoin(base_url + "/", str(column_id))}), 200
    except SQLAlchemyError:
        return {
            "error": "Something went wrong while querying the database.",
            "url": base_url}, 500

def patch_by_id_from_model(model: DeclarativeMeta,
                           column_name: str,
                           column_id: int,
                           base_url: str,
                           data: Dict[str, Union[str, int]]):
    """
    Update an entry from the database giving the model corresponding to a certain table,
    a column name and its value.

    Args:
        model: DeclarativeMeta - The model corresponding to the table to update.
        column_name: str - The name of the column to update.
        id: int - The id of the entry to update.
        data: Dict[str, Union[str, int]] - The data to update the entry with.

    Returns:
        The entry updated from the database if the operation was successful, otherwise
        a message indicating that something went wrong while updating the entry.
    """
    try:
        result: Query = model.query.filter(getattr(model, column_name) == column_id).first()
        if not result:
            return {"message": "Resource not found", "url": base_url}, 404
        for key, value in data.items():
            setattr(result, key, value)
        db.session.commit()
        return jsonify({
            "data": result,
            "message": "Resource updated successfully",
            "url": urljoin(base_url + "/", str(column_id))}), 200
    except SQLAlchemyError:
        return {"error": "Something went wrong while updating the database.",
                "url": base_url}, 500
