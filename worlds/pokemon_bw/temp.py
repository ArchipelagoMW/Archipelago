import os

if __name__ == "__main__":
    for root, dirs, files in os.walk("./"):
        print(f"root {root}, dirs {dirs}, files {files}")
