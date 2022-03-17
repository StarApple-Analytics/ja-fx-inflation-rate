from flask import Blueprint
from api.controllers.TimeseriesController import index



timeseries_rates_bp  = Blueprint('timeseries', __name__)


# CRUD routes
timeseries_rates_bp.route('/timeseries/rates', methods=['GET'])(index)