import torch
from torch.utils.data import Dataset, DataLoader
import librosa
from dataset.dataset_helper import get_all_audio_files_and_labels
from utils.audio_helper import pad_waveforms


class LibriDatasetDefault(Dataset):

    def __init__(self, main_path, vocab, sr=16000, audio_extension=".flac"):
        self.main_path = main_path
        self.sr = sr
        self.vocab = vocab
        self.audio_path, self.raw_transcripts = get_all_audio_files_and_labels(main_path, audio_extension)
        assert len(self.audio_path) == len(self.raw_transcripts)
        assert len(self.audio_path) != 0

    def __len__(self):
        return len(self.audio_path)

    def __getitem__(self, idx):
        path_idx = self.audio_path[idx]
        raw_transcript = self.raw_transcripts[idx]
        waveform, _ = librosa.load(path_idx, sr=self.sr)
        transcript = self._transcript_cleaning(raw_transcript)
        tokens = self._tokenize(transcript)
        return torch.tensor(waveform), torch.tensor(tokens, dtype=torch.long)

    def _transcript_cleaning(self, raw_transcript):
        # This is the default behaviour to clean the transcript, for other case you can change it
        transcript = raw_transcript.upper()
        transcript = transcript.replace(" ", "|")
        return transcript

    def _tokenize(self, transcript):
        return [self.vocab.lookup_token(token) for token in list(transcript)]



def collate_fn_w2v(batch):
    waveforms, transcriptions = zip(*batch)

    waveform_lengths = torch.tensor([w.size(0) for w in waveforms], dtype=torch.long)
    padded_waveforms = pad_waveforms(waveforms)

    transcription_lengths = torch.tensor([len(t) for t in transcriptions], dtype=torch.long)
    transcriptions = torch.cat(transcriptions)

    return padded_waveforms.squeeze(1), transcriptions, waveform_lengths, transcription_lengths


class LibriDataLoaderDefault(DataLoader):
    def __init__(self, *args, **kwargs):
        super(LibriDataLoaderDefault, self).__init__(*args, **kwargs)
        self.collate_fn = collate_fn_w2v
