#!/usr/bin/env python3
"""Generate the IntelliJ themes and editor colour schemes."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
THEMES_DIR = ROOT / "src/main/resources/themes"

PALETTES = (
    ("Black Metal", "black-metal", "#486e6f", "#dd9999", "#a06666"),
    ("Black Metal (Bathory)", "black-metal-bathory", "#5f8787", "#fbcb97", "#e78a53"),
    ("Black Metal (Burzum)", "black-metal-burzum", "#5f8787", "#ddeecc", "#99bbaa"),
    ("Black Metal (Dark Funeral)", "black-metal-dark-funeral", "#5f8787", "#d0dfee", "#5f81a5"),
    ("Black Metal (Gorgoroth)", "black-metal-gorgoroth", "#5f8787", "#9b8d7f", "#8c7f70"),
    ("Black Metal (Immortal)", "black-metal-immortal", "#5f8787", "#7799bb", "#556677"),
    ("Black Metal (Khold)", "black-metal-khold", "#5f8787", "#eceee3", "#974b46"),
    ("Black Metal (Marduk)", "black-metal-marduk", "#5f8787", "#a5aaa7", "#626b67"),
    ("Black Metal (Mayhem)", "black-metal-mayhem", "#5f8787", "#f3ecd4", "#eecc6c"),
    ("Black Metal (Nile)", "black-metal-nile", "#5f8787", "#aa9988", "#777755"),
    ("Black Metal (Venom)", "black-metal-venom", "#5f8787", "#f8f7f2", "#79241f"),
)


def blend(foreground: str, background: str, opacity: float) -> str:
    foreground_channels = tuple(int(foreground[index : index + 2], 16) for index in (1, 3, 5))
    background_channels = tuple(int(background[index : index + 2], 16) for index in (1, 3, 5))
    channels = tuple(
        round(foreground_channel * opacity + background_channel * (1 - opacity))
        for foreground_channel, background_channel in zip(foreground_channels, background_channels)
    )
    return "#" + "".join(f"{channel:02x}" for channel in channels)


def theme(name: str, slug: str, red: str, accent: str, secondary: str) -> dict[str, object]:
    background = "#000000"
    surface = "#0b0b0b"
    elevated = "#151515"
    control = "#1b1b1b"
    hover = "#303030"
    foreground = "#c1c1c1"
    muted = "#999999"
    disabled = "#555555"
    border = "#2e2e2e"
    main_window = elevated
    transparent = "#00000000"
    selection = blend(accent, background, 0.35)
    selection_inactive = blend(accent, background, 0.20)
    accent_subtle = blend(accent, surface, 0.18)
    secondary_subtle = blend(secondary, surface, 0.20)
    error_subtle = blend(red, surface, 0.22)

    return {
        "name": name,
        "dark": True,
        "author": "Samuel Boyden",
        "parentTheme": "Islands Dark",
        "editorScheme": f"/themes/{slug}.xml",
        "colors": {
            "background": background,
            "surface": surface,
            "elevated": elevated,
            "control": control,
            "hover": hover,
            "foreground": foreground,
            "muted": muted,
            "disabled": disabled,
            "border": border,
            "mainWindow": main_window,
            "transparent": transparent,
            "accent": accent,
            "accentSubtle": accent_subtle,
            "secondary": secondary,
            "secondarySubtle": secondary_subtle,
            "error": red,
            "errorSubtle": error_subtle,
            "selection": selection,
            "selectionInactive": selection_inactive,
        },
        "ui": {
            "*": {
                "background": "background",
                "foreground": "foreground",
                "selectionBackground": "selection",
                "selectionForeground": "foreground",
                "selectionInactiveBackground": "selectionInactive",
                "selectionBackgroundInactive": "selectionInactive",
                "disabledBackground": "surface",
                "inactiveBackground": "surface",
                "disabledForeground": "disabled",
                "disabledText": "disabled",
                "inactiveForeground": "muted",
                "errorForeground": "error",
                "borderColor": "border",
                "disabledBorderColor": "surface",
                "focusColor": "accent",
                "focusedBorderColor": "accent",
                "hoverBorderColor": "accent",
                "pressedBorderColor": "secondary",
                "separatorColor": "border",
                "lineSeparatorColor": "border",
            },
            "ActionButton": {
                "hoverBackground": "hover",
                "pressedBackground": "selection",
            },
            "Borders": {
                "color": "border",
                "ContrastBorderColor": "border",
            },
            "Button": {
                "startBackground": "control",
                "endBackground": "control",
                "startBorderColor": "border",
                "endBorderColor": "border",
                "default": {
                    "foreground": "background",
                    "startBackground": "accent",
                    "endBackground": "accent",
                    "startBorderColor": "accent",
                    "endBorderColor": "accent",
                    "focusedBorderColor": "secondary",
                },
            },
            "ComboBox": {
                "nonEditableBackground": "control",
                "modifiedItemForeground": "secondary",
                "ArrowButton": {
                    "iconColor": "foreground",
                    "disabledIconColor": "disabled",
                    "nonEditableBackground": "control",
                },
            },
            "CompletionPopup": {
                "background": "elevated",
                "foreground": "foreground",
                "matchForeground": "accent",
                "matchSelectionForeground": "secondary",
                "selectionBackground": "selection",
                "selectionForeground": "foreground",
                "selectionInactiveBackground": "selectionInactive",
            },
            "Component": {
                "focusedBorderColor": "accent",
                "errorFocusColor": "error",
                "inactiveErrorFocusColor": "errorSubtle",
                "warningFocusColor": "secondary",
                "inactiveWarningFocusColor": "secondarySubtle",
                "iconColor": "foreground",
                "hoverIconColor": "accent",
            },
            "Counter": {
                "background": "accent",
                "foreground": "background",
            },
            "DefaultTabs": {
                "underlineColor": "accent",
                "inactiveUnderlineColor": "selectionInactive",
                "hoverBackground": "hover",
            },
            "Editor": {
                "background": "background",
                "foreground": "foreground",
                "shortcutForeground": "secondary",
            },
            "EditorTabs": {
                "background": "background",
                "borderColor": "border",
                "underTabsBorderColor": "border",
                "selectedBackground": "surface",
                "hoverBackground": "hover",
                "hoverColor": "hover",
                "underlineColor": "accent",
                "underlinedBorderColor": "accent",
                "inactiveUnderlinedTabBorderColor": "selectionInactive",
                "underlinedTabBackground": "surface",
                "inactiveUnderlinedTabBackground": "background",
                "inactiveColoredFileBackground": "background",
            },
            "Link": {
                "activeForeground": "accent",
                "hoverForeground": "secondary",
                "pressedForeground": "secondary",
                "secondaryForeground": "muted",
                "focusedBorderColor": "accent",
            },
            "List": {
                "background": "background",
                "foreground": "foreground",
                "hoverBackground": "hover",
                "hoverInactiveBackground": "control",
            },
            "MainMenu": {
                "background": "background",
                "foreground": "foreground",
                "selectionBackground": "selection",
                "selectionForeground": "foreground",
            },
            "Island": {"borderColor": "background"},
            "MainToolbar": {
                "background": "mainWindow",
                "borderColor": "transparent",
                "separatorColor": "border",
                "Icon": {
                    "background": "background",
                    "pressedBackground": "selection",
                },
                "Dropdown": {
                    "pressedBackground": "selection",
                    "transparentHoverBackground": "hover",
                },
            },
            "MainWindow": {
                "background": "mainWindow",
                "Tab": {
                    "background": "background",
                    "foreground": "muted",
                    "selectedBackground": "surface",
                    "selectedInactiveBackground": "surface",
                    "selectedForeground": "foreground",
                    "hoverBackground": "hover",
                    "hoverForeground": "foreground",
                    "separatorColor": "border",
                    "borderColor": "border",
                },
            },
            "Menu": {
                "background": "elevated",
                "foreground": "foreground",
                "selectionBackground": "selection",
                "selectionForeground": "foreground",
            },
            "MenuItem": {
                "background": "elevated",
                "foreground": "foreground",
                "selectionBackground": "selection",
                "selectionForeground": "foreground",
                "disabledForeground": "disabled",
            },
            "Notification": {
                "background": "elevated",
                "foreground": "foreground",
                "borderColor": "border",
                "linkForeground": "accent",
                "errorBackground": "errorSubtle",
                "errorBorderColor": "error",
                "errorForeground": "foreground",
            },
            "Popup": {
                "background": "elevated",
                "innerBorderColor": "border",
                "separatorColor": "border",
                "separatorForeground": "muted",
                "Header": {
                    "activeForeground": "foreground",
                    "inactiveForeground": "muted",
                },
                "Advertiser": {
                    "background": "surface",
                    "borderColor": "border",
                    "foreground": "muted",
                },
            },
            "PopupMenu": {
                "background": "elevated",
                "foreground": "foreground",
                "selectionBackground": "selection",
                "selectionForeground": "foreground",
            },
            "ProgressBar": {
                "progressColor": "accent",
                "failedColor": "error",
                "failedEndColor": "error",
                "passedColor": "accent",
                "passedEndColor": "accent",
                "warningColor": "secondary",
                "warningEndColor": "secondary",
            },
            "SearchEverywhere": {
                "Header": {"background": "elevated"},
                "SearchField": {
                    "background": "control",
                    "borderColor": "accent",
                    "infoForeground": "muted",
                },
                "Advertiser": {
                    "background": "surface",
                    "foreground": "muted",
                },
                "List": {
                    "separatorColor": "border",
                    "separatorForeground": "muted",
                    "settingsBackground": "surface",
                },
                "Tab": {
                    "selectedBackground": "selection",
                    "selectedForeground": "foreground",
                },
            },
            "StatusBar": {
                "background": "mainWindow",
                "borderColor": "transparent",
                "Widget": {
                    "foreground": "muted",
                    "hoverBackground": "hover",
                    "hoverForeground": "foreground",
                    "pressedBackground": "selection",
                },
            },
            "Table": {
                "background": "background",
                "foreground": "foreground",
                "hoverBackground": "hover",
                "hoverInactiveBackground": "control",
                "lightSelectionBackground": "selection",
                "lightSelectionForeground": "foreground",
                "lightSelectionInactiveBackground": "selectionInactive",
                "lightSelectionInactiveForeground": "foreground",
                "alternativeRowBackground": "surface",
                "stripeColor": "surface",
            },
            "TextField": {
                "background": "control",
                "foreground": "foreground",
                "selectionBackground": "selection",
                "selectionForeground": "foreground",
                "inactiveForeground": "muted",
            },
            "ToolWindow": {
                "background": "background",
                "borderColor": "border",
                "Header": {
                    "background": "surface",
                    "inactiveBackground": "surface",
                    "borderColor": "border",
                },
                "HeaderTab": {
                    "selectedBackground": "surface",
                    "selectedInactiveBackground": "surface",
                    "hoverBackground": "hover",
                    "hoverInactiveBackground": "control",
                    "underlineColor": "accent",
                    "inactiveUnderlineColor": "selectionInactive",
                    "underlinedTabBackground": "surface",
                    "underlinedTabInactiveBackground": "surface",
                },
                "Button": {
                    "foreground": "muted",
                    "hoverBackground": "hover",
                    "selectedBackground": "selection",
                    "selectedForeground": "foreground",
                },
                "Stripe": {
                    "background": "mainWindow",
                    "borderColor": "transparent",
                    "separatorColor": "border",
                },
            },
            "Tree": {
                "background": "background",
                "foreground": "foreground",
                "selectionBackground": "selection",
                "selectionForeground": "foreground",
                "selectionInactiveBackground": "selectionInactive",
                "hoverBackground": "hover",
                "hoverInactiveBackground": "control",
            },
            "WelcomeScreen": {
                "background": "background",
                "borderColor": "border",
                "captionBackground": "surface",
                "captionForeground": "foreground",
                "footerBackground": "background",
                "footerForeground": "muted",
                "headerBackground": "background",
                "headerForeground": "foreground",
                "separatorColor": "border",
                "SidePanel": {"background": "surface"},
                "Projects": {
                    "background": "background",
                    "selectionBackground": "selection",
                    "selectionInactiveBackground": "selectionInactive",
                },
            },
        },
        "icons": {
            "ColorPalette": {
                "Actions.Grey": secondary,
                "Actions.Red": secondary,
                "Actions.Yellow": secondary,
                "Actions.Green": secondary,
                "Actions.Blue": secondary,
                "Actions.GreyInline.Dark": secondary,
                "Objects.Grey": secondary,
                "Objects.RedStatus": secondary,
                "Objects.Red": secondary,
                "Objects.Pink": secondary,
                "Objects.Yellow": secondary,
                "Objects.Green": secondary,
                "Objects.Blue": secondary,
                "Objects.Purple": secondary,
                "Objects.BlackText": background,
                "Objects.YellowDark": secondary,
                "Objects.GreenAndroid": secondary,
                "#CED0D6": secondary,
                "#AFB1B3": secondary,
                "#548AF7": secondary,
                "#DB5C5C": secondary,
                "#C75450": secondary,
                "#57965C": secondary,
                "#3592C4": secondary,
                "#499C54": secondary,
                "#F2C55C": secondary,
                "#F0A732": secondary,
                "#C77D55": secondary,
                "#868A91": secondary,
                "#A571E6": secondary,
                "#B589EC": secondary,
                "#9DA0A8": secondary,
                "#B4B8BF": secondary,
                "#F98B9E": secondary,
                "#5FAD65": secondary,
                "#43454A": accent_subtle,
                "#25324D": accent_subtle,
                "#253627": accent_subtle,
                "#402929": accent_subtle,
                "#45322B": accent_subtle,
                "#3D3223": accent_subtle,
                "#2F2936": accent_subtle,
                "Checkbox.Background.Default.Dark": control,
                "Checkbox.Border.Default.Dark": muted,
                "Checkbox.Background.Selected.Dark": accent,
                "Checkbox.Border.Selected.Dark": accent,
                "Checkbox.Foreground.Selected.Dark": background,
                "Checkbox.Focus.Wide.Dark": accent,
                "Checkbox.Focus.Thin.Default.Dark": accent,
                "Checkbox.Focus.Thin.Selected.Dark": secondary,
                "Checkbox.Background.Disabled.Dark": surface,
                "Checkbox.Border.Disabled.Dark": disabled,
                "Checkbox.Foreground.Disabled.Dark": disabled,
            }
        },
    }


def xml_colour(colour: str) -> str:
    return colour.removeprefix("#").upper()


def add_colour(parent: ElementTree.Element, name: str, colour: str) -> None:
    ElementTree.SubElement(parent, "option", {"name": name, "value": xml_colour(colour)})


def add_attribute(
    parent: ElementTree.Element,
    name: str,
    *,
    foreground: str | None = None,
    background: str | None = None,
    font_type: int | None = None,
    effect_colour: str | None = None,
    effect_type: int | None = None,
) -> None:
    option = ElementTree.SubElement(parent, "option", {"name": name})
    value = ElementTree.SubElement(option, "value")
    if foreground is not None:
        add_colour(value, "FOREGROUND", foreground)
    if background is not None:
        add_colour(value, "BACKGROUND", background)
    if font_type is not None:
        ElementTree.SubElement(value, "option", {"name": "FONT_TYPE", "value": str(font_type)})
    if effect_colour is not None:
        add_colour(value, "EFFECT_COLOR", effect_colour)
    if effect_type is not None:
        ElementTree.SubElement(value, "option", {"name": "EFFECT_TYPE", "value": str(effect_type)})


def editor_scheme(name: str, red: str, accent: str, secondary: str) -> ElementTree.Element:
    background = "#000000"
    foreground = "#c1c1c1"
    muted = "#808080"
    punctuation = "#888888"
    operator = "#999999"
    parameter = "#aaaaaa"
    active_line = "#121212"
    selection = blend(accent, background, 0.35)
    selection_inactive = blend(accent, background, 0.20)

    scheme = ElementTree.Element(
        "scheme",
        {"name": name, "version": "142", "parent_scheme": "Darcula"},
    )
    metadata = ElementTree.SubElement(scheme, "metaInfo")
    for property_name, property_value in (
        ("created", "2026-04-10T00:00:00"),
        ("ide", "idea"),
        ("ideVersion", "2025.2.6.2"),
        ("modified", "2026-04-10T00:00:00"),
        ("originalScheme", name),
    ):
        property_node = ElementTree.SubElement(metadata, "property", {"name": property_name})
        property_node.text = property_value

    colours = ElementTree.SubElement(scheme, "colors")
    for colour_name, colour in (
        ("CARET_COLOR", accent),
        ("CARET_ROW_COLOR", active_line),
        ("CONSOLE_BACKGROUND_KEY", background),
        ("DOCUMENTATION_COLOR", "#151515"),
        ("GUTTER_BACKGROUND", background),
        ("INDENT_GUIDE", "#181818"),
        ("LINE_NUMBERS_COLOR", "#666666"),
        ("LINE_NUMBER_ON_CARET_ROW_COLOR", accent),
        ("METHOD_SEPARATORS_COLOR", "#2e2e2e"),
        ("RIGHT_MARGIN_COLOR", "#242424"),
        ("SELECTED_INDENT_GUIDE", "#353535"),
        ("SELECTION_BACKGROUND", selection),
        ("SELECTION_FOREGROUND", foreground),
        ("INACTIVE_SELECTION_BACKGROUND", selection_inactive),
        ("TEARLINE_COLOR", "#2e2e2e"),
        ("WHITESPACES", "#242424"),
    ):
        add_colour(colours, colour_name, colour)

    attributes = ElementTree.SubElement(scheme, "attributes")
    add_attribute(attributes, "TEXT", foreground=foreground, background=background)
    add_attribute(attributes, "DEFAULT_TEXT", foreground=foreground, background=background)

    plain = {
        "DEFAULT_IDENTIFIER": foreground,
        "DEFAULT_INSTANCE_FIELD": foreground,
        "DEFAULT_STATIC_FIELD": foreground,
        "DEFAULT_LOCAL_VARIABLE": foreground,
        "DEFAULT_GLOBAL_VARIABLE": foreground,
        "DEFAULT_FUNCTION_CALL": foreground,
        "DEFAULT_PROPERTY": foreground,
        "DEFAULT_CONSTRUCTOR": foreground,
        "DEFAULT_OPERATION_SIGN": operator,
        "DEFAULT_COMMA": punctuation,
        "DEFAULT_DOT": punctuation,
        "DEFAULT_SEMICOLON": punctuation,
        "DEFAULT_BRACES": operator,
        "DEFAULT_BRACKETS": operator,
        "DEFAULT_PARENTHESES": operator,
        "DEFAULT_PARAMETER": parameter,
        "DEFAULT_KEYWORD": secondary,
        "DEFAULT_LABEL": secondary,
        "DEFAULT_METADATA": secondary,
        "DEFAULT_NUMBER": accent,
        "DEFAULT_CONSTANT": accent,
        "DEFAULT_PREDEFINED_SYMBOL": accent,
        "DEFAULT_STRING": accent,
        "DEFAULT_VALID_STRING_ESCAPE": secondary,
        "DEFAULT_MARKUP_TAG": secondary,
        "DEFAULT_TAG": secondary,
        "DEFAULT_MARKUP_ATTRIBUTE": secondary,
        "DEFAULT_ENTITY": red,
        "DEFAULT_CLASS_NAME": accent,
        "DEFAULT_INTERFACE_NAME": accent,
        "DEFAULT_ENUM_NAME": accent,
        "DEFAULT_TYPE_PARAMETER": accent,
        "DEFAULT_REASSIGNED_PARAMETER": secondary,
        "DEFAULT_REASSIGNED_LOCAL_VARIABLE": secondary,
        "CONSOLE_NORMAL_OUTPUT": foreground,
        "CONSOLE_SYSTEM_OUTPUT": operator,
        "CONSOLE_USER_INPUT": accent,
        "CONSOLE_ERROR_OUTPUT": red,
    }
    for attribute_name, colour in plain.items():
        add_attribute(attributes, attribute_name, foreground=colour)

    for attribute_name in (
        "DEFAULT_LINE_COMMENT",
        "DEFAULT_BLOCK_COMMENT",
        "DEFAULT_DOC_COMMENT",
        "DEFAULT_DOC_COMMENT_TAG_VALUE",
    ):
        add_attribute(attributes, attribute_name, foreground=muted, font_type=2)

    for attribute_name in (
        "DEFAULT_FUNCTION_DECLARATION",
        "DEFAULT_STATIC_METHOD",
        "DEFAULT_CLASS_REFERENCE",
        "KOTLIN_DSL_STYLE1",
        "KOTLIN_DSL_STYLE2",
        "KOTLIN_DSL_STYLE3",
        "KOTLIN_DSL_STYLE4",
    ):
        add_attribute(attributes, attribute_name, foreground=foreground, font_type=1)

    kotlin_plain = {
        "KOTLIN_KEYWORD": secondary,
        "KOTLIN_BUILTIN_ANNOTATION": secondary,
        "KOTLIN_KEYWORD_VAL": secondary,
        "KOTLIN_KEYWORD_VAR": secondary,
        "KOTLIN_ANNOTATION": secondary,
        "KOTLIN_LABEL": secondary,
        "KOTLIN_NAMED_ARGUMENT": secondary,
        "KOTLIN_ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES": secondary,
        "KDOC_TAG_NAME": secondary,
        "KDOC_LINK": accent,
        "KOTLIN_NUMBER": accent,
        "KOTLIN_STRING": accent,
        "KOTLIN_STRING_ESCAPE": secondary,
        "KOTLIN_OPERATION_SIGN": operator,
        "KOTLIN_AMPERSAND": operator,
        "KOTLIN_PARENTHESIS": operator,
        "KOTLIN_BRACES": operator,
        "KOTLIN_BRACKETS": operator,
        "KOTLIN_COMMA": punctuation,
        "KOTLIN_SEMICOLON": punctuation,
        "KOTLIN_COLON": punctuation,
        "KOTLIN_DOUBLE_COLON": punctuation,
        "KOTLIN_DOT": punctuation,
        "KOTLIN_SAFE_ACCESS": punctuation,
        "KOTLIN_QUEST": operator,
        "KOTLIN_EXCLEXCL": operator,
        "KOTLIN_ARROW": operator,
        "KOTLIN_CLASS": accent,
        "KOTLIN_TYPE_PARAMETER": accent,
        "KOTLIN_ABSTRACT_CLASS": accent,
        "KOTLIN_TRAIT": accent,
        "KOTLIN_OBJECT": accent,
        "KOTLIN_ENUM": accent,
        "KOTLIN_ENUM_ENTRY": secondary,
        "KOTLIN_TYPE_ALIAS": accent,
        "KOTLIN_DATA_CLASS": accent,
        "KOTLIN_DATA_OBJECT": accent,
        "KOTLIN_MUTABLE_VARIABLE": foreground,
        "KOTLIN_LOCAL_VARIABLE": foreground,
        "KOTLIN_PARAMETER": parameter,
        "KOTLIN_WRAPPED_INTO_REF": foreground,
        "KOTLIN_INSTANCE_PROPERTY": foreground,
        "KOTLIN_PACKAGE_PROPERTY": foreground,
        "KOTLIN_BACKING_FIELD_VARIABLE": foreground,
        "KOTLIN_EXTENSION_PROPERTY": foreground,
        "KOTLIN_SYNTHETIC_EXTENSION_PROPERTY": foreground,
        "KOTLIN_DYNAMIC_PROPERTY_CALL": foreground,
        "KOTLIN_ANDROID_EXTENSIONS_PROPERTY_CALL": foreground,
        "KOTLIN_INSTANCE_PROPERTY_CUSTOM_PROPERTY_DECLARATION": foreground,
        "KOTLIN_PACKAGE_PROPERTY_CUSTOM_PROPERTY_DECLARATION": foreground,
        "KOTLIN_CLOSURE_DEFAULT_PARAMETER": parameter,
        "KOTLIN_FUNCTION_CALL": foreground,
        "KOTLIN_EXTENSION_FUNCTION_CALL": foreground,
        "KOTLIN_SUSPEND_FUNCTION_CALL": foreground,
        "KOTLIN_VARIABLE_AS_FUNCTION": foreground,
        "KOTLIN_VARIABLE_AS_FUNCTION_LIKE": foreground,
        "KOTLIN_CONTEXT_ARGUMENT": parameter,
        "KOTLIN_SMART_CAST_VALUE": foreground,
        "KOTLIN_SMART_CONSTANT": foreground,
        "KOTLIN_SMART_CAST_RECEIVER": foreground,
    }
    for attribute_name, colour in kotlin_plain.items():
        add_attribute(attributes, attribute_name, foreground=colour)

    for attribute_name in (
        "KOTLIN_FUNCTION_DECLARATION",
        "KOTLIN_PACKAGE_FUNCTION_CALL",
        "KOTLIN_CONSTRUCTOR",
        "KOTLIN_DYNAMIC_FUNCTION_CALL",
    ):
        add_attribute(attributes, attribute_name, foreground=foreground, font_type=1)

    for attribute_name in ("KOTLIN_LINE_COMMENT", "KOTLIN_BLOCK_COMMENT", "KOTLIN_DOC_COMMENT"):
        add_attribute(attributes, attribute_name, foreground=muted, font_type=2)

    add_attribute(attributes, "KOTLIN_INVALID_STRING_ESCAPE", foreground=red, effect_colour=red, effect_type=2)
    add_attribute(attributes, "KOTLIN_BAD_CHARACTER", foreground=foreground, background=red)
    add_attribute(attributes, "KOTLIN_RESOLVED_TO_ERROR", effect_colour=red, effect_type=2)

    add_attribute(attributes, "DEFAULT_DOC_COMMENT_TAG", foreground=secondary, font_type=2)
    add_attribute(attributes, "DEFAULT_DOC_MARKUP", foreground=operator, font_type=2)
    add_attribute(attributes, "DEFAULT_INVALID_STRING_ESCAPE", foreground=red, effect_colour=red, effect_type=2)
    add_attribute(attributes, "BAD_CHARACTER", foreground=foreground, background=red)
    add_attribute(attributes, "ERRORS_ATTRIBUTES", effect_colour=red, effect_type=2)
    add_attribute(attributes, "WARNING_ATTRIBUTES", effect_colour=secondary, effect_type=2)
    add_attribute(attributes, "WEAK_WARNING_ATTRIBUTES", effect_colour=muted, effect_type=2)
    add_attribute(attributes, "DEPRECATED_ATTRIBUTES", effect_colour=muted, effect_type=3)
    add_attribute(attributes, "TODO_DEFAULT_ATTRIBUTES", foreground=accent, font_type=1)
    add_attribute(attributes, "HYPERLINK_ATTRIBUTES", foreground=accent, effect_colour=accent, effect_type=1)
    add_attribute(attributes, "FOLLOWED_HYPERLINK_ATTRIBUTES", foreground=secondary, effect_colour=secondary, effect_type=1)
    add_attribute(attributes, "SEARCH_RESULT_ATTRIBUTES", background=blend(accent, background, 0.28))
    add_attribute(attributes, "WRITE_SEARCH_RESULT_ATTRIBUTES", background=blend(secondary, background, 0.28))
    add_attribute(attributes, "TEXT_SEARCH_RESULT_ATTRIBUTES", background=blend(accent, background, 0.28))
    add_attribute(attributes, "LIVE_TEMPLATE_ATTRIBUTES", effect_colour=accent, effect_type=1)
    add_attribute(attributes, "INJECTED_LANGUAGE_FRAGMENT", background="#0b0b0b")
    add_attribute(attributes, "FOLDED_TEXT_ATTRIBUTES", foreground=muted, background="#151515")
    add_attribute(attributes, "NOT_USED_ELEMENT_ATTRIBUTES", foreground="#666666")
    add_attribute(attributes, "MATCHED_BRACE_ATTRIBUTES", foreground=foreground, background=selection, font_type=1)
    add_attribute(attributes, "UNMATCHED_BRACE_ATTRIBUTES", foreground=foreground, background=red, font_type=1)

    diff_colours = {
        "DIFF_INSERTED": blend(accent, background, 0.16),
        "DIFF_DELETED": blend(red, background, 0.20),
        "DIFF_MODIFIED": blend(secondary, background, 0.18),
        "DIFF_CONFLICT": blend(secondary, background, 0.28),
    }
    for attribute_name, colour in diff_colours.items():
        add_attribute(attributes, attribute_name, background=colour)

    return scheme


def indent_xml(root: ElementTree.Element) -> str:
    ElementTree.indent(root, space="  ")
    xml = ElementTree.tostring(root, encoding="unicode", short_empty_elements=True)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml}\n'


def main() -> None:
    if THEMES_DIR.exists():
        shutil.rmtree(THEMES_DIR)
    THEMES_DIR.mkdir(parents=True)

    for name, slug, red, accent, secondary in PALETTES:
        theme_path = THEMES_DIR / f"{slug}.theme.json"
        theme_path.write_text(json.dumps(theme(name, slug, red, accent, secondary), indent=2) + "\n")

        scheme_path = THEMES_DIR / f"{slug}.xml"
        scheme_path.write_text(indent_xml(editor_scheme(name, red, accent, secondary)))

    generated = sorted(path.name for path in THEMES_DIR.iterdir())
    if len(generated) != len(PALETTES) * 2:
        raise RuntimeError(f"Expected {len(PALETTES) * 2} generated files, found {len(generated)}")
    if any(not re.fullmatch(r"black-metal(?:-[a-z]+)*\.(?:theme\.json|xml)", name) for name in generated):
        raise RuntimeError("Generated an unexpected file name")


if __name__ == "__main__":
    main()
