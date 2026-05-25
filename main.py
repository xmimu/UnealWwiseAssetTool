from pathlib import Path

from config import Config
from wwise_console import run_generate_soundbank
from unreal_console import run_reconcile

def main():
    config = Config.load_from_file(Path("config.json"))
    run_generate_soundbank(
        config.wwise_console_path,
        config.wwise_project_path,
        config.platforms,
        config.languages,
        log_verbose=True,
    )
    run_reconcile(
        config.unreal_cmd_path,
        config.unreal_uproject_path,
    )


if __name__ == "__main__":
    main()
