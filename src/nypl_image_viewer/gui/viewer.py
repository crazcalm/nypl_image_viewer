import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

from ..store import ItemImageStore


class ImageViewer:
    def __init__(self, root: tk.Tk, image_paths: list[Path]):
        self.root = root
        self.image_paths = image_paths
        self.index = 0

        # UI setup
        self.label = tk.Label(root)
        self.label.pack(padx=10, pady=10)

        self.next_button = tk.Button(root, text="Next", command=self.show_next)
        self.next_button.pack(pady=5)

        self.show_image()

    def show_image(self) -> None:
        path = self.image_paths[self.index]

        # Load and convert image
        image = Image.open(path)
        photo = ImageTk.PhotoImage(image)

        # Keep a reference or image disappears
        self.label.image = photo
        self.label.config(image=photo)

        self.root.title(f"{path.name} ({self.index + 1}/{len(self.image_paths)})")

    def show_next(self) -> None:
        self.index = (self.index + 1) % len(self.image_paths)
        self.show_image()


def main() -> None:
    import pdb
    pdb.set_trace()
    test = "/home/crazcalm/Documents/Github/nypl_image_viewer/data/collections/"
    image_store = ItemImageStore(Path(test))
    image_paths = image_store.all()

    
    #image_dir = Path("images")  # change to your folder
    #image_paths = list(image_dir.glob("*.jpg"))  # adjust extension if needed

    if not image_paths:
        raise RuntimeError("No images found.")

    root = tk.Tk()
    root.geometry("800x600")

    ImageViewer(root, image_paths)

    root.mainloop()


if __name__ == "__main__":
    main()
