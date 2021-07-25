from termcolor import cprint


class LandmarkDetector:

    @staticmethod
    def display_failed_files(files):
        if files:
            cprint(f"Face could not be detected on:", "yellow")
            for f in files:
                cprint(f"\t- {f}", "red")
        else:
            cprint(f"Successfully detected face on every image.", "green")

    @staticmethod
    def check_extension(filename: str, default_ext: str):
        filename_as_array = filename.split(".")
        if len(filename_as_array) > 1:
            return filename, filename_as_array[-1]
        return default_ext
