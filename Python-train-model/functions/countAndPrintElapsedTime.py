def countAndPrintElapsedTime(start: float,
                             end: float,
                             device=None,
                             plotTime: bool = True,
                             isTrain: bool = True):
    """Prints difference between start and end time.

    Args:
        start (float): Start time of computation (preferred in timeit format).
        end (float): End time of computation.
        device (torch.device [str], optional): Device that compute is running on. Defaults to None.
        plotTime (bool, optional): Whether to print elapsed time or not. Defaults to True.
        isTrain (bool, optional): Specify proper value during printing time. True stands for "Train", false for "Test/eval"

    Returns:
        float: time between start and end in seconds (higher is longer).
    """
    total_time = end - start
    if plotTime:
        print(f"\n{'Train' if isTrain else 'Test/eval'} time on {device}: {total_time:.3f} seconds")
    return total_time
