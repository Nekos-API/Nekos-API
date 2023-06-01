import io

from django.core.files import File

import PIL
import PIL.Image


class AnimatedImageFile:
    def __init__(self, bs: io.BytesIO):
        self.bs = bs

    def save(self, file: io.BytesIO):
        self.bs.seek(0)
        file.write(self.bs.read())


def calculate_cropping(size: tuple, ar_size: tuple) -> tuple:
    """
    Returns a new size.
    """

    new_aspect_ratio = ar_size[0] / ar_size[1]
    current_aspect_ratio = size[0] / size[1]

    if new_aspect_ratio < current_aspect_ratio:
        # The new aspect ratio is wider than the current one.
        new_size = (
            size[1] / ar_size[0] * ar_size[1],
            size[1]
        )

        return new_size, ((size[0] - new_size[0]) / 2, 0)

    elif new_aspect_ratio > current_aspect_ratio:
        # The new aspect ratio is taller than the current one.
        new_size = (
            size[0],
            size[0] / ar_size[0] * ar_size[1]
        )

        return new_size, (0, (size[1] - new_size[1]) / 2)

    else:
        # No modifications need to be done.
        return size, (0, 0)


def gif_resize(image, aspect_ratio: str):
    """
    Resize a GIF while maintaining it animated.
    """

    image = image.get_pil_image()

    ar_size = [int(d) for d in aspect_ratio.split("/")]
    current_size = (image.width, image.height)
    new_size, padding = calculate_cropping(current_size, ar_size)

    frames = PIL.ImageSequence.Iterator(image)
    frame_duration = 0

    def thumbs():
        frame_durations = []
        for frame in frames:
            thumbnail = frame.copy()
            thumbnail = thumbnail.crop((
                padding[0],
                padding[1],
                new_size[0] + padding[0],
                new_size[1] + padding[1]
            ))
            frame_durations.append(frame.info['duration'])
            yield thumbnail
        frame_duration = sum(frame_durations) / len(frame_durations)

    thumbnails = thumbs()

    om = next(thumbnails)
    om.info = image.info

    bs = io.BytesIO()
        
    om.save(
        bs,
        save_all=True,
        append_images=list(thumbnails),
        loop=0,
        duration=frame_duration,
        format="GIF",
    )
    return AnimatedImageFile(bs=bs)
