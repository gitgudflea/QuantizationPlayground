import os


def get_all_txt_files(main_folder):
    txt_files = []
    for root, dirs, files in os.walk(main_folder):
        for file in files:
            if file.endswith(".txt"):
                txt_files.append(os.path.join(root, file))
    return txt_files


def generate_audio_path_libri(audio_code, path_directory, audio_extension=".flac"):
    audio_path = os.path.join(path_directory, audio_code + audio_extension)
    if os.path.exists(audio_path):
        return audio_path
    else:
        raise ValueError(f"The path {audio_path} do not exists for directory {path_directory} audio code {audio_code}")


def get_audio_path_and_label_from_transcript(path_transcript, audio_extension):
    audio_paths = list()
    transcripts = list()
    path_directory = os.path.dirname(path_transcript)
    with open(path_transcript) as f:
        for idx, line in enumerate(f.readlines()):
            audio_code, transcript = line.split(' ', 1)
            audio_path = generate_audio_path_libri(audio_code, path_directory, audio_extension)
            transcript = transcript.replace('\n', '')
            audio_paths.append(audio_path)
            transcripts.append(transcript)
    return audio_paths, transcripts


def get_all_audio_files_and_labels(main_folder, audio_extension):
    txt_files = get_all_txt_files(main_folder)
    all_audio_paths = []
    all_transcript = []
    for txt_path in txt_files:
        audio_paths, transcript = get_audio_path_and_label_from_transcript(txt_path, audio_extension)
        all_audio_paths += audio_paths
        all_transcript += transcript
    return all_audio_paths, all_transcript



