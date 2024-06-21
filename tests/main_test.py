import json

import pytest
from fastapi import status
import sqlalchemy as sql
import db_models as db


class TestRegisterAuthFlow:
    @pytest.mark.anyio
    async def test_auth(self, async_client, async_session):
        test_username = 'new_test_user'
        test_password = 'test_password'
        test_email = 'testemail@email.com'
        register_response = await async_client.post('/auth/register', json={'username': test_username,
                                                                            'password': test_password,
                                                                            'email': test_email})
        assert register_response.status_code == 201

        user_query = await async_session.execute(sql.select(db.User).filter_by(username=test_username).limit(1))
        user = user_query.scalars().one_or_none()
        assert user is not None

        verify_response = await async_client.post('/auth/verify', json={'user_guid': str(user.guid)})
        assert verify_response.status_code == 200

        login_response = await async_client.post('/auth/token', data={'username': test_username,
                                                                      'password': test_password})
        assert login_response.status_code == 200

        response_user_data = await async_client.get('/email', cookies=login_response.cookies)
        assert response_user_data.status_code == 200, response_user_data.text
        assert response_user_data.json() == test_email


class TestSuperuserRights:
    @pytest.mark.anyio
    async def test_superuser_not_allowed(self, async_client, user_cookie):
        users_resp = await async_client.get('/superuser/users/all', cookies=user_cookie)
        assert users_resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.anyio
    async def test_superuser_good(self, async_client, superuser_cookie):
        users_resp = await async_client.get('/superuser/users/all', cookies=superuser_cookie)
        assert users_resp.status_code == status.HTTP_200_OK
        assert len(users_resp.json()) > 0
