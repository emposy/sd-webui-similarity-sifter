import os
import gradio as gr
import face_recognition
import numpy as np
from datetime import datetime
import hashlib
import re

from modules import scripts, shared, images
from modules.processing import Processed
from modules.ui_components import FormColumn

from scripts.ss_config import ss_output_dir

class SimilaritySifter(scripts.Script):
    def title(self):
        return "SimilaritySifter"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion("SimilaritySifter", open=False):
            with FormColumn():
                is_enabled = gr.Checkbox(label="Enable SimilaritySifter", value=False)
                uploaded_image = gr.Image(label="Upload Image", source="upload", interactive=True)
                gr.Markdown("<br>")
                with gr.Row():
                    remove_low_similarity = gr.Checkbox(
                        label="Remove Low Similarity Images",
                        value=False
                    )
                    similarity_threshold = gr.Slider(
                        label="Similarity Threshold",
                        minimum=0.0,
                        maximum=1.0,
                        value=0.7,
                        step=0.01,
                        info="Threshold for removing low similarity images."
                    )
                return [is_enabled, uploaded_image, remove_low_similarity, similarity_threshold]

    def save_images(self, processed: Processed):
        if not os.path.exists(shared.opts.data.get("ss_output_dir", ss_output_dir)):
            os.makedirs(shared.opts.data.get("ss_output_dir", ss_output_dir), exist_ok=True)
        output_folder = os.path.join(shared.opts.data.get("ss_output_dir", ss_output_dir), f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{processed.seed}")
        os.makedirs(output_folder, exist_ok=True)
        for image in processed.images[1:]:
            similarity_per = int(image.info.get("SS_similarity", 0) * 1000)
            seed_match = re.search(r"Seed: (\d+)", image.info.get("parameters", ""))
            if seed_match:
                seed = int(seed_match.group(1))
            else:
                seed = 0
            images.save_image(image, path=output_folder, basename="", seed=seed, pnginfo_section_name="parameters", info=image.info.get("parameters", ""), extension=".png", save_to_dirs=False, forced_filename=f"{similarity_per:04d}_{seed}")

    def calculate_similarity(self, uploaded_image, generated_image):
        uploaded_encodings = face_recognition.face_encodings(uploaded_image)
        if len(uploaded_encodings) == 0:
            return 0
        generated_image = np.array(generated_image)
        generated_encodings = face_recognition.face_encodings(generated_image)
        if len(generated_encodings) == 0:
            return 0
        similarity = face_recognition.face_distance([uploaded_encodings[0]], generated_encodings[0])[0]
        return 1 - similarity
    
    def postprocess_image(self, p: Processed, pp: scripts.PostprocessImageArgs, is_enabled, uploaded_image, remove_low_similarity, similarity_threshold):
        if not is_enabled or uploaded_image is None:
            return
        similarity = self.calculate_similarity(uploaded_image, pp.image)
        pp.image.info["SS_similarity"] = similarity
        p.extra_generation_params['SS similarity'] = similarity
        
    def postprocess(self, p: Processed, processed: Processed, is_enabled, uploaded_image, remove_low_similarity, similarity_threshold):
        if not is_enabled or uploaded_image is None:
            return
        max_len = len(processed.infotexts)
        similarities = [image.info.get("SS_similarity", 0) for image in processed.images[1:max_len]]
        if remove_low_similarity:
            filtered_similarities = [sim for sim in similarities if sim >= similarity_threshold]
            filtered_images = [image for image, sim in zip(processed.images[1:], similarities) if sim >= similarity_threshold]
            filtered_infotexts = [infotext for infotext, sim in zip(processed.infotexts[1:], similarities) if sim >= similarity_threshold]
        else:
            filtered_similarities = similarities
            filtered_images = processed.images[1:]
            filtered_infotexts = processed.infotexts[1:]
        sorted_indices = np.argsort(filtered_similarities)[::-1]
        processed.images[1:] = [filtered_images[i] for i in sorted_indices] + processed.images[max_len:]
        processed.infotexts[1:] = [filtered_infotexts[i] for i in sorted_indices]
        if len(similarities) > 1 and len(processed.images[1:]) > 0:
            self.save_images(processed)