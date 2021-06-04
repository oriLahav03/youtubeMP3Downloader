from __future__ import unicode_literals
import youtube_dl
import tkinter as tk
from tkinter import filedialog

from pytube import Playlist


def introduction():
    """
    The function prints the introduction
    :return: None
    """
    msgs = [
        '---------- Youtube MP3 downloader ----------',
        '         © Program created by Ori ©\n',
        'Follow the next steps:',
        '1. Select the file that contain all the youtube links (1 link in every line)(.txt).',
        '2. Select the folder you want all the audio files to be save to.\n'
    ]
    print('\n'.join(msgs))


def get_user_choices():
    """
    The function take input from user about the links file and save location
    :return: all the information
    """
    file_links_location = choose_file_dialog()
    links = get_list_of_links(file_links_location)
    save_location = save_folder_dialog()
    if save_location == '':
        print('Downloading canceled!')
        exit()
    else:
        print('Links taken from: ', file_links_location)
        print('files saves to: ', save_location)
    print()
    return file_links_location, links, save_location


def save_folder_dialog():
    """
    Open a dialog that let the user choose the saving folder path
    :return: the folder path
    """
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    root.destroy()
    return folder_path


def choose_file_dialog():
    """
    Open a dialog that let the user choose the links file path
    :return: the file path
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[('TXT', '*.txt')])
    root.destroy()
    return file_path


def get_list_of_links(file_path):
    """
    The function make list of all the links from the file
    :param file_path: the links file path
    :return: list with all the links
    """
    if file_path != '':
        try:
            with open(file_path, 'r') as links_file:
                return [i.replace(' ', '').replace('\n', '') for i in links_file.readlines() if i != '\n']
        except FileNotFoundError as e:
            print(e)
            exit()
    else:
        print('Downloading canceled!')
        exit()


def download_video(index, link, save_location):
    """
    The function download the video from youtube
    :param index: the index of the video
    :param link: the link to the video
    :param save_location: the location to save the video
    :return: None
    """
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': save_location + '/%(title)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            print(f'{index} » has been successfully downloaded')

    except youtube_dl.utils.DownloadError:
        print(index, '» There was an error with the link:', link)
    except Exception as e:
        print(e)


def save_file(links, save_location):
    """
    The function save every audio file from every link
    :param links: the youtube links list
    :param save_location: the location to save the file to
    :return: None
    """
    index = 1
    for link in links:

        # url input from user
        try:
            playlist = Playlist(link)
            # extract only audio
            for url in playlist.video_urls:
                download_video(index, url, save_location)
                index += 1

        except KeyError:
            download_video(index, link, save_location)
            index += 1


def main():
    introduction()
    file_links_location, links, save_location = get_user_choices()
    save_file(links, save_location)
    input(f'\nDone saving all files at: {save_location}')


if __name__ == "__main__":
    main()
