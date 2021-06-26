import sys

from converter import converter


def analyze_args():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'convert':
            if len(sys.argv) > 3:
                path = sys.argv[2]
                goal_dir = sys.argv[3] if len(sys.argv) == 4 else 'converted_images'
                converter.run(path, goal_dir=goal_dir, images_type='png')


def main():
    print(f"Welcome")
    analyze_args()
