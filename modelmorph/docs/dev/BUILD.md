# Build Instructions for ModelMorph

## Prerequisites

Before you begin, ensure you have met the following requirements:
- You have installed [Python](https://www.python.org/downloads/) (>= 3.9).
- You have installed [Poetry](https://python-poetry.org/docs/#installation).

## Setting Up the Project

1. **Clone the repository**:
    ```sh
    git clone https://github.com/Butis498/ModelMorph.git
    cd ModelMorph
    ```

2. **Install dependencies**:
    ```sh
    poetry install
    ```

## Building the Project

To build the project, follow these steps:

1. **Build the project**:
    ```sh
    poetry build
    ```

2. **Check the `dist` directory**:
    The built distributions will be located in the `dist` directory.

## Running Tests

To run tests, use the following command:
```sh
poetry run pytest