# Interwebs speed

Interwebs Speed is a Python project that monitors and logs internet download, upload, and ping speeds to a CSV file, helping users track performance and identify trends.

## Used Technologies

The project utilizes the following key technologies:

- **Python**: The core programming language (version 3.9 or higher).
- **Poetry**: For dependency management and project packaging.
- **speedtest-cli**: A command-line interface for testing internet bandwidth.
- **Typer**: A library for building command-line applications.
- **python-dotenv**: For loading environment variables from `.env` files.

## Available CLI Commands

The `interwebs-speed` command-line interface provides the following commands:

- `interwebs-speed analyze`: Runs the internet speed analysis and saves the data.
- `interwebs-speed summary [--previous-month / -p]`: Sends a monthly summary email. Use `--previous-month` or `-p` to send the summary for the previous month.
- `interwebs-speed --version / -v`: Shows the application's version and exits.

## How to run

### Local env

This project uses [Poetry](https://python-poetry.org) for dependency management.

1.  **Install Poetry**: Follow the instructions on the [official website](https://python-poetry.org/docs/#installation).
2.  **Install dependencies**:
    ```bash
    poetry install
    ```
3.  **Run the application**:
    ```bash
    poetry run interwebs-speed analyze
    ```
    or to send a monthly summary:
    ```bash
    poetry run interwebs-speed summary
    ```

### Using Docker & Docker Compose

You can run the application using Docker & Docker Compose.

1.  **Build and run**:
    ```bash
    docker-compose up --build
    ```
    This will build the Docker image and start the `interwebs-speed` service. By default, it will execute the `analyze` command.
2.  **Data Volume**: The `./data` directory on your host machine will be mounted into the container at `/app/data` to store CSV files.
3.  **Configuration**: Environment variables (e.g., `CSV_FILES_PATH`, `SMTP_HOST`, etc.) can be set in a `.env` file in the project root, which will be used by the `docker-compose.yml`.


## How to install

### Using Helm

The project can be installed as a Helm chart using the provided scripts.

1.  **Install**:
    ```bash
    ./tools/scripts/install.sh
    ```
    This script will install the Helm chart named `interwebs-speed` from the `tools/helm` directory, setting various configuration values from a `.env` file (which you'll need to create with the necessary environment variables).

2.  **Uninstall**:
    ```bash
    ./tools/scripts/uninstall.sh
    ```
    This script will uninstall the `interwebs-speed` Helm chart.


## References

- [Poetry: Basic Usage](https://python-poetry.org/docs/basic-usage)
- [Blazing fast Python Docker builds with Poetry 🏃](https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0)
