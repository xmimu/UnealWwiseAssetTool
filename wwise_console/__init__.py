import subprocess
from pathlib import Path
from loguru import logger


# WwiseConsole generate-soundbank "C:\MyProject\MyProject.wproj" --platform "Windows" "Mac" --language "English(US)"
wwise_command_line_args: str = "{} generate-soundbank {} --platform {} --language {}"


def run_generate_soundbank(
    wwise_console_path: Path,
    wwise_project_path: Path,
    platforms: list[str],
    languages: list[str],
    log_verbose: bool = False,
) -> None:
    platforms_str = " ".join(f'"{i}"' for i in platforms)
    languages_str = " ".join(f'"{i}"' for i in languages)
    command = wwise_command_line_args.format(
        f'"{wwise_console_path}"',
        f'"{wwise_project_path}"',
        platforms_str,
        languages_str,
    )
    if log_verbose:
        command += " --verbose"
    logger.info(f"Running command: {command}")
    # 由于WwiseConsole.exe 生成SoundBanks的过程中输出的错误不一定致命，这里 check 设为 False，避免因为某些非致命错误导致整个流程中断
    subprocess.run(command, shell=True, check=False)
