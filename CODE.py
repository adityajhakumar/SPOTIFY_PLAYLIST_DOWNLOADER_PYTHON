!pip install spotdl
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
