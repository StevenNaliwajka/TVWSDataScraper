def write_data_thread(read_data_event, write_data_event, outfile_list):
    # log data every time write_data_event pulls high
    # for output_type in outfile_list:

    while 1:
        # Wait till set by the update_data_thread
        write_data_event.wait()
        print("(WriteDataThread): Writing data.")
        read_data_event.clear()
        write_data_event.clear()

        for outfile in outfile_list:
            # Write to all outfile
            outfile.write_to_outfile()
        read_data_event.set()