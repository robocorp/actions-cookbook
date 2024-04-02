"""
Read receipts to JSON with Donut model from HuggingFace
"""

from robocorp.actions import action

import re
from transformers import DonutProcessor, VisionEncoderDecoderModel
import torch
import requests
from PIL import Image
from io import BytesIO

@action
def read_and_extract_receipt_from_url(receipt_url: str) -> str:
    """
    Converts a picture of an invoice to a structured data 

    Args:
        receipt_url (str): A complete URL that points to a one image file of a receipt.
 
    Returns:
        str: A JSON representation of a receipts content
    """

    #receipt_url = "https://c8.alamy.com/comp/CNTYDX/tesco-shopping-receipt-CNTYDX.jpg"
    response = requests.get(receipt_url)
    if response.status_code == 200:
        # Open the image directly from the bytes
        image = Image.open(BytesIO(response.content))
    
    else:
        return f"There was an error fetching image, status code: {response.status_code}"

    processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
    model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    task_prompt = "<s_cord-v2>"
    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids
    pixel_values = processor(image, return_tensors="pt").pixel_values

    outputs = model.generate(
        pixel_values.to(device),
        decoder_input_ids=decoder_input_ids.to(device),
        max_length=model.decoder.config.max_position_embeddings,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )

    sequence = processor.batch_decode(outputs.sequences)[0]
    sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
    sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()  # remove first task start token
    print(processor.token2json(sequence))

    return str(processor.token2json(sequence))