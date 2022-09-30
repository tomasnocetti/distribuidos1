import logging

from common.message import MessageEnd, VideoMessage
from common.worker import Worker


class LikesFilter(Worker):
    def __init__(self, middleware) -> None:
        super().__init__(middleware)

    def run(self):
        self.middleware.recv_video_message(self.recv_videos)

    def recv_videos(self, message):

        if MessageEnd.is_message(message):
            logging.info(
                f'Finish Recv Videos')

            self.middleware.send_video_message(message)
            return

        video = VideoMessage.decode(message)

        try:
            if (video.content['likes'] != None and int(video.content['likes']) > 5000000):
                self.middleware.send_video_message(message)
        except KeyError:
            logging.error(
                f'Key likes not found in {message.content}')
        except ValueError:
            logging.error(
                f'Data not formatted correctly {message.content}')