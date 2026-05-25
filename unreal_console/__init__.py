from pathlib import Path
import subprocess
from loguru import logger

# generate soundbanks command line args for Unreal Editor Commandlet
# <UnrealEditor-cmd.exe> <path_to_uproject> -run=GenerateSoundBanks [-platforms=listOfPlatforms] [-languages=listOfLanguages] [-wwiseConsolePath=pathToWwiseConsole]
ue_gen_bank_cmd: str = (
    '{} -run=GenerateSoundBanks -platforms="{}" -languages="{}" -wwiseConsolePath="{}"'
)

# replace with UnrealEditor-cmd.exe path
# <UnrealEditor-cmd.exe> <path_to_uproject> -run=WwiseReconcileCommandlet -modes=listOfOperation
ue_reconcile_cmd: str = "{} {} -run=WwiseReconcileCommandlet -modes={}"


def run_reconcile(
    unreal_editor_cmd_path: Path,
    uproject_path: Path,
    modes: list[str] = ["create", "update"],
) -> None:
    modes_str = ",".join(f'{i}' for i in modes)
    command = ue_reconcile_cmd.format(
        f'"{unreal_editor_cmd_path}"',
        f'"{uproject_path}"',
        modes_str,
    )
    logger.info(f"Running command: {command}")
    subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    run_reconcile(
        Path("C:/Path/To/UnrealEditor-cmd.exe"),
        Path("C:/Path/To/YourProject.uproject"),
        modes=["create", "update"],
    )
