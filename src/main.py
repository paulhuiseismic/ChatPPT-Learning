import os
import argparse
from input_parser import parse_input_text
from ppt_generator import generate_presentation
from template_manager import load_template, get_layout_mapping, print_layouts
from layout_manager import LayoutManager
from config import Config
from logger import LOG


def main(input_file):
    config = Config()

    if not os.path.exists(input_file):
        LOG.error(f"Input file {input_file} does not exist")
        return

    with open(input_file, "r", encoding='utf-8') as file:
        input_text = file.read()

    prs = load_template(config.ppt_template)
    LOG.info("Available slide layouts:")
    print_layouts(prs)

    layout_manager = LayoutManager(config.layout_mapping)

    powerpoint_data, presentation_title = parse_input_text(input_text, layout_manager)

    LOG.info(f"Parsed ChatPPT PowerPoint data structure: \n{powerpoint_data}")

    output_pptx = f"output/{presentation_title}.pptx"

    generate_presentation(powerpoint_data, config.ppt_template, output_pptx)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='From markdown text to PowerPoint presentation.')
    parser.add_argument(
        'input_file',
        nargs='?',
        default='inputs/test_input.md',
        help='Input markdown text file path (default: inputs/test_input.md)'
    )

    args = parser.parse_args()

    main(args.input_file)