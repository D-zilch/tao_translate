from typing import Any, List, Optional

import PySimpleGUI as sg

from .crawler import get_sugar, update_sugar, yd_translate
from .settings import LANGUAGE_MAPPING, TRANSLATE_SELECTED

sg.ChangeLookAndFeel("GreenTan")


menu_list = [
    ["File", ["close"]],
    ["Help", "about"],
]
combo_frame = sg.Frame(
    layout=[
        [
            sg.Combo(
                key="-FROM LANG-",
                values=TRANSLATE_SELECTED,
                default_value="中文",
                font=("微软雅黑", 12),
                size=(5, 10),
                pad=((15, 5), (10, 5)),
                enable_events=True,
            ),
            sg.Text(" » ", auto_size_text=True),
            sg.Combo(
                key="-TO LANG-",
                values=TRANSLATE_SELECTED,
                default_value="英语",
                font=("微软雅黑", 12),
                size=(5, 10),
                pad=((15, 5), (10, 5)),
                enable_events=True,
            ),
        ]
    ],
    title="选择翻译语言",
    title_color="white",
)

ml_frame1 = sg.Frame(
    key="-IN LANG-",
    layout=[
        [
            sg.ML(
                key="-INPUT-",
                size=(40, 8),
                font=("微软雅黑", 12),
                pad=((15, 15), (5, 15)),
                autoscroll=True,
                enable_events=True,
            ),
        ]
    ],
    title="中文",
)

ml_frame2 = sg.Frame(
    key="-OUTPUT LANG-",
    layout=[
        [
            sg.ML(
                key="-OUTPUT-",
                size=(40, 8),
                font=("微软雅黑", 12),
                pad=((15, 15), (5, 5)),
                write_only=True,
            )
        ]
    ],
    title="英文",
)

layout: List[List[Any]] = [
    [sg.Menu(menu_list, font=("宋体", 9))],
    [
        combo_frame,
        sg.Checkbox(
            "开启实时翻译",
            key="-REALTIME-",
            font=("微软雅黑", 10),
            pad=((40, 5), (50, 5)),
            enable_events=True,
        ),
    ],
    [ml_frame1],
    [ml_frame2],
    [
        sg.Button(
            "翻译",
            key="-TRANSLATE-",
            font=("微软雅黑", 10, "bold"),
            size=(10, 1),
            button_color=("white", "red"),
            auto_size_button=True,
            pad=((333, 15), (5, 10)),
            enable_events=True,
        ),
    ],
]


def run_gui(window) -> Optional[str]:
    event, values = window.read()
    realtime = False
    try:
        sugar = get_sugar()
    except Exception:
        update_sugar()
        sugar = get_sugar()

    if event == "-FROM LANG-":
        window.Element("-IN LANG-").update(values["-FROM LANG-"])

    if event == "-TO LANG-":
        window.Element("-OUTPUT LANG-").update(values["-TO LANG-"])

    if event == "-REALTIME-":
        realtime = not realtime

    if (
        (event == "-INPUT-" or event == "-FROM LANG-")
        and realtime
        or event == "-TRANSLATE-"
    ):
        zh_lang = values["-INPUT-"]
        from_lang, to_lang = (
            LANGUAGE_MAPPING[values["-FROM LANG-"]],
            LANGUAGE_MAPPING[values["-TO LANG-"]],
        )
        try:
            other_lang = yd_translate(
                zh_lang, sugar, from_lang=from_lang, to_lang=to_lang
            )
        except ValueError:
            button = sg.popup_ok_cancel(
                "数据源需要更新，请点击确认",
                title="Error",
                keep_on_top=True,
                font=("微软雅黑", 10),
            )
            if button == "OK":
                update_sugar()
                sg.popup_no_buttons("数据源更新完成", keep_on_top=True, font=("微软雅黑", 11))
        except ConnectionError:
            sg.popup("网络连接错误，请检查你的网络", title="Error", keep_on_top=True)
        except Exception as e:
            sg.popup_scrolled(
                e,
                title="Error",
                keep_on_top=True,
            )
        else:
            window["-OUTPUT-"].update(other_lang)

    if event in (sg.WINDOW_CLOSED, "close"):
        return "EXIT"

    if event == "about":
        sg.popup("Created by zilch")

    return None
