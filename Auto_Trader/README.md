# Automated Trading Script using Selenium

This Python script automates trading operations on a web page using Selenium. It interacts with the webpage to place bets based on certain conditions and data extracted from the site.

## Getting Started

### Prerequisites

-   Python 3.x
-   Selenium
-   WebDriver (compatible with your browser)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/automated-trading-script.git
    ```

2. Install the required dependencies using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

### Requirements

The following Python packages are required for running the script:

```plaintext
selenium
pandas
```

### Browser Compatibility

The script Webdriver is compatible with this Chrome browser version:

-   Version 128.0.6613.139 (Official Build) (64-bit)

### ChromeDriver Location

The Webdriver(ChromeDriver) executable is located in the `chrome_driver` directory.
<br>To ensure it run successfully make sure to use a compactable webdriver for your browser:

-   `chrome_driver/chromedriver.exe`

## Usage

1. Update the script with your specific XPaths, stake amounts, and other parameters as needed.

2. Run the script:

    ```bash
    python automated_trading_script.py
    ```

3. The script will automate the trading process based on the defined conditions.

## Features

-   Automated trading based on predefined conditions.
-   Exception handling for common issues like button click interception.
-   Data collection and storage in a CSV file for analysis.
