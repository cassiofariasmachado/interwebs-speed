import speedtest

from interwebs_speed.core.analisys import Analysis


def get_internet_speed() -> Analysis:
    s = speedtest.Speedtest()

    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()

    response = s.results.dict()

    download = response.get('download')
    upload = response.get('upload')
    ping = response.get('ping')

    return Analysis(download, upload, ping)
