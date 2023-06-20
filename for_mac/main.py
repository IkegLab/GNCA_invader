import onnxruntime
import numpy as np
import json
import os
from datetime import datetime
import codecs

def delete_all_files(directory):
    # Get list of all files in the directory
    files = os.listdir(directory)
    # Loop over all files
    for i in range(len(files)-2):
        file_path = os.path.join(directory, files[i])
        # Check if it's a regular file and then delete it
        if os.path.isfile(file_path):
            os.remove(file_path)

def delete_old_files(directory, max_files=15):
    # Get list of all files in the directory
    files = os.listdir(directory)
    # If there are more files than max_files
    while len(files) > max_files:
        # Sort files by creation time
        files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        # Remove the oldest file
        os.remove(os.path.join(directory, files[0]))
        # Update files list
        files = os.listdir(directory)


class GNCA():
    def __init__(self, height=72, width=72, n_channels=16, model_path=r"./public/growing-neural-cellular-automata.onnx"):
        self.height: int = height
        self.width: int = width
        self.n_channels: int = n_channels
        self.session = onnxruntime.InferenceSession(model_path)
        self.input : np.ndarray
        self.output : np.ndarray
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    def write_json(self, path, data):
        json.dump(data, codecs.open(path, 'w', encoding='utf-8'),
            separators=(',', ':'),
            sort_keys=True,
            indent=4) ### this saves the array in .json format

    def to_alpha(self, x):
        return np.clip(x[..., 3:4], 0, 0.9999)

    def to_rgba(self, x):
        rgb, a = x[..., :3], self.to_alpha(x)
        return np.concatenate((np.clip(1.0-a+rgb, 0, 0.9999), a), axis=3)

    def load_input_json(self, path):
        with open(path) as f:
            data = json.load(f)
            # data = json_numpy.loads(data)
        return np.asarray(data)

    def write_rgba_json(self, path, x):
        rgba = self.to_rgba(x)
        data = json_numpy.dumps(rgba)
        with open(path, mode='wt', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=True, indent=2)

    def write_rgba_tolist_json(self, path, x):
        rgba = self.to_rgba(x)
        color_list = []
        for i in range(rgba.shape[1]):
            for j in range(rgba.shape[2]):
                color = {
                    "r": float(rgba[0, i, j, 0]),
                    "g": float(rgba[0, i, j, 1]),
                    "b": float(rgba[0, i, j, 2]),
                    "a": float(rgba[0, i, j, 3])
                }
                color_list.append(color)
        # Write the color_list to the file.
        try:
            with open(path, 'w') as f:
                json.dump(color_list, f)
        except PermissionError:
            pass

    def write_alpha_json(self, path, x):
        data = json_numpy.dumps(self.to_alpha(x))
        with open(path, mode='wt', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=True, indent=2)

    def write_alpha_tolist_json(self, path, x):
        alpha = self.to_alpha(x).tolist()
        # with open(path, mode='wt', encoding='utf-8') as f:
        #     json.dump(data, f, ensure_ascii=True, indent=2)
        self.write_json(path, alpha)

    def make_seeds(self, path):
        x = np.zeros([1, self.height, self.width, self.n_channels], np.float32)
        x[:, self.height//2-10:self.height//2+10, self.width//2-10:self.width//2+10, 3:] = 1.0
        self.input = x
        # self.write_alpha_json(path, self.input)
        self.write_alpha_tolist_json(path, self.input)
        return x

    def update(self, directory):
        # Get list of all files in the directory
        files = os.listdir(directory)
        # Sort files by creation time
        files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        # Load the most recent file
        path = os.path.join(directory, files[-2])
        data = self.load_input_json(path)
        alpha = data.reshape(self.height, self.width)
        alive_mask = np.where(alpha == 0, 0, 1)
        self.input = ((self.input[0].T * alive_mask).T).reshape(1, self.height, self.width, self.n_channels).astype(np.float32)

    def run(self) -> np.ndarray:
        out = self.session.run([self.output_name], {self.input_name: self.input})
        self.output = out[0].astype(np.float32)
        self.input = out[0].astype(np.float32)

    def generate_output_path(self, base_directory,counter):
        filename = f"{counter}.json"
        return os.path.join(base_directory, filename)

def main():
    os.makedirs("./log", exist_ok=True)
    input_base_directory = "./log/input"
    output_base_directory = "./log/output"
    gnca = GNCA()
    for i in range(3):
        input_path = os.path.join(input_base_directory, f"input{i}.json")
        gnca.input = gnca.make_seeds(input_path)
    #delete_all_files(input_base_directory)
    #delete_all_files(output_base_directory)
    counter = 0
    while True:
        gnca.update(input_base_directory) # Load input from Unity.
        gnca.run()
        output_path = gnca.generate_output_path(output_base_directory,counter) # Create new output file for each iteration
        # gnca.write_rgba_json(output_path, gnca.output) # Write output for Unity.
        gnca.write_rgba_tolist_json(output_path, gnca.output) # Write output for Unity.
        delete_old_files(input_base_directory)
        delete_old_files(output_base_directory)
        counter += 1

if __name__ == "__main__":
    main()
