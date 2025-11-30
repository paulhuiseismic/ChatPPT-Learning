import os
from input_parser import parse_input_text
from ppt_generator import generate_presentation
from template_manager import load_template, get_layout_mapping, print_layouts


def main():
    input_text = """
    # ChatPPT_Demo_Homework

    ## ChatPPT Demo [Title]

    ## 2024 业绩概述 [Introduction]
    - 总收入增长15%
    - 市场份额扩大至30%

    ## 业绩图表 [Title and Picture]
    ![业绩图表](images/performance_chart.png)

    ## 新产品发布 [Summary and Picture]
    - 产品A: 特色功能介绍
    - 产品B: 市场定位
    ![未来增长](images/forecast.png)
    """

    # Get the absolute path to the template file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    template_file = os.path.join(project_dir, 'templates', 'Fair frames presentation.pptx')
    prs = load_template(template_file)

    print("Available Slide Layouts:")
    print_layouts(prs)

    layout_mapping = get_layout_mapping(prs)

    powerpoint_data, presentation_title = parse_input_text(input_text, layout_mapping)

    # Create output directory and file path
    output_dir = os.path.join(project_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    output_pptx = os.path.join(output_dir, f"{presentation_title}.pptx")
    generate_presentation(powerpoint_data, template_file, output_pptx)


if __name__ == "__main__":
    main()