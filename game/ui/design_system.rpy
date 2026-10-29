init -40 python:
    NS_COLOR = {
        "neutral_950": "#151922", "neutral_900": "#1D2330", "neutral_800": "#293241",
        "neutral_700": "#39475A", "neutral_500": "#7F8DA3", "neutral_200": "#C7D0DD",
        "neutral_100": "#F0F3F7", "text_secondary": "#C7D0DD", "text_disabled": "#9AA6B899",
        "amber": "#E4A63A", "coral": "#D87468", "teal": "#4FA7A0",
        "green": "#71A36F", "violet": "#8F78B8", "red": "#B9544F",
        "hud_default": "#293241A8", "hud_hover": "#39475AE6",
        "hud_selected": "#355B66E6", "hud_disabled": "#29324166",
        "hud_border": "#C7D0DD66", "overlay": "#151922CC",
        "box": "#39475A", "box_dark": "#232C3A", "wardrobe": "#334154", "mirror": "#8B9795",
    }
    NS_SPACE = {"xs": 4, "s": 8, "m": 12, "l": 16, "xl": 24, "xxl": 32, "huge": 48}
    NS_SIZE = {"top_medallion": 68, "world_tile": 104, "icon": 24, "item_cell": 160}

style ns_panel:
    background Solid(NS_COLOR["neutral_800"] + "EB")
    padding (24, 20)

style ns_panel_compact is ns_panel:
    padding (16, 12)

style ns_surface_light is ns_panel:
    background Solid(NS_COLOR["neutral_700"] + "E8")

style ns_title:
    color NS_COLOR["neutral_100"]
    size 30
    bold True

style ns_section_title is ns_title:
    size 20

style ns_text:
    color NS_COLOR["neutral_100"]
    size 18

style ns_muted:
    color NS_COLOR["text_secondary"]
    size 16

style ns_caption is ns_muted:
    size 13

style ns_button:
    background Solid(NS_COLOR["neutral_800"] + "D9")
    hover_background Solid(NS_COLOR["neutral_700"] + "F2")
    selected_background Solid(NS_COLOR["hud_selected"])
    selected_hover_background Solid(NS_COLOR["hud_selected"])
    insensitive_background Solid(NS_COLOR["hud_disabled"])
    padding (18, 12)

style ns_button_text:
    color NS_COLOR["neutral_100"]
    hover_color NS_COLOR["amber"]
    selected_color NS_COLOR["amber"]
    insensitive_color NS_COLOR["text_disabled"]
    size 18
    text_align 0.5

style ns_tab_button is ns_button:
    xminimum 116
    ysize 52
    padding (16, 10)

style ns_tab_button_text is ns_button_text:
    size 16

style ns_item_button is ns_button:
    xsize 160
    ysize 160
    padding (12, 12)

style ns_item_button_text is ns_button_text:
    size 16

style ns_shop_item_button is ns_button:
    xsize 320
    ysize 250
    padding (18, 16)

style ns_shop_item_button_text is ns_button_text:
    size 16

style ns_empty_cell:
    background Solid(NS_COLOR["neutral_900"] + "55")
    xsize 160
    ysize 160
    padding (12, 12)

style ns_close_button is ns_button:
    xminimum 112
    ysize 48
    padding (12, 8)

style ns_close_button_text is ns_button_text:
    size 16

style ns_hud_panel:
    background Frame("ui/hud/panel.svg", 20, 20)
    padding (18, 14)

style ns_hud_top_medallion:
    background "ui/hud/circle-idle.svg"
    hover_background "ui/hud/circle-hover.svg"
    insensitive_background "ui/hud/circle-disabled.svg"
    padding (0, 0)
    xsize 68
    ysize 68

style ns_hud_circle_button:
    background "ui/hud/circle-idle.svg"
    hover_background "ui/hud/circle-hover.svg"
    insensitive_background "ui/hud/circle-disabled.svg"
    padding (0, 0)
    xsize 104
    ysize 104

style ns_hud_circle_selected is ns_hud_circle_button:
    background "ui/hud/circle-selected.svg"
    hover_background "ui/hud/circle-selected.svg"

style ns_hud_circle_context is ns_hud_circle_button:
    background "ui/hud/circle-context.svg"
    hover_background "ui/hud/circle-context.svg"

style ns_hud_tile_label:
    color NS_COLOR["neutral_100"]
    size 15
    bold True
    text_align 0.5
    outlines [(2, NS_COLOR["neutral_950"] + "E6", 0, 2)]

style ns_hud_tile_caption:
    color NS_COLOR["text_secondary"]
    size 13
    text_align 0.5
    outlines [(2, NS_COLOR["neutral_950"] + "E6", 0, 2)]

transform ns_hud_dimmed:
    alpha 0.32

transform ns_hud_active:
    alpha 1.0
