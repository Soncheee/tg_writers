import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.generate import ai_generate
import app.keyboards as kb

logger = logging.getLogger(__name__)

router = Router()


# Определяем состояния
class Gen(StatesGroup):
    wait = State()  # Ожидание генерации
    writer_selected = State()  # Писатель выбран
    sticker_selection = State()  # Выбор стикерпака


# Стили писателей (будут использоваться только после ввода пользователем запроса)
WRITER_PROMPTS = {
    "ltolstoy": f"Поговори как Лев Толстой, используй его манеру речи: обстоятельную, философскую,"
            f"с глубокими размышлениями о жизни и морали. Ограничься 2-3 преложениями, отвечая на вопрос,"
                f" задавай вопросы по схожей теме собеседнику",
    "atolstoy": f"Поговори как Алексей Толстой, используй его стиль: живой, образный,"
            f"с элементами фантастики и исторической романтики.Ограничься 2-3 предложениями, отвечая на вопрос, задавай вопросы "
                f"по схожей теме собеседнику",
    "fmdostoevsckiy": f"Поговори как Ф.М. Достоевский, используй его манеру: напряженную,"
                  f"психологически глубокую, с драматизмом и внутренними конфликтами."
                      f"Ограничься 2-3 предложениями, отвечая на вопрос, задавай вопросы "
                  f"по схожей теме собеседнику"
}

# Стикеры (для Достоевского — ссылка, для остальных — placeholder или стикеры позже)
STICKER_PACKS = {
    "ltolstoy": "https://t.me/addstickers/LevTolstoj6",  # Замените на реальный sticker_id, если есть
    "atolstoy": "https://t.me/addstickers/AleksejTolstoj",  # Замените на реальный sticker_id, если есть
    "fmdostoevsckiy": "https://t.me/addstickers/Dostoevskij313"  # Ссылка на стикерпак Достоевского
}

# Фиксированные сообщения
HELP_MESSAGE = "Я - бот для общения с писателями, если у вас проблемы с кнопками и они не работают, введите название нужной вам кнопки вручную."
ABOUT_MESSAGE = ("Привет, я - бот для общения с писателями, здесь вы можете выбрать нужного вам писателя в каталоге, "
                 "а он поддержит диалог с вами в манере писателя, также есть команды /start для запуска бота и /help "
                 "и кнопка \"Помощь\" для вызова помощи. Приятного общения с писателями прошлого!")


@router.message(CommandStart())
async def cmd_start(message: Message):
    logger.info("Пользователь начал взаимодействие")
    await message.answer("Добро пожаловать! Выберите писателя в каталоге или посмотрите стикеры.", reply_markup=kb.main)


@router.message(Gen.wait)
async def stop_flood(message: Message):
    logger.info("Пользователь отправил запрос во время генерации")
    await message.answer("Подождите, ваш запрос генерируется")


@router.message(Command('help'))
async def cmd_help(message: Message):
    logger.info("Пользователь запросил помощь через команду")
    await message.answer(HELP_MESSAGE)


@router.message(F.text == 'Помощь')
async def help_info(message: Message):
    logger.info("Пользователь запросил помощь через кнопку")
    await message.answer(HELP_MESSAGE)


@router.message(F.text == 'О нас')
async def about_us(message: Message):
    logger.info("Пользователь запросил информацию о нас")
    await message.answer(ABOUT_MESSAGE)


@router.message(F.text == 'Стикеры')
async def stickers_catalog(message: Message, state: FSMContext):
    logger.info("Пользователь запросил стикеры")
    await message.answer("Выберите писателя, чтобы получить его стикер или стикерпак:", reply_markup=kb.catalog)
    await state.set_state(Gen.sticker_selection)


@router.message(F.text == 'Каталог писателей')
async def catalog(message: Message):
    logger.info("Пользователь запросил каталог")
    await message.answer('Выберите писателя', reply_markup=kb.catalog)


