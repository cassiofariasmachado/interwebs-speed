import os
from interwebs_speed.services import file_service, internet_speed_service, mail_service
from interwebs_speed.utils import create_logger, format_csv_line, get_config


def analyze():
    try:
        config = get_config()
        logger = create_logger()

        logger.info('Starting analyze')

        analysis = internet_speed_service.get_internet_speed()

        lines = []

        csv_files_path = config.get('csv_files_path')
        expected_download = config.get('expected_download')
        expected_upload = config.get('expected_upload')

        file_name = analysis.date.strftime('%m-%Y.csv')

        file_path = os.path.join(csv_files_path, file_name)

        file_exists = file_service.exists(file_path)
        file_mode = 'a'

        if not file_exists:
            file_mode = 'w'
            lines.append(format_csv_line('download', 'upload', 'ping', 'date'))

        if analysis.is_under_expected(expected_download, expected_upload):
            logger.info('Download or upload is under expected.')

            message = analysis.mount_analysis_mail(
                expected_download, expected_upload)

            mail_service.send_email(
                config, 'Internet Speed oscilation alert', message)
        else:
            logger.info('Download and upload are normal.')

        lines.append(format_csv_line(analysis.download,
                     analysis.upload, analysis.ping, analysis.date))

        file_service.save_csv(file_path, lines, mode=file_mode)

        logger.info('Analyze completed')
    except Exception as e:
        logger.error(e)
