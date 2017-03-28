import logging
import requests


class Tvst(object):

    def __init__(self, client_id, client_secret, user_agent):
        self.logger = logging.getLogger(__name__)

        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.token = None
        self.session = None

        self.config = {
            'base_uri': 'https://api.tvshowtime.com/v1'
        }

    def _get_auth_infos(self):
        data = {
            'client_id': self.client_id
        }
        return self._post("oauth/device/code", data=data)

    def _get_access_token(self, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
        }
        return self._post("oauth/access_token", data=params)

    def authenticate_user(self, token=None):

        if token:
            self.token = token
        else:
            print('== Requesting tvshowtime.com auth ==')

            auth_infos = self._get_auth_infos()
            accepted = 'n'
            print()
            print('Please do the following to authorize the scrobbler')
            print(
                '* Connect on {auth_url}'.format(auth_url=auth_infos['verification_url']))
            print(
                '* Enter the code: {code}'.format(code=auth_infos['user_code']))

            while accepted.lower() == 'n':
                accepted = input('Have you authorized me [y/N] :')

            try:
                access_token_infos = self._get_access_token(
                    auth_infos['device_code'])
            except Exception as e:
                print(
                    'Unable to send authorization request {error}'.format(error=e))
                return False

            if access_token_infos['result'] != 'OK':
                print('Unable to use authorization request {erroer}').format(
                    error=access_token_infos['message'])
                return False

            self.token = access_token_infos['access_token']

            if not self.session:
                self._start_http_session()

            print()
            print('TVShow Time authorization successful.')
            print('Your token is: {}'.format(self.token))

    def _start_http_session(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})
        if self.token:
            self.session.params['access_token'] = self.token

    def _request(self, request_type, sub_uri, params=None, callback=None, raise_for_status=True, raw=False, **kwargs):

        if not self.session or not self.token:
            self._start_http_session()

        if params:
            kwargs.update(params=params)

        url = "{}/{}".format(self.config['base_uri'], sub_uri)

        response = self.session.request(request_type, url, **kwargs)

        if raise_for_status:
            response.raise_for_status()

        if callback:
            return callback(response)
        elif not response.text and not raw:
            return None
        else:
            return response.content if raw else response.json()

    def _post(self, *args, **kwargs):
        return self._request("post", *args, **kwargs)

    def _get(self, *args, **kwargs):
        return self._request("get", *args, **kwargs)

    def _parse_episode_param(filename=None, episode_id=None, imdb_id=None, show_id=None, season_number=None, episode_number=None):
        # TODO Verification

        params = {}
        if filename:
            params["filename"] = filename
        if episode_id:
            params["episode_id"] = episode_id
        if imdb_id:
            params["imdb_id"] = imdb_id
        if show_id and season_number and episode_number:
            params["show_id"] = show_id
            params["season_number"] = season_number
            params["number"] = episode_number

        return params

    def user(self):
        return self._get("user")

    def to_watch(self, page=None, limit=None, lang=None):
        params = {}
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit
        if lang:
            assert lang in {"en", "fr", "es", "it", "pt"}
            params["lang"] = lang

        return self._get("to_watch", params=params)

    def agenda(self, page=None, limit=None, include_watched=None):
        params = {}
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit
        if include_watched:
            assert include_watched in {True, False, 0, 1, "0", "1"}
            params["include_watched"] = int(include_watched)

        return self._get("agenda", params=params)

    def library(self, page=None, limit=None):
        params = {}
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit

        return self._get("library", params=params)

    def explore(self, page=None, limit=None):
        params = {}
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit

        return self._get("explore", params=params)

    def show(self, show_id=None, show_name=None, include_episodes=None, exact=None):
        # TODO Make verification of parameters

        params = {}
        if show_id:
            params["show_id"] = show_id
        if show_name:
            params["show_name"] = show_name
        if include_episodes:
            params["include_episodes"] = include_episodes
        if exact:
            params["exact"] = exact

        return self._get("show", params=params)

    def follow(self, show_id):
        return self._post("follow", params={"show_id": show_id})

    def is_followed(self, show_id):
        return self._get("follow", params={"show_id": show_id})

    def unfollow(self, show_id):
        return self._post("unfollow", params={"show_id": show_id})

    def archive(self, show_id):
        return self._post("archive", params={"show_id": show_id})

    def is_archived(self, show_id):
        return self._get("archive", params={"show_id": show_id})

    def unarchive(self, show_id):
        return self._post("unarchive", params={"show_id": show_id})

    def save_show_progress(self, show_id, season_number=None, episode_number=None):
        params = {
            "show_id": show_id,
        }

        if season_number:
            params["season"] = season_number
        if episode_number:
            params["episode"] = episode_number

        return self._post("show_progress", data=params)

    def delete_show_progress(self, show_id, season_number=None, episode_number=None):
        params = {
            "show_id": show_id,
        }

        if season_number:
            params["season"] = season_number
        if episode_number:
            params["episode"] = episode_number

        return self._post("delete_show_progress", params=params)

    def episode(self, *args, **kwargs):
        params = self._parse_episode_param(*args, **kwargs)
        return self._get("episode", params=params)

    def checkin(self, *args, **kwargs):
        params = self._parse_episode_param(*args, **kwargs)
        return self._post("checkin", data=params)

    def is_checked(self, *args, **kwargs):
        params = self._parse_episode_param(*args, **kwargs)
        return self._get("checkin", data=params)

    def checkout(self, *args, **kwargs):
        params = self._parse_episode_param(*args, **kwargs)
        return self._post("checkout", data=params)

    def retrieve_progress(self, *args, **kwargs):
        raise NotImplementedError()

    def save_progress(self, *args, **kwargs):
        raise NotImplementedError()

    def set_emotion(self, episode_id, emotion_id):
        assert episode_id in {0, 1, 2, 3, 4, 6,
                              7, "0", "1", "2", "3", "4", "6", "7"}

        params = {
            "episode_id": episode_id,
            "emotion_id": int(emotion_id),
        }

        return self._get("emotion", data=params)

    def delete_emotion(self, episode_id):
        return self._post("delete_emotion", data={"episode_id": episode_id})
