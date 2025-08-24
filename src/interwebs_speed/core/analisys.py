from datetime import datetime
from interwebs_speed.utils import bytes_to_mb


class Analysis:

    def __init__(self, download: float, upload: float, ping: float):
        self.download = download
        self.upload = upload
        self.ping = ping
        self.date = datetime.now()

    def is_under_expected(self, expected_download: float, expected_upload: float) -> bool:
        return self.download_is_under_expected(expected_download) or self.upload_is_under_expected(expected_upload)

    def download_is_under_expected(self, expected_download: float) -> bool:
        return self.download < expected_download

    def upload_is_under_expected(self, expected_upload) -> bool:
        return self.upload < expected_upload

    def mount_analysis_mail(self, expected_download: float, expected_upload: float):
        message = ''

        if (self.download_is_under_expected(expected_download)):
            message += 'Download is under expected, please check it.\n'

        if (self.upload_is_under_expected(expected_upload)):
            message += 'Upload is under expected, please check it.\n'

        message += f'- Download: {bytes_to_mb(self.download)} MB\n'
        message += f'- Upload: {bytes_to_mb(self.upload)} MB\n'
        message += f'- Ping: {self.ping} ms\n'

        return message
