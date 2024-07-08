    #print(f"The shape of wgn_matrix: {wgn_matrix.T.shape}")

    #NEW = np.vstack([wgn_matrix[0],wgn_matrix[1],wgn_matrix[2]])

    #sd.play(NEW.T, fs, mapping=[2,4,6])



      """ Spectral analysis of calibration noise.
    # Plot time waveform - original
    plt.subplot(2,2,1)
    plt.plot(wgn)
    plt.title("Time Waveform - Original")
    # Plot FFT - original
    xf, yf = ts.doFFT(wgn,fs)
    plt.subplot(2,2,2)
    plt.plot(xf,yf)
    plt.title("FFT - DC Offset")

    # Remove DC offset
    wgn_no_dc = wgn - np.mean(wgn)
    print(np.mean(wgn))

    # Plot time waveform - DC removed
    plt.subplot(2,2,3)
    plt.plot(wgn_no_dc)
    plt.title("Time Waveform - DC Removed")
    # Plot FFT - DC removed
    plt.subplot(2,2,4)
    xf, yf = ts.doFFT(wgn_no_dc,fs)
    plt.plot(xf,yf)
    plt.title("FFT - DC Removed")
    plt.show()
    # Plot density to ensure Gaussian distribution
    df = pd.Series(wgn_no_dc)
    df.plot.density()
    plt.show()
    """


    