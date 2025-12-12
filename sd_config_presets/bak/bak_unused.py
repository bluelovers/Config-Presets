
def _replace_text_in_file(old: str, new: str, file_path: str):  # pyright: ignore[reportUnusedFunction]
    """
    Replace text in a file with new text.
    
    用新文本替换文件中的文本。
    """
    with open(file_path, "r") as file:
        content = file.read()

    with open(file_path, "w") as file:
        file.write(content.replace(old, new))  # pyright: ignore[reportUnusedCallResult]