@router.callback_query(F.data == 'ltolstoy')
async def lev_t_choose(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Gen.sticker_selection.state:
        logger.info("Пользователь выбрал стикер Льва Толстого")
        await callback.answer('Вы выбрали стикерпак Льва Толстого', show_alert=True)
        await callback.message.answer_sticker(f"Вот стикерпак Льва Толстого: {STICKER_PACKS['ltolstoy']}")
        await state.clear()
    else:
        logger.info("Пользователь выбрал Льва Толстого для диалога")
        await callback.answer('Вы выбрали Льва Толстого', show_alert=True)
        await callback.message.answer('Вы выбрали Льва Толстого. Напишите ваш запрос, и я отвечу в его стиле.')
        await state.update_data(writer="ltolstoy", context=[])  # Инициализируем пустой контекст
        await state.set_state(Gen.writer_selected)


@router.callback_query(F.data == 'atolstoy')
async def a_t_choose(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Gen.sticker_selection.state:
        logger.info("Пользователь выбрал стикер Алексея Толстого")
        await callback.answer('Вы выбрали стикерпак Алексея Толстого', show_alert=True)
        await callback.message.answer_sticker(f"Вот стикерпак Алексея Толстого: {STICKER_PACKS['atolstoy']}")
        await state.clear()
    else:
        logger.info("Пользователь выбрал Алексея Толстого для диалога")
        await callback.answer('Вы выбрали Алексея Толстого', show_alert=True)
        await callback.message.answer('Вы выбрали Алексея Толстого. Напишите ваш запрос, и я отвечу в его стиле.')
        await state.update_data(writer="atolstoy", context=[])  # Инициализируем пустой контекст
        await state.set_state(Gen.writer_selected)


@router.callback_query(F.data == 'fmdostoevsckiy')
async def fm_dost_choose(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Gen.sticker_selection.state:
        logger.info("Пользователь выбрал стикерпак Ф.М. Достоевского")
        await callback.answer('Вы выбрали стикерпак Ф.М. Достоевского', show_alert=True)
        await callback.message.answer(f"Вот стикерпак Ф.М. Достоевского: {STICKER_PACKS['fmdostoevsckiy']}")
        await state.clear()
    else:
        logger.info("Пользователь выбрал Ф.М. Достоевского для диалога")
        await callback.answer('Вы выбрали Ф.М. Достоевского', show_alert=True)
        await callback.message.answer('Вы выбрали Ф.М. Достоевского. Напишите ваш запрос, и я отвечу в его стиле.')
        await state.update_data(writer="fmdostoevsckiy", context=[])  # Инициализируем пустой контекст
        await state.set_state(Gen.writer_selected)


@router.message(Gen.writer_selected)
async def handle_writer_conversation(message: Message, state: FSMContext):
    logger.info("Обработка сообщения в режиме выбранного писателя")
    data = await state.get_data()
    writer = data.get("writer")
    context = data.get("context", [])

    if not writer:
        await message.answer("Сначала выберите писателя из каталога.", reply_markup=kb.main)
        await state.clear()
        return

    await state.set_state(Gen.wait)
    try:
        # Добавляем промт писателя в начало контекста, если это первый запрос
        if not context:
            context = [{"role": "system", "content": WRITER_PROMPTS[writer]}]
        response, new_context = await ai_generate(message.text, context)
        await message.answer(response, parse_mode='Markdown')
        await state.update_data(context=new_context)
    except Exception as e:
        logger.error(f"Ошибка при генерации ответа: {e}")
        await message.answer("Произошла ошибка при генерации ответа.")
    finally:
        await state.set_state(Gen.writer_selected)


@router.message()
async def generating(message: Message, state: FSMContext):
    logger.info("Начало генерации ответа без выбранного писателя")
    await state.set_state(Gen.wait)
    try:
        response, context = await ai_generate(message.text)
        await message.answer(response, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Ошибка при генерации ответа: {e}")
        await message.answer("Произошла ошибка при генерации ответа.")
    finally:
        await state.clear()