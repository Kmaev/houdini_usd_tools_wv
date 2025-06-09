import argparse
from usd_scene_init import utils
from pathlib import Path

_THIS = Path(__file__)

TEMPLATE_PATH = _THIS.parent.joinpath("init_scene_template.json")
DEFAULT_OUTPUT_PATH = "./template_scene1.usda"


def main(args: list[str] | None = None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--template-path", default=TEMPLATE_PATH)
    parser.add_argument("--output-path", default=DEFAULT_OUTPUT_PATH)

    namespace = parser.parse_args(args)

    utils.create_scene_from_json(
        namespace.template_path,
        namespace.output_path,
    )


if __name__ == "__main__":
    main()
