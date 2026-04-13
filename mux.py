from muxtools import Setup, GlobSearch, SubFile, mux, Premux, Chapters, ASSHeader


def make_mux(x):
    setup = Setup(f"{x:02}", config_file="config.ini")

    webdl = GlobSearch(f"./{setup.episode}/*-ToonsHub.mkv")

    premux = Premux(
        webdl,
        video=-1,
        audio=-1,
        subtitles=None,
        keep_attachments=False,
        mkvmerge_args='--no-global-tags --track-name 0:"1080p H.264 WEB-DL [CR]" --track-name 1:"Japanese 2.0 AAC [CR]" --track-name 2:"English 2.0 AAC [CR]" --language 0:und --language 1:jpn --language 2:eng --default-track-flag 0:1 --default-track-flag 1:1 --default-track-flag 2:1 --original-flag 1:1',
    )

    dialogue = SubFile(f"./{setup.episode}/WHA - {setup.episode} - Dialogue.ass")

    ts = SubFile(f"./{setup.episode}/WHA - {setup.episode} - Signs.ass")

    full = dialogue.merge(ts)

    dubtitles = SubFile.from_srt(
        f"./{setup.episode}/WHA - {setup.episode} - Dubtitles.srt"
    ).merge(ts)

    #japanese = SubFile(f"./{setup.episode}/WHA - {setup.episode} - Japanese.ass")

    chapters = Chapters.from_sub(full)

    #full, dubtitles, ts, japanese = [
    full, dubtitles, ts = [
        x.set_headers(
            (ASSHeader.PlayResX, 1920),
            (ASSHeader.PlayResY, 1080),
            (ASSHeader.LayoutResX, 1920),
            (ASSHeader.LayoutResY, 1080),
            (ASSHeader.ScaledBorderAndShadow, True),
            (ASSHeader.WrapStyle, 0),
            (ASSHeader.YCbCr_Matrix, "TV.709"),
        )
        .clean_styles()
        .clean_garbage()
        #for x in (full, dubtitles, ts, japanese)
        for x in (full, dubtitles, ts)
    ]

    fonts = full.collect_fonts(use_system_fonts=True)

    #jp_fonts = japanese.collect_fonts(use_system_fonts=False)

    mux(
        premux,
        full.to_track(name="Full Subtitles [Chika]", lang="eng"),
        dubtitles.to_track(name="Dubtitles [NF]", lang="eng", default=False),
        ts.to_track(
            name="Signs & Songs [Chika]", lang="en", default=False, forced=True
        ),
        #japanese.to_track(
        #    name="Japanese Subtitles [SonicMaster]", lang="jpn", default=False
        #),
        chapters,
        *fonts,
        #*jp_fonts,
    )


ep = int(input("Enter episode number: "))

make_mux(ep)
