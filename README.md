
# Spotify Playlist Downloader

!![Spotify Logo](https://www.scdn.co/i/_global/open-graph-default.png)


## Overview

This project provides a simple way to download Spotify playlists to your local machine using Python. By specifying a playlist URL and an output directory, you can download all songs from the playlist into your chosen folder.

## Features

- Download entire Spotify playlists.
- Save downloaded songs into a specified folder.
- Easy to use with minimal setup.

## Prerequisites

Before using this tool, ensure you have the following installed:

- [Python](https://www.python.org/downloads/) (version 3.6 or higher)
- [SpotDL](https://github.com/spotDL/spotdl) (Spotify Downloader)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/spotify-playlist-downloader.git
   cd spotify-playlist-downloader
   ```

2. **Install SpotDL:**

   You can install SpotDL via pip:

   ```bash
   pip install spotdl
   ```

## Usage

1. **Open your terminal or command prompt.**

2. **Navigate to the project directory.**

3. **Run the script:**

   ```python
   python download_spotify_playlist.py
   ```

4. **Enter the Spotify playlist URL when prompted.**

   The default output folder is `"Downloaded_Songs"`. You can modify this in the script if needed.

## Script Code

Here is the Python script you will be running:

```python
import os

# Function to download a Spotify playlist
def download_spotify_playlist(playlist_url, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Construct the command to download the playlist and save it to the specified folder
    command = f"spotdl {playlist_url} --output \"{output_folder}/%(title)s.%(ext)s\""
    
    # Execute the command
    os.system(command)

# Take user input for the playlist URL
playlist_url = input("Enter the Spotify playlist URL: ")
output_folder = "Downloaded_Songs"

# Download the playlist
download_spotify_playlist(playlist_url, output_folder)
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please contact:

- **Name:** Aditya Kumar Jha
- **LinkedIn:** [Aditya Kumar Jha](https://www.linkedin.com/in/aditya-kumar-jha-b0b669252)


![Python Logo](https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg)
```

