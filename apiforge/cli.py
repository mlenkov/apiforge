"""CLI module for ApiForge."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from .config import get_config_path, list_configs, load_config
from .exceptions import ApiForgeConfigError


def doctor(provider: Optional[str] = None, api_name: Optional[str] = None) -> None:
    """Check integrity of ApiForge configs.

    Args:
        provider: Check specific provider (e.g., 'yandex')
        api_name: Check specific API (e.g., 'metrika')
    """
    print("ApiForge Doctor")
    print("=" * 50)

    configs = list_configs()

    if not configs:
        print("No configs found in ~/.apiforge/configs/")
        print("\nTo install configs, run:")
        print("  apiforge install")
        return

    errors: list[str] = []
    warnings: list[str] = []

    providers_to_check = [provider] if provider else list(configs.keys())

    for prov in providers_to_check:
        if prov not in configs:
            errors.append(f"Provider '{prov}' not found")
            continue

        apis_to_check = [api_name] if api_name else configs[prov]

        for api in apis_to_check:
            config_path = get_config_path(prov, api)
            print(f"\nChecking {prov}/{api}...")

            if not config_path.exists():
                errors.append(f"Config file not found: {config_path}")
                continue

            try:
                config = load_config(config_path)
                print(f"  ✓ Valid JSON")

                if "base_url" in config:
                    print(f"  ✓ Base URL: {config['base_url']}")

                resources = config.get("resources", {})
                print(f"  ✓ Resources: {len(resources)}")

                for res_name, res_config in resources.items():
                    if "path" not in res_config:
                        errors.append(
                            f"  ✗ Resource '{res_name}' missing 'path'"
                        )

            except ApiForgeConfigError as e:
                errors.append(f"  ✗ {e}")

    print("\n" + "=" * 50)

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for error in errors:
            print(f"  {error}")

    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for warning in warnings:
            print(f"  {warning}")

    if not errors and not warnings:
        print("\n✓ All checks passed!")

    sys.exit(1 if errors else 0)


def install() -> None:
    """Install default configs."""
    config_dir = Path.home() / ".apiforge" / "configs"
    config_dir.mkdir(parents=True, exist_ok=True)

    print(f"Configs directory: {config_dir}")
    print("\nTo add configs, place JSON files in:")
    print(f"  {config_dir}/<provider>/<api_name>.json")


def main() -> None:
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="apiforge",
        description="ApiForge - Modern Python API Client Generator",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    doctor_parser = subparsers.add_parser("doctor", help="Check config integrity")
    doctor_parser.add_argument("--provider", help="Check specific provider")
    doctor_parser.add_argument("--api", help="Check specific API")

    subparsers.add_parser("install", help="Install default configs")

    args = parser.parse_args()

    if args.command == "doctor":
        doctor(provider=args.provider, api_name=args.api)
    elif args.command == "install":
        install()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
