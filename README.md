# Local Knowledge Base for Serverless Application Documentation

This project aims to create a local knowledge base for a development team working on a serverless application using AWS Lambda for the backend and React for the frontend. The knowledge base is built by scraping and structuring relevant documentation, which can later be queried using an LLM-powered system.

## Requirements

Before running the scripts, ensure that the following dependencies are installed:

### 1. **Python 3.x**:

- Make sure you have Python 3.x installed. You can download it from the [official Python website](https://www.python.org/downloads/).

### 2. **Python Libraries**:

- Install the required Python libraries by running:
  ```bash
  pip install -r requirements.txt
  ```

## Project Structure

- `reactscraper/`: Contains the Python script `reactscraper.py` for scraping React-related documentation.
- `awsscraper/`: Contains the Scrapy spider `awslearnspider` for scraping AWS Lambda-related documentation.
- `react.json`: Output file containing the scraped React documentation.
- `aws.json`: Output file containing the scraped AWS Lambda documentation.
- `combined.json`: Final file that combines the content from `react.json` and `aws.json`.

## How to Run the Script

### 1. **Clone the Repository**:

First, clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-name>
```

### 1. **Run the Script**:

The main script that runs the entire scraping and combining process is `main.py`. To run it, execute the following command:

```bash
python main.py
```

This will:

- Scrape React documentation by running `reactscraper.py`.
- Scrape AWS Lambda documentation using Scrapy (`awslearnspider`).
- Merge both `react.json` and `aws.json` into a single file called `combined.json`.

### 3. **Check the Output**:
After running the script, the merged content will be saved in the `combined.json` file located in the root directory.

