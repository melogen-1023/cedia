from db.mysql.audio import AudioDAO
from core.conf.config import config as configuration
import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('./config.ini')
    configuration.load(dbc=config['dbc'], storage=config['storage'])
    audio = AudioDAO()
    audio.insert({
        'album_name': '00',
        'singer_name': '00',
        'audio_id': '000',
        'audio_name': "Live while We\'re Young"
    })
