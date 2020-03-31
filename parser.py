import argparse

def parameter_parser():
    parser = argparse.ArgumentParser(description = "Command Line Tool for editing PDF Metadata Information")

    parser.add_argument("FILENAME",
                        type=str,
                        help="Name/Path of the corresponding PDF file.")

    parser.add_argument("-p", "--print",
                        type=bool,
                        nargs='?',
                        const=True,
	                    help = "Print the current metadata for the file.")

    parser.add_argument("-ow", "--overwrite",
                        type=bool,
                        nargs='?',
                        const=True,
	                    help = "Overwrite the existing file.")

    parser.add_argument("-e", "--export",
                        type=str,
                        nargs=1,
                        default="edited.pdf",
	                    help = "Exporting edited version of the file to the given name/path.")

    return parser.parse_args()