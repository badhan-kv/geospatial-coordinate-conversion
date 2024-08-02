def sp32satcsv(file_path, output_file_path,sat_id):
    """
    Read a file, remove lines that do not start with 'PG05', replace spaces with commas, add a time column,
    and write the result to a new CSV file.

    :param file_path: Path to the input file.
    :param output_file_path: Path to the output CSV file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(output_file_path, 'w') as output_file:
        # Write the header
        header = "time,satellite id,x in m,y in m,z in m,clock error,x-sdev,y-sdev,z-sdev,c-sdev\n"
        output_file.write(header)

        time = 0
        for line in lines:
            if line.startswith(sat_id):
                # Normalize spaces and replace them with commas
                normalized_line = ','.join(line.split())
                # Write the line with the time column
                output_file.write(f"{time},{normalized_line}\n")
                time += 15  # Increment time by 15

if __name__ == "__main__":
    # Example usage
    input_file_path = 'jpl22430.sp3'
    output_file_path = r'C:\Users\KhushaldasBadhan\OneDrive - ODYSSEUS SPACE\Documents\semester\GNSS\HW4\sat_positions\sat15.csv'
    sat_id = 'PG15' #satellite id

    sp32satcsv(input_file_path, output_file_path, sat_id)
    print("done!")