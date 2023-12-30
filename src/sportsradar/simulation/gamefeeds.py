import requests
from src.sportsradar.simulation.available_recordings import AvailableRecordings
from src.sportsradar.simulation.session import create_session
from src.sportsradar.simulation.config import Config

GAME_FEEDS_TYPE = "replay"


class GameFeeds:
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.game_feeds = "replay"

    def get_available_recordings(self):
        av_rec = AvailableRecordings(base_url=f"{self.base_url}/graphql")
        query = av_rec.construct_query()
        recording_id = av_rec.post_json_data(query)
        return recording_id.json()["data"]["recordings"][0]["id"]

    def get_session(self, recording_id):
        session = create_session(
            url=f"{self.base_url}/graphql", recording_id=recording_id
        )
        return session.json()["data"]["createSession"]


def get_game_boxscore(recording_id, session_id):
    url = f"{Config.BASE_URL}/{GAME_FEEDS_TYPE}/{Config.LEAGUE}/{recording_id}?feed=boxscore&contentType={Config.CONTENT_TYPE}&sessionId={session_id}"
    response = requests.get(url=url)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code: {response.status_code}")
    return response.json()


def get_game_info(recording_id, session_id):
    url = f"{Config.BASE_URL}/{GAME_FEEDS_TYPE}/{Config.LEAGUE}/{recording_id}?feed=game&contentType={Config.CONTENT_TYPE}&sessionId={session_id}"
    response = requests.get(url=url)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code: {response.status_code}")
    return response.json()


def get_pbp_info(recording_id, session_id):
    url = f"{Config.BASE_URL}/{GAME_FEEDS_TYPE}/{Config.LEAGUE}/{recording_id}?feed=pbp&contentType={Config.CONTENT_TYPE}&sessionId={session_id}"
    response = requests.get(url=url)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code: {response.status_code}")
    return response.json()


def get_game_roster(recording_id, session_id):
    url = f"{Config.BASE_URL}/{GAME_FEEDS_TYPE}/{Config.LEAGUE}/{recording_id}?feed=rosters&contentType={Config.CONTENT_TYPE}&sessionId={session_id}"
    response = requests.get(url=url)
    print(response)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code: {response.status_code}")
    return response.json()


# Usage
# game_feeds = GameFeeds()
# rec_id = game_feeds.get_available_recordings()
# session_id = game_feeds.get_session(recording_id=rec_id)
# game_feeds_data = {'rec_id': rec_id, 'session_id': session_id}
# game_boxscore = get_game_boxscore(recording_id=game_feeds_data['rec_id'], session_id=game_feeds_data['session_id'])
# game_info = get_game_info(recording_id=game_feeds_data['rec_id'], session_id=game_feeds_data['session_id'])
# game_rosters = get_game_roster(recording_id=game_feeds_data['rec_id'], session_id=game_feeds_data['session_id'])
