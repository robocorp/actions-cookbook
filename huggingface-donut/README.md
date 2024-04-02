# Using HuggingFace Transformer models in Actions

This example uses [Donut OCR-less](https://huggingface.co/naver-clova-ix/donut-base-finetuned-cord-v2) Document Understanding model from HuggingFace Transformers to extract data from receipts.

- Takes a URL of an receipt as input. This is because most of the GPTs are still very restricted in their ability to send files to Actions.
- Uses model's example code for extraction - nothing fancy there!
- First start of the Action Server will take some serious time as all the bits and pieces are downloaded.
- TODO: Switch to use `dict` as output instead of `str`.