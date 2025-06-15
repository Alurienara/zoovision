# translations.py

TRANSLATIONS = {
    "ru": {
        "title": "🐾 ZooVision — кто перед нами?",
        "description": (
            "Загрузите фото животного — "
            "и ZooVision постарается определить вид. "
            "Чем крупнее и чётче мордочка, тем точнее результат! "
            "Рекомендуем обрезать лишний фон "
            "вручную для лучшего распознавания 🎯"
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
        "feedback_input": "Введите, что изображено на фото "
        "(сервис лучше распознаёт английский язык)",
        "matches_title": "🔎 Наиболее похожие варианты:",
        "select_best": "Выберите наиболее подходящий вариант:",
        "confirm_button": "✅ Подтвердить правильность",
        "thanks": "Спасибо! Фото учтено как '{label}'",
        "remove": "🗑️ Очистить всё",
        "about": "## ℹ️ О проекте",
        "about_text": (
            "**ZooVision** — финальный проект по курсу "
            "*Программная инженерия*.\n\n"
            "Это интерактивный веб-сервис для автоматической классификации "
            "изображений животных "
            "на основе предобученной нейросети ResNet50 — популярной "
            "архитектуры компьютерного зрения.\n\n"
            "ZooVision умеет распознавать вид животного по вашей фотографии "
            "практически любого качества! "
            "Модель обрабатывает более 300 классов животных, "
            "так что она точно отличит вашего попугайчика "
            "от голубя за окном. Если вдруг животное дикое "
            "или вы предпочитаете фотографировать своего хищника издалека — "
            "не беда! Вы можете обрезать изображение прямо на сайте так, "
            "как нужно.\n\n"
            "Хотя ZooVision и умный, он иногда может ошибаться. "
            "В этом случае вы всегда можете его поправить — "
            "указать правильное название животного. "
            "ZooVision бережно сохранит ваше исправление вместе с фотографией"
            ", и в будущем мы дообучим модель, чтобы она работала ещё точнее! "
            "Сервис доступен на русском и английском языках.\n\n"
            "Надеемся, что вам понравится работать с ZooVision ❤️"
        ),
        "footer": (
            "---\n"
            "🐾 **ZooVision © 2025** | "
            "Сделано с ❤️ студентами Богаткиной В.Е и Нестеровым Д.Д"
        ),
    },
    "en": {
        "title": "🐾 ZooVision — Who's here?",
        "description": (
            "Upload an animal photo and "
            "ZooVision will try to identify the species. "
            "The clearer and closer the animal's face, "
            "the more accurate the result! "
            "We recommend cropping unnecessary "
            "background for better recognition 🎯"
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
        "remove": "🗑️ Remove all",
        "about": "## ℹ️ About the project",
        "about_text": (
            "**ZooVision** — a final project for the "
            "*Software Engineering* course.\n\n"
            "It is an interactive web service for automatic "
            "animal image classification "
            "based on a pre-trained ResNet50 neural network — "
            "a popular computer vision architecture.\n\n"
            "ZooVision can recognize an animal species "
            "from your photo, no matter its quality! "
            "The model covers over 300 animal classes, "
            "so it will easily tell your parakeet "
            "from a pigeon outside the window. "
            "If the animal is wild or you prefer "
            "taking photos from afar — no problem! "
            "You can crop the image right in the browser as needed.\n\n"
            "Although ZooVision is smart, it can sometimes make mistakes. "
            "In that case, you can correct it by providing the right "
            "animal name. ZooVision carefully saves your correction together "
            "with the photo, and we plan to retrain the model in the future "
            "to make it even better! "
            "The service is available in both Russian and English.\n\n"
            "We hope you enjoy working with ZooVision ❤️"
        ),
        "footer": (
            "---\n"
            "🐾 **ZooVision © 2025** | "
            "Made with ❤️ by students Bogatkina V.E and Nesterov D.D"
        ),
    },
}
