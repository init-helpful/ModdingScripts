## BatchModDownloader
This Python script is designed to automatically download and optionally unzip files from a list of URLs. The script reads a configuration file (`config.json`) to get the list of URLs and other settings, then performs the download and unzipping tasks asynchronously. It's particularly useful for batch downloading and extracting zip files from various sources.

## Requirements
- Python 3.6 or higher
- aiohttp
- asyncio

### Releases
For users who prefer not to run the script from source, there is an executable version available in the [Releases](https://github.com/init-helpful/ModdingScripts/releases) section of this repository. This executable is packaged with all necessary dependencies and can be run directly without setting up a Python environment.

### Run Python Script Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/init-helpful/ModdingScripts.git
   cd ModdingScripts
   ```

2. Set up a Virtual Environment (Optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Unix or MacOS
   venv\Scripts\activate  # For Windows
   ```
3. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```
 
## Config File Properties
Edit the `config.json` file to specify the URLs, the regular expression for parsing the URLs, and paths for saving zipped and unzipped files.

1. **`zip_name_regex`**:
   - **Description**: A regular expression (regex) used to parse URLs in the `urls` list. It's primarily used to extract specific parts or identifiers from these URLs, which are often utilized for naming the downloaded files.
   - **Example Usage**: If the regex is `"resources/(.*?)\\."`, and the URL is `http://example.com/resources/file1.zip`, the script will extract `file1` as the identifier.

2. **`urls`**:
   - **Description**: This property lists the URLs from which the script will download files. Each URL should directly point to a downloadable file, usually a `.zip` file.
   - **Example Usage**: `["http://example.com/file1.zip", "http://example.com/file2.zip"]`. The script will download `file1.zip` and `file2.zip` from these URLs.

3. **`zipped_path`**:
   - **Description**: Specifies the directory path where the downloaded zip files will be stored. The script creates this directory if it doesn't already exist.
   - **Example Usage**: With `"./zipped"`, downloaded zip files will be stored in a folder named `zipped` in the same directory as the script.

4. **`unzipped_path`**:
   - **Description**: Indicates the directory path where the contents of the downloaded zip files will be extracted. This directory is also created by the script if it does not exist.
   - **Example Usage**: If set to `"./unzipped"`, the script will extract the contents of each zip file into a folder named `unzipped`, located in the script's directory.

Example `config.json`:
```json
{
    "zip_name_regex": "resources/(.*?)\\.",
    "urls": ["http://example.com/file1.zip", "http://example.com/file2.zip"],
    "zipped_path": "./zipped",
    "unzipped_path": "./unzipped"
}
```





## Additional Notes

- **Asynchronous Operations**: The script downloads and unzips files asynchronously, making it efficient for handling multiple files.
- **Regular Expression Matching**: Ensure that the regular expression in the `config.json` file correctly matches the format of your URLs. This is crucial for the script to correctly identify and process the files.
