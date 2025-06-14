# translations.py

TRANSLATIONS = {
    "ru": {
        "title": "🐾 ZooVision — кто перед нами?",
        "description": (
            "Загрузите фото животного — и мы постараемся определить вид. "
            "Вы можете вручную обрезать изображение, "
            "чтобы повысить точность анализа 🎯"
        ),
        "upload_prompt": "📷 Загрузите изображение",
        "analyze_button": "🔍 Определить, кто это",
        "crop_manual": "✂️ Обрезать изображение вручную?",
        "original_image": "🖼 Оригинальное изображение",
        "cropped_image": "🔍 Обрезанное изображение",
        "analyze_image": "Анализируем изображение...",
        "results_title": "🔎 Результаты классификации:",
        "main_result": "✅ Это, скорее всего: **{label}** ({score:.2%})",
        "also_possible": "### Также возможные варианты:",
        "no_confidence": "Модель не смогла уверенно распознать "
        "объект на изображении.",
        "wrong_detected": "❌ Животное распознано неверно",
        "feedback_input": "Введите, что изображено на фото",
        "matches_title": "🔎 Наиболее похожие варианты:",
        "select_best": "Выберите наиболее подходящий вариант:",
        "confirm_button": "✅ Подтвердить правильность",
        "thanks": "Спасибо! Фото учтено как '{label}'",
    },
    "en": {
        "title": "🐾 ZooVision — Who's here?",
        "description": (
            "Upload an animal photo and we'll try to identify it. "
            "You can crop the image manually to improve accuracy 🎯"
        ),
        "upload_prompt": "📷 Upload an image",
        "analyze_button": "🔍 Identify animal",
        "crop_manual": "✂️ Crop image manually?",
        "original_image": "🖼 Original image",
        "cropped_image": "🔍 Cropped image",
        "analyze_image": "Analyzing image...",
        "results_title": "🔎 Classification results:",
        "main_result": "✅ Most likely: **{label}** ({score:.2%})",
        "also_possible": "### Other possible options:",
        "no_confidence": "The model couldn't confidently identify "
        "an object in the image.",
        "wrong_detected": "❌ Animal identified incorrectly",
        "feedback_input": "Enter what is shown in the photo",
        "matches_title": "🔎 Most similar options:",
        "select_best": "Select the most suitable option:",
        "confirm_button": "✅ Confirm",
        "thanks": "Thank you! The photo is marked as '{label}'",
    },
}
