"""一款适合手机竖屏使用的单牌塔罗占卜应用。"""

import random

from kivy.app import App
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rotate
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget


CARDS = [
    ("愚者", "新的旅程正在展开。保持好奇，先迈出一步，答案会在路上出现。", "00_Fool.jpg"),
    ("魔术师", "你手中的资源已经足够。把想法说出来，并把它变成一个具体行动。", "01_Magician.jpg"),
    ("女祭司", "直觉比喧闹的意见更接近真相。给自己一点安静的时间再做决定。", "02_High_Priestess.jpg"),
    ("皇后", "滋养与创造力正在增长。照顾好自己，也让重要的关系自然发展。", "03_Empress.jpg"),
    ("皇帝", "建立秩序，守住边界。清晰的计划会让你的力量真正落地。", "04_Emperor.jpg"),
    ("教皇", "向可靠的传统或导师学习。共同的价值观会为你带来支持。", "05_Hierophant.jpg"),
    ("恋人", "重要的选择需要诚实面对内心。真诚的连接比完美答案更重要。", "06_Lovers.jpg"),
    ("战车", "目标清晰时，前进会比犹豫更有力量。保持方向，别被阻力带偏。", "07_Chariot.jpg"),
    ("力量", "真正的力量来自温柔而坚定。相信自己的耐心，你能驯服眼前的难题。", "08_Strength.jpg"),
    ("隐者", "答案需要独处才能浮现。暂时离开外界的声音，听听内心真正想要什么。", "09_Hermit.jpg"),
    ("命运之轮", "变化正在发生。顺势而行，把握当下出现的转机。", "10_Wheel_of_Fortune.jpg"),
    ("正义", "用事实和诚实做决定。你现在的选择会带来相应的结果。", "11_Justice.jpg"),
    ("倒吊人", "暂缓行动，换一个角度看问题。新的理解可能就在等待之后。", "12_Hanged_Man.jpg"),
    ("死神", "旧的阶段正在结束。放下已经完成使命的事物，给新生留出空间。", "13_Death.jpg"),
    ("节制", "慢慢调和不同的需要。平衡与耐心会带来比急进更好的结果。", "14_Temperance.jpg"),
    ("恶魔", "看清让你失去自由的执着。你拥有重新选择的能力。", "15_Devil.jpg"),
    ("高塔", "突如其来的变化会拆掉不稳固的结构，也为真实重建腾出位置。", "16_Tower.jpg"),
    ("星星", "希望没有消失，只是在慢慢发芽。继续修复自己，未来值得期待。", "17_Star.jpg"),
    ("月亮", "不确定感会放大恐惧。先辨认事实，再相信逐渐清晰的直觉。", "18_Moon.jpg"),
    ("太阳", "喜悦、坦诚和好消息正在靠近。允许自己被看见，事情会变得明朗。", "19_Sun.jpg"),
    ("审判", "听见内心的召唤，回顾经验后做出清醒的回应。", "20_Judgement.jpg"),
    ("世界", "一个阶段即将圆满。回望走过的路，然后带着新的经验开启下一章。", "21_World.jpg"),
]

MINOR_RANKS = {
    1: "王牌", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七",
    8: "八", 9: "九", 10: "十", 11: "侍者", 12: "骑士", 13: "王后", 14: "国王",
}
SUITS = {
    "Cups": ("圣杯", "情感、关系与直觉"),
    "Pents": ("星币", "工作、财富与现实基础"),
    "Swords": ("宝剑", "思想、沟通与选择"),
    "Wands": ("权杖", "行动、热情与创造力"),
}
RANK_MEANINGS = {
    1: "新的能量正在出现，适合打开局面。",
    2: "寻找平衡，也留意与他人的合作。",
    3: "成果开始显现，继续投入会有回报。",
    4: "先稳定节奏，给自己恢复和整理的时间。",
    5: "竞争或摩擦带来挑战，保持清醒不要失去方向。",
    6: "事情正在改善，帮助与好消息值得被接受。",
    7: "坚持自己的立场，但也要重新审视方法。",
    8: "进展加快，专注行动可以突破停滞。",
    9: "你已经走了很远，保护成果并相信经验。",
    10: "一个阶段的压力或收获达到高点，准备转向下一步。",
    11: "以学习者的心态接收消息，新的可能正在靠近。",
    12: "带着热情行动，但记得控制速度和冲动。",
    13: "成熟的理解力正在形成，温柔而坚定地做决定。",
    14: "发挥领导力，把经验转化为稳定的支持。",
}

