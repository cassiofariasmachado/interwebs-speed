import speedtest


def get_internet_speed():
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    return s.results.dict()