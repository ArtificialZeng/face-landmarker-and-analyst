import json
import argparse

def extract_points(obj, result):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, dict) and 'x' in v and 'y' in v:
                result.append(v)
            else:
                extract_points(v, result)
    elif isinstance(obj, list):
        for item in obj:
            extract_points(item, result)

def main(json_path):
    # 从文件读取json
    with open(json_path, 'r') as f:
        json_obj = json.load(f)

    # 提取x，y值
    points = []
    extract_points(json_obj, points)

    # 以空格分隔并输出x，y值
    for point in points:
        print(f"{point['x']} {point['y']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process json file.')
    parser.add_argument('--json_path', type=str, help='path to json file')

    args = parser.parse_args()

    main(args.json_path)
