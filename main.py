import streamlit as st
from PIL import Image
from model.predictor import predict_image as predict_image_inat
from rapidfuzz import process, fuzz
import os
import time
from streamlit_cropper import st_cropper


@st.cache_resource
def load_categories():
    import urllib.request

    url = (
        "https://raw.githubusercontent.com/pytorch/hub/master/"
        "imagenet_classes.txt"
    )
    with urllib.request.urlopen(url) as f:
        categories = [line.strip().decode("utf-8") for line in f]
    return categories


categories = load_categories()

# --- Настройки страницы ---
st.set_page_config(page_title="ZooVision", layout="centered")
st.title("🐾 ZooVision — кто перед нами?")

st.markdown(
    """
    Загрузите фото животного — и мы постараемся определить вид.
    Вы можете вручную обрезать изображение, чтобы повысить точность анализа 🎯
    """
)

# --- Инициализация Session State ---
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

# --- Загрузка файла ---
uploaded_file = st.file_uploader(
    "📷 Загрузите изображение", type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_width, img_height = image.size

    # --- Сброс при новом файле ---
    current_filename = uploaded_file.name
    if "last_filename" not in st.session_state:
        st.session_state.last_filename = ""
    if current_filename != st.session_state.last_filename:
        st.session_state.last_filename = current_filename
        st.session_state.results = None
        st.session_state.feedback_expanded = False
        st.session_state.correction_confirmed = False
        st.session_state.user_text = ""
        st.session_state.selected_correction = ""

    st.image(
        image, caption="🖼 Оригинальное изображение", use_container_width=True
    )

    image_for_prediction = image  # дефолт

    # --- Обрезка с Cropper ---
    use_crop = st.checkbox("✂️ Обрезать изображение вручную?", value=False)

    if use_crop:
        st.subheader("📐 Настройка обрезки")

        cropped_image = st_cropper(
            image,
            realtime_update=True,
            box_color="#9DFF00FF",
            aspect_ratio=None,
            return_type='image'
        )

        if cropped_image and cropped_image.size[0] > 0 and cropped_image.size[1] > 0:
            st.image(
                cropped_image,
                caption="🔍 Обрезанное изображение",
                use_container_width=True
            )
            image_for_prediction = cropped_image
        else:
            st.info("🔹 Подвиньте рамку или начните редактировать!")
            image_for_prediction = image
    else:
        image_for_prediction = image

    # --- Кнопка запуска анализа ---
    if st.button("🔍 Определить, кто это", key="predict_button"):
        progress = st.progress(0)
        with st.spinner("Анализируем изображение..."):

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

    # --- Показ результатов и блока обратной связи ---
    if st.session_state.results:
        results = st.session_state.results

        filtered_results = [
            (label, score) for label, score in results if score > 0.01
        ]

        st.subheader("🔎 Результаты классификации:")
        if filtered_results:
            main_label, main_score = filtered_results[0]
            st.success(
                f"✅ Это, скорее всего: **{main_label}** ({main_score:.2%})"
            )

            if len(filtered_results) > 1:
                st.markdown("### Также возможные варианты:")
                for label, score in filtered_results[1:]:
                    st.write(f"• {label} — {score:.2%}")
        else:
            st.warning(
                "Модель не смогла уверенно распознать объект на изображении."
            )

        # --- Блок обратной связи ---
        if not st.session_state.feedback_expanded:
            if st.button("❌ Животное распознано неверно"):
                st.session_state.feedback_expanded = True

        if st.session_state.feedback_expanded:
            if not st.session_state.correction_confirmed:
                st.session_state.user_text = st.text_input(
                    "Введите, что изображено на фото",
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
                    st.write("🔎 Наиболее похожие варианты:")
                    for label, score, _ in matches:
                        st.write(f"- **{label}** ({score:.1f}%)")

                    options = [label for label, score, _ in matches]
                    selected = st.radio(
                        "Выберите наиболее подходящий вариант:", options
                    )

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
                        "✅ Подтвердить правильность",
                        on_click=confirm_correction,
                        disabled=st.session_state.correction_confirmed,
                    )

            else:
                st.success(
                    f"Спасибо! Фото учтено как "
                    f"'{st.session_state.selected_correction}'"
                )
