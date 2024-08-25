import os
from datetime import datetime
from IPython.display import Image, display


def generate_graph_image(app, description="langgraph"):
    # Get the PNG data from the graph
    png_data = app.get_graph().draw_png()

    # Create output directory if it doesn't exist
    output_dir = "data/output/graphs"
    os.makedirs(output_dir, exist_ok=True)

    # Generate a unique filename with description, timestamp, and counter
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    counter = 1
    while True:
        filename = f"{description}_{timestamp}_{counter:03d}.png"
        filepath = os.path.join(output_dir, filename)
        if not os.path.exists(filepath):
            break
        counter += 1

    # Save the PNG data to a file
    with open(filepath, 'wb') as f:
        f.write(png_data)

    print(f"Graph image saved as {filepath}")

    # Return both the filepath and the Image object
    return filepath, Image(png_data)

# Usage example:
# from your_langgraph_app import app
# filepath, img = generate_graph_image(app, "my_app_graph")
# print(f"Graph saved to: {filepath}")
# display(img)  # This will display the image in a Jupyter notebook
