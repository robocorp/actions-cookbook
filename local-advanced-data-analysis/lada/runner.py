import os
from tempfile import NamedTemporaryFile

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import matplotlib
import base64

matplotlib.use('Agg')  # Set the backend to 'Agg'
import matplotlib.pyplot as plt
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from dotenv import load_dotenv


load_dotenv()

# Fetch keys from environment variables
private_key = os.environ.get('IMAGEKIT_PRIVATE_KEY')
public_key = os.environ.get('IMAGEKIT_PUBLIC_KEY')


def run_code(code: str) -> str:
    # Create a new notebook object and cell with the code
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_code_cell(code))

    # Execute the notebook/cell
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': './'}})
    # Concatenate all outputs
    print("-- testing --")
    return _create_output(nb.cells[0].outputs)


def _create_output(outputs) -> str:
    output_str = ""
    print("Processing outputs...")  # Log at the start

    # Process each output in the cell
    for output in outputs:
        print(f"Output type: {output.output_type}")  # Log the type of each output
        if output.output_type == 'stream' and output.name == 'stdout':
            output_str += output.text
            print(f"Captured stdout: {output.text}")  # Log captured stdout
        elif output.output_type == 'execute_result':
            output_str += output.data.get('text/plain', '')
            print(f"Captured execute_result: {output.data.get('text/plain', '')}")  # Log captured execution result
        elif output.output_type == 'display_data':
            if 'image/png' in output.data:
                image_data = base64.b64decode(output.data['image/png'])
                with NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
                    tmpfile.write(image_data)
                    tmpfile.flush()
                    image_url = upload_to_imagekit(tmpfile.name)
                    output_str += f"![]( {image_url} )"  # Markdown format for images
                print(f"Captured and uploaded display_data {image_url}")  # Log captured and uploaded image

    # Check and process the current matplotlib figure
    if plt.get_fignums():
        print("Found matplotlib figures, processing...")  # Log if figures are found
        with NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            plt.savefig(tmpfile.name, format='png', bbox_inches='tight')
            plt.close()
            image_url = upload_to_imagekit(tmpfile.name)
            output_str += f"![]( {image_url} )"
        print("Matplotlib figure processed and added to output")  # Log after processing figure

    else:
        print("No matplotlib figures found")  # Log if no figures are found

    return output_str


def upload_to_imagekit(file_path: str) -> str:
    print("Preparing to upload to ImageKit...")
    imagekit = ImageKit(
        private_key=private_key,
        public_key=public_key,
        url_endpoint='llmfoo'
    )
    options = UploadFileRequestOptions(
        use_unique_file_name=True,
        is_private_file=False
    )

    print(f"Opening file at path: {file_path}")
    with open(file_path, "rb") as file:
        print("File opened successfully, starting upload...")
        response = imagekit.upload_file(
            file=file,
            file_name='image.png',
            options=options
        )

    if response.url:
        image_url = response.url
        print(f"Image successfully uploaded. URL: {image_url}")
        return image_url
    else:
        error_message = "Upload did not return a URL."
        print(error_message)
        raise Exception(error_message)



if __name__ == '__main__':
    print(run_code("""
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
plt.show()  # This line is not needed for capturing the plot
"""))
