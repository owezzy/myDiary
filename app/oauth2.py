from authlib.flask.oauth2 import AuthorizationServer, ResourceProtector
from authlib.flask.oauth2.sqla import (
create_query_client_func,
create_save_token_func,
create_revocation_endpoint,
create_bearer_token_validator,
)
from authlib.specs.rfc6749 import grants
from werkzeug.security import gen_salt
from .models import db, UserModel
from .models OAuth2Client, OAuth2AutorizationCode, OAuth2Token


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def create_authorization_code(self, client, grant_user, request):
        code = gen_salt(48)
        item = OAuth2AutorizationCode(
            code=code,
            client_id=client.client_id,
            user_id=grant_user.id
        )
        db.session.add(item)
        db.session.commit()
        return code

    def parse_authorization_code(self, code, client):
        item = OAuth2AutorizationCode.query.filter_by(
            code=code, client_id=client.client_id).first()
        if item and not item.is_expired():
            return item

    def delete_authorization_code(self, authorization_code):
        db.session.delete(authorization_code)
        db.session.commit()

    def authenticate_user(self, authorization_code):
        return UserModel.query.get(authorization_code)


class RefreshTokenGrant(grants.RefreshTokenGrant):
    def authenticate_refresh_token(self, refresh_token):

