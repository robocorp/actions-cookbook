from robocorp.actions import action
from robocorp.log import warn

import base64
import io
from PIL import ImageFilter, ImageEnhance, Image, ImageDraw
import pyautogui
import pytesseract
from pytesseract import Output


MAX_DISTANCE = 8
MAX_VERTICAL_VARIANCE = 2
ZOOM_FACTOR = 2


@action
def adjust_image_for_ocr(image_as_string: str = "") -> str:
    """
    Return adjusted image for OCR in Base64 string format

    :param image_as_string: Base64 encoded image string
    :return: Base64 encoded image string after image adjustments

    """
    if len(image_as_string) > 0:
        # Decode the base64 string
        image_data = base64.b64decode(image_as_string)
        # Create a BytesIO buffer from the decoded data
        image_buffer = io.BytesIO(image_data)
        # Open the image with PIL
        original_target_image = Image.open(image_buffer)
    else:
        warn("No image provided. Using whole desktop.")
        image_buffer = pyautogui.screenshot()
        # Open the image with PIL
        original_target_image = Image.frombytes(
            "RGB", image_buffer.size, image_buffer.tobytes()
        )

    target_image = get_zoomed(original_target_image, ZOOM_FACTOR)
    enhancer = ImageEnhance.Brightness(target_image)
    target_image = enhancer.enhance(1.5)
    target_image = get_grayscale(target_image)
    enhancer = ImageEnhance.Contrast(target_image)
    target_image = enhancer.enhance(1.2)
    # Noise Reduction (Simple Blur)
    target_image = target_image.filter(ImageFilter.GaussianBlur(1))
    threshold = 200  # You might need to adjust this value
    # # Apply thresholding
    target_image = target_image.point(lambda p: 255 if p > threshold else 0)
    # Encode the bytes buffer to a base64 string
    buffer = io.BytesIO()
    target_image.save(buffer, format="PNG")
    encoded_string = base64.b64encode(buffer.getvalue()).decode()
    return encoded_string


@action
def find_and_click(text: str, button: str = "left", click_count: int = 1):
    """Find text on desktop to click. By default clicks once using left mouse button.

    Clicks on all matches found.

    :param text: text to find on the desktop display
    :param button: type of mouse button to click, defaults to "left"
    :param click_count: how many times button is clicked, defaults to 1
    :return: location of the text found and clicked, or "Could not find text: {text}"
    """
    click_count = int(click_count)
    image_buffer = pyautogui.screenshot()
    # Open the image with PIL
    original_target_image = Image.frombytes(
        "RGB", image_buffer.size, image_buffer.tobytes()
    )
    texts, image = find_texts(original_target_image)
    result = find_matching(texts, text, inclusive=False, case_sensitive=True)

    for r in result:
        padding = 5
        print(f"RESULT: {r}")
        pyautogui.click(
            r["match"]["x"],
            r["match"]["y"],
            clicks=click_count,
            button=button,
        )
        draw = ImageDraw.Draw(image)
        left, top, right, bottom = (
            r["match"]["left"] - padding,
            r["match"]["top"] - padding,
            r["match"]["right"] + padding,
            r["match"]["bottom"] + padding,
        )
        draw.rectangle([left, top, right, bottom], outline="red", width=2)
        return f"RESULT: {r}"
    else:
        return f"Could not find text: {text}"


def find_matching(
    texts,
    search,
    inclusive: bool = False,
    case_sensitive: bool = False,
    offsets: tuple = (0, 0),
):
    print(f"FINDING MATCH FOR: {search}\n")
    matches = []
    for text in texts:
        search = search if case_sensitive else search.lower()
        image_text = text["text"] if case_sensitive else text["text"].lower()
        image_text = image_text.strip()
        if inclusive and search in image_text:
            matches.append(
                {
                    "text": text["text"],
                    "point": f"point:{int(text['x'])+offsets[0]},{int(text['y'])+offsets[1]}",
                    "match": text,
                }
            )
        elif not inclusive and search == image_text:
            matches.append(
                {
                    "text": text["text"],
                    "point": f"point:{int(text['x'])+offsets[0]},{int(text['y'])+offsets[1]}",
                    "match": text,
                }
            )
    return matches


def find_texts(
    target,
    configuration=None,
    image_path: str = "ocrtarget.png",
):
    original_target_image = (
        Image.open(target).convert("RGBA") if isinstance(target, str) else target
    )
    configuration = configuration or {}
    # Initialize variables
    show_image = bool(configuration.get("show_image", False))
    zoom_value = configuration.get("zoomlevel", ZOOM_FACTOR)
    brightness_value = configuration.get("brightness", 1.1)
    contrast_value = configuration.get("contrast", 1.3)
    threshold_value = configuration.get("threshold", None)
    text_blocks = []
    current_text = ""
    start_x, start_y, end_x, end_y = 0, 0, 0, 0

    target_image = get_zoomed(original_target_image, zoom_value)
    enhancer = ImageEnhance.Brightness(target_image)
    target_image = enhancer.enhance(brightness_value)
    target_image = get_grayscale(target_image)
    enhancer = ImageEnhance.Contrast(target_image)
    target_image = enhancer.enhance(contrast_value)

    # Apply thresholding
    if threshold_value:
        target_image = target_image.point(lambda p: 255 if p > threshold_value else 0)
    if show_image:
        target_image.show()
    if image_path:
        target_image.save(image_path)

    custom_config = r"--oem 3 --psm 6"
    ocr_data = pytesseract.image_to_data(
        target_image, output_type=Output.DICT, lang="fin", config=custom_config
    )

    # Process OCR results
    for i in range(len(ocr_data["text"])):
        text = ocr_data["text"][i].strip()
        if text != "":
            warn(f'index {i} {ocr_data["text"][i]} {ocr_data["left"][i]}')
        if text != "" and int(ocr_data["conf"][i]) > 40:
            current_text = text
            start_x, start_y = ocr_data["left"][i], ocr_data["top"][i]
            end_x, end_y = (
                start_x + ocr_data["width"][i],
                start_y + ocr_data["height"][i],
            )
            middle_x = (start_x + end_x) // 2 / zoom_value
            middle_y = (start_y + end_y) // 2 / zoom_value
            text_blocks.append(
                {
                    "text": current_text,
                    "x": int(middle_x),
                    "y": int(middle_y),
                    "left": start_x / zoom_value,
                    "top": start_y / zoom_value,
                    "right": end_x / zoom_value,
                    "bottom": end_y / zoom_value,
                }
            )

    return text_blocks, original_target_image


def get_grayscale(image):
    return image.convert("L")


def get_binary(image, threshold=100):
    return image.point(lambda p: p > threshold and 255)


def get_zoomed(image, zoom_factor):
    return image.resize(
        (int(image.width * zoom_factor), int(image.height * zoom_factor))
    )