for suit, (suit_name, theme) in SUITS.items():
    for number, rank_name in MINOR_RANKS.items():
        card_name = f"{suit_name}{rank_name}"
        meaning = f"关于{theme}：{RANK_MEANINGS[number]}"
        CARDS.append((card_name, meaning, f"{suit}{number:02d}.jpg"))


SPREADS = {
    "单张牌": ["今日指引"],
    "圣三角": ["过去", "现在", "未来"],
    "二选一": ["共同主题", "选择 A", "选择 B", "行动建议"],
    "凯尔特十字": [
        "现状", "阻碍", "根源", "过去影响", "可能目标",
        "近期走向", "内心状态", "外部环境", "希望与担忧", "最终走向",
    ],
}
SPREAD_GUIDANCE = {
    "单张牌": "把这张牌当作今天最值得留意的主题和一个可以执行的小方向。",
    "圣三角": "过去说明背景，现在说明正在发生什么，未来表示按当前趋势发展的可能方向。",
    "二选一": "共同主题是这次选择的核心，A 与 B 分别展示两条路的气质，行动建议帮助你落地。",
    "凯尔特十字": "从现状与阻碍出发，串联根源、环境、内心和走向，适合慢慢阅读整组牌的关系。",
}


class TarotCardImage(Image):
    def __init__(self, reversed_card=False, **kwargs):
        super().__init__(**kwargs)
        self.reversed_card = reversed_card
        if reversed_card:
            self.canvas.before.add(Rotate(angle=180, origin=self.center))
            self.bind(pos=self._update_rotation, size=self._update_rotation)

    def _update_rotation(self, *_):
        self.canvas.before.children[0].origin = self.center


class CardBack(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.12, 0.08, 0.24, 1)
            self.background = RoundedRectangle(pos=self.pos, size=self.size, radius=[18])
            Color(0.83, 0.67, 0.28, 1)
            self.border = RoundedRectangle(
                pos=(self.x + 10, self.y + 10),
                size=(self.width - 20, self.height - 20),
                radius=[12],
            )
        self.bind(pos=self._update, size=self._update)

    def _update(self, *_):
        self.background.pos = self.pos
        self.background.size = self.size
        self.border.pos = (self.x + 10, self.y + 10)
        self.border.size = (self.width - 20, self.height - 20)


