    """ For multiple files 
    # Returns a tuple of names
    filenames = filedialog.askopenfilenames(initialdir=_thisDir)
    file_list = []
    for file in filenames:
        fs, audio_file = wavfile.read(file)
        file_list.append(audio_file)
    all_files = np.array(file_list,dtype=object)
    sd.play(all_files[0].T,fs)
    """