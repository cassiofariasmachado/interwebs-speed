from datetime import datetime
import os


from services import internet_speed_service
from services import file_service
from utils import get_config, create_logger, format_csv_line


if __name__ == '__main__':
    try:
        config = get_config()

        logger = create_logger()
        logger.info('Starting analyze')
        
        response = internet_speed_service.get_internet_speed()

        download = response.get('download')
        upload = response.get('upload')
        ping = response.get('ping')
        date = datetime.now()

        lines = []

        csv_files_path = config.get('csv_files_path')
        file_name = date.strftime('%m-%Y.csv')
        
        file_path = os.path.join(csv_files_path, file_name)

        file_exists = file_service.exists(file_path)

        if not file_exists:
            lines.append(format_csv_line('download', 'upload', 'ping', 'date'))

        lines.append(format_csv_line(download, upload, ping, date))

        file_service.save_csv(file_path, lines, mode='a')

        logger.info('Analyze completed')
    except Exception as e:
        logger.error(e)

    