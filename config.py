import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from dataclasses import dataclass, field
from loguru import logger


def _parse_wproj(wproj_path: Path) -> tuple[set[str], set[str]]:
    tree = ET.parse(wproj_path)
    root = tree.getroot()
    platforms = {i.get("Name") for i in root.iter("Platform") if i.get("Name")}
    languages = {i.get("Name") for i in root.iter("Language") if i.get("Name")}
    return platforms, languages  # type: ignore


@dataclass
class Config:
    wwise_console_path: Path = field(
        default_factory=lambda: Path(
            "C:/Program Files (x86)/Audiokinetic/Wwise 2023.1.0/Authoring/x64/Release/bin/WwiseConsole.exe"
        )
    )
    wwise_project_path: Path = field(
        default_factory=lambda: Path(
            "C:/Users/User/Documents/Wwise Projects/MyProject/MyProject.wproj"
        )
    )
    wwise_bank_output_path: Path = field(
        default_factory=lambda: Path(
            "C:/Users/User/Documents/Wwise Projects/MyProject/GeneratedSoundBanks"
        )
    )
    platforms: list[str] = field(default_factory=lambda: ["Windows", "Mac"])
    languages: list[str] = field(default_factory=lambda: ["English(US)"])
    unreal_cmd_path: Path = field(
        default_factory=lambda: Path("C:/Path/To/UnrealEditor-cmd.exe")
    )
    unreal_uproject_path: Path = field(
        default_factory=lambda: Path("C:/Path/To/YourProject.uproject")
    )
    unreal_wwise_audio_path: Path = field(
        default_factory=lambda: Path("C:/Path/To/UnrealProject/Plugins/Wwise/Audio")
    )

    @staticmethod
    def load_from_file(config_path: Path) -> "Config":
        with open(config_path, "r") as f:
            data = json.load(f)
            cache_cwd = os.getcwd()  # Get current working directory for logging
            os.chdir(
                config_path.parent
            )  # Change working directory to config file location

            config = Config(
                wwise_console_path=Path(data["wwise_console_path"]).resolve(),
                wwise_project_path=Path(data["wwise_project_path"]).resolve(),
                wwise_bank_output_path=Path(data["wwise_bank_output_path"]).resolve(),
                platforms=data["platforms"],
                languages=data["languages"],
                unreal_cmd_path=Path(data["unreal_cmd_path"]).resolve(),
                unreal_uproject_path=Path(data["unreal_uproject_path"]).resolve(),
                unreal_wwise_audio_path=Path(data["unreal_wwise_audio_path"]).resolve(),
            )

            os.chdir(cache_cwd)  # Restore original working directory
            if not Config.validate(config):
                raise ValueError("Invalid configuration")
            return config

    @staticmethod
    def validate(config: "Config") -> bool:
        if not config.wwise_console_path.is_file():
            logger.error(f"WwiseConsole.exe not found at {config.wwise_console_path}")
            return False
        if not config.wwise_project_path.is_file():
            logger.error(f"Wwise project file not found at {config.wwise_project_path}")
            return False
        if not config.wwise_bank_output_path.is_dir():
            logger.error(
                f"Bank output path is not a directory at {config.wwise_bank_output_path}"
            )
            return False
        if not config.platforms:
            logger.error("No platforms specified")
            return False
        if not config.languages:
            logger.error("No languages specified")
            return False

        # 从.wproj解析项目支持的平台和语言，配置项必须是其子集
        valid_platforms, valid_languages = _parse_wproj(config.wwise_project_path)
        invalid_platforms = set(config.platforms) - valid_platforms
        if invalid_platforms:
            logger.error(
                f"Invalid platforms: {invalid_platforms}. Valid: {valid_platforms}"
            )
            return False
        invalid_languages = set(config.languages) - valid_languages
        if invalid_languages:
            logger.error(
                f"Invalid languages: {invalid_languages}. Valid: {valid_languages}"
            )
            return False

        if not config.unreal_cmd_path.is_file():
            logger.error(f"UnrealEditor-cmd.exe not found at {config.unreal_cmd_path}")
            return False
        if not config.unreal_uproject_path.is_file():
            logger.error(
                f"Unreal project file not found at {config.unreal_uproject_path}"
            )
            return False
        if not config.unreal_wwise_audio_path.is_dir():
            logger.error(
                f"Unreal Wwise audio path is not a directory at {config.unreal_wwise_audio_path}"
            )
            return False
        return True


if __name__ == "__main__":
    # Example usage
    from pprint import pprint

    config = Config.load_from_file(Path("config.json"))
    pprint(config)
