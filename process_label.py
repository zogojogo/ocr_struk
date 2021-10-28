import os, json

label_dir = "./label"
if not os.path.isdir(label_dir):
    os.mkdir(label_dir)

def main():
    label_name = input("filename (or enter if in the same folder) : ")
    label_raw = open("Label.txt", "r") if label_name == "" else open(label_name, "r")
    label_lines = label_raw.readlines()
    for line in label_lines:
        lines = []
        fname, data = line.split("\t")
        data = json.loads(data)
        fname = fname.split("/")[-1].split(".")[0] + ".txt"
        print(fname)
        for d in data:
            cur_data = ""
            cur_data += ",".join([str(i) for x in d['points'] for i in x])
            cur_data += "," + d['transcription'].upper()
            lines.append(cur_data)
        with open("{}/{}".format(label_dir, fname), "w") as f:
            f.write('\n'.join(lines))


if __name__ == "__main__":
    main()
