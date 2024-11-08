
from pytube import YouTube, Playlist
import logging
import os
import soundfile as sf
logging.basicConfig(level=logging.INFO)



def download_audio(vidoe_url):
    # the try statement to excute the download the video code
    # getting video url from entry
    # checking if the entry and combobox is empty
    if vidoe_url == '':
        # display error message when url entry is empty
        logging.error(msg='Please enter the MP3 URL')
    # else let's download the audio file
    else:
        # this try statement will run if the mp3 url is filled
        try:

            # creating the YouTube object and passing the the on_progress function
            audio = YouTube(vidoe_url)
            # extracting and downloading the audio file
            output = audio.streams.get_audio_only().download()
            # this splits the audio file, the base and the extension
            base, ext = os.path.splitext(output)
            # this converts the audio file to mp3 file
            # new_file = base + '.mp3'
            new_file = 'audio.mp3'
            # this renames the mp3 file
            os.rename(output, new_file)
            # popup for dispalying the mp3 downlaoded success message
            logging.info(msg=f'{base} MP3 has been downloaded successfully.')
            return new_file
        except:
            logging.error(msg='An error occurred while trying to ' \
                              'download the MP3\nThe following could ' \
                              'be the causes:\n->Invalid link\n->No internet connection\n' \
                              'Make sure you have stable internet connection and the MP3 link is valid')
            # ressetting the progress bar and the progress label
            # progress_label.config(text='')
            # progress_bar['value'] = 0


def get_playlist_video_urls(playlist_url):
    """
    Retrieves a list of video URLs from a given YouTube playlist URL.

    Args:
    playlist_url (str): URL of the YouTube playlist.

    Returns:
    list: A list of video URLs from the playlist.
    """
    try:
        playlist = Playlist(playlist_url)
        return playlist.video_urls
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def get_video_title(video_url):
    """
    Retrieves the title of a YouTube video.

    Args:
    video_url (str): URL of the YouTube video.

    Returns:
    str: Title of the YouTube video.
    """
    try:
        video = YouTube(video_url)
        return video.title
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


def get_audio_transcript(filename):
    """
    Retrieves the transcript of a YouTube video.

    Args:
    video_url (str): URL of the YouTube video.

    Returns:
    str: Transcript of the YouTube video.
    """
    # initialize the recognizer
    r = sr.Recognizer()
    # open the file
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source, duration=120)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language='en-US', show_all=True)
        return text

def wav_it(filename):
    """
    Converts an audio file to a .wav file.

    Args:
    filename (str): Name of the audio file to be converted.

    Returns:
    str: Name of the converted .wav file.
    """
    try:
        x,_ = librosa.load(filename, sr=16000)
        sf.write('tmp.wav', x, 16000)
        print('completed')
        return 'completed'
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


if __name__ == '__main__':
    url = 'https://youtu.be/w7scynkCLBU?si=pOy1BmJIjxd7HR5M'
    # print(f"Title: {get_video_title(url)}")
    file_name = download_audio(url)
    #from wav_it import wav_it
    #wav_it('audio.wav')
    #audio_transcript = get_audio_transcript('tmp.wav')
    #transcripts = [item['transcript'] for item in audio_transcript['alternative']]
    #full_transcript = ' '.join(transcripts)
    #print(full_transcript)
