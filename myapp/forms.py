from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets as W

from .models import Question, Answer


class BootstrapFormMixin:
    """
    各フィールドのウィジェットに Bootstrap クラスを自動付与する Mixin。
    - text/textarea/input -> form-control
    - select -> form-select
    - checkbox/radio -> form-check-input
    - file -> form-control
    などをよしなに設定。
    """
    default_textarea_rows = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget

            # 既存 class を保持しつつ付与
            def add_class(w, class_name):
                existing = w.attrs.get("class", "")
                w.attrs["class"] = (existing + " " + class_name).strip()

            # プレースホルダ（なければラベルを入れる）
            if getattr(field, "label", None) and "placeholder" not in widget.attrs:
                widget.attrs["placeholder"] = field.label

            # 種類ごとに最適な Bootstrap クラス
            if isinstance(widget, (W.Select, W.SelectMultiple)):
                add_class(widget, "form-select")

            elif isinstance(widget, (W.CheckboxInput, W.NullBooleanSelect)):
                # NullBooleanSelect は select だが見た目は特殊なのでここで扱う
                add_class(widget, "form-check-input")

            elif isinstance(widget, W.RadioSelect):
                add_class(widget, "form-check-input")

            elif isinstance(widget, W.ClearableFileInput):
                add_class(widget, "form-control")

            else:
                # 通常の input/text/textarea など
                add_class(widget, "form-control")

                # Textarea の行数をデフォルト設定
                if isinstance(widget, W.Textarea) and "rows" not in widget.attrs:
                    widget.attrs["rows"] = self.default_textarea_rows

            # アクセシビリティ向上（任意）
            if "aria-label" not in widget.attrs and getattr(field, "label", None):
                widget.attrs["aria-label"] = field.label


class QuestionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "content"]
        # 必要に応じて初期ウィジェット設定（任意）
        widgets = {
            "content": W.Textarea(attrs={"rows": 8}),
        }


class AnswerForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["content"]
        widgets = {
            "content": W.Textarea(attrs={"rows": 6}),
        }


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        # ヘルプテキストがうるさい場合は空に
        help_texts = {
            "username": "",
            "password1": "",
            "password2": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 追加でプレースホルダやオートコンプリートを調整（任意）
        self.fields["username"].widget.attrs.setdefault("placeholder", "ユーザー名")
        self.fields["email"].widget.attrs.setdefault("placeholder", "メールアドレス")
        self.fields["password1"].widget.attrs.setdefault("placeholder", "パスワード")
        self.fields["password2"].widget.attrs.setdefault("placeholder", "パスワード（確認）")

        self.fields["password1"].widget.attrs.setdefault("autocomplete", "new-password")
        self.fields["password2"].widget.attrs.setdefault("autocomplete", "new-password")
