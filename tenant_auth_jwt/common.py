# Copyright 2020 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import jwt
import functools
from odoo.http import request
from odoo import api
from odoo.tools import SUPERUSER_ID


def get_jwt_token_from_header():
    headers = request.httprequest.environ
    token_raw = headers.get("Authorization")
    return token_raw.partition("Bearer ")[2]


def translate_claims(token, env):
    require = {"require": ["iss", "sub", "exp"]}
    claims = jwt.decode(token, verify=False, options=require)
    backend_model, backend_id = claims["iss"].split(",")
    tenant_model, tenant_id = claims["sub"].split(",")
    backend = env[backend_model].browse(backend_id)
    tenant = env[tenant_model].browse(tenant_id)
    return backend, tenant


def jwt_info():
    token = get_jwt_token_from_header()
    env = api.Environment(request.cr, SUPERUSER_ID, request.context)
    return translate_claims(token, env)


# def use_jwt(fn):
#     return functools.partial(fn, jwt_info)