class TarotApp(App):
    def build(self):
        Window.clearcolor = (0.035, 0.025, 0.09, 1)
        self.spread_name = "单张牌"
        self.cards = []

        root = BoxLayout(orientation="vertical", padding=(18, 20), spacing=10)
        root.add_widget(Label(text="今日塔罗", font_size=29, bold=True,
                              color=(0.95, 0.84, 0.5, 1), size_hint_y=None, height=44))
        root.add_widget(Label(text="选择牌阵，默念问题，再让牌面展开故事",
                              font_size=15, color=(0.75, 0.72, 0.86, 1),
                              size_hint_y=None, height=28))

        spread_bar = GridLayout(cols=2, spacing=7, size_hint_y=None, height=86)
        for spread_name in SPREADS:
            button = Button(text=spread_name, font_size=15,
                            background_color=(0.26, 0.16, 0.4, 1), background_normal="")
            button.bind(on_release=lambda _, name=spread_name: self.select_spread(name))
            spread_bar.add_widget(button)
        root.add_widget(spread_bar)

        self.spread_hint = Label(text="单张牌：抽 1 张，获得当日简短提示",
                                 font_size=14, color=(0.88, 0.82, 0.65, 1),
                                 size_hint_y=None, height=30)
        root.add_widget(self.spread_hint)

        self.scroll = ScrollView(do_scroll_x=False)
        self.card_grid = GridLayout(cols=2, spacing=10, padding=6,
                                    size_hint_y=None)
        self.card_grid.bind(minimum_height=self.card_grid.setter("height"))
        self.scroll.add_widget(self.card_grid)
        root.add_widget(self.scroll)

        self.result_scroll = ScrollView(do_scroll_x=False, size_hint_y=None, height=105)
        self.result = Label(text="牌面会在这里串成一段故事。",
                    font_size=14, color=(0.85, 0.82, 0.92, 1),
                    halign="left", valign="top", size_hint_y=None)
        self.result.bind(width=self._update_result_text_size,
                 texture_size=self._update_result_height)
        self.result_scroll.add_widget(self.result)
        root.add_widget(self.result_scroll)

        self.action = Button(text="开始抽牌", font_size=18, bold=True,
                             size_hint_y=None, height=54,
                             background_color=(0.71, 0.38, 0.65, 1), background_normal="")
        self.action.bind(on_release=self.draw_spread)
        root.add_widget(self.action)
        self.root_layout = root
        Window.bind(size=self._resize_for_screen)
        self._resize_for_screen(Window, Window.size)
        return root

    def _update_result_text_size(self, label, width):
        label.text_size = (max(1, width - 8), None)

    def _update_result_height(self, label, texture_size):
        label.height = max(60, texture_size[1] + 10)

    def _resize_for_screen(self, _, size):
        width, height = size
        self.result_scroll.height = max(76, min(190, height * 0.25))
        image_height = max(135, min(205, width * 0.38))
        for card_box in getattr(self, "card_boxes", []):
            card_box.height = image_height + 55
            card_box.children[1].height = image_height

    def select_spread(self, spread_name):
        self.spread_name = spread_name
        count = len(SPREADS[spread_name])
        descriptions = {
            "单张牌": "抽 1 张：当日简短提示与行动指引",
            "圣三角": "抽 3 张：过去、现在、未来",
            "二选一": "抽 4 张：共同主题、选择 A、选择 B、行动建议",
            "凯尔特十字": "抽 10 张：适合深挖一件事的根源与走向",
        }
        self.spread_hint.text = descriptions[spread_name]
        self.action.text = f"抽取 {count} 张牌"
        self.reset_cards()

    def reset_cards(self):
        self.card_grid.clear_widgets()
        self.card_boxes = []
        self.result.text = "牌面会在这里串成一段故事。"

    def draw_spread(self, *_):
        selected_cards = random.sample(CARDS, len(SPREADS[self.spread_name]))
        self.cards = [(position, card, random.choice([False, True]))
                      for position, card in zip(SPREADS[self.spread_name], selected_cards)]
        self.card_grid.clear_widgets()
        self.card_boxes = []
        image_height = max(135, min(205, Window.width * 0.38))
        for position, card, reversed_card in self.cards:
            name, meaning, filename = card
            card_box = BoxLayout(orientation="vertical", spacing=4,
                                                                 size_hint_y=None, height=image_height + 55)
            image = TarotCardImage(source="720px/" + filename,
                                   reversed_card=reversed_card,
                                   allow_stretch=True, keep_ratio=True,
                                                                     size_hint_y=None, height=image_height)
            card_box.add_widget(image)
            direction = "逆位" if reversed_card else "正位"
            card_box.add_widget(Label(text=f"{position}\n{name} · {direction}",
                                      font_size=14, color=(0.95, 0.9, 0.75, 1),
                                      halign="center", size_hint_y=None, height=48))
            self.card_grid.add_widget(card_box)
            self.card_boxes.append(card_box)
        self.result.text = self.interpret_spread()
        self.action.text = "重新抽牌"

    def interpret_spread(self):
        major_count = sum(card[1][2].startswith(tuple(f"{number:02d}_" for number in range(22)))
                          for card in self.cards)
        suit_counts = {suit: 0 for suit in SUITS.values()}
        for _, card, _ in self.cards:
            for key, (suit_name, _) in SUITS.items():
                if card[2].startswith(key):
                    suit_counts[suit_name] += 1
        active_suits = [f"{suit} {count} 张" for suit, count in suit_counts.items() if count]
        reversed_count = sum(reversed_card for _, _, reversed_card in self.cards)
        lines = [f"【{self.spread_name}解读】共 {len(self.cards)} 张：大阿尔卡那 {major_count} 张，逆位 {reversed_count} 张。",
                 SPREAD_GUIDANCE[self.spread_name]]
        for position, card, reversed_card in self.cards:
            direction = "逆位" if reversed_card else "正位"
            direction_hint = "这股能量可能被压抑、延迟，或需要先处理内在阻力。" if reversed_card else "这股能量较容易被看见，可以作为当前的支持方向。"
            lines.append(f"{position}：{card[0]}（{direction}）{card[1]}{direction_hint}")
        if active_suits:
            lines.append("花色重点：" + "、".join(active_suits) + "。权杖看行动，圣杯看情绪，宝剑看思考与冲突，星币看现实与物质。")
        if major_count >= 2:
            lines.append("大牌较多：这件事可能牵涉重要的心态转折或人生课题，适合放慢速度，观察长期方向。")
        elif major_count == 0:
            lines.append("没有出现大牌：重点更偏向日常选择和当下可执行的行动，改变可以从小处开始。")
        if reversed_count:
            lines.append("逆位提示：相关能量可能受阻、内化或尚未成熟，不等于绝对的坏结果；请结合对应位置理解。")
        lines.append("请把每张牌放回自己的现实处境中：牌阵提供的是观察角度和参考建议，而不是替你做决定。")
        return "\n".join(lines)


if __name__ == "__main__":
    TarotApp().run()
