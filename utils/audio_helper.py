import torch

def pad_waveforms(waveforms):
    max_len = max([waveform.size(-1) for waveform in waveforms])
    padded_waveforms = []

    for waveform in waveforms:
        padding = max_len - waveform.size(-1)
        padded_waveform = torch.nn.functional.pad(waveform, (0, padding))
        padded_waveforms.append(padded_waveform)

    return torch.stack(padded_waveforms)