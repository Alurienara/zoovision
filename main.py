import csv
from datetime import datetime
import streamlit as st
from PIL import Image
from model.predictor import predict_image as predict_image_inat
from rapidfuzz import process, fuzz
import os
import time
from streamlit_cropper import st_cropper
from translations import TRANSLATIONS


# Настройки страницы
st.set_page_config(page_title="ZooVision", layout="centered")

# Выбор языка
language = st.radio(
    "🌐 Язык | Language",
    options=["ru", "en"],
    horizontal=True
)
translations = TRANSLATIONS[language]

# Заголовок и описание
st.title(translations["title"])
st.markdown(translations["description"])

# Инициализация Session State
for key in [
    "results",
    "feedback_expanded",
    "correction_confirmed",
    "user_text",
    "selected_correction",
]:
    if key not in st.session_state:
        st.session_state[key] = (
            False if "confirmed" in key or "expanded" in key else ""
        )

# Загрузка файла
uploaded_file = st.file_uploader(
    translations["upload_prompt"], type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    current_filename = uploaded_file.name
    if "last_filename" not in st.session_state:
        st.session_state.last_filename = ""
    if current_filename != st.session_state.last_filename:
        st.session_state.results = None
        st.session_state.feedback_expanded = False
        st.session_state.correction_confirmed = False
        st.session_state.user_text = ""
        st.session_state.selected_correction = ""
        st.session_state.last_filename = current_filename

    st.image(image, caption=translations["original_image"],
             use_container_width=True)

    image_for_prediction = image

    # Обрезка по желанию
    use_crop = st.checkbox(translations["crop_manual"], value=False)

    if use_crop:
        st.subheader(translations["crop_manual"])

        cropped_image = st_cropper(
            image,
            realtime_update=True,
            box_color="#FF4860A6",
            aspect_ratio=None,
            return_type="image",
        )

        if cropped_image and cropped_image.size[0] > 0:
            st.image(
                cropped_image,
                caption=translations["cropped_image"],
                use_container_width=True,
            )
            image_for_prediction = cropped_image
        else:
            st.info("🔹 Подвиньте рамку или начните редактировать!")
            image_for_prediction = image

    # Кнопка запуска анализа
    if st.button(translations["analyze_button"], key="predict_button"):
        progress = st.progress(0)
        with st.spinner(translations["analyze_image"]):

            time.sleep(0.2)
            progress.progress(20)

            time.sleep(0.3)
            progress.progress(40)

            time.sleep(0.1)
            st.session_state.results = predict_image_inat(image_for_prediction)
            progress.progress(80)

            time.sleep(0.1)
            progress.progress(100)

        progress.empty()

        # Сбросить фидбек при новом анализе
        st.session_state.feedback_expanded = False
        st.session_state.correction_confirmed = False
        st.session_state.user_text = ""
        st.session_state.selected_correction = ""

    # Показ результатов и блока обратной связи
    if st.session_state.results:
        results = st.session_state.results

        filtered_results = [
            (label, score) for label, score in results if score > 0.01
        ]

        st.subheader(translations["results_title"])
        if filtered_results:
            main_label, main_score = filtered_results[0]
            st.success(
                translations["main_result"].format(label=main_label,
                                                   score=main_score)
            )

            if len(filtered_results) > 1:
                st.markdown(translations["also_possible"])
                for label, score in filtered_results[1:]:
                    st.write(f"• {label} — {score:.2%}")
        else:
            st.warning(translations["no_confidence"])

        # Блок обратной связи
        if not st.session_state.feedback_expanded:
            if st.button(translations["wrong_detected"]):
                st.session_state.feedback_expanded = True

        if st.session_state.feedback_expanded:
            if not st.session_state.correction_confirmed:
                st.session_state.user_text = st.text_input(
                    translations["feedback_input"],
                    value=st.session_state.user_text,
                )

                if st.session_state.user_text:
                    options_for_feedback = [
                        label for label, score in filtered_results
                    ]

                    matches = process.extract(
                        st.session_state.user_text,
                        options_for_feedback,
                        scorer=fuzz.token_sort_ratio,
                        limit=3,
                    )
                    st.write(translations["matches_title"])
                    for label, score, _ in matches:
                        st.write(f"- **{label}** ({score:.1f}%)")

                    options = [label for label, score, _ in matches]
                    selected = st.radio(translations["select_best"], options)

                    def confirm_correction():
                        st.session_state.correction_confirmed = True
                        st.session_state.selected_correction = selected

                        label_folder = (
                            f"corrections/{selected.replace(' ', '_')}"
                        )
                        os.makedirs(label_folder, exist_ok=True)

                        base_name = os.path.splitext(uploaded_file.name)[0]
                        new_filename = f"{base_name}_corrected.jpg"
                        save_path = os.path.join(label_folder, new_filename)

                        with open(save_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                    st.button(
                        translations["confirm_button"],
                        on_click=confirm_correction,
                        disabled=st.session_state.correction_confirmed,
                    )
                    log_entry = {
                        "file_name": uploaded_file.name,
                        "model_prediction": filtered_results[0][0],
                        "user_correction": selected,
                        "timestamp": datetime.now().isoformat(),
                    }

                    with open(
                        "feedback.csv", mode="a", newline="", encoding="utf-8"
                    ) as f:
                        writer = csv.DictWriter(f, fieldnames=log_entry.keys())
                        if f.tell() == 0:
                            writer.writeheader()
                        writer.writerow(log_entry)

            else:
                st.success(
                    translations["thanks"].format(
                        label=st.session_state.selected_correction
                    )
                )
# Кнопка "Очистить всё"
if st.button(translations["remove"]):
    st.session_state.clear()
    st.rerun()

# "О проекте"
with st.sidebar:
    st.markdown(translations["about"])
    st.write(translations["about_text"])

# Футер
st.markdown(translations["footer"])
