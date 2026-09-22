# ArtistRadio
A next-generation AutoDJ and Internet Radio Engine written in Python. ArtistRadio automatically builds artist-based radio stations from your music library and streams them to Icecast.


## Streaming

ArtistRadio can publish the same local audio mix to Icecast through a Windows virtual audio cable. FFmpeg captures the cable recording device with DirectShow and encodes MP3 for Icecast. Configure the virtual cable first, then enable streaming in `src/config.py`.
