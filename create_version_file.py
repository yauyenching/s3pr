import pyinstaller_versionfile

pyinstaller_versionfile.create_versionfile_from_input_file(
    output_file="file_version_info.txt",
    input_file="metadata.yml",
)