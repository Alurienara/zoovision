import streamlit as st
from PIL import Image
from model.predictor import predict_image as predict_image_inat

st.set_page_config(page_title="ZooVision", layout="centered")
st.title("🐾 ZooVision — кто перед нами?")

st.markdown(
    """
    Загрузите фото животного — и мы постараемся определить вид.
    При желании вы можете вручную обрезать изображение, чтобы повысить точность анализа 🎯
    """
)

uploaded_file = st.file_uploader("📷 Загрузите изображение", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_width, img_height = image.size

    # --- Сброс обрезки при новом файле ---
    current_filename = uploaded_file.name
    if "last_filename" not in st.session_state:
        st.session_state.last_filename = ""
    if current_filename != st.session_state.last_filename:
        st.session_state.left = 0
        st.session_state.right = img_width
        st.session_state.top = 0
        st.session_state.bottom = img_height
        st.session_state.last_filename = current_filename

    st.image(image, caption="🖼 Оригинальное изображение", use_container_width=True)

    # --- Включение обрезки по желанию ---
    use_crop = st.checkbox("✂️ Обрезать изображение вручную?", value=False)

    if use_crop:
        st.subheader("📐 Настройка обрезки")

        # Читаем значения из состояния
        left = st.session_state.get("left", 0)
        right = st.session_state.get("right", img_width)
        top = st.session_state.get("top", 0)
        bottom = st.session_state.get("bottom", img_height)

        # Слайдеры
        col1, col2 = st.columns(2)
        with col1:
            left = st.slider("Слева", 0, img_width - 1, left)
            right = st.slider("Справа", left + 1, img_width, right)
        with col2:
            top = st.slider("Сверху", 0, img_height - 1, top)
            bottom = st.slider("Снизу", top + 1, img_height, bottom)

        # Обновляем session_state
        st.session_state.left = left
        st.session_state.right = right
        st.session_state.top = top
        st.session_state.bottom = bottom

        # Кроп и предпросмотр
        cropped_image = image.crop((left, top, right, bottom))
        st.image(cropped_image, caption="🔍 Обрезанное изображение", use_container_width=True)
        image_for_prediction = cropped_image
    else:
        image_for_prediction = image

    # --- Кнопка запуска анализа ---
    if st.button("🔍 Определить, кто это"):
        with st.spinner("Анализируем изображение..."):
            results = predict_image_inat(image_for_prediction)

        # --- Фильтрация слабых вероятностей ---
        filtered_results = [(label, score) for label, score in results if score > 0.01]

        st.subheader("🔎 Результаты классификации:")
        if filtered_results:
            main_label, main_score = filtered_results[0]
            st.success(f"✅ Это, скорее всего: **{main_label}** ({main_score:.2%})")

            if len(filtered_results) > 1:
                st.markdown("### Также возможные варианты:")
                for label, score in filtered_results[1:]:
                    st.write(f"• {label} — {score:.2%}")
        else:
            st.warning("Модель не смогла уверенно распознать объект на изображении.")